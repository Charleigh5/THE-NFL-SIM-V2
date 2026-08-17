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
    team_id = 1
    
    # Mock existing roster (No QBs, 5 RBs)
    existing_players = [
        MockPlayer(10 + i, "RB", 80, is_rookie=False, team_id=team_id) for i in range(5)
    ]
    
    # Mock Rookies
    rookie_rb = MockPlayer(101, "RB", 90, is_rookie=True)
    rookie_qb = MockPlayer(102, "QB", 85, is_rookie=True)
    rookies = [rookie_rb, rookie_qb]
    
    # Mock Draft Pick
    pick = MockPick(team_id, 1)
    
    def execute_side_effect(stmt):
        mock_result = MagicMock()
        stmt_str = str(stmt).lower()
        
        if "from draft_pick" in stmt_str:
            next_pick = pick if pick.player_id is None else None
            mock_result.scalars.return_value.first.return_value = next_pick
        elif "from player" in stmt_str:
            if "team_id is null" in stmt_str:
                mock_result.scalars.return_value.all.return_value = [r for r in rookies if r.is_rookie]
            else:
                mock_result.scalars.return_value.all.return_value = existing_players
        return mock_result

    mock_db.execute.side_effect = execute_side_effect
    mock_db.get.return_value = None
    mock_db.commit.return_value = None
    
    # Run simulation
    service.simulate_draft(season_id=1)
    
    # Assertions
    # Should have picked the QB (85) over the RB (90) because of need
    assert pick.player_id == 102
    assert rookie_qb.team_id == team_id
    assert not rookie_qb.is_rookie


def test_draft_logic_bpa(service, mock_db):
    """Test that draft logic takes BPA if no immediate need in top prospects."""
    team_id = 1
    
    existing_players = []
    
    # Mock Rookies: QB (99) top, K (60) way down at index 11
    rookie_qb = MockPlayer(201, "QB", 99, is_rookie=True)
    rookie_k = MockPlayer(202, "K", 60, is_rookie=True)
    rookies = [rookie_qb] + [MockPlayer(300 + i, "WR", 70, is_rookie=True) for i in range(10)] + [rookie_k]
    
    pick = MockPick(team_id, 1)
    
    def execute_side_effect(stmt):
        mock_result = MagicMock()
        stmt_str = str(stmt).lower()
        
        if "from draft_pick" in stmt_str:
            next_pick = pick if pick.player_id is None else None
            mock_result.scalars.return_value.first.return_value = next_pick
        elif "from player" in stmt_str:
            if "team_id is null" in stmt_str:
                mock_result.scalars.return_value.all.return_value = [r for r in rookies if r.is_rookie]
            else:
                mock_result.scalars.return_value.all.return_value = existing_players
        return mock_result

    mock_db.execute.side_effect = execute_side_effect
    mock_db.get.return_value = None
    mock_db.commit.return_value = None
    
    service.simulate_draft(season_id=1)
    
    # Should pick the QB (BPA) because Kicker was too far down
    assert pick.player_id == 201
