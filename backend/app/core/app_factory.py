"""
Application Factory Pattern.

Provides a clean factory function for creating the FastAPI application.
This enables better testing and configuration flexibility.
"""

import logging
import logging.handlers
import os
import sys

from fastapi import FastAPI

from app.core.config import settings
from app.core.setup import (
    configure_exception_handlers,
    configure_middleware,
    configure_prometheus,
    configure_rate_limiting,
    configure_routes,
)


def configure_logging() -> None:
    """Configure application logging with file rotation."""
    log_dir = settings.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = (
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        if settings.LOG_FORMAT == "text"
        else '{"time":"%(asctime)s","name":"%(name)s","level":"%(levelname)s","message":"%(message)s"}'
    )

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, "app.log"),
                maxBytes=settings.LOG_MAX_BYTES,
                backupCount=settings.LOG_BACKUP_COUNT,
            ),
        ],
    )


def create_app(config: dict | None = None) -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.

    Args:
        config: Optional configuration overrides for testing

    Returns:
        Configured FastAPI application instance
    """
    # Configure logging first
    configure_logging()

    # Create the FastAPI application
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        debug=settings.DEBUG,
    )

    # Add root endpoint
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Stellar Sagan NFL Simulation Engine"}

    # Configure all application components
    configure_rate_limiting(app)
    configure_prometheus(app)
    configure_middleware(app)
    configure_exception_handlers(app)
    configure_routes(app)

    logger = logging.getLogger(__name__)
    logger.info("Application initialized successfully")

    return app
