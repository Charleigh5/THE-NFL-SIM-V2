

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, select
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from app.models.player import Player, Position
from app.models.team import Team
from app.models.season import Season
from app.models.dead_cap import DeadCapCharge, DeadCapReason

if TYPE_CHECKING:
    from app.models.player import Player as PlayerType
    from app.models.team import Team as TeamType
    from app.models.season import Season as SeasonType

class SalaryCapService:
    """
    Service for calculating and analyzing team salary cap situations.
    """
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_team_cap_breakdown(self, team_id: int, season_id: int) -> Dict[str, Any]:
        """
        Get a detailed breakdown of a team's salary cap situation, including Dead Money.
        """
        stmt = select(Team).where(Team.id == team_id)
        team = self.db.execute(stmt).scalar_one_or_none()
        if not team:
            raise ValueError(f"Team {team_id} not found")

        # Get Season Year
        stmt_season = select(Season).where(Season.id == season_id)
        season = self.db.execute(stmt_season).scalar_one_or_none()
        current_year = season.year if season else 2025 # Fallback to 2025

        # Get all active players on the team
        stmt_players = select(Player).where(Player.team_id == team_id)
        players = list(self.db.execute(stmt_players).scalars().all())

        # Get Dead Money for this year
        stmt_dead = select(func.sum(DeadCapCharge.amount)).where(
            DeadCapCharge.team_id == team_id,
            DeadCapCharge.year == current_year
        )
        dead_money = self.db.execute(stmt_dead).scalar() or 0

        # Calculate total cap usage
        active_cap = sum(p.contract_salary for p in players)
        used_cap = active_cap + dead_money

        # Get top 5 contracts
        top_contracts = sorted(players, key=lambda p: p.contract_salary, reverse=True)[:5]
        top_contracts_data = [
            {
                "player_id": p.id,
                "name": f"{p.first_name} {p.last_name}",
                "position": p.position,
                "salary": p.contract_salary,
                "years_left": p.contract_years
            }
            for p in top_contracts
        ]

        # Calculate position breakdown
        position_groups = {
            "QB": ["QB"],
            "RB": ["RB"],
            "WR/TE": ["WR", "TE"],
            "OL": ["OT", "OG", "C"],
            "DL": ["DE", "DT"],
            "LB": ["LB"],
            "DB": ["CB", "S"],
            "ST": ["K", "P"]
        }

        pos_breakdown = []
        for group_name, positions in position_groups.items():
            group_salary = sum(p.contract_salary for p in players if p.position in positions)
            if used_cap > 0:
                percentage = (group_salary / used_cap) * 100
            else:
                percentage = 0

            pos_breakdown.append({
                "group": group_name,
                "total_salary": group_salary,
                "percentage": round(percentage, 1)
            })

        # Sort breakdown by salary
        pos_breakdown.sort(key=lambda x: x["total_salary"], reverse=True)

        # Calculate league average available cap
        stmt_teams = select(Team)
        all_teams = list(self.db.execute(stmt_teams).scalars().all())
        total_league_space: float = float(sum(t.salary_cap_space for t in all_teams) or 0)  # type: ignore[arg-type]
        league_avg_space: float = total_league_space / len(all_teams) if all_teams else 0.0

        # Calculate projected rookie pool (simplified estimation based on draft picks)
        projected_rookie_impact = 10000000 # Placeholder $10M rookie pool

        # Calculate total cap
        salary_cap_limit = 279200000

        return {
            "team_id": team.id,
            "team_name": team.name,
            "total_cap": salary_cap_limit,
            "used_cap": used_cap,
            "active_cap": active_cap,
            "dead_money": dead_money,
            "available_cap": salary_cap_limit - used_cap,
            "cap_percentage": round((used_cap / salary_cap_limit) * 100, 1) if salary_cap_limit > 0 else 0,
            "top_contracts": top_contracts_data,
            "position_breakdown": pos_breakdown,
            "league_avg_available": int(float(league_avg_space)),
            "projected_rookie_impact": projected_rookie_impact
        }

    def process_dead_money_charge(self, team_id: int, player_id: Optional[int], amount: int, year: int, reason: DeadCapReason) -> DeadCapCharge:
        """
        Creates a DeadCapCharge record.
        """
        charge = DeadCapCharge(
            team_id=team_id,
            player_id=player_id,
            amount=amount,
            year=year,
            reason=reason.value
        )
        self.db.add(charge)
        self.db.commit()
        self.db.refresh(charge)
        return charge

    def calculate_potential_dead_money(self, player: Player) -> int:
        """
        Calculates the potential dead money if this player were cut today.
        Heuristic: 50% of current salary is considered 'guaranteed/bonus' acceleration.
        """
        if not player or not player.contract:
            return 0

        # Simplified logic: 50% of annual salary is considered the 'signing bonus prorated' portion
        # In a full sim, we would track unamortized_bonus explicitly.
        return int(player.contract_salary * 0.5)
