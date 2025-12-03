# Database Migrations Guide

This document provides comprehensive guidance on managing database migrations for the NFL SIM application using Alembic.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Creating Migrations](#creating-migrations)
- [Running Migrations](#running-migrations)
- [Rollback Procedures](#rollback-procedures)
- [Testing Migrations](#testing-migrations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The NFL SIM application uses **Alembic** for database schema versioning and migrations. Alembic provides:

- **Version control** for database schema
- **Automatic migration generation** from SQLAlchemy models
- **Up and down migration** capabilities
- **Safe rollback** procedures

## Prerequisites

```bash
# Ensure Alembic is installed
cd backend
pip install alembic

# Verify database connection
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/nfl_sim"
```

## Creating Migrations

### Auto-generate from Model Changes

When you modify SQLAlchemy models, generate a migration automatically:

```bash
cd backend

# Generate migration with descriptive message
alembic revision --autogenerate -m "Add player chemistry tracking"

# This creates a new file in backend/alembic/versions/
# Example: 20240312_123456_add_player_chemistry_tracking.py
```

### Manual Migration Creation

For complex changes or data migrations:

```bash
cd backend

# Create empty migration
alembic revision -m "Migrate legacy player data"

# Edit the generated file to add custom upgrade/downgrade logic
```

### Migration File Structure

```python
"""Add player chemistry tracking

Revision ID: abc123def456
Revises: prev_revision_id
Create Date: 2024-03-12 12:34:56
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = 'abc123def456'
down_revision = 'prev_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    # Add new table
    op.create_table(
        'player_chemistry',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.Column('chemistry_score', sa.Float(), default=0.0),
        sa.Column('games_together', sa.Integer(), default=0),
    )

    # Add foreign key
    op.create_foreign_key(
        'fk_player_chemistry_player',
        'player_chemistry', 'players',
        ['player_id'], ['id'],
        ondelete='CASCADE'
    )

    # Add index
    op.create_index(
        'ix_player_chemistry_player_id',
        'player_chemistry',
        ['player_id']
    )

def downgrade():
    # Drop in reverse order
    op.drop_index('ix_player_chemistry_player_id')
    op.drop_constraint('fk_player_chemistry_player', 'player_chemistry')
    op.drop_table('player_chemistry')
```

## Running Migrations

### Apply All Pending Migrations

```bash
cd backend

# Upgrade to latest version
alembic upgrade head

# View current version
alembic current

# View migration history
alembic history --verbose
```

### Apply Specific Migration

```bash
# Upgrade to specific revision
alembic upgrade abc123def456

# Upgrade one version forward
alembic upgrade +1

# Upgrade two versions forward
alembic upgrade +2
```

### Dry Run (Check SQL)

```bash
# See SQL without executing
alembic upgrade head --sql

# Output to file for review
alembic upgrade head --sql > migration_preview.sql
```

## Rollback Procedures

### Standard Rollback

```bash
cd backend

# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123def456

# Rollback all migrations (CAUTION!)
alembic downgrade base
```

### Emergency Rollback

If a migration fails in production:

1. **Identify the failed migration:**

   ```bash
   alembic current
   alembic history
   ```

2. **Rollback to previous stable version:**

   ```bash
   alembic downgrade -1
   ```

3. **Verify database state:**

   ```bash
   psql -U user -d nfl_sim -c "\dt"  # List tables
   ```

4. **Fix the migration locally and test:**

   ```bash
   # Edit the migration file
   # Test in development
   alembic upgrade head
   alembic downgrade -1
   ```

5. **Redeploy corrected migration:**

   ```bash
   alembic upgrade head
   ```

## Testing Migrations

### Local Testing Workflow

```bash
# 1. Create test database
createdb nfl_sim_migration_test

# 2. Set test database URL
export DATABASE_URL="postgresql://user:password@localhost:5432/nfl_sim_migration_test"

# 3. Run migrations
cd backend
alembic upgrade head

# 4. Test rollback
alembic downgrade -1

# 5. Re-apply
alembic upgrade head

# 6. Verify data integrity
# Run application tests against migrated database
pytest tests/

# 7. Clean up
dropdb nfl_sim_migration_test
```

### Automated Testing Script

Create `backend/scripts/test_migration.sh`:

```bash
#!/bin/bash
set -e

echo "Testing database migration..."

# Create test database
createdb nfl_sim_migration_test

# Export test DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost:5432/nfl_sim_migration_test"

# Run migrations
cd backend
alembic upgrade head

# Test downgrade
alembic downgrade -1

# Re-upgrade
alembic upgrade head

# Run tests
pytest tests/integration/ -v

# Cleanup
dropdb nfl_sim_migration_test

echo "Migration test completed successfully!"
```

Make executable:

```bash
chmod +x backend/scripts/test_migration.sh
```

## Best Practices

### 1. Always Review Auto-generated Migrations

Auto-generated migrations may miss:

- **Data migrations** (e.g., transforming existing data)
- **Complex constraints** (e.g., check constraints)
- **Index optimizations**

Always review and edit generated files before committing.

### 2. Handle Non-Nullable Columns Carefully

When adding a non-nullable column to an existing table:

```python
def upgrade():
    # Add column as nullable first
    op.add_column('players', sa.Column('new_field', sa.Integer(), nullable=True))

    # Populate with default values
    op.execute("UPDATE players SET new_field = 0")

    # Make it non-nullable
    op.alter_column('players', 'new_field', nullable=False)

def downgrade():
    op.drop_column('players', 'new_field')
```

### 3. Use Descriptive Migration Messages

```bash
# Good
alembic revision --autogenerate -m "Add player fatigue tracking with HRV metrics"

# Bad
alembic revision --autogenerate -m "Update models"
```

### 4. Test Both Upgrade and Downgrade

```bash
alembic upgrade head  # Apply migration
alembic downgrade -1  # Test rollback
alembic upgrade head  # Re-apply
```

### 5. Keep Migrations Small

- One logical change per migration
- Easier to review
- Safer to rollback
- Better git history

### 6. Backup Before Production Migrations

```bash
# PostgreSQL backup
pg_dump nfl_sim > backup_before_migration_$(date +%Y%m%d_%H%M%S).sql

# Apply migration
alembic upgrade head

# If issues occur, restore:
# dropdb nfl_sim
# createdb nfl_sim
# psql nfl_sim < backup_before_migration_20240312_123456.sql
```

## Troubleshooting

### Migration History Conflict

**Error:** `Target database is not up to date`

**Solution:**

```bash
# Check current version
alembic current

# View pending migrations
alembic history

# Stamp database with current code version (CAUTION)
alembic stamp head
```

### Multiple Heads Detected

**Error:** `Multiple head revisions are present`

**Solution:**

```bash
# Merge heads
alembic merge heads -m "Merge migration branches"
```

### Constraint Violations

**Error:** `IntegrityError` during migration

**Solution:**

1. Review the migration
2. Add data migration logic to handle existing data
3. Consider using `batch_alter_table` for SQLite compatibility

```python
with op.batch_alter_table('players') as batch_op:
    batch_op.add_column(sa.Column('new_field', sa.Integer()))
```

### Foreign Key Issues

**Error:** Foreign key constraint fails

**Solution:**

```python
def upgrade():
    # Drop foreign key first
    op.drop_constraint('fk_name', 'table_name', type_='foreignkey')

    # Make changes
    op.alter_column(...)

    # Re-create foreign key
    op.create_foreign_key('fk_name', 'table_name', 'ref_table',
                         ['col'], ['ref_col'])
```

## CI/CD Integration

Migrations are automatically tested in the CI/CD pipeline. See `.github/workflows/ci.yml` for the migration check job.

Manual verification before deployment:

```bash
# In CI environment
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- NFL SIM Model Definitions: `backend/app/models/`
- Migration History: `backend/alembic/versions/`
