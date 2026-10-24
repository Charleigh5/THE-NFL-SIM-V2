from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from hashlib import sha256
import os
from pathlib import Path
import re
import threading
import time
import uuid

from app.core.config import settings
from app.schemas.narrator import NarrationResponse

_HEX64_RE = re.compile(r"^[a-f0-9]{64}$")


def validate_cache_key(key: str) -> str:
    """Validate that key is a strict 64-character lowercase hex SHA-256 digest."""
    if not isinstance(key, str) or not _HEX64_RE.fullmatch(key):
        raise ValueError(f"Invalid narrator cache key: {key!r}")
    return key


NarratorResponseCacheKey = tuple[str, int, int | None, int | None, str, int, int]
# (page, team_id, player_id, game_id, style, season_year, current_week)


class NarratorResponseCache:
    """Thread-safe L1 in-memory cache for NarrationResponse objects with monotonic TTL."""

    def __init__(self, ttl: float = 60.0):
        self.ttl = ttl
        self._lock = threading.Lock()
        self._cache: dict[NarratorResponseCacheKey, tuple[NarrationResponse, float]] = {}

    def get(self, key: NarratorResponseCacheKey) -> NarrationResponse | None:
        now = time.monotonic()
        with self._lock:
            if key in self._cache:
                resp, expire_at = self._cache[key]
                if now < expire_at:
                    return resp
                del self._cache[key]
        return None

    def set(self, key: NarratorResponseCacheKey, response: NarrationResponse) -> None:
        now = time.monotonic()
        with self._lock:
            self._cache[key] = (response, now + self.ttl)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


_narration_response_cache = NarratorResponseCache(ttl=60.0)


def clear_narrator_response_cache() -> None:
    """Flush the narrator response cache upon season/week simulation or trade acceptance."""
    _narration_response_cache.clear()


class NarratorCacheService:
    """
    Single-flight content-addressed MP3 disk cache with 0600 permissions and mtime LRU eviction.
    """

    def __init__(
        self,
        cache_dir: str | None = None,
        max_files: int | None = None,
    ):
        self.cache_dir = Path(
            cache_dir if cache_dir is not None else settings.NARRATOR_CACHE_DIR
        )
        self.max_files = (
            max_files if max_files is not None else settings.NARRATOR_CACHE_MAX_FILES
        )
        self._locks: dict[str, asyncio.Lock] = {}
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def compute_cache_key(model: str, voice: str, seed: int, script: str) -> str:
        return sha256(f"{model}:{voice}:{seed}:{script}".encode("utf-8")).hexdigest()

    def _get_lock(self, key: str) -> asyncio.Lock:
        lock = self._locks.get(key)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[key] = lock
        return lock

    def _path_for_key(self, key: str) -> Path:
        validated = validate_cache_key(key)
        return self.cache_dir / f"{validated}.mp3"

    def get_cached_path(self, key: str) -> Path | None:
        """Return Path if cached MP3 exists (and touch mtime for LRU), else None."""
        target = self._path_for_key(key)
        if target.is_file():
            try:
                os.utime(target, None)
            except OSError:
                pass
            return target
        return None

    async def get_or_synthesize(
        self,
        key: str,
        script: str,
        synthesizer: Callable[[str], Awaitable[bytes | None]],
    ) -> Path | None:
        """
        Return cached MP3 Path if present; otherwise serialize concurrent callers via per-key
        asyncio.Lock, invoke synthesizer once, write atomically with 0o600 permissions, and evict LRU.
        """
        validated = validate_cache_key(key)
        existing = self.get_cached_path(validated)
        if existing is not None:
            return existing

        lock = self._get_lock(validated)
        async with lock:
            existing_inside = self.get_cached_path(validated)
            if existing_inside is not None:
                return existing_inside

            try:
                audio_bytes = await synthesizer(script)
                if not audio_bytes:
                    return None

                return self._write_atomic(validated, audio_bytes)
            finally:
                if not (self.cache_dir / f"{validated}.mp3").exists():
                    self._locks.pop(validated, None)

    def _write_atomic(self, validated_key: str, data: bytes) -> Path:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        target = self.cache_dir / f"{validated_key}.mp3"
        tmp_path = self.cache_dir / f".{validated_key}.{uuid.uuid4().hex}.tmp"

        fd = os.open(str(tmp_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(data)
            try:
                os.chmod(tmp_path, 0o600)
            except OSError:
                pass
            os.replace(tmp_path, target)
            try:
                os.chmod(target, 0o600)
            except OSError:
                pass
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass

        self._evict_if_needed()
        return target

    def _evict_if_needed(self) -> None:
        if self.max_files <= 0:
            return
        mp3_files = list(self.cache_dir.glob("*.mp3"))
        if len(mp3_files) <= self.max_files:
            return

        def _mtime(p: Path) -> float:
            try:
                return p.stat().st_mtime
            except OSError:
                return 0.0

        sorted_files = sorted(mp3_files, key=_mtime)
        excess = len(sorted_files) - self.max_files
        for old_file in sorted_files[:excess]:
            try:
                old_file.unlink()
                self._locks.pop(old_file.stem, None)
            except OSError:
                pass
