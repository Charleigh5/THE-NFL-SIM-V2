#!/usr/bin/env python3
"""
Database Migrations Module
==========================
Manages schema versioning and migrations.

Phase 12: Database Enhancements
- Migration tracking
- Schema versioning
- Rollback support
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MigrationStatus(str, Enum):
    """Migration execution status."""
    PENDING = "PENDING"
    APPLIED = "APPLIED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass
class Migration:
    """A single database migration."""
    version: str
    name: str
    description: str
    up_sql: str
    down_sql: str
    status: MigrationStatus = MigrationStatus.PENDING
    applied_at: datetime | None = None


@dataclass
class MigrationHistory:
    """Record of applied migrations."""
    migrations: list[Migration] = field(default_factory=list)
    current_version: str = "0.0.0"


class MigrationManager:
    """
    Manages database schema migrations.
    """

    def __init__(self):
        self.history = MigrationHistory()
        self.pending: list[Migration] = []

    def register_migration(self, migration: Migration):
        """Add a migration to the pending queue."""
        self.pending.append(migration)

    def apply_migration(self, migration: Migration) -> bool:
        """
        Apply a single migration (mock - would execute SQL).
        """
        try:
            # In real implementation: execute migration.up_sql
            migration.status = MigrationStatus.APPLIED
            migration.applied_at = datetime.now()
            self.history.migrations.append(migration)
            self.history.current_version = migration.version
            return True
        except Exception:
            migration.status = MigrationStatus.FAILED
            return False

    def rollback_migration(self, migration: Migration) -> bool:
        """
        Rollback a migration (mock - would execute down_sql).
        """
        try:
            # In real implementation: execute migration.down_sql
            migration.status = MigrationStatus.ROLLED_BACK
            return True
        except Exception:
            return False

    def apply_all_pending(self) -> int:
        """
        Apply all pending migrations in order.
        Returns count of applied migrations.
        """
        applied = 0
        for migration in sorted(self.pending, key=lambda m: m.version):
            if self.apply_migration(migration):
                applied += 1
            else:
                break  # Stop on failure
        self.pending = [m for m in self.pending if m.status == MigrationStatus.PENDING]
        return applied

    def get_status(self) -> dict:
        """Get migration status summary."""
        return {
            "current_version": self.history.current_version,
            "applied_count": len(self.history.migrations),
            "pending_count": len(self.pending),
            "last_migration": self.history.migrations[-1].name if self.history.migrations else None,
        }
