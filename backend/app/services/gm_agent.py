from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.player import Player
from app.models.team import Team
from app.models.gm import GM, GMDecision
from app.core.mcp_registry import registry
from app.core.mcp_cache import mcp_cache
import random
from app.core.random_utils import DeterministicRNG

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
                "scouting": 50
            }
        else:
            self.gm_traits = {
                "philosophy": self.gm.philosophy,
                "aggression": self.gm.aggression,
                "patience": self.gm.patience,
                "negotiation": self.gm.negotiation,
                "scouting": self.gm.scouting
            }

    async def evaluate_trade(self,
                           offered_players_ids: list[int],
                           requested_players_ids: list[int],
                           offered_picks: list[dict] = [],
                           requested_picks: list[dict] = []) -> Dict[str, Any]:
        """
        Evaluate a trade proposal based on value, team needs, and GM personality.
        """
        reasoning = []

        # 1. Fetch Objects
        offered_players = [self.db.get(Player, pid) for pid in offered_players_ids]
        requested_players = [self.db.get(Player, pid) for pid in requested_players_ids]

        # Filter out None in case of bad IDs
        offered_players = [p for p in offered_players if p]
        requested_players = [p for p in requested_players if p]

        # 2. Financial & Roster Check
        # Calculate incoming salary
        incoming_salary = sum([p.salary for p in offered_players])
        outgoing_salary = sum([p.salary for p in requested_players])
        net_salary_change = incoming_salary - outgoing_salary

        if self.team.salary_cap_space < net_salary_change:
            result = {
                "decision": "REJECT",
                "score": -100,
                "reasoning": f"Cannot afford trade. Net change: ${net_salary_change/1000000:.2f}M, Cap Space: ${self.team.salary_cap_space/1000000:.2f}M"
            }
            self._log_decision("TRADE_EVALUATION", "REJECT", result)
            return result

        # 3. Value Calculation
        offered_value = self._calculate_package_value(offered_players, offered_picks, is_acquiring=True)
        requested_value = self._calculate_package_value(requested_players, requested_picks, is_acquiring=False)

        # Base score is the difference in value
        raw_score = offered_value - requested_value

        # 4. Apply GM Personality Modifiers
        modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)

        # 5. MCP/LLM Context (Mocked for now, but structured for integration)
        llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
        modified_score += llm_adjustment.get("score_modifier", 0)
        if llm_adjustment.get("reasoning"):
            reasoning.append(llm_adjustment["reasoning"])

        # 6. Final Decision
        # Aggression lowers the threshold to accept
        acceptance_threshold = 0 - (self.gm_traits["aggression"] - 50) * 0.5

        decision = "ACCEPT" if modified_score >= acceptance_threshold else "REJECT"

        reasoning.append(f"Base Value Diff: {raw_score:.1f}")
        reasoning.append(f"GM Adjusted Score: {modified_score:.1f}")

        result = {
            "decision": decision,
            "score": modified_score,
            "reasoning": "; ".join(reasoning)
        }

        self._log_decision("TRADE_EVALUATION", decision, result)
        return result

    def generate_trade_proposal(self, target_position: str = None) -> Dict[str, Any]:
        """
        Propose a trade to address a team need.
        """
        # Identify need if not provided
        if not target_position:
            positions = ["QB", "RB", "WR", "TE", "OL", "DL", "LB", "CB", "S"]
            # Find position with highest need multiplier
            target_position = max(positions, key=lambda p: self._get_position_need(p))

        # Find potential trade partners (teams with surplus at this position)
        # In a real app, we would query the DB for teams with depth > X at position
        # Here we will mock finding a target player

        # Mock: Find a random player from another team at this position
        # This is a placeholder for a complex query
        stmt = select(Player).where(Player.position == target_position).where(Player.team_id != self.team_id).limit(5)
        candidates = self.db.execute(stmt).scalars().all()

        if not candidates:
            return {"error": "No suitable trade targets found."}

        target_player = self.rng.choice(candidates)

        # Determine what to offer (picks or players)
        # Simple logic: Offer a draft pick of roughly equal value
        target_value = self._calculate_package_value([target_player], [], is_acquiring=True)

        # Find a pick that matches value
        # Mocking pick selection
        offered_pick = {"round": 3, "year": 2025} # Placeholder

        proposal = {
            "target_team_id": target_player.team_id,
            "requested_players": [target_player.id],
            "offered_picks": [offered_pick],
            "reasoning": f"Addressing need at {target_position}"
        }

        self._log_decision("TRADE_PROPOSAL", "GENERATED", proposal)
        return proposal

    def negotiate_contract(self, player: Player, demand: float) -> Dict[str, Any]:
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

        accepted = counter_offer >= (demand * 0.9) # Player accepts if within 10% of demand

        result = {
            "accepted": accepted,
            "counter_offer": int(counter_offer),
            "original_demand": demand,
            "gm_skill_impact": f"{(1-skill_factor)*100:.1f}% reduction"
        }

        self._log_decision("CONTRACT_NEGOTIATION", "ACCEPTED" if accepted else "REJECTED", result)
        return result

    def _calculate_package_value(self, players: List[Player], picks: List[dict], is_acquiring: bool) -> float:
        total_value = 0.0

        for player in players:
            # Base value from overall rating
            if player.overall < 50:
                val = 1.0
            else:
                val = ((player.overall - 50) ** 1.6) / 2.0

            # Age modifier
            if player.age < 24:
                val *= 1.3 # Young talent premium
            elif player.age > 32:
                val *= 0.7 # Age decline penalty

            # Contract modifier (simplified)
            if is_acquiring and player.salary > 20000000 and player.overall < 85:
                val *= 0.8

            # Positional Need Modifier (if acquiring)
            if is_acquiring:
                need_multiplier = self._get_position_need(player.position)
                val *= need_multiplier

            total_value += val

        for pick in picks:
            round_num = pick.get("round", 1)
            pick_val = 3000 * (0.5 ** (round_num - 1))

            year_offset = pick.get("year", 2025) - 2025
            if year_offset > 0:
                discount_rate = 0.8 + (self.gm_traits["patience"] / 500)
                pick_val *= (discount_rate ** year_offset)

            total_value += (pick_val / 30.0)

        return total_value

    def _get_position_need(self, position: str) -> float:
        """
        Determine need for a position based on roster count and quality.
        Returns a multiplier > 1.0 for high need, < 1.0 for surplus.
        """
        players_at_pos = [p for p in self.team.players if p.position == position]
        count = len(players_at_pos)

        if not players_at_pos:
            return 2.0 # Critical need

        avg_rating = sum(p.overall for p in players_at_pos) / count

        multiplier = 1.0

        if position == "QB" and count < 2: multiplier += 0.2
        if position in ["WR", "CB"] and count < 5: multiplier += 0.1
        if position in ["OL", "DL"] and count < 7: multiplier += 0.1

        if avg_rating < 70: multiplier += 0.2
        if avg_rating > 85: multiplier -= 0.1

        return multiplier

    def _apply_gm_traits(self, score: float, offered_players: List[Player], requested_players: List[Player], offered_picks: List[dict], requested_picks: List[dict]) -> float:
        """
        Adjust score based on GM philosophy.
        """
        philosophy = self.gm_traits["philosophy"]

        if philosophy == "WIN_NOW":
            if offered_players: score += 5
            if offered_picks: score -= 5

        elif philosophy == "REBUILD":
            if offered_picks: score += 10
            young_players = [p for p in offered_players if p.age < 25]
            score += len(young_players) * 3

        return score

    async def _get_llm_trade_opinion(self, offered: List[Player], requested: List[Player]) -> Dict[str, Any]:
        """
        Mock LLM call to evaluate trade sentiment/intangibles.
        """
        modifier = 0
        reasoning = ""

        stars_offered = [p for p in offered if p.overall > 90]
        if stars_offered:
            modifier += 5
            reasoning = f"AI Analyst: Acquiring a superstar like {stars_offered[0].last_name} is a franchise-altering move."

        return {"score_modifier": modifier, "reasoning": reasoning}

    def _log_decision(self, decision_type: str, outcome: str, details: Dict[str, Any]):
        if self.gm:
            decision = GMDecision(
                gm_id=self.gm.id,
                decision_type=decision_type,
                outcome=outcome,
                details=details
            )
            self.db.add(decision)
            self.db.commit()
