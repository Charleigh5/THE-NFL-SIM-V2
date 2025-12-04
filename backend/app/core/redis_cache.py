"""
Redis caching for chemistry calculations
"""
import json
import hashlib
from typing import Optional, Dict
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ChemistryCache:
    """
    Redis-backed cache for chemistry metadata.
    """

    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        # Check if REDIS_ENABLED exists in settings, default to False if not
        self.enabled = getattr(settings, "REDIS_ENABLED", False)
        self.ttl = 604800  # 7 days in seconds

    async def connect(self):
        """Initialize Redis connection"""
        if not self.enabled:
            logger.info("Redis caching disabled")
            return

        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("✅ Connected to Redis for chemistry caching")
        except Exception as e:
            logger.warning(f"Redis connection failed, disabling cache: {e}")
            self.enabled = False

    def _make_key(
        self,
        team_id: int,
        season_id: int,
        week: int,
        lineup_hash: str
    ) -> str:
        """Generate cache key"""
        return f"chemistry:{team_id}:{season_id}:{week}:{lineup_hash}"

    def _hash_lineup(self, lineup: Dict[str, int]) -> str:
        """Create deterministic hash of OL lineup"""
        lineup_str = ",".join(f"{k}:{v}" for k, v in sorted(lineup.items()))
        return hashlib.md5(lineup_str.encode()).hexdigest()[:12]

    async def get(
        self,
        team_id: int,
        season_id: int,
        week: int,
        lineup: Dict[str, int]
    ) -> Optional[Dict]:
        """
        Retrieve cached chemistry metadata.

        Returns:
            Chemistry metadata dict or None if cache miss
        """
        if not self.enabled or not self.redis:
            return None

        lineup_hash = self._hash_lineup(lineup)
        key = self._make_key(team_id, season_id, week, lineup_hash)

        try:
            cached = await self.redis.get(key)
            if cached:
                logger.debug(f"✅ Chemistry cache HIT: {key}")
                return json.loads(cached)
            else:
                logger.debug(f"❌ Chemistry cache MISS: {key}")
                return None
        except Exception as e:
            logger.warning(f"Redis get error: {e}")
            return None

    async def set(
        self,
        team_id: int,
        season_id: int,
        week: int,
        lineup: Dict[str, int],
        metadata: Dict
    ):
        """
        Store chemistry metadata in cache.
        """
        if not self.enabled or not self.redis:
            return

        lineup_hash = self._hash_lineup(lineup)
        key = self._make_key(team_id, season_id, week, lineup_hash)

        try:
            await self.redis.setex(
                key,
                self.ttl,
                json.dumps(metadata)
            )
            logger.debug(f"💾 Chemistry cached: {key}")
        except Exception as e:
            logger.warning(f"Redis set error: {e}")

    async def invalidate_team(self, team_id: int, season_id: int):
        """
        Invalidate all cache entries for a team in a season.

        Called when:
        - Roster changes
        - Trade/signing affects OL
        - Manual cache flush
        """
        if not self.enabled or not self.redis:
            return

        pattern = f"chemistry:{team_id}:{season_id}:*"

        try:
            cursor = 0
            deleted = 0

            # Scan and delete matching keys
            while True:
                cursor, keys = await self.redis.scan(
                    cursor,
                    match=pattern,
                    count=100
                )

                if keys:
                    await self.redis.delete(*keys)
                    deleted += len(keys)

                if cursor == 0:
                    break

            logger.info(f"🗑️ Invalidated {deleted} chemistry cache entries for team {team_id}")
        except Exception as e:
            logger.warning(f"Redis invalidation error: {e}")


# Global instance
chemistry_cache = ChemistryCache()
