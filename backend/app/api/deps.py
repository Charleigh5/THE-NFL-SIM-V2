"""
API dependencies for FastAPI endpoints.
"""
from app.core.database import get_db

__all__ = ["get_db"]
