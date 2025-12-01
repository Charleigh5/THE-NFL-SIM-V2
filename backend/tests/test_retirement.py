import pytest
from unittest.mock import MagicMock, patch, ANY
from app.services.offseason_service import OffseasonService
from app.models.player import Player
from app.models.season import Season
from app.models.hall_of_fame import HallOfFame
from app.models.stats import PlayerGameStats

class MockPlayer:
    def __init__(self, id, first_name, last_name, age, overall_rating, team_id=1, is_retired=False, legacy_score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.overall_rating = overall_rating
        self.team_id = team_id
        self.is_retired = is_retired
        self.legacy_score = legacy_score
        self.retirement_year = None

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    return OffseasonService(mock_db)

def test_process_retirements_old_player(service, mock_db):
    """Test that very old players retire."""
    season = Season(id=1, year=2025)
    player = MockPlayer(1, "Old", "Guy", age=41, overall_rating=70)
    
    mock_db.query.return_value.get.return_value = season
    mock_db.query.return_value.filter.return_value.all.return_value = [player]
    
    # Mock career stats calculation
    with patch.object(service, '_calculate_career_stats', return_value={}):
        service.process_retirements(1)
    
    assert player.is_retired is True
    assert player.retirement_year == 2025
    assert player.team_id is None

def test_process_retirements_young_player(service, mock_db):
    """Test that young players do not retire."""
    season = Season(id=1, year=2025)
    player = MockPlayer(1, "Young", "Guy", age=22, overall_rating=90)
    
    mock_db.query.return_value.get.return_value = season
    mock_db.query.return_value.filter.return_value.all.return_value = [player]
    
    service.process_retirements(1)
    
    assert player.is_retired is False
    assert player.team_id == 1

def test_hall_of_fame_induction(service, mock_db):
    """Test that great players get inducted into Hall of Fame."""
    season = Season(id=1, year=2025)
    player = MockPlayer(1, "Legend", "Player", age=41, overall_rating=95, legacy_score=2000)
    
    mock_db.query.return_value.get.return_value = season
    mock_db.query.return_value.filter.return_value.all.return_value = [player]
    
    # Mock career stats
    career_stats = {"pass_yards": 50000, "pass_tds": 400}
    
    # We need to mock _calculate_career_stats because it uses complex query
    with patch.object(service, '_calculate_career_stats', return_value=career_stats):
        service.process_retirements(1)
        
    assert player.is_retired is True
    
    # Verify HallOfFame entry added
    # We check if db.add was called with a HallOfFame object
    args = mock_db.add.call_args
    assert args is not None
    hof_entry = args[0][0]
    assert isinstance(hof_entry, HallOfFame)
    assert hof_entry.player_id == player.id
    assert hof_entry.year_inducted == 2025
    assert hof_entry.career_stats_snapshot == career_stats
