"""
High-Throughput Roster Cache-Aside Layer.
Provides sub-millisecond thread-safe in-memory caching (L1) with transparent Redis fallback (L2).
Guarantees zero 500 errors and zero latency degradation when Redis is offline.
"""

import logging
import threading
import time
from typing import Dict, Optional, Tuple

from app.core.config import settings

logger = logging.getLogger(__name__)


class RosterCacheManager:
    """
    Two-tier Cache-Aside Manager for Team Rosters:
    - Tier 1: Thread-safe in-memory cache protected by threading.Lock() with monotonic TTL.
    - Tier 2: Redis cache with strict fast-fail circuit breaker.
    """

    def __init__(self, default_ttl: Optional[int] = None) -> None:
        self.default_ttl = (
            default_ttl
            if default_ttl is not None
            else getattr(settings, "ROSTER_CACHE_TTL_SECONDS", 60)
        )
        self._lock = threading.Lock()
        # Memory storage: team_id -> (serialized_json_str, expire_monotonic_timestamp)
        self._memory_cache: Dict[int, Tuple[str, float]] = {}

        # Redis setup with fast-fail circuit breaker
        self.redis_enabled = getattr(settings, "REDIS_ENABLED", False)
        self.redis_client = None
        self._init_redis()

    def _init_redis(self) -> None:
        """Attempt connection to Redis once at startup with strict 200ms socket timeout."""
        if not self.redis_enabled:
            return

        try:
            import redis

            redis_url = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")
            client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_timeout=0.2,
                socket_connect_timeout=0.2,
                health_check_interval=30,
            )
            client.ping()
            self.redis_client = client
            logger.info("Connected to Redis for L2 roster caching")
        except Exception as e:
            logger.warning(
                "Redis unavailable (%s); running purely on in-memory roster cache", e
            )
            self.redis_client = None
            self.redis_enabled = False

    def _cache_key(self, team_id: int) -> str:
        return f"roster:team:{team_id}"

    def get_roster(self, team_id: int) -> Optional[str]:
        """
        Retrieve serialized roster JSON string for a team.
        Returns None if cache miss or expired.
        """
        now = time.monotonic()

        # 1. Check L1 In-Memory Cache (sub-millisecond)
        with self._lock:
            if team_id in self._memory_cache:
                data, expire_at = self._memory_cache[team_id]
                if now < expire_at:
                    return data
                # Expired: evict immediately
                del self._memory_cache[team_id]

        # 2. Check L2 Redis Cache (if active)
        if self.redis_enabled and self.redis_client:
            try:
                key = self._cache_key(team_id)
                cached = self.redis_client.get(key)
                if cached is not None:
                    # Backfill L1 Memory Cache
                    with self._lock:
                        self._memory_cache[team_id] = (cached, now + self.default_ttl)
                    return cached
            except Exception as e:
                logger.warning(
                    "Redis get error for team %s: %s; falling back to in-memory cache",
                    team_id,
                    e,
                )
                self.redis_client = None
                self.redis_enabled = False

        return None

    def set_roster(
        self, team_id: int, serialized_json: str, ttl: Optional[int] = None
    ) -> None:
        """
        Populate serialized roster JSON string in L1 and L2 caches.
        """
        effective_ttl = ttl if ttl is not None else self.default_ttl
        now = time.monotonic()

        # 1. Store in L1 In-Memory Cache
        with self._lock:
            self._memory_cache[team_id] = (serialized_json, now + effective_ttl)

        # 2. Store in L2 Redis Cache
        if self.redis_enabled and self.redis_client:
            try:
                key = self._cache_key(team_id)
                self.redis_client.setex(key, effective_ttl, serialized_json)
            except Exception as e:
                logger.warning(
                    "Redis set error for team %s: %s; falling back to in-memory cache",
                    team_id,
                    e,
                )
                self.redis_client = None
                self.redis_enabled = False

    def invalidate_team(self, team_id: int) -> None:
        """Invalidate cached roster for a specific team."""
        with self._lock:
            self._memory_cache.pop(team_id, None)

        if self.redis_enabled and self.redis_client:
            try:
                key = self._cache_key(team_id)
                self.redis_client.delete(key)
            except Exception as e:
                logger.warning(
                    "Redis delete error for team %s: %s; falling back to in-memory cache",
                    team_id,
                    e,
                )
                self.redis_client = None
                self.redis_enabled = False

    def invalidate_all(self) -> None:
        """Flush all cached rosters across all teams."""
        with self._lock:
            self._memory_cache.clear()

        if self.redis_enabled and self.redis_client:
            try:
                keys = self.redis_client.keys("roster:team:*")
                if keys:
                    self.redis_client.delete(*keys)
            except Exception as e:
                logger.warning(
                    "Redis invalidate_all error: %s; falling back to in-memory cache",
                    e,
                )
                self.redis_client = None
                self.redis_enabled = False

    def clear(self) -> None:
        """Alias for invalidate_all."""
        self.invalidate_all()


# Global Singleton Instance
roster_cache: RosterCacheManager = RosterCacheManager()


def invalidate_team_roster_cache(team_id: int) -> None:
    """Invalidate the cached roster for a specific team (synchronous, thread-safe)."""
    roster_cache.invalidate_team(team_id)


def invalidate_all_team_roster_caches() -> None:
    """Invalidate all cached rosters across all teams (synchronous, thread-safe)."""
    roster_cache.invalidate_all()


__all__ = [
    "RosterCacheManager",
    "roster_cache",
    "invalidate_team_roster_cache",
    "invalidate_all_team_roster_caches",
]
