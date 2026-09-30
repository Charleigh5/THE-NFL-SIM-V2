"""
Base abstractions, DTOs, and interfaces for real-time NFL roster data providers.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime, date as dt_date
from pydantic import BaseModel, Field


class RosterPlayerDTO(BaseModel):
    """Normalized player representation from external providers."""
    gsis_id: Optional[str] = None
    espn_id: Optional[str] = None
    first_name: str
    last_name: str
    position: str
    team_abbr: str
    jersey_number: Optional[int] = None
    college: Optional[str] = None
    status: str = "ACTIVE"  # ACTIVE, INJURED_RESERVE, PRACTICE_SQUAD, SUSPENDED, FREE_AGENT
    depth_order: Optional[int] = None
    injury_designation: Optional[str] = None
    contract_salary: Optional[int] = None
    contract_years: Optional[int] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class TransactionDTO(BaseModel):
    """Player transaction event (trade, signing, release, reserve)."""
    player_name: str
    position: Optional[str] = None
    from_team: Optional[str] = None
    to_team: Optional[str] = None
    transaction_type: str  # "TRADE", "SIGNING", "CUT", "RESERVE"
    description: str
    transaction_date: Optional[dt_date] = Field(default=None, alias="date")

    model_config = {"populate_by_name": True}


class InjuryDTO(BaseModel):
    """Injury status record."""
    player_name: str
    team_abbr: str
    position: Optional[str] = None
    status: str  # "Questionable", "Doubtful", "Out", "Injured Reserve", "PUP"
    injury_type: Optional[str] = None


class DepthOrderDTO(BaseModel):
    """Depth chart positioning."""
    team_abbr: str
    position: str
    player_name: str
    rank: int


class ProviderStatusDTO(BaseModel):
    """Current health and configuration status of the roster provider."""
    provider_name: str
    is_authenticated: bool
    masked_key: Optional[str] = None
    description: str
    last_sync_timestamp: Optional[str] = None
    available_features: List[str] = Field(default_factory=list)


class SyncResultDTO(BaseModel):
    """Detailed outcome of a differential roster synchronization."""
    provider: str
    timestamp: str
    dry_run: bool
    transfers_count: int = 0
    depth_updates_count: int = 0
    injuries_count: int = 0
    unmatched_count: int = 0
    transfers: List[Dict[str, Any]] = Field(default_factory=list)
    depth_updates: List[Dict[str, Any]] = Field(default_factory=list)
    injuries: List[Dict[str, Any]] = Field(default_factory=list)
    unmatched: List[str] = Field(default_factory=list)
    message: str = "Sync completed successfully"


class BaseRosterProvider(ABC):
    """
    Abstract interface for external NFL roster providers.
    All concrete providers (Tank01, SportsDataIO, NFLVerse) must adhere to this contract.
    """

    @property
    @abstractmethod
    def provider_id(self) -> str:
        """Unique identifier for the provider (e.g. 'tank01', 'sportsdataio', 'nflverse')."""
        pass

    @abstractmethod
    def get_status(self) -> ProviderStatusDTO:
        """Return connectivity and credential health status."""
        pass

    @abstractmethod
    def fetch_rosters(self) -> List[RosterPlayerDTO]:
        """Fetch all active roster entries normalized to internal DTOs."""
        pass

    @abstractmethod
    def fetch_transactions(self) -> List[TransactionDTO]:
        """Fetch recent roster moves, trades, cuts, and free agency signings."""
        pass

    @abstractmethod
    def fetch_injuries(self) -> List[InjuryDTO]:
        """Fetch active injury designations."""
        pass

    @abstractmethod
    def fetch_depth_charts(self) -> List[DepthOrderDTO]:
        """Fetch official team depth chart rankings."""
        pass
