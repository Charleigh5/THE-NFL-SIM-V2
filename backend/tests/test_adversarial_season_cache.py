"""
Adversarial Stress Test Suite for Season Cache-Aside Layer & Single-Pass Aggregation.
Validates cache invalidation correctness, fresh DB state propagation,
isolation across multiple seasons, concurrent race condition safety, and cache poisoning recovery.
"""

import asyncio
import time
import pytest
from sqlalchemy import select

from app.core.season_cache import season_cache, invalidate_season_caches
from app.models.season import Season, SeasonStatus
from app.models.team import Team


@pytest.fixture(autouse=True)
def clean_season_cache():
    """Ensure season cache is completely flushed before and after each test."""
    season_cache.clear()
    yield
    season_cache.clear()


@pytest.mark.asyncio
async def test_adversarial_advance_week_evicts_summary_and_returns_fresh_state(async_client, async_db_session):
    """
    Adversarial Test 1:
    Verify that calling POST /api/season/{id}/advance-week evicts cached responses
    and guarantees the subsequent GET /api/season/summary returns fresh database state.
    """
    # 1. Setup: Seed team and active season at week 1
    team = Team(
        name="Packers",
        city="Green Bay",
        abbreviation="GB",
        conference="NFC",
        division="North",
        prestige=85,
    )
    async_db_session.add(team)
    await async_db_session.commit()

    season = Season(
        year=2026,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=18,
        current_week=1,
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # 2. First call: Cache miss, loads from DB and populates cache
    assert season_cache.get_summary() is None
    resp1 = await async_client.get("/api/season/summary")
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["season"]["current_week"] == 1
    assert season_cache.get_summary() is not None

    # 3. Second call: Cache hit, returns cached week 1
    resp2 = await async_client.get("/api/season/summary")
    assert resp2.status_code == 200
    assert resp2.json()["season"]["current_week"] == 1

    # 4. Advance week via endpoint
    adv_resp = await async_client.post(f"/api/season/{season.id}/advance-week")
    assert adv_resp.status_code == 200
    assert adv_resp.json()["current_week"] == 2

    # 5. Verify cache is evicted immediately
    assert season_cache.get_summary() is None

    # 6. Third call: MUST return week 2 (fresh database state), NOT stale week 1
    resp3 = await async_client.get("/api/season/summary")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["season"]["current_week"] == 2, (
        f"STALE CACHE ANOMALY: expected week 2, got {data3['season']['current_week']}"
    )


@pytest.mark.asyncio
async def test_adversarial_cache_poisoning_and_invalidation_recovery(async_client, async_db_session):
    """
    Adversarial Test 2:
    Simulate deliberate cache poisoning / corruption.
    Verify that invalidate_season_caches() purges corrupt state and allows
    legitimate database re-hydration.
    """
    team = Team(
        name="Chiefs",
        city="Kansas City",
        abbreviation="KC",
        conference="AFC",
        division="West",
        prestige=90,
    )
    async_db_session.add(team)
    season = Season(
        year=2026,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=18,
        current_week=5,
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # 1. Deliberately poison the L1 cache with corrupted JSON
    poisoned_payload = '{"corrupted": "adversarial_payload", "season": {"current_week": 999}}'
    season_cache.set_summary(poisoned_payload)

    # 2. Before invalidation, client receives poisoned data from cache
    resp_poisoned = await async_client.get("/api/season/summary")
    assert resp_poisoned.status_code == 200
    assert resp_poisoned.json().get("corrupted") == "adversarial_payload"

    # 3. Trigger cache invalidation
    invalidate_season_caches(season.id)
    assert season_cache.get_summary() is None

    # 4. Subsequent request must heal: re-fetch authentic data from database
    resp_healed = await async_client.get("/api/season/summary")
    assert resp_healed.status_code == 200
    healed_data = resp_healed.json()
    assert "corrupted" not in healed_data
    assert healed_data["season"]["current_week"] == 5
    assert healed_data["season"]["year"] == 2026


def test_adversarial_selective_standings_invalidation():
    """
    Adversarial Test 3:
    Verify surgical invalidation isolation:
    Invalidating Season A must purge Season A standings and active summary,
    while leaving Season B and Season C standings untouched.
    """
    # Pre-populate cache across multiple seasons and divisions
    season_cache.set_summary('{"active_season": 2026}')
    season_cache.set_standings(10, '[{"team": "BUF"}]', conference="AFC", division="East")
    season_cache.set_standings(10, '[{"team": "KC"}]', conference="AFC", division="West")
    season_cache.set_standings(20, '[{"team": "DET"}]', conference="NFC", division="North")
    season_cache.set_standings(30, '[{"team": "DAL"}]', conference="NFC", division="East")

    # Invalidate season 10 only
    invalidate_season_caches(10)

    # Summary is cleared (as it's tied to active season lifecycle)
    assert season_cache.get_summary() is None

    # Season 10 standings are gone
    assert season_cache.get_standings(10, conference="AFC", division="East") is None
    assert season_cache.get_standings(10, conference="AFC", division="West") is None

    # Season 20 and 30 standings are PRESERVED
    assert season_cache.get_standings(20, conference="NFC", division="North") == '[{"team": "DET"}]'
    assert season_cache.get_standings(30, conference="NFC", division="East") == '[{"team": "DAL"}]'

    # Invalidate all (season_id=None)
    invalidate_season_caches()
    assert season_cache.get_standings(20, conference="NFC", division="North") is None
    assert season_cache.get_standings(30, conference="NFC", division="East") is None


@pytest.mark.asyncio
async def test_adversarial_concurrent_stress_read_write_invalidation():
    """
    Adversarial Test 4:
    Stress-test concurrency under high contention:
    Multiple workers continuously reading, setting, and invalidating
    to provoke deadlocks, lock contention, or race conditions.
    """
    iterations = 50
    errors: list[Exception] = []

    async def reader_summary(worker_id: int):
        try:
            for _ in range(iterations):
                val = season_cache.get_summary()
                if val is None:
                    season_cache.set_summary(f'{{"worker": {worker_id}}}')
                await asyncio.sleep(0.001)
        except Exception as e:
            errors.append(e)

    async def reader_standings(season_id: int):
        try:
            for _ in range(iterations):
                val = season_cache.get_standings(season_id, "AFC", "East")
                if val is None:
                    season_cache.set_standings(season_id, f'[{{"season": {season_id}}}]', "AFC", "East")
                await asyncio.sleep(0.001)
        except Exception as e:
            errors.append(e)

    async def invalidator():
        try:
            for i in range(iterations):
                if i % 2 == 0:
                    invalidate_season_caches(100)
                else:
                    invalidate_season_caches()
                await asyncio.sleep(0.002)
        except Exception as e:
            errors.append(e)

    workers = [
        reader_summary(1),
        reader_summary(2),
        reader_standings(100),
        reader_standings(200),
        invalidator(),
        invalidator(),
    ]

    await asyncio.gather(*workers)
    assert len(errors) == 0, f"Concurrent stress test produced {len(errors)} errors: {errors}"


def test_adversarial_ttl_monotonic_expiry():
    """
    Adversarial Test 5:
    Verify that expired entries are automatically evicted on read via time.monotonic().
    """
    # Set short TTL (50ms)
    season_cache.set_summary('{"transient": true}', ttl=0.05)
    season_cache.set_standings(99, '[{"transient": true}]', ttl=0.05)

    # Immediate access hits cache
    assert season_cache.get_summary() is not None
    assert season_cache.get_standings(99) is not None

    # Wait past TTL
    time.sleep(0.07)

    # Subsequent access must return None (expired)
    assert season_cache.get_summary() is None
    assert season_cache.get_standings(99) is None
