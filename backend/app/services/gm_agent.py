import random
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.mcp_registry import registry
from app.core.random_utils import DeterministicRNG
from app.core.trade_config import trade_config  # Fix import to get instance
from app.models.gm import GMDecision
from app.models.player import Player
from app.models.team import Team
from app.services.trade_engine.decision import evaluate_trade_package
from app.services.trade_engine.market import PlayerSnapshot
from app.services.trade_engine.modifiers import TeamContextProfile
from app.services.trade_engine.picks import PickValuationInput


class GMAgent:
    def __init__(self, db: Session, team_id: int, seed: int = None):
        self.db = db
        self.team_id = team_id
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))
        self.team = db.get(Team, team_id)
        self.gm = self.team.gm if self.team else None

        # Default GM traits if none exist
        if not self.gm:
            # Create a temporary GM structure for logic if one doesn't exist in DB
            # In a real scenario, every team should have a GM.
            self.gm_traits = {
                "philosophy": "BALANCED",
                "aggression": 50,
                "patience": 50,
                "negotiation": 50,
                "scouting": 50,
            }
        else:
            self.gm_traits = {
                "philosophy": self.gm.philosophy,
                "aggression": self.gm.aggression,
                "patience": self.gm.patience,
                "negotiation": self.gm.negotiation,
                "scouting": self.gm.scouting,
            }

    async def evaluate_trade(
        self,
        offered_players_ids: list[int],
        requested_players_ids: list[int],
        offered_picks: list[dict] = None,
        requested_picks: list[dict] = None,
        offering_team_id: int | None = None,
        log_decision: bool = True,
    ) -> dict[str, Any]:
        """
        Evaluate a trade proposal based on value, team needs, and GM personality.
        """
        if requested_picks is None:
            requested_picks = []
        if offered_picks is None:
            offered_picks = []
        try:
            reasoning = []

            # Check if team exists
            if not self.team:
                return {
                    "decision": "REJECT",
                    "score": 0,
                    "reasoning": "Team not found in database.",
                }

            # 1. Fetch Objects
            offered_players = [self.db.get(Player, pid) for pid in offered_players_ids]
            requested_players = [self.db.get(Player, pid) for pid in requested_players_ids]

            # Filter out None in case of bad IDs
            offered_players = [p for p in offered_players if p]
            requested_players = [p for p in requested_players if p]

            # 2. Financial & Roster Check
            # Calculate incoming salary
            incoming_salary = sum([getattr(p, "contract_salary", 0) or 0 for p in offered_players])
            outgoing_salary = sum(
                [getattr(p, "contract_salary", 0) or 0 for p in requested_players]
            )
            net_salary_change = incoming_salary - outgoing_salary

            # Get salary cap space (default to large value if not set)
            salary_cap_space = getattr(self.team, "salary_cap_space", 50000000) or 50000000

            if salary_cap_space < net_salary_change:
                result = {
                    "decision": "REJECT",
                    "score": -100,
                    "reasoning": f"Cannot afford trade. Net change: ${net_salary_change / 1000000:.2f}M, Cap Space: ${salary_cap_space / 1000000:.2f}M",
                }
                if log_decision:
                    self._log_decision("TRADE_EVALUATION", "REJECT", result)
                return result

            # 3. CTVE Package Evaluation
            offered_snapshots = [PlayerSnapshot.from_orm_player(p) for p in offered_players]
            requested_snapshots = [PlayerSnapshot.from_orm_player(p) for p in requested_players]

            offered_pick_inputs = [
                PickValuationInput(
                    round=pk.get("round", 1),
                    year=pk.get("year", 2025),
                    projected_slot_in_round=pk.get("projected_slot_in_round", 16),
                    original_team_id=pk.get("original_team_id"),
                )
                for pk in (offered_picks or [])
            ]
            requested_pick_inputs = [
                PickValuationInput(
                    round=pk.get("round", 1),
                    year=pk.get("year", 2025),
                    projected_slot_in_round=pk.get("projected_slot_in_round", 16),
                    original_team_id=pk.get("original_team_id"),
                )
                for pk in (requested_picks or [])
            ]

            ai_team_profile = TeamContextProfile(
                team_id=self.team_id,
                conference=getattr(self.team, "conference", "") or "",
                division=getattr(self.team, "division", "") or "",
            )
            if offering_team_id is None:
                if offered_players and hasattr(offered_players[0], "team_id") and offered_players[0].team_id:
                    offering_team_id = offered_players[0].team_id
                elif offered_pick_inputs and offered_pick_inputs[0].original_team_id:
                    offering_team_id = offered_pick_inputs[0].original_team_id
                else:
                    offering_team_id = 1

            offering_team_profile = TeamContextProfile(team_id=offering_team_id)
            if hasattr(self.db, "get"):
                offering_team_orm = self.db.get(Team, offering_team_id)
                if offering_team_orm:
                    offering_team_profile = TeamContextProfile(
                        team_id=offering_team_id,
                        conference=getattr(offering_team_orm, "conference", "") or "",
                        division=getattr(offering_team_orm, "division", "") or "",
                    )

            ai_roster_snapshots = []
            if hasattr(self.team, "players") and self.team.players:
                ai_roster_snapshots = [
                    PlayerSnapshot.from_orm_player(p) for p in self.team.players
                    if p is not None
                ]

            gm_philosophy = getattr(self.gm, "philosophy", "BALANCED") if self.gm else "BALANCED"
            gm_aggr = self.gm_traits.get("aggression", 50)

            ctve_result = evaluate_trade_package(
                offered_players=offered_snapshots,
                requested_players=requested_snapshots,
                offered_picks=offered_pick_inputs,
                requested_picks=requested_pick_inputs,
                offering_team_id=offering_team_id,
                receiving_team_id=self.team_id,
                offering_roster=[],
                receiving_roster=ai_roster_snapshots,
                offering_cap_space=50_000_000,
                receiving_cap_space=int(salary_cap_space),
                offering_team_profile=offering_team_profile,
                receiving_team_profile=ai_team_profile,
                gm_archetype=str(gm_philosophy),
                gm_trade_aggression=int(gm_aggr),
            )

            decision = "ACCEPT" if ctve_result.is_accepted else "REJECT"
            final_score = round(ctve_result.score, 1)

            # 4. MCP/LLM Context (Mocked for now, but structured for integration)
            try:
                llm_adjustment = await self._get_llm_trade_opinion(
                    offered_players, requested_players
                )
                if llm_adjustment.get("score_modifier"):
                    final_score += round(llm_adjustment["score_modifier"], 1)
                if llm_adjustment.get("reasoning"):
                    reasoning.append(llm_adjustment["reasoning"])
            except Exception:
                pass  # Ignore LLM errors

            reasoning.append(ctve_result.reasoning)
            if ctve_result.narrative_notes:
                reasoning.extend(ctve_result.narrative_notes)

            result = {
                "decision": decision,
                "score": final_score,
                "reasoning": "; ".join(reasoning),
                "offered_value": ctve_result.ai_side.value_in_tvp,
                "requested_value": ctve_result.ai_side.value_out_tvp,
                "user_side": {
                    "team_id": ctve_result.user_side.team_id,
                    "competitive_window": ctve_result.user_side.competitive_window,
                    "value_in_tvp": ctve_result.user_side.value_in_tvp,
                    "value_out_tvp": ctve_result.user_side.value_out_tvp,
                    "ratio": ctve_result.user_side.ratio,
                    "grade": ctve_result.user_side.grade,
                    "factors": {
                        "market_tvp": ctve_result.user_side.factors.market_tvp,
                        "need_fit_delta": ctve_result.user_side.factors.need_fit_delta,
                        "cap_impact_delta": ctve_result.user_side.factors.cap_impact_delta,
                        "window_fit_delta": ctve_result.user_side.factors.window_fit_delta,
                        "class_fit_delta": ctve_result.user_side.factors.class_fit_delta,
                        "realism_modifiers_delta": ctve_result.user_side.factors.realism_modifiers_delta,
                        "gm_threshold": ctve_result.user_side.factors.gm_threshold,
                    },
                },
                "ai_side": {
                    "team_id": ctve_result.ai_side.team_id,
                    "competitive_window": ctve_result.ai_side.competitive_window,
                    "value_in_tvp": ctve_result.ai_side.value_in_tvp,
                    "value_out_tvp": ctve_result.ai_side.value_out_tvp,
                    "ratio": ctve_result.ai_side.ratio,
                    "grade": ctve_result.ai_side.grade,
                    "factors": {
                        "market_tvp": ctve_result.ai_side.factors.market_tvp,
                        "need_fit_delta": ctve_result.ai_side.factors.need_fit_delta,
                        "cap_impact_delta": ctve_result.ai_side.factors.cap_impact_delta,
                        "window_fit_delta": ctve_result.ai_side.factors.window_fit_delta,
                        "class_fit_delta": ctve_result.ai_side.factors.class_fit_delta,
                        "realism_modifiers_delta": ctve_result.ai_side.factors.realism_modifiers_delta,
                        "gm_threshold": ctve_result.ai_side.factors.gm_threshold,
                    },
                },
                "ai_threshold": ctve_result.ai_threshold,
                "counter_offer": (
                    {
                        "add_player_ids": ctve_result.counter_offer.add_player_ids,
                        "add_picks": [
                            {
                                "round": pk.round,
                                "year": pk.year,
                                "original_team_id": pk.original_team_id,
                            }
                            for pk in ctve_result.counter_offer.add_picks
                        ],
                        "summary": ctve_result.counter_offer.summary,
                    }
                    if ctve_result.counter_offer
                    else None
                ),
                "narrative_notes": ctve_result.narrative_notes,
            }

            if log_decision:
                self._log_decision("TRADE_EVALUATION", decision, result)
            return result

        except Exception as e:
            # Fallback for any unexpected errors
            import logging

            logging.getLogger(__name__).error(f"GMAgent.evaluate_trade error: {e}")
            return {
                "decision": "REJECT",
                "score": 0,
                "reasoning": f"Trade evaluation failed: {str(e)}",
            }

    def generate_trade_proposal(self, target_position: str = None) -> dict[str, Any]:
        """
        Propose a trade to address a team need.
        """
        # Identify need if not provided
        if not target_position:
            positions = ["QB", "RB", "WR", "TE", "OT", "OG", "C", "DE", "DT", "LB", "CB", "S"]
            # Find position with highest need multiplier
            target_position = max(positions, key=lambda p: self._get_position_need(p))

        # Find potential trade partners (teams with surplus at this position)
        # In a real app, we would query the DB for teams with depth > X at position
        # Here we will mock finding a target player

        # Mock: Find a random player from another team at this position
        # This is a placeholder for a complex query
        stmt = (
            select(Player)
            .where(Player.position == target_position)
            .where(Player.team_id != self.team_id)
            .limit(5)
        )
        candidates = self.db.execute(stmt).scalars().all()

        if not candidates:
            return {"error": "No suitable trade targets found."}

        target_player = self.rng.choice(candidates)

        # Determine what to offer (picks or players)
        # Simple logic: Offer a draft pick of roughly equal value
        self._calculate_package_value([target_player], [], is_acquiring=True)

        # Find a pick that matches value
        # Mocking pick selection
        offered_pick = {"round": 3, "year": 2025}  # Placeholder

        proposal = {
            "target_team_id": target_player.team_id,
            "requested_players": [target_player.id],
            "offered_picks": [offered_pick],
            "reasoning": f"Addressing need at {target_position}",
        }

        self._log_decision("TRADE_PROPOSAL", "GENERATED", proposal)
        return proposal

    def negotiate_contract(self, player: Player, demand: float) -> dict[str, Any]:
        """
        Simulate contract negotiation.
        """
        negotiation_skill = self.gm_traits["negotiation"]

        # Skill factor: 0.8 to 1.2 (High skill reduces price)
        skill_factor = 1.2 - (negotiation_skill / 250)

        counter_offer = demand * skill_factor

        # Random variance
        variance = self.rng.uniform(0.95, 1.05)
        counter_offer *= variance

        accepted = counter_offer >= (demand * 0.9)  # Player accepts if within 10% of demand

        result = {
            "accepted": accepted,
            "counter_offer": int(counter_offer),
            "original_demand": demand,
            "gm_skill_impact": f"{(1 - skill_factor) * 100:.1f}% reduction",
        }

        self._log_decision("CONTRACT_NEGOTIATION", "ACCEPTED" if accepted else "REJECTED", result)
        return result

    def _evaluate_contract_value(self, player: Player) -> float:
        """
        Assess contract efficiency relative to production.
        Returns a multiplier for trade value (1.0 = neutral/fair).
        """
        years_remaining = getattr(player, "contract_years", 1)
        contract_salary = getattr(player, "contract_salary", 0) or 0
        contract_salary / 250_000_000  # Assume 250M cap for now

        # Rookie deals are premium assets
        if years_remaining >= 3 and player.age < 26:
            # Basic check for rookie wage scale (low salary for age)
            if contract_salary < 10_000_000:
                return 1.25

        # Check for expiring contracts (rentals)
        if years_remaining == 1:
            # If acquiring team is contender, rental is fine (1.0)
            # But generally, 1 year of control is worth less than long term control
            return 0.9

        # Calculate expected salary based on rating (simple heuristic)
        # Elite (90+): $25M+
        # Good (80+): $15M+
        # Starter (75+): $5M+
        expected_salary = 0
        if player.overall_rating >= 90:
            expected_salary = 25_000_000
        elif player.overall_rating >= 80:
            expected_salary = 15_000_000
        elif player.overall_rating >= 75:
            expected_salary = 5_000_000
        else:
            expected_salary = 1_000_000

        # Ratio of Actual / Expected
        # If paying 20M for 5M player -> Ratio 4.0 (Bad)
        # If paying 5M for 20M player -> Ratio 0.25 (Good)
        if expected_salary == 0:
            ratio = 10.0  # avoid div/0
        else:
            ratio = contract_salary / expected_salary

        if ratio < 0.5:
            return 1.20  # Steal (Team Friendly)
        if ratio < 0.9:
            return 1.10  # Good Value
        if ratio < 1.1:
            return 1.00  # Fair Market
        if ratio < 1.5:
            return 0.85  # Overpaid
        return 0.60  # Albatross

    def _is_contract_dump_candidate(self, player: Player) -> bool:
        """
        Determine if a player is a candidate for a salary dump.
        (High salary, low production, expiring or long term bad deal)
        """
        contract_salary = getattr(player, "contract_salary", 0) or 0
        if contract_salary < 10_000_000:
            return False  # Too cheap to be a "dump" usually

        # Check rating vs salary
        # Dump if we are paying Elite money for non-Elite play
        startable_rating = 80
        if player.position == "QB":
            startable_rating = 85

        if player.overall_rating < startable_rating and contract_salary > 15_000_000:
            return True

        return False

    def _calculate_flight_risk_discount(self, player: Player) -> float:
        """
        Calculate discount factor for players likely to leave in free agency.
        """
        years_remaining = getattr(player, "contract_years", 1)
        if years_remaining > 1:
            return 1.0  # Under contract

        # Expiring deal logic
        # If team is bad (not contender), likely to leave testing market
        # Simple heuristic for now:
        return 0.85  # Rental discount

    def _calculate_package_value(
        self, players: list[Player], picks: list[dict], is_acquiring: bool
    ) -> float:
        total_value = 0.0

        for player in players:
            # 1. Base Value (Exponential Curve)
            if player.overall_rating < 50:
                base_val = 1.0
            else:
                base_val = ((player.overall_rating - 50) ** 1.6) / 2.0

            # 2. Age Modifier (Young Talent Premium / Veteran Decline)
            age_mult = 1.0
            if player.age < 24:
                age_mult = 1.3
            elif player.age > 30:
                # Gradual decline: 0.95 at 31, 0.9 at 32, etc.
                age_mult = max(0.5, 1.0 - ((player.age - 30) * 0.05))

            # 3. Positional Value Tier
            pos_mult = trade_config.get_position_multiplier(player.position)

            # 4. Contract Efficiency (New)
            contract_mult = self._evaluate_contract_value(player)

            # 5. Flight Risk (New)
            risk_mult = self._calculate_flight_risk_discount(player)

            # 6. Dump Logic (New)
            # If player is a dump candidate, their value is severely penalized
            dump_penalty = 1.0
            if self._is_contract_dump_candidate(player):
                dump_penalty = 0.5  # 50% value reduction (or even negative in future)

            # Calculate Player Value
            player_val = base_val * age_mult * pos_mult * contract_mult * risk_mult * dump_penalty

            # 7. Positional Need Modifier (Only if acquiring)
            if is_acquiring:
                need_multiplier = self._get_position_need(player.position)
                player_val *= need_multiplier

            total_value += player_val

        # Draft Pick Valuation
        # Using simplified Jimmy Johnson / Fitzgerald-Spielberger hybrid for now
        # Ideally should delegate to draft_value_chart.py if fully integrated
        # For this sprint, we keep logic internal or simple delegate?
        # Plan says "Draft Chart" is Sprint 1 task 1.3 (done)
        # So we should USE it.
        from app.data.draft_value_chart import DraftValueChart  # lazy import to avoid circle

        for pick in picks:
            round_num = pick.get("round", 1)
            pick_year = pick.get("year", 2025)
            years_out = pick_year - 2025

            # Use new Chart Service
            try:
                if years_out == 0:
                    # Estimate pick number (mid-round)
                    pick_num = ((round_num - 1) * 32) + 16
                    pick_val = DraftValueChart.get_pick_value(pick_num)
                else:
                    pick_val = DraftValueChart.get_future_pick_value(round_num, years_out)

                # Normalize to player value scale (approx /30 to match player ratings curve)
                total_value += pick_val / 30.0
            except Exception:
                # Fallback
                total_value += 10 / 30.0

        return total_value

    def _get_position_need(self, position: str) -> float:
        """
        Determine need for a position based on roster count and quality.
        Returns a multiplier > 1.0 for high need, < 1.0 for surplus.
        """
        players_at_pos = [p for p in self.team.players if p.position == position]
        count = len(players_at_pos)

        if not players_at_pos:
            return 2.0  # Critical need

        avg_rating = sum(p.overall_rating for p in players_at_pos) / count

        multiplier = 1.0

        if position == "QB" and count < 2:
            multiplier += 0.2
        if position in ["WR", "CB"] and count < 5:
            multiplier += 0.1
        if position in ["OT", "OG", "DE", "DT", "LB", "S"] and count < 3:
            multiplier += 0.1
        if position in ["OL", "DL"] and count < 7:
            multiplier += 0.1

        if avg_rating < 70:
            multiplier += 0.2
        if avg_rating > 85:
            multiplier -= 0.1

        return multiplier

    def _apply_gm_traits(
        self,
        score: float,
        offered_players: list[Player],
        requested_players: list[Player],
        offered_picks: list[dict],
        requested_picks: list[dict],
    ) -> float:
        """
        Adjust score based on GM philosophy.
        """
        philosophy = self.gm_traits["philosophy"]

        if philosophy == "WIN_NOW":
            if offered_players:
                score += 5
            if offered_picks:
                score -= 5

        elif philosophy == "REBUILD":
            if offered_picks:
                score += 10
            young_players = [p for p in offered_players if p.age < 25]
            score += len(young_players) * 3

        return score

    async def _get_llm_trade_opinion(
        self, offered: list[Player], requested: list[Player]
    ) -> dict[str, Any]:
        """
        Evaluate trade sentiment/intangibles and incorporate news/MCP context.
        """
        modifier = 0
        reasoning_parts = []

        stars_offered = [p for p in offered if p.overall_rating > 90]
        if stars_offered:
            modifier += 5
            reasoning_parts.append(
                f"AI Analyst: Acquiring a superstar like {stars_offered[0].last_name} is a franchise-altering move."
            )

        # Check MCP news for all involved players
        try:
            mcp_client = registry.get_client("news")
            if mcp_client:
                for player in offered + requested:
                    news_items = await mcp_client.call_tool(
                        "get_player_news", {"player_id": player.id}
                    )
                    if news_items and isinstance(news_items, list):
                        for item in news_items:
                            headline = (
                                item.get("headline", "") if isinstance(item, dict) else str(item)
                            )
                            if "injury" in headline.lower():
                                modifier -= 5
                                reasoning_parts.append(f"Injury Concern: {headline}")
                            elif headline:
                                reasoning_parts.append(f"Player Intel: {headline}")
        except Exception:
            pass

        return {"score_modifier": modifier, "reasoning": "; ".join(reasoning_parts)}

    def _log_decision(self, decision_type: str, outcome: str, details: dict[str, Any]):
        if self.gm:
            decision = GMDecision(
                gm_id=self.gm.id, decision_type=decision_type, outcome=outcome, details=details
            )
            self.db.add(decision)
            self.db.commit()
