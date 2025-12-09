"""
Structured Logging Configuration for NFL Sim Engine
====================================================

This module provides enterprise-grade structured logging using structlog
with 2025 best practices including:

- JSON-formatted logs for production (machine-readable)
- Console-formatted logs for development (human-readable)
- Context variables for request tracing (correlation IDs)
- FastAPI middleware integration
- Async-safe logging with contextvars
- Log rotation with configurable limits
- Exception formatting with full tracebacks

References:
- https://www.structlog.org/en/stable/
- https://docs.python.org/3/library/contextvars.html
- https://fastapi.tiangolo.com/tutorial/middleware/

Author: NFL Sim Engine Team
Version: 2.0.0
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

import structlog
from structlog.types import EventDict, WrappedLogger

if TYPE_CHECKING:
    from fastapi import Request, Response

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Context variables for request tracing (async-safe)
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)
user_id_var: ContextVar[str | None] = ContextVar("user_id", default=None)
session_id_var: ContextVar[str | None] = ContextVar("session_id", default=None)

# Paths
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Default settings
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE = "application.log"
DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10MB
DEFAULT_BACKUP_COUNT = 5


# ==============================================================================
# ERROR CATEGORIES
# ==============================================================================

class ErrorCategory:
    """
    Standardized error categories for consistent error classification.

    Use these categories when logging errors to enable easy filtering
    and aggregation in log management systems.
    """
    # Game Engine Errors
    CHEMISTRY_ERROR = "CHEMISTRY_ERROR"
    SACK_CALC_ERROR = "SACK_CALC_ERROR"
    PLAY_RESOLUTION_ERROR = "PLAY_RESOLUTION_ERROR"
    WEATHER_ERROR = "WEATHER_ERROR"

    # Player/Trait Errors
    TRAIT_ERROR = "TRAIT_ERROR"
    PLAYER_ERROR = "PLAYER_ERROR"
    PROGRESSION_ERROR = "PROGRESSION_ERROR"

    # API/Database Errors
    API_ERROR = "API_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTH_ERROR = "AUTH_ERROR"

    # System Errors
    CONFIG_ERROR = "CONFIG_ERROR"
    INTEGRATION_ERROR = "INTEGRATION_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


# ==============================================================================
# PROCESSORS
# ==============================================================================

def add_request_context(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """
    Add request context from contextvars to log events.

    This processor adds correlation IDs and user information
    to every log entry for distributed tracing.
    """
    # Add request_id if available
    request_id = request_id_var.get()
    if request_id:
        event_dict["request_id"] = request_id

    # Add user_id if available
    user_id = user_id_var.get()
    if user_id:
        event_dict["user_id"] = user_id

    # Add session_id if available
    session_id = session_id_var.get()
    if session_id:
        event_dict["session_id"] = session_id

    return event_dict


def add_service_context(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """Add service metadata to log events."""
    event_dict["service"] = "nfl-sim-engine"
    event_dict["environment"] = _get_environment()
    return event_dict


def _get_environment() -> str:
    """Get the current environment from environment variables."""
    import os
    return os.getenv("ENVIRONMENT", os.getenv("ENV", "development"))


def format_exception(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """
    Format exceptions for structured logging.

    Extracts exception information and formats it as structured data
    rather than a multi-line string for better log parsing.
    """
    exc_info = event_dict.pop("exc_info", None)
    if exc_info:
        if isinstance(exc_info, tuple):
            exc_type, exc_value, exc_tb = exc_info
        elif isinstance(exc_info, BaseException):
            exc_type = type(exc_info)
            exc_value = exc_info
            exc_tb = exc_info.__traceback__
        else:
            return event_dict

        if exc_type is not None:
            import traceback
            event_dict["exception"] = {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "traceback": "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
            }

    return event_dict


# ==============================================================================
# CONFIGURATION FUNCTIONS
# ==============================================================================

def configure_logging(
    log_level: str = DEFAULT_LOG_LEVEL,
    json_format: bool | None = None,
    log_file: str | None = DEFAULT_LOG_FILE,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
    enable_console: bool = True,
) -> None:
    """
    Configure structured logging for the application.

    This function sets up both the standard logging module and structlog
    with a unified configuration. Call this once at application startup.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: If True, use JSON format; if False, use console format;
                     if None, auto-detect based on environment
        log_file: Path to log file (relative to LOGS_DIR), or None to disable
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        enable_console: Whether to output logs to console

    Example:
        >>> configure_logging(log_level="DEBUG", json_format=False)
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started", version="1.0.0")
    """
    # Auto-detect format based on environment
    if json_format is None:
        json_format = _get_environment() != "development"

    # Configure standard logging handlers
    handlers: list[logging.Handler] = []

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        handlers.append(console_handler)

    # File handler with rotation
    if log_file:
        log_path = LOGS_DIR / log_file
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=handlers,
        format="%(message)s",
        force=True  # Override any existing configuration
    )

    # Disable noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Build processor chain - core processors shared between modes
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        add_request_context,
        add_service_context,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_format:
        # Production: JSON output with our custom exception formatter
        shared_processors.append(format_exception)
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        # Development: Pretty console output with structlog's built-in exception handling
        # Note: Don't use format_exception here - it conflicts with dev.set_exc_info
        shared_processors.extend([
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.rich_traceback
            )
        ])

    # Configure structlog
    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a configured logger for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured structlog BoundLogger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing request", player_id=123)
    """
    return structlog.get_logger(name)


# ==============================================================================
# FASTAPI MIDDLEWARE
# ==============================================================================

def create_logging_middleware() -> Callable:
    """
    Create FastAPI middleware for request logging and context tracking.

    This middleware:
    - Generates unique request IDs for correlation
    - Logs request start/end with timing
    - Clears context between requests to prevent leakage
    - Adds request metadata to all logs within the request

    Returns:
        FastAPI middleware function

    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> app.middleware("http")(create_logging_middleware())
    """
    logger = get_logger("middleware.request")

    async def logging_middleware(request: Request, call_next: Callable) -> Response:
        import time

        # Clear context from previous requests
        structlog.contextvars.clear_contextvars()

        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)

        # Bind request context
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        # Log request start
        start_time = time.perf_counter()
        logger.info(
            "Request started",
            query_params=dict(request.query_params),
        )

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log request completion
            logger.info(
                "Request completed",
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            # Add correlation headers to response
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Request failed",
                error_category=ErrorCategory.API_ERROR,
                duration_ms=round(duration_ms, 2),
                exc_info=e,
            )
            raise

    return logging_middleware


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def log_error(
    logger: structlog.BoundLogger,
    category: str,
    message: str,
    exc_info: bool | BaseException = True,
    **context: Any
) -> None:
    """
    Log an error with standardized category and context.

    Args:
        logger: The structlog logger instance
        category: Error category from ErrorCategory
        message: Error message
        exc_info: Exception info (True to capture current, or exception instance)
        **context: Additional context key-value pairs

    Example:
        >>> try:
        ...     calculate_chemistry(team_id)
        ... except Exception as e:
        ...     log_error(logger, ErrorCategory.CHEMISTRY_ERROR,
        ...               "Failed to calculate chemistry", exc_info=e, team_id=team_id)
    """
    logger.error(
        message,
        error_category=category,
        exc_info=exc_info,
        **context
    )


def set_user_context(user_id: str | None, session_id: str | None = None) -> None:
    """
    Set user context for logging within the current async context.

    Call this after user authentication to include user info in logs.

    Args:
        user_id: The authenticated user's ID
        session_id: Optional session identifier
    """
    if user_id:
        user_id_var.set(user_id)
        structlog.contextvars.bind_contextvars(user_id=user_id)

    if session_id:
        session_id_var.set(session_id)
        structlog.contextvars.bind_contextvars(session_id=session_id)


# ==============================================================================
# INITIALIZATION
# ==============================================================================

# Auto-configure on import with sensible defaults
# Applications can reconfigure by calling configure_logging() explicitly
configure_logging()
