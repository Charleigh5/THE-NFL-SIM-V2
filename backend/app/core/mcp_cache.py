from typing import Optional, Dict, Any, Tuple
import time
import logging

logger = logging.getLogger(__name__)

class MCPCache:
    """
    Simple time-based cache for MCP responses.
    """

    def __init__(self):
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.ttl_config = {
            "league_averages": 3600,  # 1 hour
            "player_news": 900,       # 15 minutes
            "weather": 1800,          # 30 minutes
        }

    def get(self, key: str, cache_type: str) -> Optional[Any]:
        """
        Retrieve item from cache if it exists and hasn't expired.
        """
        if key in self.cache:
            data, timestamp = self.cache[key]
            ttl = self.ttl_config.get(cache_type, 600) # Default 10 mins

            if time.time() - timestamp < ttl:
                logger.debug(f"MCP Cache HIT: {key}")
                return data
            else:
                logger.debug(f"MCP Cache EXPIRED: {key}")
                del self.cache[key]

        return None

    def set(self, key: str, value: Any, cache_type: str):
        """
        Set item in cache with current timestamp.
        """
        logger.debug(f"MCP Cache SET: {key}")
        self.cache[key] = (value, time.time())

    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()

# Global cache instance
mcp_cache = MCPCache()
