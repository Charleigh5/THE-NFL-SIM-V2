from typing import Optional, Dict, Any, Tuple
import time
import logging
import json
import os
try:
    import redis
except ImportError:
    redis = None

logger = logging.getLogger(__name__)

class MCPCache:
    """
    Hybrid cache for MCP responses using Redis with in-memory fallback.
    """

    def __init__(self):
        self.memory_cache: Dict[str, Tuple[Any, float]] = {}
        self.ttl_config = {
            "league_averages": 3600,  # 1 hour
            "player_news": 900,       # 15 minutes
            "weather": 1800,          # 30 minutes
        }

        self.redis_client = None
        if redis:
            try:
                redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                # Test connection
                self.redis_client.ping()
                logger.info("Connected to Redis cache")
            except Exception as e:
                logger.warning(f"Redis connection failed, using in-memory cache: {e}")
                self.redis_client = None

    def get(self, key: str, cache_type: str) -> Optional[Any]:
        """
        Retrieve item from cache if it exists and hasn't expired.
        """
        # Try Redis first
        if self.redis_client:
            try:
                data = self.redis_client.get(key)
                if data:
                    logger.debug(f"MCP Redis Cache HIT: {key}")
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")

        # Fallback to memory
        if key in self.memory_cache:
            data, timestamp = self.memory_cache[key]
            ttl = self.ttl_config.get(cache_type, 600) # Default 10 mins

            if time.time() - timestamp < ttl:
                logger.debug(f"MCP Memory Cache HIT: {key}")
                return data
            else:
                logger.debug(f"MCP Memory Cache EXPIRED: {key}")
                del self.memory_cache[key]

        return None

    def set(self, key: str, value: Any, cache_type: str):
        """
        Set item in cache.
        """
        ttl = self.ttl_config.get(cache_type, 600)

        # Set in Redis
        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl, json.dumps(value))
                logger.debug(f"MCP Redis Cache SET: {key}")
            except Exception as e:
                logger.error(f"Redis set error: {e}")

        # Set in Memory (as backup or primary)
        self.memory_cache[key] = (value, time.time())
        logger.debug(f"MCP Memory Cache SET: {key}")

    def clear(self):
        """Clear all cache entries."""
        if self.redis_client:
            try:
                self.redis_client.flushdb()
            except Exception as e:
                logger.error(f"Redis clear error: {e}")
        self.memory_cache.clear()

# Global cache instance
mcp_cache = MCPCache()
