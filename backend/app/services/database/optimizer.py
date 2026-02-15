#!/usr/bin/env python3
"""
Database Optimization Module
============================
Query optimization and caching strategies.

Phase 12: Database Enhancements
- Query caching
- Index recommendations
- Performance monitoring
"""

import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass
class CacheEntry:
    """Cached query result."""
    key: str
    value: Any
    created_at: datetime
    ttl_seconds: int
    hits: int = 0

    @property
    def is_expired(self) -> bool:
        """Check if cache entry expired."""
        return datetime.now() > self.created_at + timedelta(seconds=self.ttl_seconds)


@dataclass
class QueryStats:
    """Statistics for a query pattern."""
    query_pattern: str
    execution_count: int = 0
    avg_duration_ms: float = 0.0
    max_duration_ms: float = 0.0
    last_executed: datetime | None = None


class QueryCache:
    """
    In-memory query result cache.
    """

    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self.cache: dict[str, CacheEntry] = {}

    def _generate_key(self, query: str, params: dict | None = None) -> str:
        """Generate cache key from query and params."""
        key_str = query + str(params or {})
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, query: str, params: dict | None = None) -> Any | None:
        """Retrieve cached result."""
        key = self._generate_key(query, params)
        entry = self.cache.get(key)

        if entry and not entry.is_expired:
            entry.hits += 1
            return entry.value
        elif entry and entry.is_expired:
            del self.cache[key]

        return None

    def set(self, query: str, value: Any, params: dict | None = None, ttl: int | None = None):
        """Cache a query result."""
        key = self._generate_key(query, params)
        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.now(),
            ttl_seconds=ttl or self.default_ttl
        )

    def invalidate(self, pattern: str = None):
        """
        Invalidate cache entries.

        If pattern is None, clears all.
        """
        if pattern is None:
            self.cache.clear()
        else:
            # Would use pattern matching
            pass

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total_entries = len(self.cache)
        total_hits = sum(e.hits for e in self.cache.values())

        return {
            "total_entries": total_entries,
            "total_hits": total_hits,
            "expired_entries": sum(1 for e in self.cache.values() if e.is_expired),
        }


class QueryOptimizer:
    """
    Analyzes and optimizes database queries.
    """

    def __init__(self):
        self.query_stats: dict[str, QueryStats] = {}

    def record_query(self, query_pattern: str, duration_ms: float):
        """Record a query execution for analysis."""
        if query_pattern not in self.query_stats:
            self.query_stats[query_pattern] = QueryStats(query_pattern=query_pattern)

        stats = self.query_stats[query_pattern]

        # Update running average
        total_duration = stats.avg_duration_ms * stats.execution_count + duration_ms
        stats.execution_count += 1
        stats.avg_duration_ms = total_duration / stats.execution_count
        stats.max_duration_ms = max(stats.max_duration_ms, duration_ms)
        stats.last_executed = datetime.now()

    def get_slow_queries(self, threshold_ms: float = 100.0) -> list[QueryStats]:
        """Get queries that exceed duration threshold."""
        return [s for s in self.query_stats.values() if s.avg_duration_ms > threshold_ms]

    def recommend_indexes(self) -> list[str]:
        """
        Recommend indexes based on query patterns.
        (Simplified - real implementation would analyze query structure)
        """
        recommendations = []

        for pattern, stats in self.query_stats.items():
            if stats.execution_count > 100 and stats.avg_duration_ms > 50:
                # Frequent slow query
                if "WHERE" in pattern.upper():
                    recommendations.append(f"Consider index for: {pattern[:50]}...")

        return recommendations
