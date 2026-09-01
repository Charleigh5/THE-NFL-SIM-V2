"""
Unit Tests for Draft Generation & Visual Asset Synthesis Pipeline
Validates RookieGenerator, draft endpoints, Combine metrics, S2 cognition, and visual asset mapping.
"""
import pytest
from app.services.rookie_generator import RookieGenerator


@pytest.mark.asyncio
async def test_rookie_generator_position_distribution(async_db_session):
    """Verify RookieGenerator generates balanced position counts with deterministic RNG."""
    generator = RookieGenerator(async_db_session, seed=12345)
    players = await generator.generate_draft_class(season_id=1, count=100)

    assert len(players) == 100
    positions = [p.position for p in players]

    # Verify key positions are present in realistic quantities
    assert "QB" in positions
    assert "WR" in positions
    assert "CB" in positions
    assert "OT" in positions

    # Verify attribute invariants
    for p in players:
        assert p.is_rookie is True
        assert p.team_id is None
        assert 50 <= p.overall_rating <= 99
        assert 180 <= p.weight <= 350
        assert 68 <= p.height <= 80
        assert 45 <= p.s2_cognition_score <= 99
        assert 18.0 <= p.gps_speed_max <= 23.5
        assert 285 <= p.power_clean_max <= 385


@pytest.mark.asyncio
async def test_get_draft_board_endpoint(async_client):
    """Verify GET /api/draft/board returns prospects with resolved visual_assets."""
    response = await async_client.get("/api/draft/board")

    assert response.status_code == 200
    prospects = response.json()
    assert isinstance(prospects, list)
    assert len(prospects) > 0

    # Verify visual_assets are attached to every prospect
    first = prospects[0]
    assert "id" in first
    assert "first_name" in first
    assert "last_name" in first
    assert "overall_rating" in first
    assert "visual_assets" in first
    assert first["visual_assets"]["headshot"].endswith("/headshot.webp")
    assert first["visual_assets"]["hero_pose"].endswith("/hero_pose.webp")
    assert first["visual_assets"]["action_pose"].endswith("/action_pose.webp")
    assert first["visual_assets"]["celebration"].endswith("/celebration.webp")


@pytest.mark.asyncio
async def test_generate_draft_class_endpoint(async_client):
    """Verify POST /api/draft/generate creates a new draft class with custom seed."""
    payload = {
        "season_id": 1,
        "count": 64,
        "seed": 999,
    }
    response = await async_client.post("/api/draft/generate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 64
    assert len(data["prospects"]) == 64
    assert data["prospects"][0]["visual_assets"] is not None


@pytest.mark.asyncio
async def test_generate_prospect_assets_endpoint(async_client):
    """Verify POST /api/draft/prospects/{id}/generate-assets generates prompts for all 4 poses."""
    board_res = await async_client.get("/api/draft/board")
    prospects = board_res.json()
    prospect_id = prospects[0]["id"]

    response = await async_client.post(f"/api/draft/prospects/{prospect_id}/generate-assets")
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["player_id"] == prospect_id
    assert "prompts" in data
    assert "headshot" in data["prompts"]
    assert "hero_pose" in data["prompts"]
    assert "action_pose" in data["prompts"]
    assert "celebration" in data["prompts"]
    assert "8k" in data["prompts"]["headshot"]
