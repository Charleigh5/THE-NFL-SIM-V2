import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.enhanced_chemistry_service import EnhancedChemistryService
from app.models.game import Game
from app.models.stats import PlayerGameStart

@pytest.mark.asyncio
async def test_calculate_chemistry_level():
    service = EnhancedChemistryService(AsyncMock())

    # Test < 5 games
    assert service.calculate_chemistry_level(0) == 0.0
    assert service.calculate_chemistry_level(4) == 0.0

    # Test 5 games (Threshold)
    assert abs(service.calculate_chemistry_level(5) - 0.6) < 0.001

    # Test 10 games (Max)
    assert service.calculate_chemistry_level(10) == 1.0
    assert service.calculate_chemistry_level(15) == 1.0

    # Test intermediate values
    chem_6 = service.calculate_chemistry_level(6)
    chem_7 = service.calculate_chemistry_level(7)
    assert 0.6 < chem_6 < chem_7 < 1.0

@pytest.mark.asyncio
async def test_get_team_chemistry_metadata_optimized_no_history():
    mock_result = MagicMock()
    mock_result.all.return_value = []
    mock_result.scalars.return_value.all.return_value = []

    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    service = EnhancedChemistryService(mock_db)

    starters = {"LT": 1, "LG": 2, "C": 3, "RG": 4, "RT": 5}
    metadata = await service.get_team_chemistry_metadata_optimized(1, starters)

    assert metadata.chemistry_level == 0.0
    assert metadata.consecutive_games == 0

@pytest.mark.asyncio
async def test_get_team_chemistry_metadata_optimized_with_history():
    # Mock 5 games of history with same starters
    # Rows: game_id, week, position, player_id
    rows = []
    for i in range(1, 6):
        rows.append((i, i, "LT", 1))
        rows.append((i, i, "LG", 2))
        rows.append((i, i, "C", 3))
        rows.append((i, i, "RG", 4))
        rows.append((i, i, "RT", 5))

    mock_result = MagicMock()
    mock_result.all.return_value = rows
    mock_result.scalars.return_value.all.return_value = rows

    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    service = EnhancedChemistryService(mock_db)

    starters = {"LT": 1, "LG": 2, "C": 3, "RG": 4, "RT": 5}
    metadata = await service.get_team_chemistry_metadata_optimized(1, starters)

    assert metadata.consecutive_games == 5
    assert abs(metadata.chemistry_level - 0.6) < 0.001
    assert metadata.bonuses["pass_block"] > 0

@pytest.mark.asyncio
async def test_get_team_chemistry_metadata_optimized_broken_streak():
    # Mock 5 games, but game 3 has different LT
    rows = []
    for i in range(1, 6):
        lt_id = 1 if i != 3 else 99 # Streak broken at game 3 (going backwards from 5..1)
        # Wait, the service sorts by game_id desc.
        # If games are 1, 2, 3, 4, 5. 5 is most recent.
        # If 5, 4 match, and 3 doesn't, consecutive is 2.

        # Let's say game 5 (most recent) matches.
        # Game 4 matches.
        # Game 3 mismatch.
        # Consecutive should be 2.
        pass

    # Re-creating rows correctly for "most recent first" logic check
    # The service queries DB, gets rows.
    # Then it groups by game_id.
    # Then it iterates sorted(game_ids, reverse=True).

    # Let's create games 1 to 5.
    rows = []
    # Game 5: Match
    rows.extend([(5, 5, "LT", 1), (5, 5, "LG", 2), (5, 5, "C", 3), (5, 5, "RG", 4), (5, 5, "RT", 5)])
    # Game 4: Match
    rows.extend([(4, 4, "LT", 1), (4, 4, "LG", 2), (4, 4, "C", 3), (4, 4, "RG", 4), (4, 4, "RT", 5)])
    # Game 3: Mismatch (LT is 99)
    rows.extend([(3, 3, "LT", 99), (3, 3, "LG", 2), (3, 3, "C", 3), (3, 3, "RG", 4), (3, 3, "RT", 5)])
    # Game 2: Match (shouldn't matter)
    rows.extend([(2, 2, "LT", 1), (2, 2, "LG", 2), (2, 2, "C", 3), (2, 2, "RG", 4), (2, 2, "RT", 5)])

    mock_result = MagicMock()
    mock_result.all.return_value = rows
    mock_result.scalars.return_value.all.return_value = rows

    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result

    service = EnhancedChemistryService(mock_db)
    starters = {"LT": 1, "LG": 2, "C": 3, "RG": 4, "RT": 5}

    metadata = await service.get_team_chemistry_metadata_optimized(1, starters)

    assert metadata.consecutive_games == 2
    assert metadata.chemistry_level == 0.0 # < 5 games
