"""Unit tests for the FreeAgencyEngine service."""
import pytest
from unittest.mock import MagicMock
from app.services.free_agency_engine import FreeAgencyEngine, POSITION_TARGETS
from app.models.player import Player, Position
from app.models.team import Team


class MockPlayer:
    def __init__(self, id, first_name, last_name, position, overall_rating, age=26, experience=3, is_rookie=False, is_retired=False, team_id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position.value if isinstance(position, Position) else position
        self.overall_rating = overall_rating
        self.age = age
        self.experience = experience
        self.is_rookie = is_rookie
        self.is_retired = is_retired
        self.team_id = team_id
        self.contract_years = 0
        self.contract_salary = 0
        self.contract = None


class MockTeam:
    def __init__(self, id, name, city="Test", abbreviation="TST", prestige=50, salary_cap_space=50_000_000.0, salary_cap_total=255_000_000.0):
        self.id = id
        self.name = name
        self.city = city
        self.abbreviation = abbreviation
        self.prestige = prestige
        self.salary_cap_space = salary_cap_space
        self.salary_cap_total = salary_cap_total


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def fa_engine(mock_db):
    return FreeAgencyEngine(mock_db)


def test_market_valuation_scale(fa_engine):
    """Test market valuation for different positions and ratings."""
    elite_qb = MockPlayer(1, "Patrick", "Mahomes", "QB", 99, age=28)
    aav_qb, years_qb, gtd_qb = fa_engine.calculate_market_value(elite_qb)
    assert aav_qb >= 40_000_000
    assert years_qb >= 3
    assert gtd_qb > 0

    starter_wr = MockPlayer(2, "Tyler", "Boyd", "WR", 82, age=27)
    aav_wr, years_wr, gtd_wr = fa_engine.calculate_market_value(starter_wr)
    assert 8_000_000 <= aav_wr <= 25_000_000
    assert years_wr >= 2

    kicker = MockPlayer(3, "Justin", "Tucker", "K", 88, age=33)
    aav_k, years_k, gtd_k = fa_engine.calculate_market_value(kicker)
    assert aav_k <= 10_000_000
    assert years_k <= 2


def test_player_tier_classification(fa_engine):
    """Test player tier categorization."""
    assert fa_engine.get_player_tier(92) == "ELITE"
    assert fa_engine.get_player_tier(80) == "STARTER"
    assert fa_engine.get_player_tier(74) == "ROTATIONAL"
    assert fa_engine.get_player_tier(66) == "DEPTH"


def test_team_interest_scoring(fa_engine):
    """Test AI team interest calculation."""
    team = MockTeam(1, "Lions", prestige=60)
    prospect = MockPlayer(10, "Aidan", "Hutchinson", "DE", 90, age=25)
    aav, _, _ = fa_engine.calculate_market_value(prospect)

    # When team has 0 DEs (huge need) and $50M cap
    empty_roster = {"DE": 0}
    interest_high = fa_engine.calculate_team_interest(team, prospect, empty_roster, aav, 50_000_000.0)
    assert interest_high > 60.0

    # When team cannot afford player
    interest_broke = fa_engine.calculate_team_interest(team, prospect, empty_roster, aav, 500_000.0)
    assert interest_broke == 0.0


def test_simulate_free_agency_bidding_flow(fa_engine, mock_db):
    """Test full multi-round competitive free agency auction."""
    teams = [
        MockTeam(1, "Patriots", prestige=70, salary_cap_space=60_000_000.0),
        MockTeam(2, "Bears", prestige=50, salary_cap_space=45_000_000.0)
    ]

    free_agents = [
        MockPlayer(101, "Star", "Quarterback", "QB", 90, age=26),
        MockPlayer(102, "Elite", "Receiver", "WR", 86, age=27),
        MockPlayer(103, "Solid", "Tackle", "OT", 78, age=28),
        MockPlayer(104, "Depth", "Safety", "S", 69, age=25),
    ]

    def execute_side_effect(stmt):
        mock_result = MagicMock()
        stmt_str = str(stmt).lower()
        if "from player" in stmt_str:
            if "team_id is null" in stmt_str or "team_id = null" in stmt_str or "team_id is" in stmt_str or "team_id !=" not in stmt_str:
                mock_result.scalars.return_value.all.return_value = free_agents
            else:
                # Active roster players
                mock_result.scalars.return_value.all.return_value = []
        elif "from team" in stmt_str:
            mock_result.scalars.return_value.all.return_value = teams
        return mock_result

    mock_db.execute.side_effect = execute_side_effect
    mock_db.commit.return_value = None

    signings = fa_engine.simulate_free_agency(season_id=1)
    assert len(signings) > 0

    # Verify top signings have realistic contracts
    top_signing = next(s for s in signings if s.player_id == 101)
    assert top_signing.annual_avg >= 20_000_000
    assert top_signing.contract_years >= 3
    assert top_signing.team_id in [1, 2]
    assert top_signing.signing_grade in ["A+", "A", "B+", "B", "C+", "C"]
