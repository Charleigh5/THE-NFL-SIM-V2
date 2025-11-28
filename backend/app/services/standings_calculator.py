from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.team import Team
from app.models.game import Game
from pydantic import BaseModel


class TeamStanding(BaseModel):
    """Represents a team's standing in the season."""
    team_id: int
    team_name: str
    team_abbreviation: str
    conference: str
    division: str
    wins: int
    losses: int
    ties: int
    win_pct: float
    points_for: int
    points_against: int
    point_differential: int
    division_rank: int
    conference_rank: int
    
    class Config:
        from_attributes = True


class StandingsCalculator:
    """
    Calculates team standings for a season.
    
    Aggregates game results and ranks teams by:
    1. Win percentage
    2. Head-to-head record (if tied)
    3. Division record
    4. Conference record
    5. Point differential
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_standings(self, season_id: int) -> List[TeamStanding]:
        """
        Calculate standings for all teams in a season.
        
        Args:
            season_id: ID of the season
        
        Returns:
            List of TeamStanding objects sorted by rank
        """
        # Get all teams
        teams = self.db.query(Team).all()
        
        # Get all played games for this season
        games = self.db.query(Game).filter(
            and_(
                Game.season_id == season_id,
                Game.is_played == True
            )
        ).all()
        
        # Calculate stats for each team
        standings_data = []
        for team in teams:
            stats = self._calculate_team_stats(team, games)
            standings_data.append(stats)
        
        # Sort by win percentage, then point differential
        standings_data.sort(
            key=lambda x: (x['win_pct'], x['point_differential']),
            reverse=True
        )
        
        # Assign conference and division ranks
        standings_with_ranks = self._assign_ranks(standings_data)
        
        # Convert to TeamStanding objects
        standings = [
            TeamStanding(**data) for data in standings_with_ranks
        ]
        
        return standings
    
    def _calculate_team_stats(self, team: Team, games: List[Game]) -> Dict:
        """Calculate stats for a single team."""
        wins = 0
        losses = 0
        ties = 0
        points_for = 0
        points_against = 0
        
        for game in games:
            if game.home_team_id == team.id:
                # Team was home
                points_for += game.home_score
                points_against += game.away_score
                
                if game.home_score > game.away_score:
                    wins += 1
                elif game.home_score < game.away_score:
                    losses += 1
                else:
                    ties += 1
                    
            elif game.away_team_id == team.id:
                # Team was away
                points_for += game.away_score
                points_against += game.home_score
                
                if game.away_score > game.home_score:
                    wins += 1
                elif game.away_score < game.home_score:
                    losses += 1
                else:
                    ties += 1
        
        # Calculate win percentage
        total_games = wins + losses + ties
        win_pct = wins / total_games if total_games > 0 else 0.0
        
        return {
            'team_id': team.id,
            'team_name': f"{team.city} {team.name}",
            'team_abbreviation': team.abbreviation,
            'conference': team.conference,
            'division': team.division,
            'wins': wins,
            'losses': losses,
            'ties': ties,
            'win_pct': round(win_pct, 3),
            'points_for': points_for,
            'points_against': points_against,
            'point_differential': points_for - points_against
        }
    
    def _assign_ranks(self, standings_data: List[Dict]) -> List[Dict]:
        """Assign conference and division ranks."""
        # Group by conference
        conferences = {}
        for data in standings_data:
            conf = data['conference']
            if conf not in conferences:
                conferences[conf] = []
            conferences[conf].append(data)
        
        # Assign conference ranks
        for conf_teams in conferences.values():
            for i, team_data in enumerate(conf_teams, 1):
                team_data['conference_rank'] = i
        
        # Group by division and assign division ranks
        divisions = {}
        for data in standings_data:
            div_key = f"{data['conference']}-{data['division']}"
            if div_key not in divisions:
                divisions[div_key] = []
            divisions[div_key].append(data)
        
        # Sort each division by win_pct
        for div_teams in divisions.values():
            div_teams.sort(
                key=lambda x: (x['win_pct'], x['point_differential']),
                reverse=True
            )
            for i, team_data in enumerate(div_teams, 1):
                team_data['division_rank'] = i
        
        return standings_data
    
    def get_division_standings(self, season_id: int, conference: str, division: str) -> List[TeamStanding]:
        """Get standings for a specific division."""
        all_standings = self.calculate_standings(season_id)
        return [
            s for s in all_standings
            if s.conference == conference and s.division == division
        ]
    
    def get_conference_standings(self, season_id: int, conference: str) -> List[TeamStanding]:
        """Get standings for a specific conference."""
        all_standings = self.calculate_standings(season_id)
        return [
            s for s in all_standings
            if s.conference == conference
        ]
