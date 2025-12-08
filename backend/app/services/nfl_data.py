import nflreadpy as nfl
import pandas as pd
from typing import List, Dict, Any, Optional

class NFLDataService:
    """
    Service to interact with NFL data using nflreadpy.
    """

    def __init__(self, cache_dir: str = ".cache/nfl_data"):
        pass

    def get_current_season_stats(self, year: int = 2024) -> List[Dict[str, Any]]:
        """
        Fetches player stats for a specific season.
        """
        try:
            # load_player_stats returns a Polars DataFrame
            df = nfl.load_player_stats(seasons=[year])
            # Convert to list of dicts for easy consumption
            return df.to_pandas().to_dict(orient="records")
        except Exception as e:
            print(f"Error fetching stats for {year}: {e}")
            return []

    def get_player_info(self) -> List[Dict[str, Any]]:
        """
        Fetches generic player information (roster data).
        """
        try:
            df = nfl.load_players()
            return df.to_pandas().to_dict(orient="records")
        except Exception as e:
            print(f"Error fetching player info: {e}")
            return []

    def get_team_info(self) -> List[Dict[str, Any]]:
        """
        Fetches team information.
        """
        try:
            df = nfl.load_team_stats(seasons=[2024])
            return df.to_pandas().to_dict(orient="records")
        except Exception as e:
            print(f"Error fetching team info: {e}")
            return []

    def get_schedule(self, year: int = 2024) -> List[Dict[str, Any]]:
        """
        Fetches schedule for a specific year.
        """
        try:
            df = nfl.load_schedules(seasons=[year])
            return df.to_pandas().to_dict(orient="records")
        except Exception as e:
            print(f"Error fetching schedule: {e}")
            return []
