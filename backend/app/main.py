from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import system, simulation, data, websocket, teams, players, season, genesis, feedback

from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
import logging
import logging.handlers
import os
import sys

from app.core.error_handlers import (
    database_exception_handler,
    database_operational_error_handler,
    validation_exception_handler,
    pydantic_validation_handler,
    generic_exception_handler
)
from app.middlewares.logging_middleware import LoggingMiddleware

# Configure logging
from app.core.config import settings

LOG_DIR = settings.LOG_DIR
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

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
            os.path.join(LOG_DIR, "app.log"),
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
        ),
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# Register Middlewares
app.add_middleware(LoggingMiddleware)

# Register exception handlers
app.add_exception_handler(IntegrityError, database_exception_handler)
app.add_exception_handler(OperationalError, database_operational_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include API routers

# Include API routers
app.include_router(system.router)
app.include_router(simulation.router)
app.include_router(data.router)
app.include_router(websocket.router)
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(season.router)
app.include_router(genesis.router)
app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])
from app.api.endpoints import settings as settings_endpoint
app.include_router(settings_endpoint.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Stellar Sagan NFL Simulation Engine"}
