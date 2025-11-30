# THE NFL SIM

Welcome to the NFL Simulation Engine, a comprehensive full-stack application for simulating NFL seasons, managing teams and players, and visualizing game outcomes.

## Documentation

We have detailed documentation available to help you get started, understand the system, and contribute.

- **[System Architecture](docs/ARCHITECTURE.md)**: High-level overview of the system design, components, and technology stack.
- **[API Documentation](docs/API.md)**: Detailed guide to the backend API endpoints, usage, and error handling.
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Instructions for building and deploying the application using Docker.
- **[Development Guide](docs/DEVELOPMENT.md)**: Comprehensive guide for local development, testing, and debugging.

## Quick Start

The easiest way to run the project is with Docker Compose:

```bash
docker-compose up --build
```

This will start:

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend**: [http://localhost:8000](http://localhost:8000)
- **Database**: PostgreSQL on port 5432

## Development Best Practices

### Code Style

- **Backend**: We use `black` for formatting and `ruff` for linting. Run `black .` in the `backend` directory before committing.
- **Frontend**: We use `Prettier` and `ESLint`. Run `npm run lint` in the `frontend` directory.

### Testing

- **Backend**: Run tests using `pytest` in the `backend` directory.
- **Frontend**: Ensure type safety by running `npm run build` (which runs `tsc`).

### Branching

- Use feature branches for new developments.
- Ensure all tests pass before merging to main.
