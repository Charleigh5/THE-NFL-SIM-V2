"""
Expanded Stats Schemas (Deprecated Alias)
=========================================
DEPRECATED: Re-exports unified stats schemas from app.schemas.stats.
"""

from app.schemas.stats import (
    DefensiveBackStat,
    DefensiveLineStat,
    KickerStat,
    LeagueLeaders,
    LinebackerStat,
    OffensiveLineStat,
    PlayerLeader,
    PlayerStat,
    PositionType,
    PunterStat,
    QuarterbackStat,
    RunningBackStat,
    SpecialTeamsStat,
    TeamStats,
    TightEndStat,
    WideReceiverStat,
)

__all__ = [
    "PositionType",
    "PlayerStat",
    "QuarterbackStat",
    "RunningBackStat",
    "WideReceiverStat",
    "TightEndStat",
    "OffensiveLineStat",
    "DefensiveLineStat",
    "LinebackerStat",
    "DefensiveBackStat",
    "KickerStat",
    "PunterStat",
    "SpecialTeamsStat",
    "LeagueLeaders",
    "TeamStats",
    "PlayerLeader",
]
