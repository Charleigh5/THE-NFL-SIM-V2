"""
Unit tests for the app factory pattern.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_create_app_returns_fastapi_instance():
    """Test that create_app returns a valid FastAPI instance."""
    from app.core.app_factory import create_app

    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.title == "Stellar Sagan NFL Simulation Engine"


def test_create_app_has_root_endpoint():
    """Test that the app has a working root endpoint."""
    from app.core.app_factory import create_app

    app = create_app()
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Stellar Sagan NFL Simulation Engine"


def test_create_app_has_middleware():
    """Test that middleware is configured."""
    from app.core.app_factory import create_app

    app = create_app()

    # Check that middleware stack has entries
    # FastAPI adds middleware as user_middleware list
    assert len(app.user_middleware) > 0


def test_create_app_has_exception_handlers():
    """Test that exception handlers are registered."""
    from app.core.app_factory import create_app

    app = create_app()

    # Check that custom exception handlers are registered
    assert len(app.exception_handlers) > 0


def test_create_app_has_routes():
    """Test that routes are configured."""
    from app.core.app_factory import create_app

    app = create_app()

    # Check that routes are registered
    routes = [route.path for route in app.routes]

    # Verify some expected routes exist
    assert "/" in routes
    assert "/health" in routes or any("/api" in r for r in routes)
