"""
Comprehensive offseason service tests focusing on core functionality.

These tests verify the offseason service's ability to:
1. Process contract expirations
2. Generate draft order
3. Simulate drafts with team needs
4. Simulate free agency
5. Generate rookie classes

Testing approach: Use mocks and patches to test service logic independently
without requiring full database integration.
"""

import pytest
from unittest.mock import MagicMock, patch, call
from app.services.offseason_service import OffseasonService
from app.services.rookie_generator import RookieGenerator
from app.models.player import Player, Position
from app.models.team import Team
from app.models.season import Season, SeasonStatus
from app.models.draft import DraftPick
from app.models.playoff import PlayoffMatchup, PlayoffRound


class MockTeam:
    """Mock Team object for testing."""
    def __init__(self, id, name, city="City", abbreviation="ABC"):
        self.id = id
        self.name = name
        self.city = city
        self.abbreviation = abbreviation


class MockPlayer:
    """Mock Player object for testing."""
    def __init__(self, id, first_name, last_name, position, team_id=None, 
                 contract_years=0, overall_rating=70, is_rookie=False):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.team_id = team_id
        self.contract_years = contract_years
        self.overall_rating = overall_rating
        self.is_rookie = is_rookie


class MockSeason:
    """Mock Season object for testing."""
    def __init__(self, id, year, status=SeasonStatus.POST_SEASON, current_week=22):
        self.id = id
        self.year = year
        self.status = status
        self.current_week = current_week


class MockStandingEntry:
    """Mock standings entry."""
    def __init__(self, team_id, wins, losses, win_pct, point_differential):
        self.team_id = team_id
        self.wins = wins
        self.losses = losses
        self.win_pct = win_pct
        self.point_differential = point_differential


class MockDraftPick:
    """Mock DraftPick object for testing."""
    def __init__(self, id, season_id, team_id, round, pick_number, player_id=None):
        self.id = id
        self.season_id = season_id
        self.team_id = team_id
        self.round = round
        self.pick_number = pick_number
        self.player_id = player_id
        self.original_team_id = team_id


# ===== FIXTURES =====

@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture
def service(mock_db):
    """Create an OffseasonService instance with mocked database."""
    return OffseasonService(mock_db)


# ===== CONTRACT EXPIRATION TESTS =====

def test_process_contract_expirations_releases_expired_players(service, mock_db):
    """Test that players with 1 year contracts get released to free agency."""
    
    # Create players with expiring contracts
    expiring_players = [
        MockPlayer(1, "John", "Doe", Position.QB, team_id=1, contract_years=1),
        MockPlayer(2, "Jane", "Smith", Position.WR, team_id=2, contract_years=1),
    ]
    
    # Setup mock query
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Player:
            filter_mock = MagicMock()
            filter_mock.all.return_value = expiring_players
            mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    
    # Process expirations
    service.process_contract_expirations()
    
    # Verify contracts decremented and players released
    for player in expiring_players:
        assert player.contract_years == 0
        assert player.team_id is None


def test_process_contract_expirations_keeps_multi_year_contracts(service, mock_db):
    """Test that players with multi-year contracts stay on team."""
    
    multi_year_players = [
        MockPlayer(3, "Bob", "Johnson", Position.RB, team_id=1, contract_years=3),
        MockPlayer(4, "Alice", "Williams", Position.TE, team_id=2, contract_years=2),
    ]
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Player:
            filter_mock = MagicMock()
            filter_mock.all.return_value = multi_year_players
            mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    
    service.process_contract_expirations()
    
    # Verify contracts decremented but players kept
    assert multi_year_players[0].contract_years == 2
    assert multi_year_players[0].team_id == 1
    assert multi_year_players[1].contract_years == 1
    assert multi_year_players[1].team_id == 2


# ===== DRAFT ORDER TESTS =====

def test_generate_draft_order_creates_correct_number_of_picks(service, mock_db):
    """Test that draft order generates 7 rounds of 32 picks (224 total)."""
    
    season_id = 1
    
    # Create standings for 32 teams
    standings = [
        MockStandingEntry(team_id=i, wins=5+i, losses=12-i, win_pct=(5+i)/17, point_differential=0)
        for i in range(1, 33)
    ]
    
    added_picks = []
    
    def add_side_effect(obj):
        if isinstance(obj, DraftPick):
            added_picks.append(obj)
    
    mock_db.add.side_effect = add_side_effect
    
    # Mock standings calculator
    with patch.object(service.standings_calculator, 'calculate_standings', return_value=standings):
        # Mock playoff matchup query
        def query_side_effect(model):
            mock_query = MagicMock()
            if model == PlayoffMatchup:
                filter_mock = MagicMock()
                filter_mock.first.return_value = None  # No Super Bowl yet
                mock_query.filter.return_value = filter_mock
            return mock_query
        
        mock_db.query.side_effect = query_side_effect
        
        service.generate_draft_order(season_id)
    
    # Verify 224 picks created (7 rounds * 32 teams)
    assert len(added_picks) == 224


def test_generate_draft_order_worst_team_picks_first(service, mock_db):
    """Test that the team with worst record gets first pick in each round."""
    
    season_id = 1
    
    # Create standings (worst to best)
    standings = [
        MockStandingEntry(team_id=1, wins=2, losses=15, win_pct=0.117, point_differential=-100),
        MockStandingEntry(team_id=2, wins=5, losses=12, win_pct=0.294, point_differential=-50),
        MockStandingEntry(team_id=3, wins=8, losses=9, win_pct=0.470, point_differential=0),
    ]
    
    added_picks = []
    
    def add_side_effect(obj):
        if isinstance(obj, DraftPick):
            added_picks.append(obj)
    
    mock_db.add.side_effect = add_side_effect
    
    with patch.object(service.standings_calculator, 'calculate_standings', return_value=standings):
        def query_side_effect(model):
            mock_query = MagicMock()
            if model == PlayoffMatchup:
                filter_mock = MagicMock()
                filter_mock.first.return_value = None
                mock_query.filter.return_value = filter_mock
            return mock_query
        
        mock_db.query.side_effect = query_side_effect
        
        service.generate_draft_order(season_id)
    
    # First pick should go to worst team (team_id=1)
    first_pick = [p for p in added_picks if p.pick_number == 1][0]
    assert first_pick.team_id == 1


# ===== ROOKIE GENERATION TESTS =====

def test_rookie_generator_creates_correct_count():
    """Test that RookieGenerator creates the specified number of rookies."""
    
    mock_db = MagicMock()
    generator = RookieGenerator(mock_db)
    
    added_players = []
    
    def add_all_side_effect(players):
        added_players.extend(players)
    
    mock_db.add_all.side_effect = add_all_side_effect
    mock_db.commit.return_value = None
    
    # Generate 100 rookies
    result = generator.generate_draft_class(season_id=1, count=100)
    
    assert len(result) == 100
    assert len(added_players) == 100


def test_rookie_generator_creates_players_with_correct_attributes():
    """Test that generated rookies have appropriate attributes."""
    
    mock_db = MagicMock()
    generator = RookieGenerator(mock_db)
    
    added_players = []
    
    def add_all_side_effect(players):
        added_players.extend(players)
    
    mock_db.add_all.side_effect = add_all_side_effect
    mock_db.commit.return_value = None
    
    rookies = generator.generate_draft_class(season_id=1, count=10)
    
    for rookie in rookies:
        # Check basic attributes
        assert rookie.is_rookie is True
        assert rookie.team_id is None  # Should be free agent
        assert rookie.experience == 0
        assert rookie.contract_years == 4  # Rookie contract
        
        # Check rating is in reasonable range
        assert 50 <= rookie.overall_rating <= 99
        
        # Check physical attributes
        assert 21 <= rookie.age <= 23
        assert 68 <= rookie.height <= 80
        assert 180 <= rookie.weight <= 350


# ===== DRAFT SIMULATION TESTS =====

def test_simulate_draft_fills_all_picks(service, mock_db):
    """Test that draft simulation assigns a player to every pick."""
    
    season_id = 1
    
    # Create mock picks
    picks = [
        MockDraftPick(i, season_id, team_id=((i-1) % 4) + 1, round=1, pick_number=i, player_id=None)
        for i in range(1, 5)  # 4 picks
    ]
    
    # Create mock rookies
    rookies = [
        MockPlayer(10+i, f"Rookie{i}", "Player", Position.QB, overall_rating=70+i, is_rookie=True)
        for i in range(10)  # More rookies than picks
    ]
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == DraftPick:
            filter_mock = MagicMock()
            order_mock = MagicMock()
            order_mock.all.return_value = picks
            filter_mock.order_by.return_value = order_mock
            mock_query.filter.return_value = filter_mock
        elif model == Player:
            filter_mock = MagicMock()
            order_mock = MagicMock()
            order_mock.all.return_value = rookies
            filter_mock.order_by.return_value = order_mock
            mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    mock_db.commit.return_value = None
    
    service.simulate_draft(season_id)
    
    # Verify all picks have been assigned
    for pick in picks:
        assert pick.player_id is not None


def test_simulate_draft_respects_team_needs(service, mock_db):
    """Test that draft prioritizes positions of need."""
    
    season_id = 1
    team_id = 1
    
    # Create a single pick
    picks = [MockDraftPick(1, season_id, team_id, round=1, pick_number=1)]
    
    # Create rookies with different positions
    rookies = [
        MockPlayer(10, "QB", "Prospect", Position.QB, overall_rating=85, is_rookie=True),
        MockPlayer(11, "WR", "Prospect", Position.WR, overall_rating=87, is_rookie=True),
    ]
    
    # Mock team having many WRs but no QBs (need QB)
    team_players = [
        MockPlayer(20+i, "Existing", f"WR{i}", Position.WR, team_id=team_id)
        for i in range(6)  # 6 WRs
    ]
    
    query_call_count = [0]
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == DraftPick:
            filter_mock = MagicMock()
            order_mock = MagicMock()
            order_mock.all.return_value = picks
            filter_mock.order_by.return_value = order_mock
            mock_query.filter.return_value = filter_mock
        elif model == Player:
            query_call_count[0] += 1
            filter_mock = MagicMock()
            
            # First call gets rookies, subsequent calls get team roster
            if query_call_count[0] == 1:
                order_mock = MagicMock()
                order_mock.all.return_value = rookies
                filter_mock.order_by.return_value = order_mock
            else:
                filter_mock.all.return_value = team_players
            
            mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    mock_db.commit.return_value = None
    
    service.simulate_draft(season_id)
    
    # Should pick QB (position of need) even though WR has higher rating
    assert picks[0].player_id == 10  # QB prospect


# ===== FREE AGENCY SIMULATION TESTS =====

def test_simulate_free_agency_fills_rosters_to_53(service, mock_db):
    """Test that free agency fills team rosters to 53 players."""
    
    season_id = 1
    
    # Create teams
    teams = [MockTeam(1, "Team1"), MockTeam(2, "Team2")]
    
    # Create free agents
    free_agents = [
        MockPlayer(100+i, f"FA{i}", "Player", Position.QB, overall_rating=70)
        for i in range(200)  # Plenty of free agents
    ]
    
    query_call_count = [0]
    current_team_id = [None]
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Team:
            mock_query.all.return_value = teams
        elif model == Player:
            query_call_count[0] += 1
            
            # First call: get free agents
            if query_call_count[0] == 1:
                filter_mock = MagicMock()
                order_mock = MagicMock()
                order_mock.all.return_value = free_agents
                filter_mock.order_by.return_value = order_mock
                mock_query.filter.return_value = filter_mock
            # Subsequent calls: check roster counts (simulate empty rosters)
            else:
                filter_mock = MagicMock()
                filter_mock.count.return_value = 0  # Empty roster
                mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    mock_db.commit.return_value = None
    
    service.simulate_free_agency(season_id)
    
    # Verify free agents were signed (first 106 players should be signed to teams)
    # Team1: 53 players, Team2: 53 players
    signed_count = sum(1 for fa in free_agents if fa.team_id is not None)
    assert signed_count == 106  # 53 * 2 teams


def test_simulate_free_agency_signs_best_available_players(service, mock_db):
    """Test that free agency prioritizes higher-rated players."""
    
    season_id = 1
    teams = [MockTeam(1, "Team1")]
    
    # Create free agents with varying ratings
    free_agents = [
        MockPlayer(1, "Star", "Player", Position.QB, overall_rating=95),
        MockPlayer(2, "Good", "Player", Position.WR, overall_rating=85),
        MockPlayer(3, "Average", "Player", Position.RB, overall_rating=70),
    ]
    
    query_call_count = [0]
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Team:
            mock_query.all.return_value = teams
        elif model == Player:
            query_call_count[0] += 1
            
            if query_call_count[0] == 1:
                # Return free agents ordered by rating (desc)
                filter_mock = MagicMock()
                order_mock = MagicMock()
                order_mock.all.return_value = free_agents
                filter_mock.order_by.return_value = order_mock
                mock_query.filter.return_value = filter_mock
            else:
                # Simulate roster needing 2 players
                filter_mock = MagicMock()
                filter_mock.count.return_value = 51  # Need 2 more
                mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    mock_db.commit.return_value = None
    
    service.simulate_free_agency(season_id)
    
    # Top 2 players should be signed
    assert free_agents[0].team_id == 1  # Star player signed
    assert free_agents[1].team_id == 1  # Good player signed
    assert free_agents[2].team_id is None  # Average player not needed


# ===== INTEGRATION TEST: START OFFSEASON =====

def test_start_offseason_executes_all_steps(service, mock_db):
    """Test that start_offseason orchestrates all offseason steps correctly."""
    
    season_id = 1
    season = MockSeason(season_id, 2025, status=SeasonStatus.POST_SEASON)
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == Season:
            filter_mock = MagicMock()
            filter_mock.first.return_value = season
            mock_query.filter.return_value = filter_mock
        return mock_query
    
    mock_db.query.side_effect = query_side_effect
    mock_db.commit.return_value = None
    
    # Mock all internal methods
    with patch.object(service, 'process_contract_expirations') as mock_contracts, \
         patch.object(service, 'generate_draft_order') as mock_draft_order, \
         patch.object(service.rookie_generator, 'generate_draft_class') as mock_rookies:
        
        result = service.start_offseason(season_id)
        
        # Verify status changed to OFF_SEASON
        assert season.status == SeasonStatus.OFF_SEASON
        
        # Verify all steps were called
        mock_contracts.assert_called_once()
        mock_draft_order.assert_called_once_with(season_id)
        mock_rookies.assert_called_once_with(season_id)
        
        # Verify commit was called
        mock_db.commit.assert_called_once()
        
        # Verify success message
        assert "Offseason started" in result["message"]
