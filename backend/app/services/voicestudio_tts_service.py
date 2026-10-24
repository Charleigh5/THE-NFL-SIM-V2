from __future__ import annotations

import ipaddress
import logging
import time
from urllib.parse import urlparse

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

CONNECT_TIMEOUT_SECONDS: float = 0.15
HEALTH_READ_TIMEOUT_SECONDS: float = 2.0
WRITE_TIMEOUT_SECONDS: float = 2.0
POOL_TIMEOUT_SECONDS: float = 1.0
OFFLINE_CIRCUIT_TTL_SECONDS: float = 30.0


def validate_loopback_base_url(base_url: str) -> str:
    """
    Ensure VoiceStudio base URL uses http scheme and a literal loopback IP address
    (127.0.0.1 or ::1). Rejects hostnames (including 'localhost') and non-loopback IPs.
    """
    parsed = urlparse(base_url.strip())
    if parsed.scheme != "http":
        raise ValueError(
            f"VoiceStudio base URL must use http:// loopback scheme, got: {base_url!r}"
        )

    host = parsed.hostname
    if not host:
        raise ValueError(f"VoiceStudio base URL missing literal loopback IP host: {base_url!r}")

    try:
        ip = ipaddress.ip_address(host)
    except ValueError as exc:
        raise ValueError(
            f"VoiceStudio base URL host must be a literal loopback IP (127.0.0.1 or ::1), got: {host!r}"
        ) from exc

    if not ip.is_loopback:
        raise ValueError(f"VoiceStudio base URL IP must be loopback, got: {host!r}")

    return base_url.rstrip("/")


class VoiceStudioTTSService:
    """
    Optional external HTTP loopback client for debpalash/VoiceStudio (/v1/audio/speech).
    Strictly honors process & license boundary and degrades gracefully to None on errors.
    """

    def __init__(
        self,
        base_url: str | None = None,
        voice_id: str | None = None,
        model: str | None = None,
        seed: int | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        raw_url = base_url if base_url is not None else settings.VOICESTUDIO_BASE_URL
        self.base_url = validate_loopback_base_url(raw_url)
        self.voice_id = voice_id if voice_id is not None else settings.VOICESTUDIO_VOICE_ID
        self.model = model if model is not None else settings.VOICESTUDIO_MODEL
        self.seed = seed if seed is not None else settings.VOICESTUDIO_SEED
        self._transport = transport
        self._has_succeeded_once = False
        self._offline_until: float = 0.0

    @property
    def current_synthesis_timeout(self) -> float:
        """60.0s before first synthesis (lazy model download), 10.0s thereafter."""
        return 10.0 if self._has_succeeded_once else 60.0

    def is_circuit_open(self) -> bool:
        """Return True if circuit is open (negative availability cache active)."""
        return time.monotonic() < self._offline_until

    def reset_circuit(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        self._offline_until = 0.0

    def trip_circuit(self) -> None:
        """Trip circuit breaker for OFFLINE_CIRCUIT_TTL_SECONDS (30s)."""
        self._offline_until = time.monotonic() + OFFLINE_CIRCUIT_TTL_SECONDS

    def _build_client(self, timeout: httpx.Timeout | float) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            headers={"x-voicestudio-csrf": "1"},
            timeout=timeout,
            trust_env=False,
            follow_redirects=False,
            transport=self._transport,
        )

    async def check_health(self, force: bool = False) -> bool:
        """
        Check VoiceStudio readiness via GET /v1/audio/voices with granular loopback timeouts.
        Short-circuits immediately in <0.01ms when circuit is open unless force=True.
        """
        if not force and self.is_circuit_open():
            logger.debug("VoiceStudio circuit is open, fast-failing health check.")
            return False

        timeout = httpx.Timeout(
            connect=CONNECT_TIMEOUT_SECONDS,
            read=HEALTH_READ_TIMEOUT_SECONDS,
            write=WRITE_TIMEOUT_SECONDS,
            pool=POOL_TIMEOUT_SECONDS,
        )
        try:
            async with self._build_client(timeout=timeout) as client:
                response = await client.get("/v1/audio/voices")
                if response.status_code == 200:
                    self.reset_circuit()
                    return True
                return False
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            logger.debug("VoiceStudio health check failed (%s), tripping 30s circuit breaker", exc)
            self.trip_circuit()
            return False
        except Exception as exc:
            logger.debug("VoiceStudio health check error: %s", exc)
            return False

    async def synthesize(self, script: str) -> bytes | None:
        """
        Synthesize speech via POST /v1/audio/speech with granular timeouts & circuit breaker.
        Returns raw MP3 bytes on HTTP 200, or None on any failure (400, 409, 500, timeout).
        """
        text_input = (script or "").strip()[:4096]
        if not text_input:
            return None

        if self.is_circuit_open():
            logger.debug("VoiceStudio circuit is open, fast-failing synthesis.")
            return None

        payload = {
            "model": self.model,
            "input": text_input,
            "voice": self.voice_id,
            "response_format": "mp3",
            "seed": self.seed,
        }

        timeout = httpx.Timeout(
            connect=CONNECT_TIMEOUT_SECONDS,
            read=self.current_synthesis_timeout,
            write=WRITE_TIMEOUT_SECONDS,
            pool=POOL_TIMEOUT_SECONDS,
        )

        try:
            async with self._build_client(timeout=timeout) as client:
                response = await client.post("/v1/audio/speech", json=payload)
                if response.status_code == 200 and response.content:
                    self._has_succeeded_once = True
                    self.reset_circuit()
                    return response.content
                logger.warning(
                    "VoiceStudio TTS returned status %s, degrading to browser speech.",
                    response.status_code,
                )
                return None
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            logger.info("VoiceStudio TTS connect/timeout failure (%s), tripping 30s circuit breaker.", exc)
            self.trip_circuit()
            return None
        except Exception as exc:
            logger.info("VoiceStudio TTS unavailable (%s), degrading to browser speech.", exc)
            return None
