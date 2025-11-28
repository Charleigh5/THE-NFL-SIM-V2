# NFL Simulation Backend

## Database Setup

This project uses **Alembic** for database migrations and **SQLAlchemy** for ORM.

### Prerequisites

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

   Default configuration uses SQLite (`nfl_sim.db`).

### Managing Migrations

**Initialize Database (Apply all migrations):**

```bash
alembic upgrade head
```

**Create a New Migration:**
After modifying models in `app/models/`, run:

```bash
alembic revision --autogenerate -m "Description of changes"
```

**View Migration History:**

```bash
alembic history
```

**Downgrade Database:**

```bash
alembic downgrade -1  # Undo last migration
```

### Project Structure

- `app/models/`: SQLAlchemy ORM models (Database tables)
- `app/schemas/`: Pydantic schemas (API validation)
- `app/core/config.py`: Application settings
- `app/core/database.py`: Database session management
- `alembic/`: Migration scripts and configuration
