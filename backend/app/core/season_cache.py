"""
High-Throughput Season & Standings Cache-Aside Layer.
Provides thread-safe in-memory caching (L1) with monotonic TTL.
"""

import logging
import threading
import time
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)


class SeasonCacheManager:
    """
    Thread-safe in-memory cache manager for season summaries and standings.
    Protected by threading.Lock() with monotonic timestamps (time.monotonic()).
    """

    def __init__(self, default_ttl: int | None = None) -> None:
        self.default_ttl: int = (
            default_ttl
            if default_ttl is not None
            else getattr(settings, "SEASON_CACHE_TTL_SECONDS", 60)
        )
        self._lock = threading.Lock()
        # Storage: summary_key -> (serialized_json, expire_at)
        self._summary_cache: dict[str, tuple[str, float]] = {}
        # Storage: (season_id, conference, division) -> (serialized_json, expire_at)
        self._standings_cache: dict[tuple[int, str | None, str | None], tuple[str, float]] = {}

    def get_summary(self, key: str = "active") -> str | None:
        """
        Retrieve cached season summary JSON string.
        Returns None on cache miss or expiration.
        """
        now = time.monotonic()
        with self._lock:
            if key in self._summary_cache:
                data, expire_at = self._summary_cache[key]
                if now < expire_at:
                    return data
                del self._summary_cache[key]
        return None

    def set_summary(
        self, serialized_json: str, key: str = "active", ttl: int | None = None
    ) -> None:
        """
        Store serialized season summary JSON string in cache.
        """
        effective_ttl = ttl if ttl is not None else self.default_ttl
        now = time.monotonic()
        with self._lock:
            self._summary_cache[key] = (serialized_json, now + effective_ttl)

    def get_standings(
        self, season_id: int, conference: str | None = None, division: str | None = None
    ) -> str | None:
        """
        Retrieve cached standings JSON string for a given season and optional filters.
        Returns None on cache miss or expiration.
        """
        key = (season_id, conference, division)
        now = time.monotonic()
        with self._lock:
            if key in self._standings_cache:
                data, expire_at = self._standings_cache[key]
                if now < expire_at:
                    return data
                del self._standings_cache[key]
        return None

    def set_standings(
        self,
        season_id: int,
        serialized_json: str,
        conference: str | None = None,
        division: str | None = None,
        ttl: int | None = None,
    ) -> None:
        """
        Store serialized standings JSON string in cache.
        """
        key = (season_id, conference, division)
        effective_ttl = ttl if ttl is not None else self.default_ttl
        now = time.monotonic()
        with self._lock:
            self._standings_cache[key] = (serialized_json, now + effective_ttl)

    def invalidate_season_caches(self, season_id: int | Any = None) -> None:
        """
        Invalidate season summary cache and standings cache.
        If season_id is None, clears all standings caches.
        If season_id is specified, clears standings for that season only.
        Always clears summary cache as summary is tied to the active season.
        """
        with self._lock:
            self._summary_cache.clear()
            if season_id is None:
                self._standings_cache.clear()
            else:
                target_id = int(season_id) if isinstance(season_id, int) or hasattr(season_id, "__int__") else None
                if target_id is not None:
                    keys_to_remove = [k for k in self._standings_cache if k[0] == target_id]
                    for k in keys_to_remove:
                        self._standings_cache.pop(k, None)
                else:
                    self._standings_cache.clear()

    def clear(self) -> None:
        """Alias to flush all season caches."""
        self.invalidate_season_caches()


# Global Singleton Instance
season_cache: SeasonCacheManager = SeasonCacheManager()


def invalidate_season_caches(season_id: int | Any = None) -> None:
    """Invalidate season caches (synchronous, thread-safe)."""
    season_cache.invalidate_season_caches(season_id)


__all__ = [
    "SeasonCacheManager",
    "season_cache",
    "invalidate_season_caches",
]
