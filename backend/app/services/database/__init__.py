"""
DATABASE Package
================
Database management and optimization systems.

Phase 12: Database Enhancements
- Migration Manager
- Query Cache
- Query Optimizer
"""

from .migrations import (
    MigrationManager,
    Migration,
    MigrationHistory,
    MigrationStatus,
)

from .optimizer import (
    QueryCache,
    CacheEntry,
    QueryOptimizer,
    QueryStats,
)

__all__ = [
    # Migrations
    "MigrationManager", "Migration", "MigrationHistory", "MigrationStatus",
    # Optimizer
    "QueryCache", "CacheEntry", "QueryOptimizer", "QueryStats",
]
