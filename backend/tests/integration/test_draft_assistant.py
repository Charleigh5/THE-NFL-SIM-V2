import pytest
from unittest.mock import AsyncMock, patch
from app.models.team import Team
from app.models.player import Player, Position
from app.core.mcp_registry import registry
from app.core.mcp_cache import mcp_cache

@pytest.fixture(autouse=True)
def clear_cache():
    mcp_cache.clear()
    yield

@pytest.fixture
async def setup_draft_data(async_db_session):
    # Create Team
    team = Team(id=1, name="Cardinals", city="Arizona", abbreviation="ARI", conference="NFC", division="West")
    async_db_session.add(team)

    # Create Players on Roster
    for i in range(3):
        async_db_session.add(Player(
            id=100+i, first_name=f"QB{i}", last_name="Test", position=Position.QB,
            overall_rating=75, team_id=1, age=25, height=75, weight=220, experience=2,
            jersey_number=10+i, is_rookie=False
        ))

    # Create Available Draft Players
    wr = Player(
        id=200, first_name="Marvin", last_name="Harrison Jr", position=Position.WR,
        overall_rating=85, team_id=None, age=21, height=76, weight=205, experience=0,
        jersey_number=18, is_rookie=True
    )
    qb = Player(
        id=201, first_name="Caleb", last_name="Williams", position=Position.QB,
        overall_rating=82, team_id=None, age=21, height=73, weight=215, experience=0,
        jersey_number=13, is_rookie=True
    )

    async_db_session.add(wr)
    async_db_session.add(qb)
    await async_db_session.commit()
    return team, wr, qb

@pytest.mark.asyncio
async def test_suggest_pick_endpoint(async_client, setup_draft_data):
    """Test the draft suggestion API endpoint."""
    team, wr, qb = setup_draft_data

    mock_client = AsyncMock()
    mock_client.call_tool.return_value = {"passing_yards": 2500}

    with patch.object(registry, 'get_client', return_value=mock_client):
        response = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 1,
                "pick_number": 4,
                "available_players": [200, 201]
            }
        )

        assert response.status_code == 200, f"Response: {response.json()}"
        data = response.json()

        assert data["recommended_player_id"] == 200
        assert "Draft Analysis" in data["reasoning"]
        assert "Team Fit:" in data["reasoning"]
        assert "Critical need" in data["reasoning"]

@pytest.mark.asyncio
async def test_suggest_pick_mcp_integration(async_client, setup_draft_data):
    """Test that MCP data is reflected in the reasoning."""
    team, wr, qb = setup_draft_data

    mock_client = AsyncMock()

    async def side_effect(tool_name, arguments):
        if tool_name == "get_player_career_stats":
            return None
        if tool_name == "get_league_averages":
            return {"receiving_yards": 800}
        return None

    mock_client.call_tool.side_effect = side_effect

    with patch.object(registry, 'get_client', return_value=mock_client):
        response = await async_client.post(
            "/api/draft/suggest-pick",
            json={
                "team_id": 1,
                "pick_number": 4,
                "available_players": [200]
            }
        )

        assert response.status_code == 200, f"Response: {response.json()}"
        data = response.json()

        assert "Historical Context:" in data["reasoning"]
        assert "League average for WR" in data["reasoning"]
