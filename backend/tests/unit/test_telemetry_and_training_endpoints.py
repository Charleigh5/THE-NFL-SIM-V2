"""
Unit tests for Client Error Telemetry (/api/errors/log),
Player Training Profile (/api/players/{id}/training-profile),
and Medical Router segregation.
"""

import pytest
from fastapi.testclient import TestClient
from app.core.app_factory import create_app
from app.models.player import Player, Position
from app.models.player_attributes import PlayerAttributes


def test_client_error_logging_endpoint(client):
    """Verify frontend telemetry /api/errors/log endpoint accepts error payloads."""
    payload = {
        "errors": [
            {
                "id": "err-123",
                "timestamp": "2026-09-24T00:00:00Z",
                "level": "error",
                "category": "ui",
                "message": "Uncaught TypeError in TestWidget",
                "stack": "TypeError: Cannot read properties of undefined at TestWidget.render",
                "url": "http://localhost:5173/training-center",
                "sessionId": "test-session-abc",
                "handled": False
            }
        ]
    }
    response = client.post("/api/errors/log", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["received"] == 1


def test_player_training_profile_endpoint(client, db_session):
    """Verify /api/players/{player_id}/training-profile returns computed weaknesses."""
    player = Player(
        first_name="Marcus",
        last_name="Testrunner",
        position=Position.WR,
        jersey_number=88,
        overall_rating=82,
        age=24,
        experience=2,
    )
    player.speed = 91
    player.acceleration = 89
    player.strength = 72
    player.agility = 85
    player.awareness = 68

    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)


    response = client.get(f"/api/players/{player.id}/training-profile")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == player.id
    assert data["first_name"] == "Marcus"
    assert data["last_name"] == "Testrunner"
    assert "awareness" in data["weaknesses"]
    assert "strength" in data["weaknesses"]


def test_medical_router_segregation():
    """Verify medical.py does not duplicate playcalling routes."""
    from app.api.endpoints.medical import router as med_router
    routes = [route.path for route in med_router.routes]
    # Ensure playcalling paths are not present in medical_router
    assert not any("playcalling" in path for path in routes)
    assert not any("recommendation" in path for path in routes)
