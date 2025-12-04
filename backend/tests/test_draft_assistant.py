import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.draft_assistant import DraftAssistant
from app.models.player import Player, Position
from app.core.mcp_registry import registry
from app.core.mcp_cache import mcp_cache
from app.schemas.draft import DraftSuggestionResponse

@pytest.fixture(autouse=True)
def clear_cache():
    mcp_cache.clear()
    yield

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def draft_assistant():
    return DraftAssistant()

@pytest.fixture
def sample_players():
    return [
        Player(id=1, first_name="Caleb", last_name="Williams", position="QB", overall_rating=95, speed=85, strength=70, agility=80),
        Player(id=2, first_name="Marvin", last_name="Harrison Jr.", position="WR", overall_rating=94, speed=92, strength=65, agility=90),
        Player(id=3, first_name="Drake", last_name="Maye", position="QB", overall_rating=92, speed=82, strength=75, agility=78),
    ]

@pytest.mark.asyncio
async def test_suggest_pick_no_players(draft_assistant, mock_db):
    """Test suggest_pick with no available players raises ValueError."""

    async def execute_side_effect(stmt):
        str_stmt = str(stmt)
        mock_result = MagicMock()

        if "FROM team" in str_stmt:
            mock_result.scalar_one_or_none.return_value = MagicMock(id=1)
        elif "FROM player" in str_stmt and "WHERE player.id IN" in str_stmt:
            mock_result.all.return_value = []

        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    with pytest.raises(ValueError, match="No available players"):
        await draft_assistant.suggest_pick(
            team_id=1,
            pick_number=1,
            available_players=[1, 2, 3],
            db=mock_db
        )

@pytest.mark.asyncio
async def test_suggest_pick_success(draft_assistant, mock_db, sample_players):
    """Test successful draft suggestion."""
    # Mock team query
    mock_db.execute.return_value.scalar_one_or_none.return_value = MagicMock(id=1)

    # Mock player query
    # The service selects specific columns, so we need to mock the rows returned
    # Row order: id, first_name, last_name, position, overall_rating, speed, strength, agility
    mock_rows = [
        (p.id, p.first_name, p.last_name, p.position, p.overall_rating, p.speed, p.strength, p.agility)
        for p in sample_players
    ]

    # We need to handle multiple execute calls.
    # 1. Team query
    # 2. Player query
    # 3. Roster query

    # Create a side effect for execute
    async def execute_side_effect(stmt):
        str_stmt = str(stmt)
        mock_result = MagicMock()

        if "FROM team" in str_stmt:
            mock_result.scalar_one_or_none.return_value = MagicMock(id=1)
        elif "FROM player" in str_stmt and "WHERE player.id IN" in str_stmt:
            mock_result.all.return_value = mock_rows
        elif "FROM player" in str_stmt and "GROUP BY player.position" in str_stmt:
            # Mock roster stats: empty roster
            mock_result.all.return_value = []

        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    suggestion = await draft_assistant.suggest_pick(
        team_id=1,
        pick_number=1,
        available_players=[1, 2, 3],
        db=mock_db,
        include_historical_data=False
    )

    assert isinstance(suggestion, DraftSuggestionResponse)
    assert suggestion.recommended_player_id == 1
    assert suggestion.player_name == "Caleb Williams"
    assert suggestion.confidence_score > 0

@pytest.mark.asyncio
async def test_suggest_pick_with_mcp(draft_assistant, mock_db, sample_players):
    """Test suggestion with MCP integration."""
    # Setup DB mocks similar to above
    mock_rows = [
        (p.id, p.first_name, p.last_name, p.position, p.overall_rating, p.speed, p.strength, p.agility)
        for p in sample_players
    ]

    async def execute_side_effect(stmt):
        str_stmt = str(stmt)
        mock_result = MagicMock()
        if "FROM team" in str_stmt:
            mock_result.scalar_one_or_none.return_value = MagicMock(id=1)
        elif "FROM player" in str_stmt and "WHERE player.id IN" in str_stmt:
            mock_result.all.return_value = mock_rows
        elif "FROM player" in str_stmt and "GROUP BY player.position" in str_stmt:
            mock_result.all.return_value = []
        return mock_result

    mock_db.execute.side_effect = execute_side_effect

    # Mock MCP client
    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {
        "name": "Patrick Mahomes",
        "years_active": "2017-Present",
        "highlights": "MVP, Super Bowl Champ"
    }

    with patch.object(registry, 'get_client', return_value=mock_client):
        suggestion = await draft_assistant.suggest_pick(
            team_id=1,
            pick_number=1,
            available_players=[1, 2, 3],
            db=mock_db,
            include_historical_data=True
        )

        assert suggestion.mcp_data_used is True
        assert suggestion.historical_comparison is not None
        assert suggestion.historical_comparison.comparable_player_name == "Patrick Mahomes"
