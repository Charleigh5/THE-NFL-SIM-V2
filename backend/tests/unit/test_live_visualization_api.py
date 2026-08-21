"""
Unit tests for Live Visualization endpoints and helper functions.
"""

from fastapi.testclient import TestClient
from app.core.app_factory import create_app
from app.api.endpoints.live_visualization import (
    get_position_group,
    get_body_type_for_position,
    get_face_mask_color,
    get_cleat_color,
    get_accessories,
    get_helmet_design,
)
from app.models.player import Player


class TestLiveVisualizationHelpers:
    """Test visual categorization and 3D attribute mapping helpers."""

    def test_get_position_group(self):
        assert get_position_group("QB") == "offense"
        assert get_position_group("RB") == "offense"
        assert get_position_group("OT") == "offense"
        assert get_position_group("DE") == "defense"
        assert get_position_group("CB") == "defense"
        assert get_position_group("K") == "special_teams"
        assert get_position_group("XYZ") == "unknown"

    def test_get_body_type_for_position(self):
        assert get_body_type_for_position("OT", None) == "large"
        assert get_body_type_for_position("WR", None) == "athletic"
        assert get_body_type_for_position("LB", None) == "muscular"
        assert get_body_type_for_position("K", None) == "average"

    def test_get_face_mask_color(self):
        assert get_face_mask_color("QB") == "light_gray"
        assert get_face_mask_color("OT") == "dark_gray"
        assert get_face_mask_color("WR") == "gray"

    def test_get_cleat_color(self):
        assert get_cleat_color("WR") == "neon"
        assert get_cleat_color("K") == "white"
        assert get_cleat_color("OT") == "black"

    def test_get_accessories(self):
        qb = Player(first_name="Tom", last_name="Brady", position="QB", height=76, weight=225, age=40)
        wr = Player(first_name="Jerry", last_name="Rice", position="WR", height=74, weight=200, age=30)
        ot = Player(first_name="Trent", last_name="Williams", position="OT", height=77, weight=320, age=32)

        assert "hand_glove" in get_accessories(qb)
        assert "gloves" in get_accessories(wr)
        assert "wrist_bands" in get_accessories(ot)

    def test_get_helmet_design_none(self):
        design = get_helmet_design(None)
        assert design["base"] == "plain"
        assert design["stripe"] == "none"


class TestLiveVisualizationEndpoints:
    """Test API endpoint responses."""

    def setup_method(self):
        self.app = create_app()
        self.client = TestClient(self.app)

    def test_get_formation_data(self):
        response = self.client.get("/api/live/game/1/formation/101")
        assert response.status_code == 200
        data = response.json()
        assert data["play_id"] == 101
        assert "formation" in data
        assert "offense" in data["formation"]
        assert "defense" in data["formation"]
        assert len(data["formation"]["offense"]["players"]) > 0

    def test_get_broadcast_clips(self):
        response = self.client.get("/api/live/game/1/broadcast/101")
        assert response.status_code == 200
        data = response.json()
        assert data["play_id"] == 101
        assert "clips" in data
        assert data["total_duration"] > 0
        assert len(data["clips"]) > 0
        assert data["clips"][0]["clip_type"] == "formation_sweep"

    def test_update_camera_angle(self):
        payload = {"x": 10.0, "y": 20.0, "z": 30.0}
        response = self.client.post("/api/live/game/1/camera/client_test_1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["client_id"] == "client_test_1"
        assert data["angle"] == payload
