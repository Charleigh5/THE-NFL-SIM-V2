from typing import List, Dict, Tuple
from app.models.team import Team
from app.models.game import Game
from app.models.season import Season
from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta


class ScheduleGenerator:
    """
    Generates an NFL-style schedule for a season.
    
    This implements a simplified NFL scheduling algorithm:
    - Each team plays 17 games
    - Division matchups (6 games): Play each team in division twice (home/away)
    - Conference matchups (4 games): Rotate through other divisions
    - Inter-conference matchups (4 games): Based on standings
    - Additional games (3 games): Based on previous season's standings
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_schedule(
        self,
        season_id: int,
        teams: List[Team],
        start_date: datetime = None,
        games_per_week: int = 16
    ) -> List[Game]:
        """
        Generate a full season schedule.
        
        Args:
            season_id: ID of the season
            teams: List of all teams
            start_date: When the season starts (defaults to next Sunday)
            games_per_week: Number of games per week (default 16, leaving room for byes)
        
        Returns:
            List of Game objects
        """
        if start_date is None:
            start_date = self._get_next_sunday()
        
        # Organize teams by division
        divisions = self._organize_by_division(teams)
        
        # Generate matchups
        matchups = []
        
        # 1. Division games (6 games per team)
        matchups.extend(self._generate_division_games(divisions))
        
        # 2. Conference games (simplified - just rotate divisions)
        matchups.extend(self._generate_conference_games(divisions))
        
        # 3. Fill remaining games to reach 17 per team
        matchups.extend(self._generate_remaining_games(teams, matchups))
        
        # Assign to weeks
        games = self._assign_to_weeks(matchups, season_id, start_date, games_per_week)
        
        return games
    
    def _organize_by_division(self, teams: List[Team]) -> Dict[str, List[Team]]:
        """
        Organize teams into a dictionary keyed by division.
        
        Args:
            teams: List of all teams.
            
        Returns:
            Dict[str, List[Team]]: Key is "Conference-Division" (e.g., "AFC-North"), value is list of Teams.
        """
        divisions = {}
        for team in teams:
            div_key = f"{team.conference}-{team.division}"
            if div_key not in divisions:
                divisions[div_key] = []
            divisions[div_key].append(team)
        return divisions
    
    def _generate_division_games(self, divisions: Dict[str, List[Team]]) -> List[Tuple[Team, Team]]:
        """
        Generate divisional matchups (home and away for each pair).
        
        Each team plays every other team in their division twice (6 games total).
        
        Args:
            divisions: Dictionary of teams organized by division.
            
        Returns:
            List[Tuple[Team, Team]]: List of (Home, Away) tuples.
        """
        matchups = []
        for div_teams in divisions.values():
            # Each team plays every other team in division twice
            for i, team1 in enumerate(div_teams):
                for team2 in div_teams[i+1:]:
                    # Home and away
                    matchups.append((team1, team2))
                    matchups.append((team2, team1))
        return matchups
    
    def _generate_conference_games(self, divisions: Dict[str, List[Team]]) -> List[Tuple[Team, Team]]:
        """
        Generate inter-division conference matchups.
        
        Simplified logic: Rotates divisions within the conference so each division plays another division.
        
        Args:
            divisions: Dictionary of teams organized by division.
            
        Returns:
            List[Tuple[Team, Team]]: List of (Home, Away) tuples.
        """
        matchups = []
        
        # Group divisions by conference
        afc_divs = {k: v for k, v in divisions.items() if k.startswith('AFC')}
        nfc_divs = {k: v for k, v in divisions.items() if k.startswith('NFC')}
        
        # Simplified: match divisions within conference
        for conf_divs in [afc_divs, nfc_divs]:
            div_list = list(conf_divs.values())
            for i in range(0, len(div_list), 2):
                if i + 1 < len(div_list):
                    div1, div2 = div_list[i], div_list[i+1]
                    for team1 in div1:
                        for team2 in div2:
                            matchups.append((team1, team2))
        
        return matchups
    
    def _generate_remaining_games(
        self,
        teams: List[Team],
        existing_matchups: List[Tuple[Team, Team]]
    ) -> List[Tuple[Team, Team]]:
        """
        Fill in remaining games to ensure each team has 17 games.
        
        This method finds teams with fewer than 17 games and pairs them up,
        avoiding duplicate matchups.
        
        Args:
            teams: List of all teams.
            existing_matchups: List of matchups already generated.
            
        Returns:
            List[Tuple[Team, Team]]: List of additional (Home, Away) tuples.
        """
        # Count games per team
        game_count = {team.id: 0 for team in teams}
        for home, away in existing_matchups:
            game_count[home.id] += 1
            game_count[away.id] += 1
        
        matchups = []
        team_list = sorted(teams, key=lambda t: game_count[t.id])
        
        # Pair up teams that need more games
        for i, team1 in enumerate(team_list):
            if game_count[team1.id] >= 17:
                continue
            
            for team2 in team_list[i+1:]:
                if game_count[team2.id] >= 17:
                    continue
                
                # Check if they already play
                already_playing = any(
                    (h.id == team1.id and a.id == team2.id) or
                    (h.id == team2.id and a.id == team1.id)
                    for h, a in existing_matchups + matchups
                )
                
                if not already_playing and game_count[team1.id] < 17 and game_count[team2.id] < 17:
                    matchups.append((team1, team2))
                    game_count[team1.id] += 1
                    game_count[team2.id] += 1
                    break
        
        return matchups
    
    def _assign_to_weeks(
        self,
        matchups: List[Tuple[Team, Team]],
        season_id: int,
        start_date: datetime,
        games_per_week: int
    ) -> List[Game]:
        """
        Assign matchups to specific weeks and create Game objects.
        
        Shuffles matchups to randomize the schedule, then distributes them across weeks.
        
        Args:
            matchups: List of (Home, Away) tuples.
            season_id: Season ID.
            start_date: Date of the first Sunday.
            games_per_week: Target number of games per week.
            
        Returns:
            List[Game]: List of Game objects ready to be saved to DB.
        """
        # Shuffle for randomness
        random.shuffle(matchups)
        
        games = []
        week = 1
        current_date = start_date
        
        for i, (home_team, away_team) in enumerate(matchups):
            if i > 0 and i % games_per_week == 0:
                week += 1
                current_date += timedelta(days=7)
            
            game = Game(
                season_id=season_id,
                season=start_date.year,  # Legacy field
                week=week,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                date=current_date,
                is_played=False
            )
            games.append(game)
        
        return games
    
    def _get_next_sunday(self) -> datetime:
        """
        Get the next Sunday from today at 1:00 PM.
        
        Returns:
            datetime: Next Sunday at 13:00:00.
        """
        today = datetime.now()
        days_until_sunday = (6 - today.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        next_sunday = today + timedelta(days=days_until_sunday)
        return next_sunday.replace(hour=13, minute=0, second=0, microsecond=0)
