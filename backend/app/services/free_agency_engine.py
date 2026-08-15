"""
Free Agency Engine Module (2025 Architecture)
==============================================
Production-grade competitive bidding, player valuation, GM AI negotiation,
and contract structuring for the NFL Sim Engine.
"""

from typing import List, Dict, Optional, Tuple, Any
import math
import random
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.player import Player, Position
from app.models.team import Team
from app.models.player_contract import PlayerContract
from app.schemas.offseason import FreeAgentSigning, FreeAgentMarketPlayer


# Target roster counts per position for standard 53-man depth
POSITION_TARGETS: Dict[str, int] = {
    "QB": 3,
    "RB": 4,
    "WR": 6,
    "TE": 3,
    "OT": 4,
    "OG": 4,
    "C": 2,
    "DE": 4,
    "DT": 4,
    "LB": 6,
    "CB": 6,
    "S": 4,
    "K": 1,
    "P": 1,
}

# Position salary multiplier (relative to QB top of market ~$55M)
POSITION_VALUE_MULTIPLIERS: Dict[str, float] = {
    "QB": 1.00,
    "DE": 0.82,
    "WR": 0.78,
    "OT": 0.72,
    "CB": 0.70,
    "DT": 0.65,
    "LB": 0.58,
    "S": 0.54,
    "OG": 0.50,
    "TE": 0.48,
    "C": 0.45,
    "RB": 0.42,
    "K": 0.18,
    "P": 0.16,
}

TOP_MARKET_CAP = 55_000_000  # Highest annual salary in NFL
MIN_SALARY = 950_000         # NFL veteran minimum


class FreeAgencyEngine:
    """
    Simulates intelligent, multi-round NFL Free Agency markets.
    """

    def __init__(self, db: Session):
        self.db = db

    # =========================================================================
    # PHASE 1: MARKET VALUATION
    # =========================================================================

    def calculate_market_value(self, player: Player) -> Tuple[int, int, int]:
        """
        Calculate a player's annual average salary (AAV), contract years, and guaranteed money.

        Returns:
            Tuple of (aav: int, years: int, guaranteed_total: int)
        """
        ovr = max(60, min(99, player.overall_rating))
        pos = player.position if isinstance(player.position, str) else player.position.value
        pos_mult = POSITION_VALUE_MULTIPLIERS.get(pos, 0.50)
        age = player.age or 26

        # Non-linear valuation curve (exponential growth for elite 88+ OVR)
        norm_rating = (ovr - 60) / 39.0  # 0.0 at 60 OVR to 1.0 at 99 OVR
        base_salary_scale = norm_rating ** 2.3

        max_pos_salary = TOP_MARKET_CAP * pos_mult
        raw_aav = MIN_SALARY + int(base_salary_scale * (max_pos_salary - MIN_SALARY))

        # Age modifier & Contract Duration
        if age <= 25:
            age_mult = 1.08
            years = 4 if ovr >= 78 else (3 if ovr >= 70 else 2)
        elif age <= 28:
            age_mult = 1.00
            years = 4 if ovr >= 85 else (3 if ovr >= 75 else 2)
        elif age <= 31:
            age_mult = 0.86
            years = 3 if ovr >= 85 else 2
        else:
            age_mult = max(0.55, 0.75 - (age - 32) * 0.10)
            years = 1 if ovr < 85 else 2

        aav = max(MIN_SALARY, int(raw_aav * age_mult))
        # Round to nearest $50k
        aav = int(round(aav / 50_000.0) * 50_000)

        # Guaranteed percentage calculation
        if ovr >= 88:
            guaranteed_pct = 0.70 + (ovr - 88) * 0.015
        elif ovr >= 80:
            guaranteed_pct = 0.50 + (ovr - 80) * 0.025
        elif ovr >= 72:
            guaranteed_pct = 0.30 + (ovr - 72) * 0.025
        else:
            guaranteed_pct = 0.10

        # Veterans 32+ get lower guarantee %
        if age >= 32:
            guaranteed_pct *= 0.75

        total_value = aav * years
        guaranteed_total = int(total_value * min(0.90, guaranteed_pct))
        guaranteed_total = int(round(guaranteed_total / 50_000.0) * 50_000)

        return aav, years, guaranteed_total

    def get_player_tier(self, overall: int) -> str:
        """Classify prospect into a free agency tier."""
        if overall >= 86:
            return "ELITE"
        elif overall >= 78:
            return "STARTER"
        elif overall >= 71:
            return "ROTATIONAL"
        return "DEPTH"

    # =========================================================================
    # PHASE 2: TEAM INTEREST & VALUATION
    # =========================================================================

    def calculate_team_interest(
        self,
        team: Team,
        player: Player,
        roster_counts: Dict[str, int],
        aav: int,
        team_cap_space: float
    ) -> float:
        """
        Calculate an AI team's interest score (0.0 - 100.0) for signing this player.
        """
        pos = player.position if isinstance(player.position, str) else player.position.value
        current_at_pos = roster_counts.get(pos, 0)
        target_at_pos = POSITION_TARGETS.get(pos, 4)

        # 1. Positional Need Factor (0 - 45 pts)
        if current_at_pos == 0:
            need_score = 45.0
        elif current_at_pos < target_at_pos:
            need_score = 35.0 * ((target_at_pos - current_at_pos) / target_at_pos)
        elif current_at_pos == target_at_pos:
            # Upgrade opportunity if player is starter caliber
            need_score = 15.0 if player.overall_rating >= 80 else 2.0
        else:
            need_score = 5.0 if player.overall_rating >= 85 else 0.0

        # 2. Cap Space Feasibility (0 - 35 pts)
        if team_cap_space < aav:
            return 0.0  # Cannot afford player

        cap_ratio = (team_cap_space - aav) / max(1.0, team_cap_space)
        cap_score = min(35.0, 35.0 * (team_cap_space / (aav * 3.0)))

        # 3. Player Quality & Scheme Fit (0 - 20 pts)
        quality_score = min(20.0, (player.overall_rating - 60) * 0.5)

        # 4. Prestige / Contender Bonus
        prestige_bonus = (team.prestige - 50) * 0.1

        total_interest = need_score + cap_score + quality_score + prestige_bonus
        return max(0.0, min(100.0, total_interest))

    # =========================================================================
    # PHASE 3: COMPETITIVE BIDDING SIMULATION
    # =========================================================================

    def simulate_free_agency(self, season_id: int) -> List[FreeAgentSigning]:
        """
        Run the complete multi-wave free agency auction and contract resolution.
        """
        # 1. Fetch available free agents (unassigned players, not rookies, not retired)
        stmt_fa = select(Player).where(
            Player.team_id == None,
            Player.is_rookie == False,
            Player.is_retired == False
        ).order_by(Player.overall_rating.desc())
        free_agents = list(self.db.execute(stmt_fa).scalars().all())

        if not free_agents:
            return []

        # 2. Fetch all teams
        stmt_teams = select(Team).order_by(Team.id)
        teams = list(self.db.execute(stmt_teams).scalars().all())
        team_map = {t.id: t for t in teams}

        # 3. Build team roster counts and effective cap space
        team_roster_counts: Dict[int, Dict[str, int]] = {t.id: {} for t in teams}
        team_roster_totals: Dict[int, int] = {t.id: 0 for t in teams}
        team_cap_trackers: Dict[int, float] = {t.id: max(1_000_000.0, t.salary_cap_space or 40_000_000.0) for t in teams}

        stmt_rosters = select(Player).where(Player.team_id != None)
        active_players = list(self.db.execute(stmt_rosters).scalars().all())
        for p in active_players:
            if p.team_id in team_roster_counts:
                pos = p.position if isinstance(p.position, str) else p.position.value
                team_roster_counts[p.team_id][pos] = team_roster_counts[p.team_id].get(pos, 0) + 1
                team_roster_totals[p.team_id] += 1

        signings: List[FreeAgentSigning] = []

        # Group Free Agents into Waves
        wave_1_fa = [p for p in free_agents if p.overall_rating >= 84]  # Elite / Starters
        wave_2_fa = [p for p in free_agents if 74 <= p.overall_rating < 84]  # Solid Starters / Rotational
        wave_3_fa = [p for p in free_agents if p.overall_rating < 74]  # Depth

        waves = [(1, wave_1_fa), (2, wave_2_fa), (3, wave_3_fa)]

        for wave_num, fa_group in waves:
            for player in fa_group:
                aav, years, guaranteed = self.calculate_market_value(player)

                # Collect bids from eligible teams
                bids: List[Tuple[Team, float, int, int]] = []

                for team in teams:
                    # Check if roster is already at maximum (53)
                    if team_roster_totals[team.id] >= 53:
                        continue

                    interest = self.calculate_team_interest(
                        team=team,
                        player=player,
                        roster_counts=team_roster_counts[team.id],
                        aav=aav,
                        team_cap_space=team_cap_trackers[team.id]
                    )

                    if interest >= (35.0 if wave_num == 1 else (25.0 if wave_num == 2 else 15.0)):
                        # Bid modifier based on interest intensity
                        bid_aav = int(aav * (1.0 + (interest - 50.0) * 0.004))
                        bid_aav = max(MIN_SALARY, min(bid_aav, int(team_cap_trackers[team.id])))
                        bid_score = interest + random.uniform(-5.0, 5.0)
                        bids.append((team, bid_score, bid_aav, years))

                if not bids:
                    continue

                # Sort bids by attractiveness
                bids.sort(key=lambda b: b[1], reverse=True)
                winning_team, score, final_aav, final_years = bids[0]
                final_guaranteed = int(final_aav * final_years * (guaranteed / max(1, aav * years)))

                # Calculate signing grade
                grade = self._calculate_signing_grade(player, final_aav, aav, team_roster_counts[winning_team.id])

                # Execute signing on player model & contract
                player.team_id = winning_team.id
                player.contract_years = final_years
                player.contract_salary = final_aav

                # Ensure satellite contract is updated or created if supported
                if hasattr(player, "contract") and player.contract:
                    player.contract.contract_years = final_years
                    player.contract.contract_salary = final_aav
                    player.contract.is_rookie = False
                    player.contract.is_retired = False
                elif hasattr(player, "id"):
                    contract = PlayerContract(
                        player_id=player.id,
                        contract_years=final_years,
                        contract_salary=final_aav,
                        is_rookie=False,
                        is_retired=False
                    )
                    self.db.add(contract)

                # Update team tracker
                pos = player.position if isinstance(player.position, str) else player.position.value
                team_roster_counts[winning_team.id][pos] = team_roster_counts[winning_team.id].get(pos, 0) + 1
                team_roster_totals[winning_team.id] += 1
                team_cap_trackers[winning_team.id] = max(0.0, team_cap_trackers[winning_team.id] - final_aav)
                winning_team.salary_cap_space = team_cap_trackers[winning_team.id]

                signing = FreeAgentSigning(
                    player_id=player.id,
                    player_name=f"{player.first_name} {player.last_name}",
                    position=pos,
                    overall_rating=player.overall_rating,
                    age=player.age or 26,
                    team_id=winning_team.id,
                    team_name=f"{winning_team.city} {winning_team.name}",
                    contract_years=final_years,
                    total_value=final_aav * final_years,
                    guaranteed=final_guaranteed,
                    annual_avg=final_aav,
                    signing_grade=grade,
                    signing_round=wave_num,
                    bidding_teams_count=len(bids)
                )
                signings.append(signing)

        # 4. Fill remaining roster gaps to 48 minimum if teams are short
        self._balance_rosters_to_minimum(teams, team_roster_counts, team_roster_totals, team_cap_trackers, signings)

        self.db.commit()
        return signings

    def _balance_rosters_to_minimum(
        self,
        teams: List[Team],
        team_roster_counts: Dict[int, Dict[str, int]],
        team_roster_totals: Dict[int, int],
        team_cap_trackers: Dict[int, float],
        signings: List[FreeAgentSigning]
    ) -> None:
        """Ensure all teams have at least 48 players by signing low-cost depth."""
        stmt_remain = select(Player).where(
            Player.team_id == None,
            Player.is_rookie == False,
            Player.is_retired == False
        ).order_by(Player.overall_rating.desc())
        remain_fas = list(self.db.execute(stmt_remain).scalars().all())
        fa_idx = 0

        for team in teams:
            needed = max(0, 48 - team_roster_totals[team.id])
            for _ in range(needed):
                if fa_idx >= len(remain_fas):
                    break
                p = remain_fas[fa_idx]
                fa_idx += 1

                p.team_id = team.id
                p.contract_years = 1
                p.contract_salary = MIN_SALARY

                pos = p.position if isinstance(p.position, str) else p.position.value
                team_roster_counts[team.id][pos] = team_roster_counts[team.id].get(pos, 0) + 1
                team_roster_totals[team.id] += 1
                team_cap_trackers[team.id] = max(0.0, team_cap_trackers[team.id] - MIN_SALARY)
                team.salary_cap_space = team_cap_trackers[team.id]

                signings.append(FreeAgentSigning(
                    player_id=p.id,
                    player_name=f"{p.first_name} {p.last_name}",
                    position=pos,
                    overall_rating=p.overall_rating,
                    age=p.age or 25,
                    team_id=team.id,
                    team_name=f"{team.city} {team.name}",
                    contract_years=1,
                    total_value=MIN_SALARY,
                    guaranteed=0,
                    annual_avg=MIN_SALARY,
                    signing_grade="C",
                    signing_round=3,
                    bidding_teams_count=1
                ))

    def _calculate_signing_grade(self, player: Player, paid_aav: int, market_aav: int, team_needs: Dict[str, int]) -> str:
        """Assign letter grade to free agent signing."""
        ratio = paid_aav / max(1, market_aav)
        pos = player.position if isinstance(player.position, str) else player.position.value
        current = team_needs.get(pos, 0)
        target = POSITION_TARGETS.get(pos, 4)
        is_major_need = current < target

        if ratio <= 0.85 and is_major_need:
            return "A+"
        elif ratio <= 0.95 or (ratio <= 1.05 and is_major_need):
            return "A"
        elif ratio <= 1.10:
            return "B+"
        elif ratio <= 1.20:
            return "B"
        elif ratio <= 1.35:
            return "C+"
        elif ratio <= 1.50:
            return "C"
        return "D"

    # =========================================================================
    # PHASE 4: MARKET PREVIEW & SCOUTING
    # =========================================================================

    def get_market_overview(self, season_id: int, limit: int = 50) -> List[FreeAgentMarketPlayer]:
        """
        Return the top available free agents with projected market valuations.
        """
        stmt = select(Player).where(
            Player.team_id == None,
            Player.is_rookie == False,
            Player.is_retired == False
        ).order_by(Player.overall_rating.desc()).limit(limit)

        players = list(self.db.execute(stmt).scalars().all())
        market_list: List[FreeAgentMarketPlayer] = []

        stmt_teams = select(Team).order_by(Team.prestige.desc()).limit(5)
        top_teams = list(self.db.execute(stmt_teams).scalars().all())
        top_team_names = [f"{t.city} {t.name}" for t in top_teams]

        for p in players:
            aav, years, _ = self.calculate_market_value(p)
            tier = self.get_player_tier(p.overall_rating)
            pos = p.position if isinstance(p.position, str) else p.position.value

            # Pick 2-3 plausible interested teams
            interested = random.sample(top_team_names, min(len(top_team_names), random.randint(2, 3)))

            market_list.append(FreeAgentMarketPlayer(
                player_id=p.id,
                name=f"{p.first_name} {p.last_name}",
                position=pos,
                overall_rating=p.overall_rating,
                age=p.age or 26,
                experience=p.experience or 3,
                projected_market_value=aav,
                projected_years=years,
                tier=tier,
                top_interested_teams=interested
            ))

        return market_list
