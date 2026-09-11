"""
Unit Tests: Sprint Capology & Free Agency Enhancements
======================================================
Tests:
1. Post-June 1st cap splits (CapologistPhysics & SalaryCapEngine).
2. NFL CBA Top-51 offseason calculation rule in SalaryCapService.
3. FreeAgencyEngine market overview parameter alignment with FreeAgentMarketPlayer schema.
4. Interactive user GM free agency bidding and competitive AI GM resolution.
5. Verification of exposed API endpoints on season router.
"""

import pytest
from unittest.mock import MagicMock
from app.kernels.empire.capologist import (
    CapologistPhysics,
    ContractYear as KernelContractYear,
    calculate_post_june1_dead_money as kernel_calc_post_june1,
)
from app.services.empire.salary_cap import (
    SalaryCapEngine,
    Contract as EmpireContract,
    ContractYear as EmpireContractYear,
    ContractType,
    calculate_post_june1_dead_money as empire_calc_post_june1,
)
from app.services.salary_cap_service import SalaryCapService
from app.services.free_agency_engine import FreeAgencyEngine, MIN_SALARY
from app.schemas.offseason import (
    FreeAgentMarketPlayer,
    FreeAgentBidRequest,
    FreeAgentBidResponse,
)
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player, Position
from app.api.endpoints.season import router as season_router


# ============================================================================
# 1. POST-JUNE 1ST CAP SPLITS
# ============================================================================

def test_capologist_post_june1_split():
    """Verify CapologistPhysics splits dead money across current and next year."""
    physics = CapologistPhysics()

    # 4-year contract with $4M/year signing bonus proration (total $16M bonus)
    contract_years = [
        KernelContractYear(year=2026, base_salary=10.0, signing_bonus_proration=4.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2027, base_salary=12.0, signing_bonus_proration=4.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2028, base_salary=14.0, signing_bonus_proration=4.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2029, base_salary=16.0, signing_bonus_proration=4.0, roster_bonus=0.0, workout_bonus=0.0),
    ]

    # Cut in 2026 post-June 1st
    current_dead, next_dead = physics.calculate_post_june1_dead_money(contract_years, current_year=2026)
    assert current_dead == 4.0
    assert next_dead == 12.0
    assert current_dead + next_dead == 16.0

    # Cut in 2027 post-June 1st
    current_dead_27, next_dead_27 = physics.calculate_post_june1_dead_money(contract_years, current_year=2027)
    assert current_dead_27 == 4.0
    assert next_dead_27 == 8.0
    assert current_dead_27 + next_dead_27 == 12.0

    # Record release in dead_money_ledger
    physics.record_post_june1_release(contract_years, current_year=2026)
    assert physics.dead_money_ledger[2026] == 4.0
    assert physics.dead_money_ledger[2027] == 12.0


def test_capologist_module_helper_post_june1():
    """Test module-level calculate_post_june1_dead_money in capologist."""
    contract_years = [
        KernelContractYear(year=1, base_salary=5.0, signing_bonus_proration=3.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2, base_salary=6.0, signing_bonus_proration=3.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=3, base_salary=7.0, signing_bonus_proration=3.0, roster_bonus=0.0, workout_bonus=0.0),
    ]
    cur, nxt = kernel_calc_post_june1(contract_years, cut_year=1)
    assert cur == 3.0
    assert nxt == 6.0


def test_salary_cap_engine_post_june1_dead_money():
    """Verify SalaryCapEngine splits dead money across current and following year."""
    engine = SalaryCapEngine()

    # Create a 5-year contract with $25M signing bonus ($5M/yr proration)
    contract = engine.create_contract(
        player_id="test_p1",
        contract_type=ContractType.VETERAN,
        total_value=50_000_000,
        years=5,
        guaranteed=30_000_000,
        signing_bonus=25_000_000,
    )

    # Cut in Year 1 post-June 1st
    cur_dead, next_dead = engine.calculate_post_june1_dead_money(contract, cut_year=1)
    assert cur_dead == 5_000_000
    assert next_dead == 20_000_000
    assert cur_dead + next_dead == 25_000_000

    # Cut in Year 3 post-June 1st
    cur_dead_y3, next_dead_y3 = engine.calculate_post_june1_dead_money(contract, cut_year=3)
    assert cur_dead_y3 == 5_000_000
    assert next_dead_y3 == 10_000_000

    # Module-level helper
    cur_m, next_m = empire_calc_post_june1(contract, cut_year=2)
    assert cur_m == 5_000_000
    assert next_m == 15_000_000


# ============================================================================
# 2. TOP-51 OFFSEASON RULE
# ============================================================================

def test_top51_cap_calculation_roster_over_51():
    """Verify that calculate_top51_cap sums exactly the top 51 highest salaries."""
    mock_db = MagicMock()

    # Create 60 mock players with decreasing salaries: $60M down to $1M
    mock_players = []
    for i in range(60, 0, -1):
        p = MagicMock()
        p.id = i
        p.team_id = 1
        p.first_name = f"Player{i}"
        p.last_name = "Test"
        p.position = "WR"
        p.contract_salary = i * 1_000_000
        p.contract_years = 2
        mock_players.append(p)

    mock_db.execute.return_value.scalars.return_value.all.return_value = mock_players

    service = SalaryCapService(mock_db)
    top51_total = service.calculate_top51_cap(team_id=1)

    # Expected: sum of 60M, 59M, ..., 10M (51 salaries)
    expected_top51 = sum(i * 1_000_000 for i in range(60, 9, -1))
    assert top51_total == expected_top51
    assert len(range(60, 9, -1)) == 51

    # Total all 60 players would be higher
    all_players_sum = sum(i * 1_000_000 for i in range(60, 0, -1))
    assert top51_total < all_players_sum


def test_top51_cap_calculation_roster_under_51():
    """Verify calculate_top51_cap when roster has fewer than 51 players."""
    mock_db = MagicMock()

    # 30 players with $2M salary each
    mock_players = []
    for i in range(30):
        p = MagicMock()
        p.id = i + 1
        p.team_id = 1
        p.contract_salary = 2_000_000
        mock_players.append(p)

    mock_db.execute.return_value.scalars.return_value.all.return_value = mock_players

    service = SalaryCapService(mock_db)
    top51_total = service.calculate_top51_cap(team_id=1)
    assert top51_total == 60_000_000


def test_salary_cap_breakdown_offseason_rule():
    """Verify get_team_cap_breakdown applies Top-51 rule during offseason."""
    mock_db = MagicMock()

    team = MagicMock()
    team.id = 1
    team.name = "Patriots"
    team.salary_cap_total = 255_000_000.0
    team.salary_cap_space = 50_000_000.0

    mock_players = []
    # 55 players: 50 players with $5M ($250M), 5 players with $1M ($5M) -> Total $255M
    for i in range(50):
        p = MagicMock()
        p.id = i + 1
        p.first_name = f"Star{i}"
        p.last_name = "Player"
        p.position = "WR"
        p.contract_salary = 5_000_000
        p.contract_years = 3
        mock_players.append(p)
    for i in range(50, 55):
        p = MagicMock()
        p.id = i + 1
        p.first_name = f"Depth{i}"
        p.last_name = "Player"
        p.position = "CB"
        p.contract_salary = 1_000_000
        p.contract_years = 1
        mock_players.append(p)

    offseason = MagicMock()
    offseason.id = 10
    offseason.status = SeasonStatus.OFF_SEASON

    def execute_off(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from team" in s_str:
            if "where team.id" in s_str or "team.id ==" in s_str:
                res.scalar_one_or_none.return_value = team
            else:
                res.scalars.return_value.all.return_value = [team]
        elif "from player" in s_str:
            res.scalars.return_value.all.return_value = mock_players
        elif "from season" in s_str:
            res.scalar_one_or_none.return_value = offseason
        return res

    mock_db.execute.side_effect = execute_off
    service = SalaryCapService(mock_db)

    # Top 51 salaries count: 50 * $5M + 1 * $1M = $251M (instead of $255M)
    off_breakdown = service.get_team_cap_breakdown(team_id=1, season_id=10)
    assert off_breakdown["is_top51_applied"] is True
    assert off_breakdown["used_cap"] == 251_000_000


def test_salary_cap_breakdown_regular_season():
    """Verify get_team_cap_breakdown counts all roster players during regular season."""
    mock_db = MagicMock()

    team = MagicMock()
    team.id = 1
    team.name = "Patriots"
    team.salary_cap_total = 255_000_000.0
    team.salary_cap_space = 50_000_000.0

    mock_players = []
    for i in range(50):
        p = MagicMock()
        p.id = i + 1
        p.first_name = f"Star{i}"
        p.last_name = "Player"
        p.position = "WR"
        p.contract_salary = 5_000_000
        p.contract_years = 3
        mock_players.append(p)
    for i in range(50, 55):
        p = MagicMock()
        p.id = i + 1
        p.first_name = f"Depth{i}"
        p.last_name = "Player"
        p.position = "CB"
        p.contract_salary = 1_000_000
        p.contract_years = 1
        mock_players.append(p)

    regseason = MagicMock()
    regseason.id = 11
    regseason.status = SeasonStatus.REGULAR_SEASON

    def execute_reg(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from team" in s_str:
            if "where team.id" in s_str or "team.id ==" in s_str:
                res.scalar_one_or_none.return_value = team
            else:
                res.scalars.return_value.all.return_value = [team]
        elif "from player" in s_str:
            res.scalars.return_value.all.return_value = mock_players
        elif "from season" in s_str:
            res.scalar_one_or_none.return_value = regseason
        return res

    mock_db.execute.side_effect = execute_reg
    service = SalaryCapService(mock_db)

    # All 55 salaries count: 50 * $5M + 5 * $1M = $255M
    reg_breakdown = service.get_team_cap_breakdown(team_id=1, season_id=11)
    assert reg_breakdown["is_top51_applied"] is False
    assert reg_breakdown["used_cap"] == 255_000_000


# ============================================================================
# 3. FREE AGENCY ENGINE MARKET OVERVIEW & PARAMETER ALIGNMENT
# ============================================================================

def test_market_overview_instantiation_parity():
    """Verify FreeAgencyEngine.get_market_overview instantiates FreeAgentMarketPlayer with 1:1 parity."""
    mock_db = MagicMock()

    player = MagicMock()
    player.id = 42
    player.first_name = "Saquon"
    player.last_name = "Barkley"
    player.position = "RB"
    player.overall_rating = 92
    player.age = 27
    player.team_id = None
    player.is_rookie = False
    player.is_retired = False

    teams = [
        MagicMock(id=1, city="Philadelphia", name="Eagles", prestige=75),
        MagicMock(id=2, city="Houston", name="Texans", prestige=70),
    ]

    def execute_side_effect(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from player" in s_str:
            res.scalars.return_value.all.return_value = [player]
        elif "from team" in s_str:
            res.scalars.return_value.all.return_value = teams
        return res

    mock_db.execute.side_effect = execute_side_effect

    engine = FreeAgencyEngine(mock_db)
    market = engine.get_market_overview(season_id=1, limit=10)

    assert len(market) == 1
    fa = market[0]
    assert isinstance(fa, FreeAgentMarketPlayer)
    assert fa.player_id == 42
    assert fa.player_name == "Saquon Barkley"
    assert fa.position == "RB"
    assert fa.overall_rating == 92
    assert fa.age == 27
    assert fa.projected_aav > 0
    assert fa.projected_years >= 2
    assert fa.tier in ["ELITE", "STARTER"]
    assert len(fa.top_interested_teams) > 0


def test_free_agent_market_player_schema_aliases():
    """Verify FreeAgentMarketPlayer schema supports both primary fields and backward-compatible aliases."""
    # Instantiation with primary fields
    fa_primary = FreeAgentMarketPlayer(
        player_id=1,
        player_name="Justin Jefferson",
        position="WR",
        overall_rating=98,
        age=25,
        projected_aav=35_000_000.0,
        projected_years=4,
        tier="ELITE",
        top_interested_teams=["Vikings", "Chiefs"]
    )
    assert fa_primary.player_name == "Justin Jefferson"
    assert fa_primary.projected_aav == 35_000_000.0

    # Instantiation with legacy alias fields
    fa_legacy = FreeAgentMarketPlayer(
        player_id=2,
        name="Lamar Jackson",
        position="QB",
        overall_rating=96,
        age=27,
        experience=6,
        projected_market_value=52_000_000.0,
        projected_years=5,
        tier="ELITE",
        top_interested_teams=["Ravens"]
    )
    assert fa_legacy.player_name == "Lamar Jackson"
    assert fa_legacy.projected_aav == 52_000_000.0


# ============================================================================
# 4. INTERACTIVE USER GM BIDDING RESOLUTION
# ============================================================================

def test_process_user_bid_accepted():
    """Test successful user GM bid when offer is competitive and within cap."""
    mock_db = MagicMock()

    player = MagicMock()
    player.id = 99
    player.first_name = "Micah"
    player.last_name = "Parsons"
    player.position = "DE"
    player.overall_rating = 95
    player.age = 26
    player.team_id = None
    player.contract = None

    user_team = MagicMock()
    user_team.id = 1
    user_team.city = "Dallas"
    user_team.name = "Cowboys"
    user_team.prestige = 80
    user_team.salary_cap_space = 45_000_000.0

    def exec_side_effect(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from player" in s_str:
            res.scalar_one_or_none.return_value = player
            res.scalars.return_value.all.return_value = []
        elif "from team" in s_str:
            if "where team.id !=" in s_str or "where team.id <>" in s_str or "!=" in s_str:
                res.scalars.return_value.all.return_value = []
            else:
                res.scalar_one_or_none.return_value = user_team
                res.scalars.return_value.all.return_value = [user_team]
        return res

    mock_db.execute.side_effect = exec_side_effect

    engine = FreeAgencyEngine(mock_db)
    bid_response = engine.process_user_bid(
        season_id=1,
        player_id=99,
        team_id=1,
        years=4,
        total_amount=120_000_000, # $30M AAV
        signing_bonus=20_000_000,
        guaranteed_amount=80_000_000,
    )

    assert isinstance(bid_response, FreeAgentBidResponse)
    assert bid_response.accepted is True
    assert bid_response.status == "ACCEPTED"
    assert player.team_id == 1
    assert player.contract_salary == 30_000_000
    assert player.contract_years == 4
    assert mock_db.commit.called


def test_process_user_bid_outbid_by_ai():
    """Test user GM bid when a competitive AI GM counter-offer outbids the user."""
    mock_db = MagicMock()

    player = MagicMock()
    player.id = 77
    player.first_name = "Chris"
    player.last_name = "Jones"
    player.position = "DT"
    player.overall_rating = 94
    player.age = 30
    player.team_id = None
    player.contract = None

    user_team = MagicMock()
    user_team.id = 1
    user_team.city = "Raiders"
    user_team.name = "Las Vegas"
    user_team.prestige = 50
    user_team.salary_cap_space = 40_000_000.0

    ai_team = MagicMock()
    ai_team.id = 2
    ai_team.city = "Kansas City"
    ai_team.name = "Chiefs"
    ai_team.prestige = 90
    ai_team.salary_cap_space = 60_000_000.0

    def exec_side_effect(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from player" in s_str:
            res.scalar_one_or_none.return_value = player
            res.scalars.return_value.all.return_value = []
        elif "from team" in s_str:
            if "where team.id !=" in s_str or "!=" in s_str:
                res.scalars.return_value.all.return_value = [ai_team]
            else:
                res.scalar_one_or_none.return_value = user_team
                res.scalars.return_value.all.return_value = [user_team]
        return res

    mock_db.execute.side_effect = exec_side_effect

    engine = FreeAgencyEngine(mock_db)
    # User makes modest offer, AI team (Chiefs, prestige 90) outbids
    bid_response = engine.process_user_bid(
        season_id=1,
        player_id=77,
        team_id=1,
        years=2,
        total_amount=36_000_000, # $18M AAV
        signing_bonus=5_000_000,
        guaranteed_amount=20_000_000,
    )

    assert isinstance(bid_response, FreeAgentBidResponse)
    assert bid_response.accepted is False
    assert bid_response.status == "OUTBID"
    assert "Kansas City" in bid_response.message
    assert player.team_id == 2


def test_process_user_bid_insufficient_cap():
    """Test user GM bid rejection when Year 1 cap hit exceeds team cap space."""
    mock_db = MagicMock()

    player = MagicMock()
    player.id = 10
    player.first_name = "Myles"
    player.last_name = "Garrett"
    player.position = "DE"
    player.overall_rating = 98
    player.age = 29
    player.team_id = None

    broke_team = MagicMock()
    broke_team.id = 2
    broke_team.city = "Cleveland"
    broke_team.name = "Browns"
    broke_team.prestige = 60
    broke_team.salary_cap_space = 5_000_000.0 # Only $5M cap space

    def exec_side_effect(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from player" in s_str:
            res.scalar_one_or_none.return_value = player
        elif "from team" in s_str:
            res.scalar_one_or_none.return_value = broke_team
        return res

    mock_db.execute.side_effect = exec_side_effect

    engine = FreeAgencyEngine(mock_db)
    # Offer $35M AAV with only $5M available cap
    bid_response = engine.process_user_bid(
        season_id=1,
        player_id=10,
        team_id=2,
        years=3,
        total_amount=105_000_000,
        signing_bonus=15_000_000,
        guaranteed_amount=60_000_000,
    )

    assert bid_response.accepted is False
    assert bid_response.status == "REJECTED"
    assert "exceeds available cap space" in bid_response.message
    assert player.team_id is None


def test_process_user_bid_lowball_rejected():
    """Test rejection when user GM submits an offensive lowball offer (<65% market value)."""
    mock_db = MagicMock()

    player = MagicMock()
    player.id = 5
    player.first_name = "Joe"
    player.last_name = "Burrow"
    player.position = "QB"
    player.overall_rating = 97
    player.age = 28
    player.team_id = None

    team = MagicMock()
    team.id = 3
    team.city = "Cincinnati"
    team.name = "Bengals"
    team.prestige = 75
    team.salary_cap_space = 80_000_000.0

    def exec_side_effect(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from player" in s_str:
            res.scalar_one_or_none.return_value = player
        elif "from team" in s_str:
            res.scalar_one_or_none.return_value = team
        return res

    mock_db.execute.side_effect = exec_side_effect

    engine = FreeAgencyEngine(mock_db)
    # Offer only $5M/year for an elite 97 OVR QB (market is ~$50M+)
    bid_response = engine.process_user_bid(
        season_id=1,
        player_id=5,
        team_id=3,
        years=4,
        total_amount=20_000_000, # $5M AAV
        signing_bonus=2_000_000,
        guaranteed_amount=5_000_000,
    )

    assert bid_response.accepted is False
    assert bid_response.status == "REJECTED"
    assert "rejected your offer" in bid_response.message


# ============================================================================
# 5. API ROUTE REGISTRATION VERIFICATION
# ============================================================================

def test_season_router_endpoints_registered():
    """Verify that both singular /api/season and plural /api/seasons routes are active."""
    registered_paths = [route.path for route in season_router.routes]

    # Check that market and bid endpoints are registered
    assert any("free-agency/market" in path for path in registered_paths)
    assert any("free-agency/bid" in path for path in registered_paths)

    # Check both singular and plural paths exist
    has_market_singular = any(path.endswith("/free-agency/market") and "season/" in path for path in registered_paths)
    has_market_plural = any("/api/seasons/" in path and "free-agency/market" in path for path in registered_paths)
    assert has_market_singular, "Singular /api/season/{season_id}/free-agency/market must be registered"
    assert has_market_plural, "Plural /api/seasons/{season_id}/free-agency/market must be registered"

    has_bid_singular = any(path.endswith("/free-agency/bid") and "season/" in path for path in registered_paths)
    has_bid_plural = any("/api/seasons/" in path and "free-agency/bid" in path for path in registered_paths)
    assert has_bid_singular, "Singular /api/season/{season_id}/free-agency/bid must be registered"
    assert has_bid_plural, "Plural /api/seasons/{season_id}/free-agency/bid must be registered"
