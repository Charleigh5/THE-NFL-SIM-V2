import pytest
from unittest.mock import MagicMock, patch
from app.services.offseason_service import OffseasonService
from app.models.player import Player, Position
from app.models.draft import DraftPick

class MockPlayer:
    def __init__(self, id, position, overall_rating, is_rookie=True, team_id=None):
        self.id = id
        self.first_name = "Mock"
        self.last_name = "Player"
        self.position = position
        self.overall_rating = overall_rating
        self.is_rookie = is_rookie
        self.team_id = team_id
        self.contract_years = 0

class MockPick:
    def __init__(self, team_id, pick_number):
        self.team_id = team_id
        self.pick_number = pick_number
        self.player_id = None
        self.round = 1

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    return OffseasonService(mock_db)

def test_draft_logic_needs(service, mock_db):
    """Test that draft logic prioritizes team needs."""
    
    # Setup: Team 1 needs a QB (has 0), has plenty of RBs
    # Available Rookies: 
    # 1. RB (90 OVR) - Best Player Available
    # 2. QB (85 OVR) - Position of Need
    
    team_id = 1
    
    # Mock existing roster (No QBs, 5 RBs)
    existing_players = [
        MockPlayer(10, "RB", 80, is_rookie=False, team_id=team_id) for _ in range(5)
    ]
    
    # Mock Rookies
    rookie_rb = MockPlayer(101, "RB", 90)
    rookie_qb = MockPlayer(102, "QB", 85)
    rookies = [rookie_rb, rookie_qb]
    
    # Mock Draft Pick
    pick = MockPick(team_id, 1)
    
    # Configure DB mocks
    # Configure DB mocks
    # 1. Picks query: query(DraftPick).filter().order_by().all()
    # 2. Rookies query: query(Player).filter().order_by().all()
    # 3. Team needs query: query(Player).filter().all()
    
    # We need to distinguish these. 
    # A simple way is to mock the return values based on the model passed to query()
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == DraftPick:
            mock_query.filter.return_value.order_by.return_value.all.return_value = [pick]
        elif model == Player:
            # This is tricky because Player is used for both Rookies and Team Needs
            # Rookies has order_by, Team Needs does not.
            
            # Mock for Rookies (has order_by)
            mock_query.filter.return_value.order_by.return_value.all.return_value = rookies
            
            # Mock for Team Needs (no order_by)
            mock_query.filter.return_value.all.return_value = existing_players
        return mock_query

    mock_db.query.side_effect = query_side_effect
    
    # Run simulation
    service.simulate_draft(season_id=1)
    
    # Assertions
    # Should have picked the QB (85) over the RB (90) because of need
    assert pick.player_id == 102
    assert rookie_qb.team_id == team_id
    assert not rookie_qb.is_rookie

def test_draft_logic_bpa(service, mock_db):
    """Test that draft logic takes BPA if no immediate need in top prospects."""
    
    # Setup: Team 1 needs a Kicker (has 0)
    # Available Rookies: 
    # 1. QB (99 OVR) - Best Player Available
    # 2. K (60 OVR) - Position of Need, but low value
    
    team_id = 1
    
    # Mock existing roster (No Kickers)
    existing_players = []
    
    # Mock Rookies
    rookie_qb = MockPlayer(201, "QB", 99)
    rookie_k = MockPlayer(202, "K", 60)
    # Kicker is far down the list (index > 10 in real scenario, but here we test the logic branch)
    # To force BPA, we make the need-player not appear in the "top X" check loop
    # In our implementation, we check top 10. So let's put Kicker at index 11.
    
    rookies = [rookie_qb] + [MockPlayer(300+i, "WR", 70) for i in range(10)] + [rookie_k]
    
    pick = MockPick(team_id, 1)
    
    def query_side_effect(model):
        mock_query = MagicMock()
        if model == DraftPick:
            mock_query.filter.return_value.order_by.return_value.all.return_value = [pick]
        elif model == Player:
            mock_query.filter.return_value.order_by.return_value.all.return_value = rookies
            mock_query.filter.return_value.all.return_value = existing_players
        return mock_query

    mock_db.query.side_effect = query_side_effect
    
    service.simulate_draft(season_id=1)
    
    # Should pick the QB (BPA) because Kicker was too far down
    assert pick.player_id == 201
