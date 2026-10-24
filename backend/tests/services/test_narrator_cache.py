import asyncio
import os
import time

import pytest

from app.services.narrator_cache_service import NarratorCacheService, validate_cache_key


def test_validate_cache_key_rejects_invalid_hex_and_traversal():
    """Verify only lowercase 64-char SHA-256 hex strings pass validation."""
    valid_key = "a" * 64
    assert validate_cache_key(valid_key) == valid_key

    for invalid_key in (
        "../etc/passwd",
        "..\\..\\windows\\win.ini",
        "A" * 64,
        "a" * 63,
        "a" * 65,
        "g" * 64,
        "",
    ):
        with pytest.raises(ValueError, match="Invalid narrator cache key"):
            validate_cache_key(invalid_key)


@pytest.mark.asyncio
async def test_cache_hit_skips_tts_and_single_flight_deduplicates_concurrent_calls(tmp_path):
    """Verify concurrent identical requests call TTS once and subsequent calls hit disk cache."""
    cache = NarratorCacheService(cache_dir=str(tmp_path), max_files=16)
    tts_call_count = 0

    async def fake_synthesizer(script: str) -> bytes | None:
        nonlocal tts_call_count
        tts_call_count += 1
        await asyncio.sleep(0.05)
        return b"ID3-cached-mp3-data"

    script = "The Chiefs move to 4-1 after a thrilling Week 5 win."
    key = cache.compute_cache_key(
        model="omnivoice", voice="default", seed=42, script=script
    )

    results = await asyncio.gather(
        cache.get_or_synthesize(key, script, fake_synthesizer),
        cache.get_or_synthesize(key, script, fake_synthesizer),
        cache.get_or_synthesize(key, script, fake_synthesizer),
    )

    assert tts_call_count == 1
    assert all(r is not None for r in results)

    # Subsequent call should be an immediate cache hit without calling fake_synthesizer
    hit_path = await cache.get_or_synthesize(key, script, fake_synthesizer)
    assert tts_call_count == 1
    assert hit_path is not None
    assert hit_path.read_bytes() == b"ID3-cached-mp3-data"


@pytest.mark.asyncio
async def test_lru_eviction_at_max_files_cap(tmp_path):
    """Verify oldest MP3 files by mtime are evicted when exceeding max_files."""
    cache = NarratorCacheService(cache_dir=str(tmp_path), max_files=3)

    async def fake_synthesizer(script: str) -> bytes | None:
        return f"audio:{script}".encode()

    keys: list[str] = []
    for idx in range(4):
        script = f"Script number {idx}"
        key = cache.compute_cache_key(
            model="omnivoice", voice="default", seed=42, script=script
        )
        keys.append(key)
        path = await cache.get_or_synthesize(key, script, fake_synthesizer)
        assert path is not None
        # Ensure distinct mtimes for deterministic LRU ordering
        mtime = time.time() + idx
        os.utime(path, (mtime, mtime))

    # Re-run eviction check after setting distinct mtimes
    cache._evict_if_needed()

    remaining_files = list(tmp_path.glob("*.mp3"))
    assert len(remaining_files) <= 3
    assert cache.get_cached_path(keys[0]) is None
    assert cache.get_cached_path(keys[3]) is not None
