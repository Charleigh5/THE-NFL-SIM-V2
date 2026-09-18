import os
import pytest
from app.engine.spatial.blender_service import BlenderService
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

DEFAULT_BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"


def test_cli_render_with_invalid_blender_path():
    service = BlenderService(blender_path=r"C:\non_existent_blender\blender.exe")
    res = service.execute_headless_cli_render(
        play_id=901,
        drama_index=80.0,
        impact_force=85.0
    )
    assert res.status == "FALLBACK_THREEJS"
    assert res.video_url is None
    assert res.render_duration_ms >= 0.0


@pytest.mark.skipif(not os.path.exists(DEFAULT_BLENDER), reason="Blender 5.2.1 LTS binary not found on host")
def test_cli_render_real_blender_execution(tmp_path):
    output_file = tmp_path / "test_highlight_888.png"
    service = BlenderService(blender_path=DEFAULT_BLENDER)

    res = service.execute_headless_cli_render(
        play_id=888,
        drama_index=85.0,
        impact_force=90.0,
        output_path=str(output_file),
        samples=2
    )

    assert res.status == "RENDERED"
    assert output_file.exists()
    assert output_file.stat().st_size > 10000
    assert "test_highlight_888.png" in (res.video_url or "")


@pytest.mark.skipif(not os.path.exists(DEFAULT_BLENDER), reason="Blender 5.2.1 LTS binary not found on host")
def test_evaluate_cutscene_endpoint_cli_mode():
    payload = {
        "game_id": 12,
        "play_id": 555,
        "drama_index": 85.0,
        "impact_force": 90.0
    }
    response = client.post(
        "/api/spatial/game/12/play/555/evaluate-cutscene?render_mode=cli",
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["play_id"] == 555
    assert data["status"] in ("RENDERED", "FALLBACK_THREEJS")
    if data["status"] == "RENDERED":
        assert data["video_url"] is not None
