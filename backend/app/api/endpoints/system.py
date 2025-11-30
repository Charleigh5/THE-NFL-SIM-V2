from fastapi import APIRouter
from datetime import datetime, timezone
import logging

from app.core.database import engine
from sqlalchemy import text
from app.core.error_decorators import handle_errors

router = APIRouter(prefix="/api/system", tags=["system"])
logger = logging.getLogger(__name__)


@router.get("/health")
@handle_errors
def health_check():
    """Health check endpoint to verify the backend is running."""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Stellar Sagan NFL Simulation Engine"
    }


@router.get("/status")
@handle_errors
def system_status():
    """Get system status including database and engine availability."""
    logger.info("System status check requested")
    db_status = "disconnected"
    
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        db_status = f"error: {str(e)}"
    
    return {
        "status": "operational" if db_status == "connected" else "degraded",
        "database": db_status,
        "engine": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
