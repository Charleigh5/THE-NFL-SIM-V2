from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.player import Player
from app.models.team import Team
from app.services.depth_chart_service import DepthChartService
# from app.engine.kernels.genesis import GenesisKernel # To be implemented/imported
# from app.engine.kernels.cortex import CortexSystem # To be implemented/imported

class MatchContext:
    """
    Holds the state of a single match simulation, including:
    - Rosters (Home/Away)
    - Active Systems (Genesis, Cortex)
    - Fatigue States
    - Game Context (Score, Time, etc.)
    """

    def __init__(self, home_team_id: int, away_team_id: int, db: AsyncSession, weather_config: Dict = None):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.db = db
        self.weather_config = weather_config or {}
        # DepthChartService is static, no instance needed

        # Rosters: player_id -> Player object
        self.home_roster: Dict[int, Player] = {}
        self.away_roster: Dict[int, Player] = {}

        # Fatigue: player_id -> fatigue_level (0.0 to 1.0, where 1.0 is exhausted)
        self.fatigue_state: Dict[int, float] = {}

        # Systems
        # self.genesis: Optional[GenesisKernel] = None
        # self.cortex: Optional[CortexSystem] = None

    async def load_rosters(self):
        """Loads full rosters for both teams from the database."""
        # Load Home Team
        stmt_home = select(Player).where(Player.team_id == self.home_team_id)
        result_home = await self.db.execute(stmt_home)
        home_players = result_home.scalars().all()
        self.home_roster = {p.id: p for p in home_players}

        # Load Away Team
        stmt_away = select(Player).where(Player.team_id == self.away_team_id)
        result_away = await self.db.execute(stmt_away)
        away_players = result_away.scalars().all()
        self.away_roster = {p.id: p for p in away_players}

        # Initialize fatigue for all players
        for pid in self.home_roster:
            self.fatigue_state[pid] = 0.0
        for pid in self.away_roster:
            self.fatigue_state[pid] = 0.0

        self.initialize_systems()

    def initialize_systems(self):
        """Initializes the simulation kernels."""
        # self.genesis = GenesisKernel(self.home_roster, self.away_roster)
        # self.cortex = CortexSystem(self.db)
        pass

    def get_fielded_players(self, team_id: int, formation: str, side: str) -> List[Player]:
        """
        Returns the 11 players on the field for a given team and formation.

        Args:
            team_id: The ID of the team.
            formation: The formation name (e.g., "I_FORM", "SHOTGUN", "4_3", "NICKEL").
            side: "OFFENSE" or "DEFENSE".
        """
        # Get the correct roster list
        if team_id == self.home_team_id:
            roster_list = list(self.home_roster.values())
        else:
            roster_list = list(self.away_roster.values())

        if side == "OFFENSE":
            starters = DepthChartService.get_starting_offense(roster_list, formation)
        else:
            starters = DepthChartService.get_starting_defense(roster_list, formation)

        # Convert dict of positions to list of players
        # Filter out None values if a position is missing in depth chart
        players = [p for p in starters.values() if p is not None]

        # If we are short players (e.g. missing depth chart), fill with best available from roster
        # This is a fallback mechanism
        if len(players) < 11:
            needed = 11 - len(players)
            # Simple fallback: grab random players not already fielded
            current_ids = {p.id for p in players}

            for player in roster_list:
                if player.id not in current_ids:
                    players.append(player)
                    if len(players) == 11:
                        break

        return players

    def update_fatigue(self, player_ids: List[int], fatigue_delta: float):
        """Updates fatigue for a list of players."""
        for pid in player_ids:
            if pid in self.fatigue_state:
                self.fatigue_state[pid] = min(1.0, max(0.0, self.fatigue_state[pid] + fatigue_delta))

    def get_player_fatigue(self, player_id: int) -> float:
        return self.fatigue_state.get(player_id, 0.0)
