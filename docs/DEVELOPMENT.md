# Development Guide

This guide covers the local development setup, environment configuration, testing procedures, and debugging techniques for the NFL Simulation Engine.

## 1. Prerequisites

Ensure you have the following installed on your system:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Download Node.js](https://nodejs.org/)
- **Git**: [Download Git](https://git-scm.com/)
- **Docker Desktop** (Optional, for containerized development): [Download Docker](https://www.docker.com/products/docker-desktop)

---

## 2. Quick Start

### 2.1 Clone the Repository

```bash
git clone https://github.com/your-username/nfl-sim-engine.git
cd nfl-sim-engine
```

### 2.2 Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**

   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   _Note: The default configuration uses SQLite, so no extra database setup is required for a quick start._

5. **Initialize the Database:**

   Apply migrations to create the database schema:

   ```bash
   alembic upgrade head
   ```

6. **Run the Backend Server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.
   API Documentation (Swagger UI): `http://localhost:8000/docs`.

### 2.3 Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Configure Environment:**

   Create a `.env` file (or copy example if available):

   ```bash
   cp .env.example .env
   ```

   Ensure `VITE_API_URL` points to your backend:

   ```properties
   VITE_API_URL=http://localhost:8000
   ```

4. **Run the Frontend Development Server:**

   ```bash
   npm run dev
   ```

   The UI will be available at `http://localhost:5173`.

---

## 3. Environment Configuration

The application is configured using environment variables.

### Backend (`backend/.env`)

| Variable       | Description                                     | Default                  |
| :------------- | :---------------------------------------------- | :----------------------- |
| `DATABASE_URL` | Database connection string                      | `sqlite:///./nfl_sim.db` |
| `LOG_LEVEL`    | Logging verbosity (DEBUG, INFO, WARNING, ERROR) | `INFO`                   |
| `ENVIRONMENT`  | App environment (development, production)       | `development`            |
| `CORS_ORIGINS` | Comma-separated list of allowed origins         | `http://localhost:5173`  |

### Frontend (`frontend/.env`)

| Variable       | Description            | Default                 |
| :------------- | :--------------------- | :---------------------- |
| `VITE_API_URL` | URL of the backend API | `http://localhost:8000` |

---

## 4. Database Management

We use **Alembic** for database migrations.

### Common Commands

- **Apply all migrations (Update DB):**

  ```bash
  alembic upgrade head
  ```

- **Create a new migration (after modifying models):**

  ```bash
  alembic revision --autogenerate -m "Description of changes"
  ```

- **Revert last migration:**

  ```bash
  alembic downgrade -1
  ```

- **View migration history:**

  ```bash
  alembic history
  ```

---

## 5. Testing Procedures

### Backend Testing

We use `pytest` for backend testing.

1. **Run all tests:**

   ```bash
   pytest
   ```

2. **Run with coverage:**

   ```bash
   pytest --cov=app
   ```

3. **Run a specific test file:**

   ```bash
   pytest tests/test_simulation.py
   ```

### Frontend Testing

- **Linting:**

  ```bash
  npm run lint
  ```

- **Type Checking:**

  ```bash
  npm run build
  ```

  _(This runs `tsc` to check for type errors)_

---

## 6. Debugging Techniques

### Backend Debugging

1. **FastAPI Debug Mode:**
   Running with `--reload` enables auto-reloading on code changes.

   ```bash
   uvicorn app.main:app --reload
   ```

2. **VS Code Debugging:**

   - Create a `.vscode/launch.json` configuration for Python: FastAPI.
   - Set breakpoints in your code.
   - Start debugging (F5).

3. **Logging:**
   Use the configured logger in your code:

   ```python
   import logging
   logger = logging.getLogger(__name__)

   logger.info("Processing season %s", season_id)
   logger.debug("Detailed variable state: %s", some_var)
   ```

   Logs are output to the console and/or `logs/` directory depending on configuration.

### Frontend Debugging

1. **React DevTools:**
   Install the React DevTools extension for Chrome/Firefox to inspect component hierarchy and state.

2. **Network Inspection:**
   Use the browser's Network tab to verify API requests and responses.

3. **Console Logging:**
   Use `console.log()` for quick checks, but prefer using the debugger statement or browser breakpoints for complex issues.

---

## 7. Code Quality

### Backend

- **Formatting:** `black .`
- **Linting:** `ruff check .`

### Frontend

- **Formatting:** `npm run format` (Prettier)
- **Linting:** `npm run lint` (ESLint)
