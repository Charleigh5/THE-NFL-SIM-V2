import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from app.models.game import GameType
from app.engine.venue_effects import VenueEffects, get_thanksgiving_atmosphere
from app.data.special_jerseys import (
    get_thanksgiving_jersey,
    is_thanksgiving_host,
    get_thanksgiving_boost,
    THANKSGIVING_JERSEYS,
    THANKSGIVING_HOSTS
)

class TestThanksgivingFeatures:
    """Test suite for Thanksgiving Day game features."""

    def test_game_type_enum(self):
        """Test GameType enum values."""
        assert GameType.REGULAR.value == "REGULAR"
        assert GameType.THANKSGIVING.value == "THANKSGIVING"
        assert GameType.PLAYOFF.value == "PLAYOFF"
        assert GameType.SUPER_BOWL.value == "SUPER_BOWL"

    def test_thanksgiving_hosts_identified(self):
        """Test that Lions and Cowboys are identified as hosts."""
        assert is_thanksgiving_host("DET")
        assert is_thanksgiving_host("DAL")
        assert not is_thanksgiving_host("KC")
        assert not is_thanksgiving_host("NE")

    def test_thanksgiving_jersey_data(self):
        """Test that jersey data exists for traditional hosts."""
        lions_jersey = get_thanksgiving_jersey("DET")
        assert lions_jersey is not None
        assert lions_jersey["name"] == "Lions 1950s Throwback"
        assert lions_jersey["jersey"]["color"] == "Honolulu Blue"

        cowboys_jersey = get_thanksgiving_jersey("DAL")
        assert cowboys_jersey is not None
        assert "Double-Star" in cowboys_jersey["name"]

    def test_thanksgiving_boost(self):
        """Test extra home-field boost for hosts."""
        assert get_thanksgiving_boost("DET") == 0.05
        assert get_thanksgiving_boost("DAL") == 0.05
        assert get_thanksgiving_boost("GB") == 0.0

    def test_venue_effects_thanksgiving(self):
        """Test VenueEffects for Thanksgiving games."""
        # Lions Thanksgiving game
        effects = VenueEffects("DET", "THANKSGIVING")
        modifiers = effects.get_all_modifiers()

        # Should have base + Thanksgiving boost
        assert modifiers["home_field_boost"] >= 0.08  # 0.03 base + 0.05 Thanksgiving
        assert modifiers["crowd_energy"] == 1.2
        assert modifiers["is_thanksgiving"] is True
        assert modifiers["is_traditional_host"] is True

    def test_venue_effects_regular(self):
        """Test VenueEffects for regular games."""
        effects = VenueEffects("KC", "REGULAR")
        modifiers = effects.get_all_modifiers()

        assert modifiers["home_field_boost"] == 0.03
        assert modifiers["crowd_energy"] == 1.0
        assert modifiers["is_thanksgiving"] is False

    def test_thanksgiving_atmosphere(self):
        """Test full Thanksgiving atmosphere settings."""
        atmosphere = get_thanksgiving_atmosphere("DAL")

        assert atmosphere["madden_celebration"] is True
        assert atmosphere["turkey_leg_award"] is True
        assert atmosphere["tradition_started"] == 1966
        assert atmosphere["game_slot"] == "late_afternoon"
