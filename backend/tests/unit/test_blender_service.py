from app.engine.spatial.blender_service import BlenderService


def test_blender_probe_returns_offline_when_unreachable():
    # Probe non-listening port to verify fallback
    service = BlenderService(host="127.0.0.1", port=19876)
    status = service.probe_socket()
    assert status is False


def test_render_request_falls_back_when_offline():
    service = BlenderService(host="127.0.0.1", port=19876)
    res = service.request_cutscene_render(play_id=999, drama_index=80.0, impact_force=20.0)
    assert res.status == "FALLBACK_THREEJS"
    assert res.video_url is None
    assert res.render_duration_ms >= 0.0
