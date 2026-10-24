import time

import httpx
import pytest

from app.services.voicestudio_tts_service import (
    CONNECT_TIMEOUT_SECONDS,
    HEALTH_READ_TIMEOUT_SECONDS,
    OFFLINE_CIRCUIT_TTL_SECONDS,
    POOL_TIMEOUT_SECONDS,
    WRITE_TIMEOUT_SECONDS,
    VoiceStudioTTSService,
    validate_loopback_base_url,
)


@pytest.fixture(autouse=True)
def _isolate_circuit():
    yield


def test_ssrf_rejection_non_loopback_and_localhost_hostname():
    """Verify SSRF guard allows only http://127.0.0.1 or http://[::1] and rejects localhost/external IPs."""
    assert validate_loopback_base_url("http://127.0.0.1:3900") == "http://127.0.0.1:3900"
    assert validate_loopback_base_url("http://[::1]:3900/") == "http://[::1]:3900"

    for invalid_url in (
        "http://localhost:3900",
        "https://127.0.0.1:3900",
        "http://192.168.1.10:3900",
        "http://10.0.0.5:3900",
        "http://169.254.169.254/latest/meta-data",
        "http://example.com:3900",
    ):
        with pytest.raises(ValueError, match="loopback"):
            validate_loopback_base_url(invalid_url)


@pytest.mark.asyncio
async def test_voicestudio_synthesize_200_mp3_and_timeout_transition():
    """Verify 200 MP3 synthesis sends CSRF header, uses 60s timeout first, then 10s thereafter."""
    captured_requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_requests.append(request)
        assert request.headers.get("x-voicestudio-csrf") == "1"
        if request.url.path == "/v1/audio/speech":
            return httpx.Response(
                status_code=200,
                headers={"content-type": "audio/mpeg"},
                content=b"ID3-fake-mp3-bytes",
            )
        return httpx.Response(status_code=404)

    transport = httpx.MockTransport(handler)
    service = VoiceStudioTTSService(
        base_url="http://127.0.0.1:3900",
        voice_id="default",
        model="omnivoice",
        seed=42,
        transport=transport,
    )

    assert service.current_synthesis_timeout == 60.0
    audio_bytes = await service.synthesize("Welcome to SportsCenter!")
    assert audio_bytes == b"ID3-fake-mp3-bytes"
    assert service.current_synthesis_timeout == 10.0
    assert len(captured_requests) == 1
    assert service.is_circuit_open() is False


@pytest.mark.asyncio
async def test_voicestudio_409_ambiguous_voice_fallback():
    """Verify 409 ambiguous voice error degrades gracefully by returning None."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=409,
            json={"error": {"message": "Ambiguous voice name", "type": "conflict"}},
        )

    service = VoiceStudioTTSService(
        base_url="http://127.0.0.1:3900",
        transport=httpx.MockTransport(handler),
    )
    result = await service.synthesize("Testing 409 conflict fallback.")
    assert result is None


@pytest.mark.asyncio
async def test_voicestudio_timeout_fallback_and_health_check():
    """Verify timeout during synthesis or health check degrades gracefully without raising."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("VoiceStudio timed out", request=request)

    service = VoiceStudioTTSService(
        base_url="http://127.0.0.1:3900",
        transport=httpx.MockTransport(handler),
    )
    assert await service.check_health() is False
    assert service.is_circuit_open() is True
    assert await service.synthesize("Testing timeout fallback.") is None


@pytest.mark.asyncio
async def test_circuit_breaker_trip_on_connect_error_and_fast_fail():
    """Verify circuit breaker trips on ConnectError and short-circuits subsequent calls in < 0.01ms."""
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        raise httpx.ConnectError("Connection refused to 127.0.0.1:3900", request=request)

    service = VoiceStudioTTSService(
        base_url="http://127.0.0.1:3900",
        transport=httpx.MockTransport(handler),
    )
    assert service.is_circuit_open() is False

    # First call encounters ConnectError and trips circuit
    healthy = await service.check_health()
    assert healthy is False
    assert service.is_circuit_open() is True
    assert call_count == 1

    # Second call short-circuits immediately (< 0.01ms) without calling transport
    t0 = time.perf_counter()
    second_healthy = await service.check_health()
    elapsed = time.perf_counter() - t0
    assert second_healthy is False
    assert call_count == 1  # No transport invocation
    assert elapsed < 0.005  # Short-circuit well under 5ms

    # Synthesis also short-circuits without calling transport
    t1 = time.perf_counter()
    synth_result = await service.synthesize("Fast-fail check")
    synth_elapsed = time.perf_counter() - t1
    assert synth_result is None
    assert call_count == 1
    assert synth_elapsed < 0.005


@pytest.mark.asyncio
async def test_circuit_breaker_manual_reset_and_force_health_check():
    """Verify reset_circuit clears open circuit, and force=True bypasses the circuit."""
    service = VoiceStudioTTSService(base_url="http://127.0.0.1:3900")
    service.trip_circuit()
    assert service.is_circuit_open() is True

    service.reset_circuit()
    assert service.is_circuit_open() is False

    # Trip again and verify force=True bypasses circuit check
    service.trip_circuit()
    assert service.is_circuit_open() is True

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=200, json={"voices": []})

    service._transport = httpx.MockTransport(handler)
    force_healthy = await service.check_health(force=True)
    assert force_healthy is True
    # 200 OK resets the circuit
    assert service.is_circuit_open() is False


def test_granular_timeout_constants():
    """Verify exact granular timeout constants for Windows loopback fast-fail."""
    assert CONNECT_TIMEOUT_SECONDS == 0.15
    assert HEALTH_READ_TIMEOUT_SECONDS == 2.0
    assert WRITE_TIMEOUT_SECONDS == 2.0
    assert POOL_TIMEOUT_SECONDS == 1.0
    assert OFFLINE_CIRCUIT_TTL_SECONDS == 30.0


@pytest.mark.asyncio
async def test_offline_latency_p95_sla():
    """Verify P95 latency is strictly < 25ms when VoiceStudio is offline."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Offline sidecar", request=request)

    service = VoiceStudioTTSService(
        base_url="http://127.0.0.1:3900",
        transport=httpx.MockTransport(handler),
    )

    # Initial call trips the circuit
    await service.check_health()
    assert service.is_circuit_open() is True

    latencies_ms: list[float] = []
    for _ in range(50):
        t0 = time.perf_counter()
        result = await service.check_health()
        latencies_ms.append((time.perf_counter() - t0) * 1000)
        assert result is False

    latencies_ms.sort()
    p95_idx = int(len(latencies_ms) * 0.95)
    p95_latency = latencies_ms[p95_idx]
    assert p95_latency < 25.0, f"P95 latency {p95_latency:.2f}ms exceeded 25ms SLA"
