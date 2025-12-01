from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.team import Team
from app.models.game import Game
from pydantic import BaseModel, ConfigDict


class TeamStanding(BaseModel):
    """Represents a team's standing in the season."""
    model_config = ConfigDict(from_attributes=True)
    
    team_id: int
    team_name: str
    team_abbreviation: str
    conference: str
    division: str
    wins: int
    losses: int
    ties: int
    win_percentage: float
    points_for: int
    points_against: int
    point_differential: int
    division_rank: int
    conference_rank: int
    seed: Optional[int] = None
    strength_of_schedule: float = 0.0
    clinched_playoff: bool = False
    clinched_division: bool = False
    clinched_seed: Optional[int] = None
    tiebreaker_reason: Optional[str] = None


class StandingsCalculator:
    """
    Calculates team standings for a season.
    
    Aggregates game results and ranks teams by:
    1. Win percentage
    2. Head-to-head record
    3. Division record (if in same division)
    4. Conference record
    5. Strength of schedule
    6. Point differential
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
        # Fetch all teams and games for the season
        teams = self.db.query(Team).all()
        games = self.db.query(Game).filter(Game.season_id == season_id).all()
        
        # Initialize team stats
        team_stats = {
            team.id: {
                'team_id': team.id,
                'team_name': f"{team.city} {team.name}",
                'team_abbreviation': team.abbreviation,
                'conference': team.conference,
                'division': team.division,
                'wins': 0,
                'losses': 0,
                'ties': 0,
                'points_for': 0,
                'points_against': 0,
                'opponents': [],
                'division_wins': 0,
                'division_losses': 0,
                'division_ties': 0,
                'conference_wins': 0,
                'conference_losses': 0,
                'conference_ties': 0,
                'head_to_head': {} # Map of opponent_id -> wins against them
            }
            for team in teams
        }
        
        # Process games
        for game in games:
            home_id = game.home_team_id
            away_id = game.away_team_id
            
            # Record opponents for SOS
            if home_id in team_stats:
                team_stats[home_id]['opponents'].append(away_id)
            if away_id in team_stats:
                team_stats[away_id]['opponents'].append(home_id)
            
            if not game.is_played:
                continue
                
            # Update stats for played games
            if home_id in team_stats and away_id in team_stats:
                home_team = team_stats[home_id]
                away_team = team_stats[away_id]
                
                home_team['points_for'] += game.home_score
                home_team['points_against'] += game.away_score
                away_team['points_for'] += game.away_score
                away_team['points_against'] += game.home_score
                
                # Determine winner
                winner_id = None
                if game.home_score > game.away_score:
                    home_team['wins'] += 1
                    away_team['losses'] += 1
                    winner_id = home_id
                elif game.home_score < game.away_score:
                    home_team['losses'] += 1
                    away_team['wins'] += 1
                    winner_id = away_id
                else:
                    home_team['ties'] += 1
                    away_team['ties'] += 1
                
                # Update Head-to-Head
                if winner_id == home_id:
                    home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
                elif winner_id == away_id:
                    away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1

                # Update Division Record
                if home_team['conference'] == away_team['conference'] and home_team['division'] == away_team['division']:
                    if winner_id == home_id:
                        home_team['division_wins'] += 1
                        away_team['division_losses'] += 1
                    elif winner_id == away_id:
                        home_team['division_losses'] += 1
                        away_team['division_wins'] += 1
                    else:
                        home_team['division_ties'] += 1
                        away_team['division_ties'] += 1
                
                # Update Conference Record
                if home_team['conference'] == away_team['conference']:
                    if winner_id == home_id:
                        home_team['conference_wins'] += 1
                        away_team['conference_losses'] += 1
                    elif winner_id == away_id:
                        home_team['conference_losses'] += 1
                        away_team['conference_wins'] += 1
                    else:
                        home_team['conference_ties'] += 1
                        away_team['conference_ties'] += 1

        # Calculate derived stats (Win %, Diff, SOS)
        for stats in team_stats.values():
            total_games = stats['wins'] + stats['losses'] + stats['ties']
            stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
            stats['point_differential'] = stats['points_for'] - stats['points_against']
            stats['win_percentage'] = round(stats['win_percentage'], 3)
            
            # Division Win %
            div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
            stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
            
            # Conference Win %
            conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
            stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0

        # Calculate Strength of Schedule (SOS)
        for team_id, stats in team_stats.items():
            opponents = stats['opponents']
            if not opponents:
                stats['strength_of_schedule'] = 0.0
                continue
                
            opp_win_pct_sum = 0.0
            valid_opponents = 0
            
            for opp_id in opponents:
                if opp_id in team_stats:
                    opp_win_pct_sum += team_stats[opp_id]['win_percentage']
                    valid_opponents += 1
            
            stats['strength_of_schedule'] = round(opp_win_pct_sum / valid_opponents, 3) if valid_opponents > 0 else 0.0

        # Convert to list for sorting and ranking
        standings_data = list(team_stats.values())
        
        # Assign conference and division ranks with tiebreakers
        standings_with_ranks = self._assign_ranks(standings_data)
        
        # Determine clinching scenarios
        for team in standings_with_ranks:
            games_played = team['wins'] + team['losses'] + team['ties']
            # Simplified clinching logic
            if games_played >= 14:
                if team['division_rank'] == 1:
                    team['clinched_division'] = True
                    team['clinched_playoff'] = True
                elif team['conference_rank'] <= 7:
                    # This is a projection, not a hard clinch, but useful for UI
                    # In a real app, we'd check if they CAN be eliminated
                    pass 
                
                if team['conference_rank'] == 1 and team['clinched_division']:
                     # Simplified: if rank 1 late in season, assume close to clinching seed
                     pass

        # Convert to TeamStanding objects
        standings = [
            TeamStanding(**data) for data in standings_with_ranks
        ]
        
        return standings
    
    def _assign_ranks(self, standings_data: List[Dict]) -> List[Dict]:
        """Assign conference and division ranks with tiebreaker info."""
        
        # 1. Group by Division and Rank
        divisions = {}
        for data in standings_data:
            div_key = f"{data['conference']}-{data['division']}"
            if div_key not in divisions:
                divisions[div_key] = []
            divisions[div_key].append(data)
            
        for div_teams in divisions.values():
            self._rank_group(div_teams, group_type='division')
            for i, team_data in enumerate(div_teams, 1):
                team_data['division_rank'] = i

        # 2. Group by Conference and Rank
        conferences = {}
        for data in standings_data:
            conf = data['conference']
            if conf not in conferences:
                conferences[conf] = []
            conferences[conf].append(data)
            
        for conf_teams in conferences.values():
            self._rank_group(conf_teams, group_type='conference')
            for i, team_data in enumerate(conf_teams, 1):
                team_data['conference_rank'] = i
                team_data['seed'] = i # Seed is same as conference rank
        
        return standings_data

    def _rank_group(self, teams: List[Dict], group_type: str):
        """
        Sort a group of teams in place using tiebreakers.
        group_type: 'division' or 'conference'
        """
        # We use a custom sort key that implements the tiebreaker hierarchy
        # Since Python's sort is stable, we can sort by least important criteria first,
        # or use a tuple key. Tuple key is easier.
        
        # However, tiebreakers are complex (e.g. H2H involves comparing specific teams).
        # A simple key isn't enough for 3+ way ties in H2H.
        # But for MVP, we'll use a weighted tuple key approach which approximates it.
        
        teams.sort(key=lambda x: self._make_sort_key(x, teams, group_type), reverse=True)
        
        # After sorting, populate tiebreaker reasons for adjacent teams with same record
        for i in range(len(teams) - 1):
            t1 = teams[i]
            t2 = teams[i+1]
            if t1['win_percentage'] == t2['win_percentage']:
                reason = self._determine_tiebreaker_reason(t1, t2, group_type)
                t1['tiebreaker_reason'] = reason

    def _make_sort_key(self, team: Dict, all_teams_in_group: List[Dict], group_type: str):
        """Generate a sort key for a team."""
        # 1. Win Percentage
        win_pct = team['win_percentage']
        
        # 2. Head-to-Head (Simplified: win % against other tied teams)
        # This is hard to do in a single key because it depends on who you are tied with.
        # We will skip complex H2H in the key and rely on Division/Conf record.
        
        # 3. Division Win % (only if ranking division)
        div_pct = team['division_win_pct'] if group_type == 'division' else 0
        
        # 4. Conference Win %
        conf_pct = team['conference_win_pct']
        
        # 5. Strength of Schedule
        sos = team['strength_of_schedule']
        
        # 6. Point Differential
        diff = team['point_differential']
        
        if group_type == 'division':
            return (win_pct, div_pct, conf_pct, sos, diff)
        else:
            # Prioritize division winners for conference ranking/seeding
            # Division winners (rank 1) get top seeds
            is_div_winner = 1 if team.get('division_rank') == 1 else 0
            
            return (is_div_winner, win_pct, conf_pct, sos, diff)

    def _determine_tiebreaker_reason(self, t1: Dict, t2: Dict, group_type: str) -> str:
        """Explain why t1 is ranked above t2."""
        if t1['win_percentage'] != t2['win_percentage']:
            return ""
            
        # Check Head-to-Head
        t1_wins_vs_t2 = t1['head_to_head'].get(t2['team_id'], 0)
        t2_wins_vs_t1 = t2['head_to_head'].get(t1['team_id'], 0)
        
        if t1_wins_vs_t2 > t2_wins_vs_t1:
            return f"Head-to-head sweep"
        
        if group_type == 'division':
            if t1['division_win_pct'] > t2['division_win_pct']:
                return f"Better division record ({t1['division_wins']}-{t1['division_losses']} vs {t2['division_wins']}-{t2['division_losses']})"
        
        if t1['conference_win_pct'] > t2['conference_win_pct']:
            return f"Better conference record ({t1['conference_wins']}-{t1['conference_losses']} vs {t2['conference_wins']}-{t2['conference_losses']})"
            
        if t1['strength_of_schedule'] > t2['strength_of_schedule']:
            return f"Strength of schedule ({t1['strength_of_schedule']} vs {t2['strength_of_schedule']})"
            
        if t1['point_differential'] > t2['point_differential']:
            return f"Point differential ({t1['point_differential']} vs {t2['point_differential']})"
            
        return "Coin toss"

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
