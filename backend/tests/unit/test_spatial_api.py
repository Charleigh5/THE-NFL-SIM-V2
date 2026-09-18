import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_evaluate_cutscene_endpoint_skipped():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/spatial/game/1/play/101/evaluate-cutscene",
            json={"game_id": 1, "play_id": 101, "drama_index": 30.0, "impact_force": 20.0}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "SKIPPED_BELOW_THRESHOLD"
        assert data["video_url"] is None


@pytest.mark.asyncio
async def test_evaluate_cutscene_endpoint_triggered_fallback():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/spatial/game/1/play/102/evaluate-cutscene",
            json={"game_id": 1, "play_id": 102, "drama_index": 88.0, "impact_force": 40.0}
        )
        assert resp.status_code == 200
        data = resp.json()
        # Without running socket server on 9876, gracefully falls back to Three.js
        assert data["status"] in ["RENDERED", "FALLBACK_THREEJS"]


@pytest.mark.asyncio
async def test_spatial_status_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/spatial/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["subsystem"] == "GRIDIRON-3D-SPATIAL"
        assert "blender_mcp_port_9876" in data
        assert data["tier1_status"] == "ONLINE"
