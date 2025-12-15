"""
NFL Verse Data Service

Bridge between nflreadpy library and THE NFL SIM's Player model.
Fetches real-world NFL data and converts it to our internal formats.
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import date

try:
    import nflreadpy as nfl
    import polars as pl
    HAS_NFLREADPY = True
except ImportError:
    HAS_NFLREADPY = False

logger = logging.getLogger(__name__)


# Team abbreviation mapping: nflverse -> our DB
TEAM_ABBR_MAP = {
    "JAX": "JAC",  # Jacksonville
    "WSH": "WAS",  # Washington
    "LA": "LAR",   # LA Rams
    "LV": "LVR",   # Las Vegas (sometimes abbreviated differently)
}


# Position normalization: nflverse -> our Position enum
POSITION_MAP = {
    # Offense
    "LT": "OT",
    "RT": "OT",
    "LG": "OG",
    "RG": "OG",
    "C": "C",
    "QB": "QB",
    "RB": "RB",
    "FB": "FB",
    "WR": "WR",
    "TE": "TE",
    # Defense
    "DE": "DE",
    "DT": "DT",
    "NT": "DT",  # Nose Tackle -> DT
    "LB": "LB",
    "ILB": "LB",
    "MLB": "LB",
    "OLB": "LB",
    "CB": "CB",
    "SS": "S",
    "FS": "S",
    "DB": "CB",  # Generic DB -> CB
    # Special Teams
    "K": "K",
    "P": "P",
    "LS": "LS",
}


def map_team_abbr(nfl_abbr: str) -> str:
    """Convert nflverse team abbreviation to our DB format."""
    return TEAM_ABBR_MAP.get(nfl_abbr, nfl_abbr)


def map_position(nfl_position: str) -> str:
    """Normalize nflverse position to our Position enum."""
    return POSITION_MAP.get(nfl_position, nfl_position)


def calculate_age(birth_date_str: Optional[str]) -> int:
    """Calculate age from birth date string (YYYY-MM-DD format)."""
    if not birth_date_str:
        return 25  # Default age
    try:
        birth_date = date.fromisoformat(str(birth_date_str)[:10])
        today = date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return max(21, min(45, age))  # Clamp between 21-45
    except (ValueError, TypeError):
        return 25


class NflverseService:
    """
    Service for importing real-world NFL data via nflreadpy.
    """

    def __init__(self, season: int = 2024):
        if not HAS_NFLREADPY:
            raise ImportError(
                "nflreadpy and polars are required. "
                "Install with: pip install nflreadpy polars"
            )
        self.season = season
        self._rosters_cache: Optional[pl.DataFrame] = None
        self._nextgen_cache: Optional[pl.DataFrame] = None
        self._combine_cache: Optional[pl.DataFrame] = None
        self._ftn_cache: Optional[pl.DataFrame] = None

    def import_rosters(self) -> pl.DataFrame:
        """
        Fetch NFL rosters for the configured season.

        Returns:
            Polars DataFrame with player roster data.
        """
        if self._rosters_cache is not None:
            return self._rosters_cache

        logger.info(f"Loading NFL rosters for {self.season}...")
        df = nfl.load_rosters(self.season)
        self._rosters_cache = df
        logger.info(f"Loaded {len(df)} roster entries.")
        return df

    def import_nextgen_stats(self) -> pl.DataFrame:
        """
        Fetch Next Gen Stats for the configured season.

        Returns:
            Polars DataFrame with advanced tracking metrics.
        """
        if self._nextgen_cache is not None:
            return self._nextgen_cache

        logger.info(f"Loading Next Gen Stats for {self.season}...")
        try:
            df = nfl.load_nextgen_stats(self.season)
            self._nextgen_cache = df
            logger.info(f"Loaded {len(df)} Next Gen Stats entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load Next Gen Stats: {e}")
            return pl.DataFrame()

    def import_combine_data(self) -> pl.DataFrame:
        """
        Fetch NFL Combine physical testing data.

        Returns:
            Polars DataFrame with combine metrics (40yd, bench, etc.).
        """
        if self._combine_cache is not None:
            return self._combine_cache

        logger.info("Loading NFL Combine data...")
        try:
            df = nfl.load_combine()
            self._combine_cache = df
            logger.info(f"Loaded {len(df)} Combine entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load Combine data: {e}")
            return pl.DataFrame()

    def import_ftn_charting(self) -> pl.DataFrame:
        """
        Fetch FTN charting data for detailed play-level analysis.

        Returns:
            Polars DataFrame with charting metrics.
        """
        if self._ftn_cache is not None:
            return self._ftn_cache

        logger.info(f"Loading FTN charting for {self.season}...")
        try:
            df = nfl.load_ftn_charting(self.season)
            self._ftn_cache = df
            logger.info(f"Loaded {len(df)} FTN charting entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load FTN charting: {e}")
            return pl.DataFrame()

    def import_player_stats(self) -> pl.DataFrame:
        """
        Fetch aggregated player statistics for the season.

        Returns:
            Polars DataFrame with standard stats (yards, TDs, etc.).
        """
        logger.info(f"Loading player stats for {self.season}...")
        try:
            df = nfl.load_player_stats(self.season)
            logger.info(f"Loaded {len(df)} player stats entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load player stats: {e}")
            return pl.DataFrame()

    def import_contracts(self) -> pl.DataFrame:
        """
        Fetch NFL contract data.

        Returns:
            Polars DataFrame with contract values and years.
        """
        logger.info("Loading NFL contracts...")
        try:
            df = nfl.load_contracts()
            logger.info(f"Loaded {len(df)} contract entries.")
            return df
        except Exception as e:
            logger.warning(f"Could not load contracts: {e}")
            return pl.DataFrame()

    def get_player_data(self, gsis_id: str) -> Optional[Dict[str, Any]]:
        """
        Get all available data for a specific player by GSIS ID.

        Args:
            gsis_id: The NFL GSIS player ID.

        Returns:
            Dictionary with merged roster, stats, and combine data.
        """
        rosters = self.import_rosters()
        if rosters.is_empty():
            return None

        # Filter roster for this player
        player_row = rosters.filter(pl.col("gsis_id") == gsis_id)
        if player_row.is_empty():
            return None

        player_dict = player_row.to_dicts()[0]

        # Try to add combine data
        combine = self.import_combine_data()
        if not combine.is_empty():
            combine_row = combine.filter(pl.col("gsis_id") == gsis_id)
            if not combine_row.is_empty():
                player_dict.update(combine_row.to_dicts()[0])

        return player_dict

    def get_all_active_players(self) -> List[Dict[str, Any]]:
        """
        Get all active players from the roster with normalized data.

        Returns:
            List of player dictionaries ready for DB insertion.
        """
        rosters = self.import_rosters()
        if rosters.is_empty():
            return []

        players = []
        for row in rosters.iter_rows(named=True):
            player = {
                "first_name": row.get("first_name", "Unknown"),
                "last_name": row.get("last_name", "Player"),
                "position": map_position(row.get("position", "WR")),
                "position_raw": row.get("position", "WR"),  # Keep original
                "team_abbr": map_team_abbr(row.get("team", "")),
                "college": row.get("college"),
                "height": row.get("height", 72),  # Default 6'0"
                "weight": row.get("weight", 200),
                "age": calculate_age(row.get("birth_date")),
                "experience": row.get("years_exp", 0),
                "jersey_number": row.get("jersey_number", 0),
                "gsis_id": row.get("gsis_id"),
            }
            players.append(player)

        logger.info(f"Processed {len(players)} active players.")
        return players
