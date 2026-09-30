"""
Unit tests for Real-Time Roster Synchronization and Multi-Provider Adapters.
Tests provider factory, Tank01, SportsDataIO, and differential reconciliation logic.
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.team import Team
from app.models.player import Player
from app.models.season import Season, SeasonStatus
from app.models.depth_chart import DepthChart
from app.models.player_injury import PlayerInjury
from app.services.roster_sync.base import (
    BaseRosterProvider,
    RosterPlayerDTO,
    TransactionDTO,
    InjuryDTO,
    DepthOrderDTO,
    ProviderStatusDTO,
)
from app.services.roster_sync.factory import get_roster_provider
from app.services.roster_sync.tank01_provider import Tank01Provider
from app.services.roster_sync.sportsdataio_provider import SportsDataIOProvider
from app.services.roster_sync.nflverse_provider import NflverseProvider
from app.services.roster_sync.sync_engine import RosterSyncService


@pytest.fixture
def sync_db_session():
    """Create an isolated in-memory SQLite database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed test season
    season = Season(year=2026, current_week=1, status=SeasonStatus.REGULAR_SEASON, is_active=True)
    session.add(season)

    # Seed test teams
    kc = Team(id=1, name="Chiefs", city="Kansas City", abbreviation="KC")
    sf = Team(id=2, name="49ers", city="San Francisco", abbreviation="SF")
    session.add_all([kc, sf])
    session.commit()

    # Seed test players
    mahomes = Player(
        id=101,
        first_name="Patrick",
        last_name="Mahomes",
        position="QB",
        team_id=1,
        jersey_number=15,
        gsis_id="00-0033873",
        depth_chart_rank=1,
    )
    cmc = Player(
        id=102,
        first_name="Christian",
        last_name="McCaffrey",
        position="RB",
        team_id=2,
        jersey_number=23,
        gsis_id="00-0033280",
        depth_chart_rank=1,
    )
    session.add_all([mahomes, cmc])
    session.commit()

    # Seed depth chart for CMC
    dc_cmc = DepthChart(team_id=2, player_id=102, position="RB", depth_order=1)
    session.add(dc_cmc)
    session.commit()

    yield session
    session.close()


class MockCustomProvider(BaseRosterProvider):
    """Test stub provider returning canned roster changes."""

    def __init__(self, players=None, depth=None, injuries=None, transactions=None):
        self._players = players or []
        self._depth = depth or []
        self._injuries = injuries or []
        self._transactions = transactions or []

    @property
    def provider_id(self) -> str:
        return "mock_custom"

    def get_status(self) -> ProviderStatusDTO:
        return ProviderStatusDTO(
            provider_name="Mock Custom Provider",
            is_authenticated=True,
            masked_key="****9999",
            description="Mock provider for deterministic testing.",
        )

    def fetch_rosters(self):
        return self._players

    def fetch_transactions(self):
        return self._transactions

    def fetch_injuries(self):
        return self._injuries

    def fetch_depth_charts(self):
        return self._depth


# ==============================================================================
# 1. FACTORY RESOLUTION TESTS
# ==============================================================================

def test_factory_resolves_explicit_provider():
    p_tank = get_roster_provider("tank01")
    assert isinstance(p_tank, Tank01Provider)
    assert p_tank.provider_id == "tank01"

    p_sports = get_roster_provider("sportsdataio")
    assert isinstance(p_sports, SportsDataIOProvider)
    assert p_sports.provider_id == "sportsdataio"

    p_nfl = get_roster_provider("nflverse")
    assert isinstance(p_nfl, NflverseProvider)
    assert p_nfl.provider_id == "nflverse"


def test_factory_auto_resolution_with_keys():
    with patch("app.services.roster_sync.factory.settings") as mock_settings:
        mock_settings.ROSTER_SYNC_PROVIDER = "auto"
        mock_settings.RAPIDAPI_KEY = "test_rapid_key_1234"
        mock_settings.RAPIDAPI_HOST = "test_host"
        mock_settings.SPORTSDATAIO_API_KEY = None

        provider = get_roster_provider()
        assert isinstance(provider, Tank01Provider)
        assert provider.api_key == "test_rapid_key_1234"


def test_factory_auto_fallback_without_keys():
    with patch("app.services.roster_sync.factory.settings") as mock_settings:
        mock_settings.ROSTER_SYNC_PROVIDER = "auto"
        mock_settings.RAPIDAPI_KEY = None
        mock_settings.SPORTSDATAIO_API_KEY = None

        provider = get_roster_provider()
        assert isinstance(provider, NflverseProvider)
        assert provider.provider_id == "nflverse"


# ==============================================================================
# 2. PROVIDER STATUS & KEY MASKING TESTS
# ==============================================================================

def test_tank01_key_masking():
    provider_with_key = Tank01Provider(api_key="abcdef123456")
    status = provider_with_key.get_status()
    assert status.is_authenticated is True
    assert status.masked_key == "****3456"

    provider_without_key = Tank01Provider(api_key=None)
    status_no_key = provider_without_key.get_status()
    assert status_no_key.is_authenticated is False
    assert status_no_key.masked_key is None


def test_sportsdataio_key_masking():
    provider = SportsDataIOProvider(api_key="sec_987654321")
    status = provider.get_status()
    assert status.is_authenticated is True
    assert status.masked_key == "****4321"


# ==============================================================================
# 3. DIFFERENTIAL RECONCILIATION TESTS (TRADES, DEPTH, INJURIES)
# ==============================================================================

def test_reconcile_trade_dry_run_vs_live(sync_db_session):
    """
    Simulate CMC being traded from SF to KC.
    Dry run must report the transfer WITHOUT modifying DB.
    Live run must modify player.team_id to KC.
    """
    # CMC DTO showing him now on KC
    cmc_trade_dto = RosterPlayerDTO(
        gsis_id="00-0033280",
        first_name="Christian",
        last_name="McCaffrey",
        position="RB",
        team_abbr="KC",  # New team
        jersey_number=23,
    )
    mock_provider = MockCustomProvider(players=[cmc_trade_dto])
    service = RosterSyncService(provider=mock_provider)

    # 1. Test Dry Run
    dry_result = service.sync_rosters(sync_db_session, dry_run=True)
    assert dry_result.dry_run is True
    assert dry_result.transfers_count == 1
    assert dry_result.transfers[0]["player_name"] == "Christian McCaffrey"
    assert dry_result.transfers[0]["from_team"] == "SF"
    assert dry_result.transfers[0]["to_team"] == "KC"

    # Verify DB was NOT changed
    cmc_in_db = sync_db_session.query(Player).filter_by(id=102).first()
    assert cmc_in_db.team_id == 2  # Still SF!

    # 2. Test Live Run
    live_result = service.sync_rosters(sync_db_session, dry_run=False)
    assert live_result.dry_run is False
    assert live_result.transfers_count == 1

    # Verify DB WAS updated
    sync_db_session.refresh(cmc_in_db)
    assert cmc_in_db.team_id == 1  # Now KC!


def test_reconcile_depth_chart_update(sync_db_session):
    """
    Simulate a depth chart demotion/promotion.
    """
    depth_dto = DepthOrderDTO(
        team_abbr="SF",
        position="RB",
        player_name="Christian McCaffrey",
        rank=2,  # Demoted to RB2
    )
    mock_provider = MockCustomProvider(depth=[depth_dto])
    service = RosterSyncService(provider=mock_provider)

    result = service.sync_rosters(sync_db_session, dry_run=False)
    assert result.depth_updates_count == 1
    assert result.depth_updates[0]["new_rank"] == 2

    # Verify DepthChart record was updated
    dc = sync_db_session.query(DepthChart).filter_by(player_id=102).first()
    assert dc.depth_order == 2


def test_reconcile_injury_update(sync_db_session):
    """
    Simulate an injury report for Patrick Mahomes.
    """
    injury_dto = InjuryDTO(
        player_name="Patrick Mahomes",
        team_abbr="KC",
        position="QB",
        status="Questionable",
        injury_type="High Ankle Sprain",
    )
    mock_provider = MockCustomProvider(injuries=[injury_dto])
    service = RosterSyncService(provider=mock_provider)

    result = service.sync_rosters(sync_db_session, dry_run=False)
    assert result.injuries_count == 1
    assert result.injuries[0]["status"] == "Questionable"

    # Verify PlayerInjury record was created in DB
    inj_rec = sync_db_session.query(PlayerInjury).filter_by(player_id=101).first()
    assert inj_rec is not None
    assert inj_rec.injury_status == "QUESTIONABLE"
    assert inj_rec.injury_type == "High Ankle Sprain"


def test_unmatched_player_handled_gracefully(sync_db_session):
    """
    Incoming player who does not exist in DB should be reported in unmatched list without throwing.
    """
    ghost_player = RosterPlayerDTO(
        gsis_id="99-9999999",
        first_name="Ghost",
        last_name="Rookie",
        position="WR",
        team_abbr="KC",
    )
    mock_provider = MockCustomProvider(players=[ghost_player])
    service = RosterSyncService(provider=mock_provider)

    result = service.sync_rosters(sync_db_session, dry_run=True)
    assert result.unmatched_count == 1
    assert "Ghost Rookie" in result.unmatched[0]
