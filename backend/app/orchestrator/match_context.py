from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging_config import get_logger
from app.models.player import Player
from app.models.trait import PlayerTrait
from app.orchestrator.kernels.genesis_kernel import GenesisKernel
from app.services.depth_chart_service import DepthChartService
from app.services.weather_service import WeatherService

logger = get_logger(__name__)

class MatchContext:
    """
    Holds the state of a single match simulation, including:
    - Rosters (Home/Away)
    - Active Systems (Genesis, Cortex)
    - Fatigue States
    - Game Context (Score, Time, etc.)
    - Weather & Chemistry Context
    """

    def __init__(self, home_team_id: int, away_team_id: int, db: AsyncSession, weather_config: dict = None):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.db = db
        self.weather_config = weather_config or {}

        # New Context Fields
        # Populate using WeatherService
        stadium_id = self.weather_config.get("stadium_id", 0)
        game_time = self.weather_config.get("timestamp", "2025-09-07T13:00:00")

        self.weather_conditions: dict[str, float] = WeatherService.get_weather_modifiers(stadium_id, game_time)
        self.home_ol_chemistry: int = 0
        self.away_ol_chemistry: int = 0

        # Rosters: player_id -> Player object
        self.home_roster: dict[int, Player] = {}
        self.away_roster: dict[int, Player] = {}

        # Fatigue: player_id -> fatigue_level (0.0 to 1.0, where 1.0 is exhausted)
        self.fatigue_state: dict[int, float] = {}

        # Systems
        self.genesis: GenesisKernel | None = None
        # self.cortex: Optional[CortexSystem] = None

        logger.info("match_context_initialized", home=home_team_id, away=away_team_id)

    async def load_rosters(self):
        """Loads full rosters for both teams from the database, including traits."""
        # Load Home Team with eager-loaded traits
        stmt_home = (
            select(Player)
            .where(Player.team_id == self.home_team_id)
            .options(selectinload(Player.player_traits).joinedload(PlayerTrait.trait))
        )
        result_home = await self.db.execute(stmt_home)
        home_players = result_home.scalars().all()
        self.home_roster = {p.id: p for p in home_players}

        # Load Away Team with eager-loaded traits
        stmt_away = (
            select(Player)
            .where(Player.team_id == self.away_team_id)
            .options(selectinload(Player.player_traits).joinedload(PlayerTrait.trait))
        )
        result_away = await self.db.execute(stmt_away)
        away_players = result_away.scalars().all()
        self.away_roster = {p.id: p for p in away_players}

        # Flatten traits to active_traits list for efficient access during game loop
        for p in list(self.home_roster.values()) + list(self.away_roster.values()):
            p.active_traits = [pt.trait.name for pt in p.player_traits if pt.trait]

        # Initialize fatigue for all players
        for pid in self.home_roster:
            self.fatigue_state[pid] = 0.0
        for pid in self.away_roster:
            self.fatigue_state[pid] = 0.0

        self.initialize_systems()

    def initialize_systems(self):
        """Initializes the simulation kernels."""
        self.genesis = GenesisKernel()

        # Register all players
        all_players = list(self.home_roster.values()) + list(self.away_roster.values())
        for p in all_players:
            # Determine climate familiarity based on team (placeholder logic)
            # In real app, Team model would have 'stadium_type' or 'climate'
            climate = "Neutral"

            self.genesis.register_player(p.id, {
                "fatigue": {"home_climate": climate},
                "anatomy": {}
            })

    def get_fielded_players(self, team_id: int, formation: str, side: str) -> list[Player]:
        """
        Returns the 11 players on the field for a given team and formation.
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
        players = [p for p in starters.values() if p is not None]

        # Fallback mechanism
        if len(players) < 11:
            needed = 11 - len(players)
            current_ids = {p.id for p in players}

            for player in roster_list:
                if player.id not in current_ids:
                    players.append(player)
                    if len(players) == 11:
                        break

        return players

    def update_fatigue(self, player_ids: list[int], fatigue_delta: float):
        """Updates fatigue for a list of players."""
        for pid in player_ids:
            if self.genesis:
                # Genesis uses 0-100 scale, MatchContext used 0.0-1.0
                self.genesis.update_fatigue(pid, fatigue_delta * 100.0)
            else:
                if pid in self.fatigue_state:
                    self.fatigue_state[pid] = min(1.0, max(0.0, self.fatigue_state[pid] + fatigue_delta))

    def get_player_fatigue(self, player_id: int) -> float:
        if self.genesis:
            return self.genesis.get_current_fatigue(player_id) / 100.0
        return self.fatigue_state.get(player_id, 0.0)
