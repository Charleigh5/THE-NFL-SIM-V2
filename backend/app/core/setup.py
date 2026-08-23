"""
Application setup utilities.

Contains modular functions for configuring middleware, exception handlers,
and routes. Used by the app factory to build the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.error_handlers import (
    database_exception_handler,
    database_operational_error_handler,
    validation_exception_handler,
    pydantic_validation_handler,
    generic_exception_handler
)
from app.middlewares.logging_middleware import LoggingMiddleware


def configure_rate_limiting(app: FastAPI) -> None:
    """Configure rate limiting with SlowAPI."""
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def configure_prometheus(app: FastAPI) -> None:
    """Configure Prometheus instrumentation for metrics."""
    Instrumentator().instrument(app).expose(app)


def configure_middleware(app: FastAPI) -> None:
    """Configure all application middleware."""
    # Custom logging middleware
    app.add_middleware(LoggingMiddleware)

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )


def configure_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers."""
    app.add_exception_handler(IntegrityError, database_exception_handler)
    app.add_exception_handler(OperationalError, database_operational_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_validation_handler)
    app.add_exception_handler(Exception, generic_exception_handler)


def configure_routes(app: FastAPI) -> None:
    """Register all API routers."""
    # Import routers here to avoid circular imports
    from app.api.endpoints import (
        system, simulation, data, websocket, teams, players, season,
        genesis, feedback, draft, settings as settings_endpoint, traits,
        news, agent_tasks, trades, scouts, medical, gameplans, abilities,
        playbook, physics_api, training, live_visualization
    )

    # Core system routes
    app.include_router(system.router)
    app.include_router(simulation.router)
    app.include_router(data.router)
    app.include_router(websocket.router)
    
    # Live Visualization (NEW - for 3D game viewing)
    app.include_router(live_visualization.router)

    # Team and player management
    app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
    app.include_router(players.router, prefix="/api/players", tags=["players"])

    # Season and game management
    app.include_router(season.router)
    app.include_router(genesis.router)
    app.include_router(draft.router)

    # Settings and configuration
    app.include_router(settings_endpoint.router)
    app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])

    # RPG and traits
    app.include_router(traits.router, prefix="/api/traits", tags=["traits"])
    app.include_router(abilities.router, prefix="/api", tags=["RPG Abilities"])

    # News and agents
    app.include_router(news.router, prefix="/api", tags=["news"])
    app.include_router(agent_tasks.router, prefix="/api/agent", tags=["agent"])

    # Trading and scouting
    app.include_router(trades.router)
    app.include_router(scouts.router)

    # Medical and gameplans
    app.include_router(medical.router)
    app.include_router(gameplans.router)
    app.include_router(training.router, prefix="/api/training", tags=["training"])

    # Playbook and familiarity (Phase 3)
    app.include_router(playbook.router, prefix="/api", tags=["playbook"])

    # 60Hz Physics (Phase 4)
    app.include_router(physics_api.router, prefix="/api", tags=["physics"])


