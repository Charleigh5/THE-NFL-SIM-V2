"""
Real-Time Roster Synchronization Package.
Provides multi-provider adapters (Tank01, SportsDataIO, NFLVerse/ESPN) and
a non-destructive differential sync engine.
"""

from app.services.roster_sync.base import (
    BaseRosterProvider,
    RosterPlayerDTO,
    TransactionDTO,
    InjuryDTO,
    DepthOrderDTO,
    ProviderStatusDTO,
    SyncResultDTO,
)
from app.services.roster_sync.factory import get_roster_provider
from app.services.roster_sync.sync_engine import RosterSyncService

__all__ = [
    "BaseRosterProvider",
    "RosterPlayerDTO",
    "TransactionDTO",
    "InjuryDTO",
    "DepthOrderDTO",
    "ProviderStatusDTO",
    "SyncResultDTO",
    "get_roster_provider",
    "RosterSyncService",
]
