#!/usr/bin/env python3
"""
Phase 12: Database Tests
========================
Unit tests for database modules.
"""

import pytest
from datetime import datetime, timedelta
from app.services.database import (
    MigrationManager, Migration, MigrationStatus,
    QueryCache, QueryOptimizer,
)


class TestMigrationManager:
    """Tests for MigrationManager."""

    @pytest.fixture
    def manager(self):
        return MigrationManager()

    @pytest.fixture
    def sample_migration(self):
        return Migration(
            version="1.0.0",
            name="add_player_traits",
            description="Adds traits column to players",
            up_sql="ALTER TABLE players ADD COLUMN traits JSON",
            down_sql="ALTER TABLE players DROP COLUMN traits"
        )

    def test_register_migration(self, manager, sample_migration):
        """Registers migration to pending."""
        manager.register_migration(sample_migration)

        assert len(manager.pending) == 1

    def test_apply_migration(self, manager, sample_migration):
        """Applies migration successfully."""
        result = manager.apply_migration(sample_migration)

        assert result
        assert sample_migration.status == MigrationStatus.APPLIED
        assert sample_migration.applied_at is not None

    def test_apply_all_pending(self, manager):
        """Applies multiple migrations in order."""
        m1 = Migration("1.0.0", "first", "", "UP1", "DOWN1")
        m2 = Migration("1.1.0", "second", "", "UP2", "DOWN2")

        manager.register_migration(m2)  # Out of order
        manager.register_migration(m1)

        applied = manager.apply_all_pending()

        assert applied == 2
        assert manager.history.current_version == "1.1.0"

    def test_get_status(self, manager, sample_migration):
        """Returns status summary."""
        manager.apply_migration(sample_migration)

        status = manager.get_status()

        assert status["current_version"] == "1.0.0"
        assert status["applied_count"] == 1


class TestQueryCache:
    """Tests for QueryCache."""

    @pytest.fixture
    def cache(self):
        return QueryCache(default_ttl=60)

    def test_set_and_get(self, cache):
        """Stores and retrieves value."""
        cache.set("SELECT * FROM players", {"name": "Test"})

        result = cache.get("SELECT * FROM players")

        assert result == {"name": "Test"}

    def test_cache_miss(self, cache):
        """Returns None on miss."""
        result = cache.get("SELECT * FROM nonexistent")

        assert result is None

    def test_cache_expiry(self, cache):
        """Expired entries are detected."""
        cache.set("SELECT 1", "value", ttl=1)

        # Entry should exist initially
        entry = cache.cache[cache._generate_key("SELECT 1")]

        # Force expiry by backdating
        from datetime import timedelta
        entry.created_at = entry.created_at - timedelta(seconds=10)

        result = cache.get("SELECT 1")
        assert result is None

    def test_cache_stats(self, cache):
        """Returns cache statistics."""
        cache.set("Q1", "V1")
        cache.get("Q1")
        cache.get("Q1")

        stats = cache.get_stats()

        assert stats["total_entries"] == 1
        assert stats["total_hits"] == 2


class TestQueryOptimizer:
    """Tests for QueryOptimizer."""

    @pytest.fixture
    def optimizer(self):
        return QueryOptimizer()

    def test_record_query(self, optimizer):
        """Records query execution."""
        optimizer.record_query("SELECT * FROM players WHERE id = ?", 50.0)
        optimizer.record_query("SELECT * FROM players WHERE id = ?", 70.0)

        stats = optimizer.query_stats["SELECT * FROM players WHERE id = ?"]

        assert stats.execution_count == 2
        assert stats.avg_duration_ms == 60.0

    def test_get_slow_queries(self, optimizer):
        """Identifies slow queries."""
        optimizer.record_query("SLOW_QUERY", 150.0)
        optimizer.record_query("FAST_QUERY", 10.0)

        slow = optimizer.get_slow_queries(threshold_ms=100.0)

        assert len(slow) == 1
        assert slow[0].query_pattern == "SLOW_QUERY"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
