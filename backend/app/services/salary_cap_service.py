
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from app.models.player import Player, Position
from app.models.team import Team
from app.models.season import Season


class SalaryCapService:
    """
    Service for calculating and analyzing team salary cap situations.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_team_cap_breakdown(self, team_id: int, season_id: int) -> Dict[str, Any]:
        """
        Get a detailed breakdown of a team's salary cap situation.
        """
        team = self.db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise ValueError(f"Team {team_id} not found")

        # Get all active players on the team
        players = self.db.query(Player).filter(Player.team_id == team_id).all()
        
        # Calculate total cap usage
        used_cap = sum(p.contract_salary for p in players)
        
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
        all_teams = self.db.query(Team).all()
        total_league_space = sum(t.salary_cap_space for t in all_teams)
        league_avg_space = total_league_space / len(all_teams) if all_teams else 0
        
        # Calculate projected rookie pool (simplified estimation based on draft picks)
        # In a real scenario, we'd look at specific draft picks owned
        projected_rookie_impact = 10000000 # Placeholder $10M rookie pool
        
        return {
            "team_id": team.id,
            "team_name": team.name,
            "total_cap": team.salary_cap_total,
            "used_cap": used_cap,
            "available_cap": team.salary_cap_space,
            "cap_percentage": round((used_cap / team.salary_cap_total) * 100, 1) if team.salary_cap_total > 0 else 0,
            "top_contracts": top_contracts_data,
            "position_breakdown": pos_breakdown,
            "league_avg_available": int(league_avg_space),
            "projected_rookie_impact": projected_rookie_impact
        }
