# Deployment Guide

This guide covers how to deploy and run the NFL Simulation Engine using Docker.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

The easiest way to run the application is using Docker Compose. This will spin up the backend, frontend, and database services.

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd THE-NFL-SIM
   ```

2. **Start the services:**

   ```bash
   docker-compose up --build
   ```

   _The `--build` flag ensures that the images are rebuilt if there are any changes._

3. **Access the application:**
   - **Frontend**: `http://localhost:5173`
   - **Backend API**: `http://localhost:8000`
   - **API Docs**: `http://localhost:8000/docs`

## Configuration

### Environment Variables

The application uses environment variables for configuration. These are defined in the `docker-compose.yml` file or can be overridden by a `.env` file.

**Backend:**

- `DATABASE_URL`: Connection string for the PostgreSQL database.
- `LOG_LEVEL`: Logging verbosity (default: INFO).

**Frontend:**

- `VITE_API_URL`: URL of the backend API (default: `http://localhost:8000`).

**Database:**

- `POSTGRES_USER`: Database user.
- `POSTGRES_PASSWORD`: Database password.
- `POSTGRES_DB`: Database name.

## Manual Deployment

If you prefer to run the services manually without Docker:

### Backend

1. Navigate to `backend/`.
2. Create a virtual environment: `python -m venv .venv`.
3. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows).
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the server: `uvicorn app.main:app --reload`.

### Frontend

1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Run the dev server: `npm run dev`.

### Database

Ensure you have a PostgreSQL instance running and update the `DATABASE_URL` in your environment to point to it.
