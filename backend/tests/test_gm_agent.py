import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.gm_agent import GMAgent
from app.models.player import Player, Position
from app.models.team import Team
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
def gm_agent(mock_db):
    # Mock team query
    mock_team = Team(id=1, name="Cardinals")
    mock_db.query.return_value.get.return_value = mock_team
    return GMAgent(mock_db, team_id=1)

@pytest.fixture
def sample_players():
    return {
        101: Player(id=101, first_name="Kyler", last_name="Murray", position=Position.QB, overall_rating=90),
        102: Player(id=102, first_name="Marvin", last_name="Harrison", position=Position.WR, overall_rating=85),
        201: Player(id=201, first_name="Patrick", last_name="Mahomes", position=Position.QB, overall_rating=99),
    }

@pytest.mark.asyncio
async def test_evaluate_trade_balanced(gm_agent, sample_players, mock_db):
    """Test a balanced trade evaluation (placeholder logic)."""
    # Mock player lookups
    def get_player(pid):
        return sample_players.get(pid)
    mock_db.query.return_value.get.side_effect = get_player

    # 1 player for 1 player (equal count logic in placeholder)
    result = await gm_agent.evaluate_trade(offered_players=[101], requested_players=[201])

    # 10 - 10 = 0 => ACCEPT
    assert result["decision"] == "ACCEPT"
    assert result["score"] == 0

@pytest.mark.asyncio
async def test_evaluate_trade_lopsided_reject(gm_agent, sample_players, mock_db):
    """Test a lopsided trade that should be rejected."""
    def get_player(pid):
        return sample_players.get(pid)
    mock_db.query.return_value.get.side_effect = get_player

    # Offer 1 player, request 2 players
    # 10 - 20 = -10 => REJECT
    result = await gm_agent.evaluate_trade(offered_players=[101], requested_players=[102, 201])

    assert result["decision"] == "REJECT"
    assert result["score"] < 0

@pytest.mark.asyncio
async def test_evaluate_trade_with_positive_news(gm_agent, sample_players, mock_db):
    """Test that positive news improves the trade score."""
    def get_player(pid):
        return sample_players.get(pid)
    mock_db.query.return_value.get.side_effect = get_player

    # Mock MCP client
    mock_client = AsyncMock()
    # Return positive news
    mock_client.call_tool.return_value = [{"headline": "Kyler Murray looks sharp in practice"}]

    with patch.object(registry, 'get_client', return_value=mock_client):
        # 1 for 1 trade (base score 0)
        result = await gm_agent.evaluate_trade(offered_players=[101], requested_players=[201])

        # Base 0 + 5 (positive news) = 5
        assert result["score"] == 5
        assert "Positive buzz" in result["reasoning"]

@pytest.mark.asyncio
async def test_evaluate_trade_with_injury_news(gm_agent, sample_players, mock_db):
    """Test that injury news hurts the trade score."""
    def get_player(pid):
        return sample_players.get(pid)
    mock_db.query.return_value.get.side_effect = get_player

    mock_client = AsyncMock()
    # Return injury news
    mock_client.call_tool.return_value = [{"headline": "Kyler Murray dealing with minor injury"}]

    with patch.object(registry, 'get_client', return_value=mock_client):
        # 1 for 1 trade (base score 0)
        result = await gm_agent.evaluate_trade(offered_players=[101], requested_players=[201])

        # Base 0 - 20 (injury) = -20
        assert result["score"] == -20
        assert result["decision"] == "REJECT"
        assert "Concern about injury" in result["reasoning"]

@pytest.mark.asyncio
async def test_evaluate_trade_mcp_failure(gm_agent, sample_players, mock_db):
    """Test graceful degradation when MCP fails."""
    def get_player(pid):
        return sample_players.get(pid)
    mock_db.query.return_value.get.side_effect = get_player

    mock_client = AsyncMock()
    mock_client.call_tool.side_effect = Exception("News Service Down")

    with patch.object(registry, 'get_client', return_value=mock_client):
        result = await gm_agent.evaluate_trade(offered_players=[101], requested_players=[201])

        # Should fallback to base logic (score 0)
        assert result["score"] == 0
        assert result["decision"] == "ACCEPT"
        # No news reasoning
        assert "injury" not in result["reasoning"]
