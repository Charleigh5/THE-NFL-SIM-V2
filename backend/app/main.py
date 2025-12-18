"""
FastAPI Application Entry Point.

This module uses the app factory pattern for better testability.
All configuration is handled by the create_app() function.
"""

from app.core.app_factory import create_app

# Create the application instance
app = create_app()
