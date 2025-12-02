import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.draft_assistant import DraftAssistant
from app.models.player import Player, Position
from app.core.mcp_registry import registry

from app.core.mcp_cache import mcp_cache

@pytest.fixture(autouse=True)
def clear_cache():
    mcp_cache.clear()
    yield

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def draft_assistant(mock_db):
    return DraftAssistant(mock_db)

@pytest.fixture
def sample_players():
    return [
        Player(id=1, first_name="Caleb", last_name="Williams", position=Position.QB, overall_rating=95),
        Player(id=2, first_name="Marvin", last_name="Harrison Jr.", position=Position.WR, overall_rating=94),
        Player(id=3, first_name="Drake", last_name="Maye", position=Position.QB, overall_rating=92),
    ]

@pytest.mark.asyncio
async def test_suggest_pick_empty_list(draft_assistant):
    """Test suggest_pick with no available players."""
    suggestion = await draft_assistant.suggest_pick(team_id=1, available_players=[])
    assert suggestion["player_id"] is None
    assert "reasoning" in suggestion

@pytest.mark.asyncio
async def test_suggest_pick_single_player(draft_assistant, sample_players):
    """Test suggest_pick with only one player available."""
    single_player = [sample_players[0]]
    suggestion = await draft_assistant.suggest_pick(team_id=1, available_players=single_player)
    assert suggestion["player_id"] == 1
    assert "Best player available" in suggestion["reasoning"]

@pytest.mark.asyncio
async def test_suggest_pick_prioritizes_highest_rated(draft_assistant, sample_players):
    """Test that the highest rated player is suggested by default logic."""
    # Ensure list is sorted by overall descending for the service (usually done by caller, but service takes top 5)
    # The service currently takes top 5 from the list passed in.
    # So we pass them in order.
    suggestion = await draft_assistant.suggest_pick(team_id=1, available_players=sample_players)
    assert suggestion["player_id"] == 1 # Caleb Williams (95)

@pytest.mark.asyncio
async def test_suggest_pick_with_mcp_integration(draft_assistant, sample_players):
    """Test that MCP data is integrated into the suggestion."""

    # Mock the MCP client and its call_tool method
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {
        "average_overall": 85,
        "average_speed": 88
    }

    # Patch registry.get_client to return our mock
    with patch.object(registry, 'get_client', return_value=mock_client):
        suggestion = await draft_assistant.suggest_pick(team_id=1, available_players=sample_players)

        # Verify MCP was called
        mock_client.call_tool.assert_called_once()
        args = mock_client.call_tool.call_args[1]['arguments']
        assert args['position'] == Position.QB

        # Verify reasoning includes MCP data
        assert "projects to exceed league average" in suggestion["reasoning"]
        assert "external_data" in suggestion
        assert suggestion["external_data"]["average_overall"] == 85

@pytest.mark.asyncio
async def test_suggest_pick_mcp_failure_graceful_degradation(draft_assistant, sample_players):
    """Test that function works even if MCP fails."""

    mock_client = AsyncMock()
    mock_client.call_tool.side_effect = Exception("MCP Connection Failed")

    with patch.object(registry, 'get_client', return_value=mock_client):
        suggestion = await draft_assistant.suggest_pick(team_id=1, available_players=sample_players)

        # Should still return a valid suggestion based on internal logic
        assert suggestion["player_id"] == 1
        # Should NOT have external data
        assert "external_data" not in suggestion
        # Reasoning should be basic
        assert "Best player available" in suggestion["reasoning"]
