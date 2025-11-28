from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/health")
def health_check():
    """Health check endpoint to verify the backend is running."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Stellar Sagan NFL Simulation Engine"
    }


from app.core.database import engine
from sqlalchemy import text

@router.get("/status")
def system_status():
    """Get system status including database and engine availability."""
    db_status = "disconnected"
    
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "operational" if db_status == "connected" else "degraded",
        "database": db_status,
        "engine": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }
