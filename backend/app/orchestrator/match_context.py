from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.player import Player
from app.services.depth_chart_service import DepthChartService
from app.orchestrator.kernels.genesis_kernel import GenesisKernel
from app.orchestrator.kernels.cortex_kernel import CortexKernel

class MatchContext:
    """
    Holds the runtime state of a match, including full rosters,
    depth charts, and kernel-specific player states (fatigue, injury).
    """
    def __init__(self, home_team_id: int, away_team_id: int, session: Session | AsyncSession, weather_config: Optional[Dict] = None, home_roster: Dict[int, Player] = None, away_roster: Dict[int, Player] = None) -> None:
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.session = session
        self.weather_config = weather_config or {"temperature": 70, "condition": "Sunny"}

        self.home_roster: Dict[int, Player] = home_roster or {}
        self.away_roster: Dict[int, Player] = away_roster or {}

        self.genesis: Optional[GenesisKernel] = None
        self.cortex: Optional[CortexKernel] = None

        # If rosters provided, initialize immediately
        if self.home_roster and self.away_roster:
            self.initialize_systems()
        # Otherwise, legacy sync init will call load_roster if session is sync
        elif isinstance(session, Session):
            self.home_roster = self.load_roster(home_team_id)
            self.away_roster = self.load_roster(away_team_id)
            self.initialize_systems()

    @classmethod
    async def create(cls, home_team_id: int, away_team_id: int, session: AsyncSession, weather_config: Optional[Dict] = None) -> "MatchContext":
        """Async factory to create MatchContext."""
        instance = cls(home_team_id, away_team_id, session, weather_config)
        instance.home_roster = await instance._load_roster_async(home_team_id)
        instance.away_roster = await instance._load_roster_async(away_team_id)
        instance.initialize_systems()
        return instance

    async def _load_roster_async(self, team_id: int) -> Dict[int, Player]:
        """Async load roster."""
        stmt = select(Player).where(Player.team_id == team_id)
        result = await self.session.execute(stmt)
        players = result.scalars().all()
        if not players:
            raise ValueError(f"No players found for team_id {team_id}")
        return {p.id: p for p in players}

    def load_roster(self, team_id: int) -> Dict[int, Player]:
        """
        Query database for all players on team and convert to dictionary indexed by player_id.
        """
        players = self.session.query(Player).filter(Player.team_id == team_id).all()
        if not players:
            raise ValueError(f"No players found for team_id {team_id}")

        return {p.id: p for p in players}

    def initialize_systems(self) -> None:
        """
        Create GenesisKernel instance with all players.
        Create CortexSystem instance with team coaches.
        Set initial fatigue states to zero.
        """
        # Initialize Genesis
        self.genesis = GenesisKernel()

        all_players = list(self.home_roster.values()) + list(self.away_roster.values())

        temperature = self.weather_config.get("temperature", 70)
        home_climate = "Neutral"
        if temperature < 40:
            home_climate = "Cold"
        elif temperature > 80:
            home_climate = "Warm"

        for player in all_players:
            # Prepare profile data for Genesis
            fast_twitch = (player.acceleration or 50) / 100.0
            wingspan = (player.height or 72) * 1.02
            hand_size = (player.height or 72) / 8.5

            profile_data = {
                "anatomy": {
                    "fast_twitch_ratio": fast_twitch,
                    "hand_size_inches": hand_size,
                    "wingspan_inches": wingspan
                },
                "fatigue": {
                    "home_climate": home_climate,
                    "hrv": 100.0,
                    "lactic_acid": 0.0
                }
            }
            self.genesis.register_player(player.id, profile_data)

        # Initialize Cortex
        # Note: CortexKernel currently does not accept coaches in init.
        # Future improvement: Pass coach data to CortexKernel.
        self.cortex = CortexKernel()

    def get_fielded_players(self, side: str, formation: str) -> List[Player]:
        """
        Pull 11 starters based on depth chart.
        Handle special teams formations.
        Return Player objects with current fatigue levels.
        """
        if side not in ["home", "away"]:
            raise ValueError("Side must be 'home' or 'away'")

        roster_dict = self.home_roster if side == "home" else self.away_roster
        roster_list = list(roster_dict.values())

        starters_map = {}

        if formation.startswith("special_teams") or formation in ["kickoff", "punt", "field_goal"]:
             starters_map = DepthChartService.get_special_teams(roster_list, formation)
             # Special teams might not return full 11, need to fill
             # For now, if we don't have 11, we fill with backups

        elif formation.startswith("defense") or formation in ["4-3", "3-4", "nickel", "dime"]:
            starters_map = DepthChartService.get_starting_defense(roster_list, formation)

        else:
            # Assume Offense
            starters_map = DepthChartService.get_starting_offense(roster_list, formation)

        fielded_players = list(starters_map.values())

        # Fallback if filtering failed or not enough players (e.g. unknown formation or missing roles)
        # Just return the first 11 players from the roster sorted by overall
        if len(fielded_players) < 11:
             # Get all players sorted by overall
             sorted_roster = sorted(roster_list, key=lambda x: -x.overall_rating)
             existing_ids = {p.id for p in fielded_players}

             for p in sorted_roster:
                 if len(fielded_players) >= 11:
                     break
                 if p.id not in existing_ids:
                     fielded_players.append(p)
                     existing_ids.add(p.id)

        if not fielded_players:
             raise ValueError(f"No fielded players found for {side} team with formation {formation}")

        return fielded_players

    def get_fatigue(self, player_id: int) -> Optional[Any]:
        """
        Get the fatigue regulator for a specific player from GenesisKernel.
        """
        if not self.genesis:
            return None

        if player_id in self.genesis.player_states:
            return self.genesis.player_states[player_id].get("fatigue")
        return None

    def get_player_bio(self, player_id: int) -> Dict[str, Any]:
        """
        Get the biological profile for a player from GenesisKernel.
        Returns dict with 'anatomy' and 'fatigue' data.
        """
        if not self.genesis or player_id not in self.genesis.player_states:
            return {}

        state = self.genesis.player_states[player_id]
        return {
            "anatomy": state["anatomy"].model_dump() if hasattr(state["anatomy"], "model_dump") else state["anatomy"].__dict__,
            "fatigue": state["fatigue"].model_dump() if hasattr(state["fatigue"], "model_dump") else state["fatigue"].__dict__
        }
