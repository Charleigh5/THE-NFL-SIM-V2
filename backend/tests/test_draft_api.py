import pytest
from httpx import AsyncClient
from app.schemas.draft import DraftSuggestionRequest


@pytest.mark.asyncio
async def test_suggest_draft_pick_success(async_client: AsyncClient, async_db_session):
    """Test draft suggestion endpoint returns valid async recommendation."""
    from app.models.team import Team
    from app.models.player import Player

    # Create team
    team = Team(city="Test", name="Team", abbreviation="TST", conference="AFC", division="North")
    async_db_session.add(team)
    await async_db_session.flush()

    # Create available players
    players = [
        Player(
            first_name="John", last_name="Doe", position="QB",
            overall_rating=85, team_id=None, jersey_number=1
        ),
        Player(
            first_name="Jane", last_name="Smith", position="WR",
            overall_rating=80, team_id=None, jersey_number=2
        ),
    ]
    for p in players:
        async_db_session.add(p)
    await async_db_session.commit()

    player_ids = [p.id for p in players]

    # Make request
    response = await async_client.post(
        "/api/draft/suggest-pick",
        json={
            "team_id": team.id,
            "pick_number": 1,
            "available_players": player_ids
        }
    )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "recommended_player_id" in data
    assert "reasoning" in data
    assert "team_needs" in data
    assert "alternative_picks" in data
    assert "confidence_score" in data

    # Verify recommendation is valid
    assert data["recommended_player_id"] in player_ids
    assert isinstance(data["reasoning"], str)
    assert len(data["reasoning"]) > 0


@pytest.mark.asyncio
async def test_suggest_draft_pick_invalid_team(async_client: AsyncClient):
    """Test draft suggestion with invalid team ID returns 400 error."""
    response = await async_client.post(
        "/api/draft/suggest-pick",
        json={
            "team_id": 9999,
            "pick_number": 1,
            "available_players": [1, 2, 3]
        }
    )

    # Should fail due to team not found
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_suggest_draft_pick_no_players(async_client: AsyncClient, async_db_session):
    """Test draft suggestion with no available players returns error."""
    from app.models.team import Team

    team = Team(city="Test", name="Team", abbreviation="TST2", conference="NFC", division="South")
    async_db_session.add(team)
    await async_db_session.commit()

    response = await async_client.post(
        "/api/draft/suggest-pick",
        json={
            "team_id": team.id,
            "pick_number": 1,
            "available_players": []
        }
    )

    assert response.status_code == 400
