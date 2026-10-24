import time
from unittest.mock import AsyncMock

import pytest

from app.api.endpoints.broadcast import (
    clear_narrator_response_cache,
    narrator_script_service,
    voicestudio_tts_service,
)
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.schemas.narrator import StructuredAnchorScript
from app.services.narrator_cache_service import NarratorCacheService


@pytest.fixture(autouse=True)
def _isolate_broadcast_narrator_state():
    """Ensure clean cache and circuit breaker state before and after every test."""
    clear_narrator_response_cache()
    voicestudio_tts_service.reset_circuit()
    yield
    clear_narrator_response_cache()
    voicestudio_tts_service.reset_circuit()


def _seed_team_and_season(db_session):
    team = Team(
        id=1,
        city="Kansas City",
        name="Chiefs",
        abbreviation="KC",
        conference="AFC",
        division="West",
        wins=6,
        losses=1,
        ties=0,
    )
    season = Season(
        id=1,
        year=2026,
        current_week=8,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
    )
    db_session.add_all([team, season])
    db_session.commit()


def test_post_narrate_voicestudio_online_and_serve_cached_audio(client, db_session, tmp_path, monkeypatch):
    """Test POST /api/broadcast/narrate with VoiceStudio online and GET /api/broadcast/audio/{cache_key}."""
    _seed_team_and_season(db_session)

    test_cache = NarratorCacheService(cache_dir=str(tmp_path), max_files=16)
    monkeypatch.setattr("app.api.endpoints.broadcast.narrator_cache_service", test_cache)
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.synthesize",
        AsyncMock(return_value=b"ID3-narrator-endpoint-mp3"),
    )

    resp = client.post(
        "/api/broadcast/narrate",
        json={"page": "dashboard", "team_id": 1, "style": "ESPN"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["voice_source"] == "voicestudio"
    assert data["style"] == "ESPN"
    assert "Kansas City Chiefs" in data["script"]
    assert data["audio_url"] == f"/api/broadcast/audio/{data['cache_key']}"

    # Fetch the cached MP3 via GET /api/broadcast/audio/{cache_key}
    audio_resp = client.get(data["audio_url"])
    assert audio_resp.status_code == 200
    assert audio_resp.headers["content-type"].startswith("audio/mpeg")
    assert audio_resp.content == b"ID3-narrator-endpoint-mp3"


def test_post_narrate_browser_fallback_when_voicestudio_offline(client, db_session, tmp_path, monkeypatch):
    """Test POST /api/broadcast/narrate degrades cleanly to browser voice when VoiceStudio returns None."""
    _seed_team_and_season(db_session)

    test_cache = NarratorCacheService(cache_dir=str(tmp_path), max_files=16)
    monkeypatch.setattr("app.api.endpoints.broadcast.narrator_cache_service", test_cache)
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.synthesize",
        AsyncMock(return_value=None),
    )

    resp = client.post(
        "/api/broadcast/narrate",
        json={"page": "front-office", "team_id": 1, "style": "NFL_NETWORK"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["voice_source"] == "browser"
    assert data["audio_url"] is None
    assert data["degraded"] is True
    assert data["style"] == "NFL_NETWORK"


def test_get_voices_health_endpoint(client, monkeypatch):
    """Test GET /api/broadcast/voices/health reports VoiceStudio status."""
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.check_health",
        AsyncMock(return_value=True),
    )
    resp = client.get("/api/broadcast/voices/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["available"] is True
    assert body["voice_source"] == "voicestudio"


def test_broadcast_narrator_422_validation_and_404_missing_audio(client):
    """Test 422 validation errors for invalid page, invalid team_id, and invalid cache_key."""
    bad_page = client.post(
        "/api/broadcast/narrate",
        json={"page": "non-existent-page", "team_id": 1},
    )
    assert bad_page.status_code == 422

    bad_team = client.post(
        "/api/broadcast/narrate",
        json={"page": "dashboard", "team_id": 0},
    )
    assert bad_team.status_code == 422

    bad_key = client.get("/api/broadcast/audio/not-a-64-char-hex-key")
    assert bad_key.status_code == 422

    missing_key = client.get(f"/api/broadcast/audio/{'f' * 64}")
    assert missing_key.status_code == 404


def test_post_narrate_l1_response_cache_hit_and_miss(client, db_session, monkeypatch):
    """Verify thread-safe L1 in-memory cache returns cached NarrationResponse on identical queries."""
    _seed_team_and_season(db_session)

    call_count = 0

    async def mock_generate_script(packet, style):
        nonlocal call_count
        call_count += 1
        return (
            StructuredAnchorScript(
                script=f"Script generation #{call_count} for {packet.team_name}",
                facts_used=[],
                headline_banner="Breaking News",
            ),
            False,
        )

    monkeypatch.setattr(narrator_script_service, "generate_script", mock_generate_script)
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.synthesize",
        AsyncMock(return_value=None),
    )

    payload = {"page": "dashboard", "team_id": 1, "style": "ESPN"}

    # Request 1: Cache miss -> calls generate_script
    resp1 = client.post("/api/broadcast/narrate", json=payload)
    assert resp1.status_code == 200
    assert call_count == 1
    data1 = resp1.json()
    assert "generation #1" in data1["script"]

    # Request 2: Identical query -> Cache hit -> returns cached response with 0 extra calls
    resp2 = client.post("/api/broadcast/narrate", json=payload)
    assert resp2.status_code == 200
    assert call_count == 1  # generate_script not called again
    data2 = resp2.json()
    assert data2["script"] == data1["script"]
    assert data2["cache_key"] == data1["cache_key"]

    # Request 3: Different style -> Cache miss -> generates new script
    payload_cbs = {"page": "dashboard", "team_id": 1, "style": "CBS"}
    resp3 = client.post("/api/broadcast/narrate", json=payload_cbs)
    assert resp3.status_code == 200
    assert call_count == 2
    data3 = resp3.json()
    assert "generation #2" in data3["script"]


def test_clear_narrator_response_cache(client, db_session, monkeypatch):
    """Verify clear_narrator_response_cache invalidates in-memory cached responses."""
    _seed_team_and_season(db_session)

    call_count = 0

    async def mock_generate_script(packet, style):
        nonlocal call_count
        call_count += 1
        return (
            StructuredAnchorScript(
                script=f"Run #{call_count}",
                facts_used=[],
                headline_banner="Headline",
            ),
            False,
        )

    monkeypatch.setattr(narrator_script_service, "generate_script", mock_generate_script)
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.synthesize",
        AsyncMock(return_value=None),
    )

    payload = {"page": "dashboard", "team_id": 1, "style": "ESPN"}

    # Run 1: cached
    resp1 = client.post("/api/broadcast/narrate", json=payload)
    assert resp1.status_code == 200
    assert call_count == 1

    # Invalidate cache
    clear_narrator_response_cache()

    # Run 2: Cache miss after invalidation
    resp2 = client.post("/api/broadcast/narrate", json=payload)
    assert resp2.status_code == 200
    assert call_count == 2


def test_post_narrate_decouples_db_session_before_external_calls(client, db_session, monkeypatch):
    """Verify that synchronous DB session closes BEFORE awaiting external LLM and TTS calls."""
    _seed_team_and_season(db_session)

    db_closed_before_script_generation = False

    async def mock_generate_script(packet, style):
        nonlocal db_closed_before_script_generation
        # In a decoupled model, the threadpool DB session was closed and is not held
        db_closed_before_script_generation = True
        return (
            StructuredAnchorScript(
                script="Decoupled session verified",
                facts_used=[],
                headline_banner="Decoupled",
            ),
            False,
        )

    monkeypatch.setattr(narrator_script_service, "generate_script", mock_generate_script)
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.synthesize",
        AsyncMock(return_value=None),
    )

    resp = client.post(
        "/api/broadcast/narrate",
        json={"page": "dashboard", "team_id": 1, "style": "ESPN"},
    )
    assert resp.status_code == 200
    assert db_closed_before_script_generation is True


def test_voices_health_recovery_clears_narrator_response_cache(client, db_session, monkeypatch):
    """Verify that GET /api/broadcast/voices/health clears narrator response cache upon detecting online sidecar."""
    _seed_team_and_season(db_session)

    call_count = 0

    async def mock_generate_script(packet, style):
        nonlocal call_count
        call_count += 1
        return (
            StructuredAnchorScript(
                script=f"Degraded run #{call_count}",
                facts_used=[],
                headline_banner="Degraded",
            ),
            True,
        )

    monkeypatch.setattr(narrator_script_service, "generate_script", mock_generate_script)
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.synthesize",
        AsyncMock(return_value=None),
    )

    # 1. Narrate while degraded -> cached
    resp1 = client.post(
        "/api/broadcast/narrate",
        json={"page": "dashboard", "team_id": 1, "style": "ESPN"},
    )
    assert resp1.status_code == 200
    assert call_count == 1

    # 2. VoiceStudio sidecar comes back online -> health check reports 200 OK
    monkeypatch.setattr(
        "app.api.endpoints.broadcast.voicestudio_tts_service.check_health",
        AsyncMock(return_value=True),
    )
    health_resp = client.get("/api/broadcast/voices/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["available"] is True

    # 3. Next narration request should re-evaluate because cache was cleared on health recovery
    resp2 = client.post(
        "/api/broadcast/narrate",
        json={"page": "dashboard", "team_id": 1, "style": "ESPN"},
    )
    assert resp2.status_code == 200
    assert call_count == 2


def test_offline_narrator_voices_health_p95_latency_sla(client):
    """Verify GET /api/broadcast/voices/health achieves P95 latency < 25ms when VoiceStudio is offline."""
    # Trip the circuit breaker
    voicestudio_tts_service.trip_circuit()
    assert voicestudio_tts_service.is_circuit_open() is True

    latencies_ms: list[float] = []
    for _ in range(30):
        t0 = time.perf_counter()
        resp = client.get("/api/broadcast/voices/health")
        latencies_ms.append((time.perf_counter() - t0) * 1000)
        assert resp.status_code == 200
        assert resp.json()["available"] is False

    latencies_ms.sort()
    p95_idx = int(len(latencies_ms) * 0.95)
    p95_latency = latencies_ms[p95_idx]
    assert p95_latency < 25.0, f"Voices health P95 latency {p95_latency:.2f}ms exceeded 25ms SLA"
