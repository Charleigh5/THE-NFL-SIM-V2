"""
NFL Data Sync Service
======================

Automated data synchronization service to keep the NFL Sim Engine
up-to-date with the latest real-world NFL data.

VISION:
-------
This service is the backbone of maintaining SOTA simulation accuracy.
By continuously syncing with real NFL data sources, we ensure:
- Accurate rosters reflecting real-time transactions
- Player ratings based on actual performance metrics
- Contract data for realistic salary cap management
- Injury updates for authentic game-day decisions

This level of authenticity and depth will make EA Sports take notice.
We're not just building a game - we're building THE definitive NFL experience.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# Check for nflreadpy availability
try:
    import nflreadpy  # type: ignore[import-not-found]
    HAS_NFLVERSE = True
except ImportError:
    HAS_NFLVERSE = False
    logger.warning("nflreadpy not available. Install with: pip install nflreadpy")


class DataSource(str, Enum):
    """Available data sources from nflverse."""
    ROSTERS = "rosters"
    CONTRACTS = "contracts"
    NEXTGEN_STATS = "nextgen_stats"
    COMBINE = "combine"
    INJURIES = "injuries"
    TRANSACTIONS = "transactions"
    DRAFT_PICKS = "draft_picks"
    PLAYER_STATS = "player_stats"
    SCHEDULES = "schedules"
    PBP = "play_by_play"  # Play-by-play data
    FTN_CHARTING = "ftn_charting"


class UpdateFrequency(str, Enum):
    """How often each data source should be refreshed."""
    REALTIME = "realtime"  # Every request
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ANNUALLY = "annually"


@dataclass
class DataSourceConfig:
    """Configuration for a data source."""
    source: DataSource
    frequency: UpdateFrequency
    loader_func: str  # nflreadpy function name
    description: str
    critical_periods: List[str]  # When this data is most important
    last_updated: Optional[datetime] = None


# =============================================================================
# DATA SOURCE CONFIGURATION
# =============================================================================

DATA_SOURCE_CONFIGS: Dict[DataSource, DataSourceConfig] = {
    DataSource.ROSTERS: DataSourceConfig(
        source=DataSource.ROSTERS,
        frequency=UpdateFrequency.WEEKLY,
        loader_func="load_rosters",
        description="Full team rosters with player positions and status",
        critical_periods=["roster_cutdown", "trade_deadline", "free_agency"]
    ),
    DataSource.CONTRACTS: DataSourceConfig(
        source=DataSource.CONTRACTS,
        frequency=UpdateFrequency.DAILY,
        loader_func="load_contracts",
        description="Player contract details, APY, guaranteed money",
        critical_periods=["free_agency", "trade_deadline", "extensions"]
    ),
    DataSource.NEXTGEN_STATS: DataSourceConfig(
        source=DataSource.NEXTGEN_STATS,
        frequency=UpdateFrequency.WEEKLY,
        loader_func="load_nextgen_stats",
        description="Advanced analytics: completion %, separation, rush RYOE",
        critical_periods=["regular_season", "playoffs"]
    ),
    DataSource.COMBINE: DataSourceConfig(
        source=DataSource.COMBINE,
        frequency=UpdateFrequency.ANNUALLY,
        loader_func="load_combine",
        description="NFL Combine results: 40yd, bench, 3-cone, etc.",
        critical_periods=["combine", "draft"]
    ),
    DataSource.INJURIES: DataSourceConfig(
        source=DataSource.INJURIES,
        frequency=UpdateFrequency.DAILY,
        loader_func="load_injuries",
        description="Injury reports, practice participation, game status",
        critical_periods=["regular_season", "playoffs"]
    ),
    DataSource.TRANSACTIONS: DataSourceConfig(
        source=DataSource.TRANSACTIONS,
        frequency=UpdateFrequency.DAILY,
        loader_func="load_transactions",
        description="Trades, signings, releases, waiver claims",
        critical_periods=["free_agency", "trade_deadline", "roster_cutdown"]
    ),
    DataSource.DRAFT_PICKS: DataSourceConfig(
        source=DataSource.DRAFT_PICKS,
        frequency=UpdateFrequency.ANNUALLY,
        loader_func="load_draft_picks",
        description="NFL Draft picks and selections",
        critical_periods=["draft"]
    ),
    DataSource.PLAYER_STATS: DataSourceConfig(
        source=DataSource.PLAYER_STATS,
        frequency=UpdateFrequency.WEEKLY,
        loader_func="load_player_stats",
        description="Weekly and season player statistics",
        critical_periods=["regular_season", "playoffs"]
    ),
    DataSource.SCHEDULES: DataSourceConfig(
        source=DataSource.SCHEDULES,
        frequency=UpdateFrequency.WEEKLY,
        loader_func="load_schedules",
        description="Game schedules, dates, times, locations",
        critical_periods=["schedule_release", "regular_season"]
    ),
    DataSource.FTN_CHARTING: DataSourceConfig(
        source=DataSource.FTN_CHARTING,
        frequency=UpdateFrequency.WEEKLY,
        loader_func="load_ftn_charting",
        description="Detailed play charting: formations, personnel, routes",
        critical_periods=["regular_season"]
    ),
}


# =============================================================================
# NFL CALENDAR - KEY DATES FOR DATA UPDATES
# =============================================================================

NFL_CALENDAR_2025 = {
    "super_bowl_lix": datetime(2025, 2, 9),  # Super Bowl LIX
    "combine": datetime(2025, 2, 27),  # NFL Combine begins
    "franchise_tag_deadline": datetime(2025, 3, 4),
    "legal_tampering": datetime(2025, 3, 10),
    "free_agency_start": datetime(2025, 3, 12),
    "draft": datetime(2025, 4, 24),  # NFL Draft Round 1
    "otas_start": datetime(2025, 5, 20),  # OTAs begin
    "mandatory_minicamp": datetime(2025, 6, 10),
    "training_camp": datetime(2025, 7, 22),
    "hall_of_fame_game": datetime(2025, 8, 3),
    "preseason_week1": datetime(2025, 8, 7),
    "roster_cutdown_90_to_53": datetime(2025, 8, 26),
    "regular_season_start": datetime(2025, 9, 4),
    "trade_deadline": datetime(2025, 11, 4),
    "playoffs_begin": datetime(2026, 1, 10),
    "super_bowl_lx": datetime(2026, 2, 8),
}


class NFLDataSyncService:
    """
    Service for synchronizing NFL data from nflverse sources.

    This is the heart of keeping our simulation authentic and up-to-date.
    Every piece of data matters - from a rookie's combine 40-time to
    a veteran's contract restructure.
    """

    def __init__(self, season: int = 2025):
        self.season = season
        self.cache: Dict[DataSource, Any] = {}
        self.last_sync: Dict[DataSource, datetime] = {}

        if not HAS_NFLVERSE:
            logger.warning("nflreadpy not installed. Using cached/static data only.")

    def get_current_nfl_period(self) -> str:
        """
        Determine the current NFL calendar period.
        This affects which data sources are most critical.
        """
        now = datetime.now()

        # Check each period
        if now < NFL_CALENDAR_2025["free_agency_start"]:
            return "offseason"
        elif now < NFL_CALENDAR_2025["draft"]:
            return "free_agency"
        elif now < NFL_CALENDAR_2025["training_camp"]:
            return "pre_draft" if now < NFL_CALENDAR_2025["draft"] else "post_draft"
        elif now < NFL_CALENDAR_2025["roster_cutdown_90_to_53"]:
            return "training_camp"
        elif now < NFL_CALENDAR_2025["regular_season_start"]:
            return "roster_cutdown"
        elif now < NFL_CALENDAR_2025["trade_deadline"]:
            return "regular_season"
        elif now < NFL_CALENDAR_2025["playoffs_begin"]:
            return "post_deadline"
        else:
            return "playoffs"

    def should_update(self, source: DataSource) -> bool:
        """Check if a data source needs updating based on frequency."""
        if source not in self.last_sync:
            return True

        config = DATA_SOURCE_CONFIGS[source]
        last = self.last_sync[source]
        now = datetime.now()

        delta_map = {
            UpdateFrequency.REALTIME: timedelta(seconds=0),
            UpdateFrequency.HOURLY: timedelta(hours=1),
            UpdateFrequency.DAILY: timedelta(days=1),
            UpdateFrequency.WEEKLY: timedelta(weeks=1),
            UpdateFrequency.MONTHLY: timedelta(days=30),
            UpdateFrequency.ANNUALLY: timedelta(days=365),
        }

        return (now - last) > delta_map[config.frequency]

    def sync_data_source(self, source: DataSource, force: bool = False) -> Optional[Any]:
        """
        Sync a specific data source from nflverse.

        Args:
            source: The data source to sync
            force: Force update even if not due

        Returns:
            The synced data or None if unavailable
        """
        if not HAS_NFLVERSE:
            logger.warning(f"Cannot sync {source.value}: nflreadpy not available")
            return self.cache.get(source)

        if not force and not self.should_update(source):
            logger.debug(f"Skipping {source.value} sync - not due yet")
            return self.cache.get(source)

        config = DATA_SOURCE_CONFIGS[source]
        loader_func = getattr(nflreadpy, config.loader_func, None)

        if not loader_func:
            logger.error(f"Loader function {config.loader_func} not found in nflreadpy")
            return None

        try:
            logger.info(f"Syncing {source.value} for season {self.season}...")

            # Different loaders have different signatures
            if source in (DataSource.COMBINE, DataSource.CONTRACTS, DataSource.DRAFT_PICKS):
                data = loader_func()  # No season parameter
            else:
                data = loader_func(self.season)

            self.cache[source] = data
            self.last_sync[source] = datetime.now()

            logger.info(f"Successfully synced {source.value}: {len(data)} entries")
            return data

        except Exception as e:
            logger.error(f"Failed to sync {source.value}: {e}")
            return self.cache.get(source)

    def sync_all(self, force: bool = False) -> Dict[DataSource, int]:
        """
        Sync all data sources.

        Returns:
            Dict mapping each source to number of entries synced
        """
        results = {}
        period = self.get_current_nfl_period()

        logger.info(f"=== NFL Data Sync ({period}) ===")

        for source, config in DATA_SOURCE_CONFIGS.items():
            # Prioritize sources critical for current period
            is_critical = period in config.critical_periods

            data = self.sync_data_source(source, force=force or is_critical)
            results[source] = len(data) if data is not None else 0

        return results

    def get_data_freshness_report(self) -> Dict[str, Any]:
        """
        Generate a report on data freshness.

        Returns:
            Dict with freshness info for each source
        """
        report = {
            "current_period": self.get_current_nfl_period(),
            "season": self.season,
            "sources": {}
        }

        for source, config in DATA_SOURCE_CONFIGS.items():
            last = self.last_sync.get(source)
            needs_update = self.should_update(source)

            report["sources"][source.value] = {
                "last_updated": last.isoformat() if last else None,
                "update_frequency": config.frequency.value,
                "needs_update": needs_update,
                "entries_cached": len(self.cache.get(source, [])) if source in self.cache else 0,
                "description": config.description
            }

        return report

    def get_sync_recommendations(self) -> List[str]:
        """
        Get recommendations for what data to sync based on current period.

        Returns:
            List of recommended actions
        """
        recommendations = []
        period = self.get_current_nfl_period()

        recommendations.append(f"Current NFL Period: {period}")
        recommendations.append("")

        # Period-specific recommendations
        if period == "free_agency":
            recommendations.append("🔥 FREE AGENCY ACTIVE - Sync daily:")
            recommendations.append("  - Contracts (new signings, extensions)")
            recommendations.append("  - Transactions (signings, releases)")
            recommendations.append("  - Rosters (player movements)")

        elif period == "draft":
            recommendations.append("📋 NFL DRAFT - Sync after each round:")
            recommendations.append("  - Draft Picks (selections)")
            recommendations.append("  - Rosters (rookie assignments)")
            recommendations.append("  - Contracts (rookie deals)")

        elif period == "training_camp":
            recommendations.append("🏈 TRAINING CAMP - Sync weekly:")
            recommendations.append("  - Injuries (camp injuries)")
            recommendations.append("  - Transactions (cuts, signings)")
            recommendations.append("  - Rosters (depth chart changes)")

        elif period == "regular_season":
            recommendations.append("🏟️ REGULAR SEASON - Sync after each week:")
            recommendations.append("  - Player Stats (performance updates)")
            recommendations.append("  - Next Gen Stats (advanced metrics)")
            recommendations.append("  - Injuries (weekly reports)")
            recommendations.append("  - Transactions (midseason moves)")

        elif period == "playoffs":
            recommendations.append("🏆 PLAYOFFS - Sync after each game:")
            recommendations.append("  - Player Stats (playoff performance)")
            recommendations.append("  - Injuries (critical for roster moves)")

        recommendations.append("")
        recommendations.append("=== Data Staleness Check ===")

        for source in DataSource:
            if self.should_update(source):
                recommendations.append(f"  ⚠️ {source.value} - NEEDS UPDATE")
            else:
                last = self.last_sync.get(source)
                if last:
                    recommendations.append(f"  ✅ {source.value} - Updated {last.strftime('%Y-%m-%d %H:%M')}")

        return recommendations


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_sync_service(season: int = 2025) -> NFLDataSyncService:
    """Create a new sync service instance."""
    return NFLDataSyncService(season=season)


def quick_sync(season: int = 2025) -> Dict[DataSource, int]:
    """Perform a quick sync of all data sources."""
    service = create_sync_service(season)
    return service.sync_all()


def check_data_freshness(season: int = 2025) -> Dict[str, Any]:
    """Check the freshness of all cached data."""
    service = create_sync_service(season)
    return service.get_data_freshness_report()


# =============================================================================
# MAIN - Testing and Development
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("NFL DATA SYNC SERVICE - STATE OF THE ART SIMULATION DATA")
    print("=" * 60)

    service = create_sync_service(2025)

    print("\n📊 Sync Recommendations:")
    for rec in service.get_sync_recommendations():
        print(f"  {rec}")

    print("\n📅 Key 2025 NFL Dates:")
    for event, date in NFL_CALENDAR_2025.items():
        print(f"  {event}: {date.strftime('%B %d, %Y')}")

    print("\n🔧 Available Data Sources:")
    for source, config in DATA_SOURCE_CONFIGS.items():
        print(f"  {source.value}: {config.description}")
        print(f"    Frequency: {config.frequency.value}")
        print(f"    Critical: {', '.join(config.critical_periods)}")
        print()
