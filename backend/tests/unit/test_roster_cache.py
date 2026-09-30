"""
Unit tests for High-Throughput Roster Cache-Aside Layer.
Verifies L1 in-memory caching, L2 Redis fallback, circuit breaking, TTL eviction,
thread safety under 20 concurrent workers, and synchronous invalidation hooks.
"""

import concurrent.futures
import json
import time
from unittest.mock import MagicMock, patch

import pytest
from app.core.roster_cache import (
    RosterCacheManager,
    invalidate_all_team_roster_caches,
    invalidate_team_roster_cache,
    roster_cache,
)


@pytest.fixture(autouse=True)
def clean_global_cache():
    """Ensure global singleton cache is cleared before and after each test."""
    roster_cache.clear()
    yield
    roster_cache.clear()


def test_cache_miss_followed_by_cache_hit():
    """Test that a cache miss returns None and a subsequent set results in a cache hit."""
    manager = RosterCacheManager(default_ttl=60)
    # Ensure starting in clean state
    manager.invalidate_all()

    # 1. Cache Miss
    assert manager.get_roster(1) is None

    # 2. Populate Cache
    payload = json.dumps([{"id": 101, "first_name": "Patrick", "last_name": "Mahomes"}])
    manager.set_roster(1, payload)

    # 3. Cache Hit
    cached = manager.get_roster(1)
    assert cached == payload
    parsed = json.loads(cached)
    assert len(parsed) == 1
    assert parsed[0]["last_name"] == "Mahomes"


def test_ttl_expiration_with_simulated_time():
    """Test that cached items expire strictly after the TTL has elapsed."""
    manager = RosterCacheManager(default_ttl=60)
    payload = json.dumps([{"id": 1, "name": "Player 1"}])

    base_time = 1000.0

    with patch("time.monotonic", return_value=base_time):
        manager.set_roster(team_id=5, serialized_json=payload, ttl=60)
        # Immediate read within TTL
        assert manager.get_roster(5) == payload

    # 59 seconds later (still valid)
    with patch("time.monotonic", return_value=base_time + 59.9):
        assert manager.get_roster(5) == payload

    # 60.1 seconds later (expired)
    with patch("time.monotonic", return_value=base_time + 60.1):
        assert manager.get_roster(5) is None
        # Verify key was actively evicted from memory
        assert 5 not in manager._memory_cache


def test_targeted_invalidation_vs_global_invalidation():
    """Test that invalidate_team_roster_cache purges only the target team and global purges all."""
    # Populate teams 1, 2, and 3 in the global singleton
    payload_1 = json.dumps([{"team": 1}])
    payload_2 = json.dumps([{"team": 2}])
    payload_3 = json.dumps([{"team": 3}])

    roster_cache.set_roster(1, payload_1)
    roster_cache.set_roster(2, payload_2)
    roster_cache.set_roster(3, payload_3)

    assert roster_cache.get_roster(1) == payload_1
    assert roster_cache.get_roster(2) == payload_2
    assert roster_cache.get_roster(3) == payload_3

    # Targeted invalidation of Team 1
    invalidate_team_roster_cache(1)

    assert roster_cache.get_roster(1) is None
    assert roster_cache.get_roster(2) == payload_2
    assert roster_cache.get_roster(3) == payload_3

    # Global invalidation across all teams
    invalidate_all_team_roster_caches()

    assert roster_cache.get_roster(1) is None
    assert roster_cache.get_roster(2) is None
    assert roster_cache.get_roster(3) is None


def test_thread_safety_20_concurrent_workers():
    """Test thread safety under 20 concurrent worker threads reading and writing simultaneously."""
    manager = RosterCacheManager(default_ttl=60)
    concurrency = 20
    operations_per_worker = 50

    errors = []

    def worker_task(worker_id: int):
        try:
            for i in range(operations_per_worker):
                team_id = (worker_id + i) % 8 + 1  # Distribute across 8 teams
                payload = json.dumps([{"worker": worker_id, "op": i, "team": team_id}])

                # Mix of set, get, and occasional invalidations
                manager.set_roster(team_id, payload)
                val = manager.get_roster(team_id)
                assert val is not None, f"Worker {worker_id} expected hit on team {team_id}"

                if i % 10 == 0:
                    manager.invalidate_team(team_id)
        except Exception as e:
            errors.append(f"Worker {worker_id} encountered exception: {e}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(worker_task, w) for w in range(concurrency)]
        concurrent.futures.wait(futures)

    assert not errors, f"Concurrent thread errors encountered: {errors}"


def test_offline_redis_defense_on_initialization():
    """Test that offline Redis during startup fails fast without exceptions and falls back to memory."""
    with patch("app.core.roster_cache.settings") as mock_settings:
        mock_settings.REDIS_ENABLED = True
        mock_settings.REDIS_URL = "redis://127.0.0.1:9999/0"
        mock_settings.ROSTER_CACHE_TTL_SECONDS = 60

        with patch("redis.from_url") as mock_from_url:
            mock_client = MagicMock()
            mock_client.ping.side_effect = TimeoutError("Connection timed out")
            mock_from_url.return_value = mock_client

            manager = RosterCacheManager()

            # Verify fast-fail circuit breaker tripped
            assert manager.redis_enabled is False
            assert manager.redis_client is None

            # Verify in-memory caching continues normally
            manager.set_roster(10, '{"offline": true}')
            assert manager.get_roster(10) == '{"offline": true}'


def test_offline_redis_defense_on_runtime_failure():
    """Test that runtime Redis errors are safely handled and trip the circuit breaker."""
    with patch("app.core.roster_cache.settings") as mock_settings:
        mock_settings.REDIS_ENABLED = True
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_settings.ROSTER_CACHE_TTL_SECONDS = 60

        with patch("redis.from_url") as mock_from_url:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_from_url.return_value = mock_client

            manager = RosterCacheManager()
            assert manager.redis_enabled is True
            assert manager.redis_client is not None

            # Simulate Redis dropping out during a get operation
            mock_client.get.side_effect = ConnectionResetError("Connection lost")

            # Must not raise 500 / exception, must return None or memory fallback
            result = manager.get_roster(99)
            assert result is None

            # Circuit breaker should have disabled Redis
            assert manager.redis_enabled is False
            assert manager.redis_client is None


def test_redis_l2_hit_and_l1_backfill():
    """Test that an L2 Redis hit backfills the L1 in-memory cache."""
    with patch("app.core.roster_cache.settings") as mock_settings:
        mock_settings.REDIS_ENABLED = True
        mock_settings.REDIS_URL = "redis://localhost:6379/0"
        mock_settings.ROSTER_CACHE_TTL_SECONDS = 60

        with patch("redis.from_url") as mock_from_url:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_from_url.return_value = mock_client

            manager = RosterCacheManager()

            redis_payload = json.dumps([{"id": 7, "name": "L2 Player"}])
            mock_client.get.return_value = redis_payload

            # 1. First get: L1 miss, L2 hit
            res = manager.get_roster(7)
            assert res == redis_payload
            assert mock_client.get.call_count == 1

            # 2. Second get: Should hit L1 directly (no second Redis get call)
            res2 = manager.get_roster(7)
            assert res2 == redis_payload
            assert mock_client.get.call_count == 1  # Still 1, proving L1 backfill hit!


@pytest.mark.asyncio
async def test_endpoint_read_team_roster_cache_hit_bypass():
    """Test that read_team_roster returns cached Response on hit without executing database query."""
    from app.api.endpoints.teams import read_team_roster
    from starlette.responses import Response

    team_id = 77
    cached_json = json.dumps([
        {
            "id": 999,
            "first_name": "Test",
            "last_name": "CachedPlayer",
            "position": "QB",
            "jersey_number": 12,
            "overall_rating": 99,
            "depth_chart_rank": 1,
            "age": 28,
            "experience": 5,
        }
    ])

    roster_cache.set_roster(team_id, cached_json)

    # Mock DB session - should NOT be called on cache hit
    mock_db = MagicMock()

    response = await read_team_roster(team_id=team_id, db=mock_db)

    assert isinstance(response, Response)
    assert response.media_type == "application/json"
    assert response.body.decode("utf-8") == cached_json
    # Verify execute was never called on DB
    mock_db.execute.assert_not_called()
