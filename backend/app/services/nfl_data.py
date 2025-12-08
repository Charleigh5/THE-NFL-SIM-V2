import nflreadpy as nfl
import polars as pl
from typing import List, Dict, Any, Optional
import threading
from datetime import datetime
from app.schemas.integration import ExternalPlayerStats, ExternalScheduleGame, ExternalPlayerInfo

class NFLDataSingleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._roster_df: Optional[pl.DataFrame] = None
        self._stats_df: Dict[int, pl.DataFrame] = {} # Keyed by year
        self._schedule_df: Dict[int, pl.DataFrame] = {} # Keyed by year
        self._initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def get_roster(self) -> pl.DataFrame:
        if self._roster_df is None:
            print(f"[{datetime.now()}] Lazy loading NFL Roster data...")
            # Load current roster. nflreadpy caches this on disk, we cache in memory.
            self._roster_df = nfl.load_players()
        return self._roster_df

    def get_stats(self, year: int) -> pl.DataFrame:
        if year not in self._stats_df:
            print(f"[{datetime.now()}] Lazy loading NFL Stats data for {year}...")
            # Load stats for the specific year
            self._stats_df[year] = nfl.load_player_stats(seasons=[year])
        return self._stats_df[year]

    def get_schedule(self, year: int) -> pl.DataFrame:
        if year not in self._schedule_df:
            print(f"[{datetime.now()}] Lazy loading NFL Schedule data for {year}...")
            self._schedule_df[year] = nfl.load_schedules(seasons=[year])
        return self._schedule_df[year]

class NFLDataService:
    """
    Service to interact with NFL data using nflreadpy.
    Uses NFLDataSingleton for in-memory caching and Polars for efficient filtering.
    """

    def __init__(self):
        self.data_store = NFLDataSingleton.get_instance()

    def get_current_season_stats(self, year: int = 2024, position: Optional[str] = None) -> List[ExternalPlayerStats]:
        """
        Fetches player stats for a specific season.
        """
        try:
            df = self.data_store.get_stats(year)

            # Efficient Polars Filtering
            if position:
                df = df.filter(pl.col("position") == position)

            # Convert to list of dicts then to Pydantic models
            records = df.to_pandas().to_dict(orient="records")
            # We filter out records that fail validation (or we could let them raise errors)
            valid_records = []
            for r in records:
                try:
                    # Map nflreadpy columns to our schema if needed, or rely on alias
                    # nflreadpy uses 'player_id' usually.
                    valid_records.append(ExternalPlayerStats(**r))
                except Exception:
                    continue # Skip malformed records
            return valid_records
        except Exception as e:
            print(f"Error fetching stats for {year}: {e}")
            return []

    def get_player_info(self, player_id: Optional[str] = None) -> List[ExternalPlayerInfo]:
        """
        Fetches generic player information (roster data).
        """
        try:
            df = self.data_store.get_roster()

            if player_id:
                df = df.filter(pl.col("gsis_id") == player_id)

            records = df.to_pandas().to_dict(orient="records")
            return [ExternalPlayerInfo(**r) for r in records]
        except Exception as e:
            print(f"Error fetching player info: {e}")
            return []

    def get_team_info(self) -> List[Dict[str, Any]]:
        """
        Fetches team information.
        """
        # Team info is often derived from stats or schedule in this library context
        # reusing stats load for now as a proxy for team list
        try:
            df = self.data_store.get_stats(2024)
            # Group by team to get unique list
            teams = df.select("recent_team").unique().drop_nulls()
            return teams.to_pandas().to_dict(orient="records")
        except Exception as e:
            print(f"Error fetching team info: {e}")
            return []

    def get_schedule(self, year: int = 2024, team: Optional[str] = None) -> List[ExternalScheduleGame]:
        """
        Fetches schedule for a specific year.
        """
        try:
            df = self.data_store.get_schedule(year)

            if team:
                df = df.filter(
                    (pl.col("home_team") == team) | (pl.col("away_team") == team)
                )

            records = df.to_pandas().to_dict(orient="records")
            return [ExternalScheduleGame(**r) for r in records]
        except Exception as e:
            print(f"Error fetching schedule: {e}")
            return []
