import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.random_utils import DeterministicRNG
from app.models.game import Game, GameType
from app.models.team import Team

# Thanksgiving Day game constants
THANKSGIVING_HOSTS = ["DET", "DAL"]  # Traditional hosts (Lions early, Cowboys late)
THANKSGIVING_WEEK = 12  # Typically Week 12 of NFL season

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

    def __init__(self, db: Session, seed: int = None):
        self.db = db
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    def generate_schedule(
        self,
        season_id: int,
        teams: list[Team],
        start_date: datetime = None,
        games_per_week: int = 16
    ) -> list[Game]:
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

    def _organize_by_division(self, teams: list[Team]) -> dict[str, list[Team]]:
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

    def _generate_division_games(self, divisions: dict[str, list[Team]]) -> list[tuple[Team, Team]]:
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

    def _generate_conference_games(self, divisions: dict[str, list[Team]]) -> list[tuple[Team, Team]]:
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
        teams: list[Team],
        existing_matchups: list[tuple[Team, Team]]
    ) -> list[tuple[Team, Team]]:
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
        matchups: list[tuple[Team, Team]],
        season_id: int,
        start_date: datetime,
        games_per_week: int
    ) -> list[Game]:
        """
        Assign matchups to specific weeks and create Game objects.

        Shuffles matchups to randomize the schedule, then distributes them across weeks.
        Flags Thanksgiving games for Lions and Cowboys in Week 12.

        Args:
            matchups: List of (Home, Away) tuples.
            season_id: Season ID.
            start_date: Date of the first Sunday.
            games_per_week: Target number of games per week.

        Returns:
            List[Game]: List of Game objects ready to be saved to DB.
        """
        # Shuffle for randomness
        self.rng.shuffle(matchups)

        games = []
        week = 1
        current_date = start_date

        for i, (home_team, away_team) in enumerate(matchups):
            if i > 0 and i % games_per_week == 0:
                week += 1
                current_date += timedelta(days=7)

            # Determine game type
            game_type = GameType.REGULAR

            # Check for Thanksgiving games (Week 12, traditional hosts)
            if week == THANKSGIVING_WEEK:
                if hasattr(home_team, 'abbreviation') and home_team.abbreviation in THANKSGIVING_HOSTS:
                    game_type = GameType.THANKSGIVING

            game = Game(
                season_id=season_id,
                season=start_date.year,  # Legacy field
                week=week,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                date=current_date,
                is_played=False,
                game_type=game_type
            )
            games.append(game)

        return games

    def generate_preseason_schedule(
        self,
        season_id: int,
        teams: list[Team],
        start_date: datetime,
        weeks: int = 3
    ) -> list[Game]:
        """
        Generate a preseason schedule.

        Args:
            season_id: Season ID
            teams: List of teams
            start_date: Start date of preseason
            weeks: Number of weeks (default 3)

        Returns:
            List of Game objects (is_preseason=True)
        """
        games = []
        current_date = start_date

        # Simple round-robin-ish generation for 3 weeks
        # Avoid division matchups for preseason if possible

        # Shuffle teams initially
        shuffled_teams = teams.copy()
        self.rng.shuffle(shuffled_teams)

        for week in range(1, weeks + 1):
            weekly_matchups = []

            # Simple pairing for this week
            # Rotate list to get new matchups
            # Implementation: Pair index i with i + len/2 (offset)
            offset = week

            used_teams = set()

            # Try to start Thursday, mostly Sunday
            # Week 1 starts Thursday (Hall of Fame week usually earlier but simplification)
            # We'll just spread them Thursday-Sunday

            for i in range(len(shuffled_teams)):
                team1 = shuffled_teams[i]
                if team1.id in used_teams:
                    continue

                # Find opponent
                # Simple logic: just take the next available team
                # In real schedule, this is complex optimization
                # We'll use a rotated offset to ensure different opponents each week
                opponent_idx = (i + offset) % len(shuffled_teams)
                team2 = shuffled_teams[opponent_idx]

                # If self or used, scan for next
                while team2.id == team1.id or team2.id in used_teams:
                    opponent_idx = (opponent_idx + 1) % len(shuffled_teams)
                    team2 = shuffled_teams[opponent_idx]

                used_teams.add(team1.id)
                used_teams.add(team2.id)

                # Randomize home/away
                if self.rng.random() > 0.5:
                    weekly_matchups.append((team1, team2))
                else:
                    weekly_matchups.append((team2, team1))

            # Create Game objects
            # Dates: Thursday (1 game), Friday (2), Saturday (3), Rest Sunday
            # Simplified: Just put them on the weekend
            game_date = current_date

            for i, (home, away) in enumerate(weekly_matchups):
                # Spread games over Thu/Fri/Sat/Sun
                # 0-1: Thu, 2-3: Fri, 4-6: Sat, Rest: Sun
                if i < 1:
                    day_offset = 0  # Thu (assuming start_date is Thu)
                elif i < 3:
                    day_offset = 1  # Fri
                elif i < 7:
                    day_offset = 2  # Sat
                else:
                    day_offset = 3  # Sun (if start_date is Thu)

                specific_date = game_date + timedelta(days=day_offset)

                games.append(Game(
                    season_id=season_id,
                    season=start_date.year,
                    week=week,
                    home_team_id=home.id,
                    away_team_id=away.id,
                    date=specific_date,
                    is_played=False,
                    is_preseason=True,
                    game_type=GameType.REGULAR
                ))

            # Advance to next week's Thursday
            current_date += timedelta(days=7)

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
