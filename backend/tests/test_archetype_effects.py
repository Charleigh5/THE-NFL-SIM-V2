"""
Tests for Archetype Effects System
===================================
Tests the NFL Identity Blueprint archetype classification and game impact cascades.
"""

from unittest.mock import MagicMock

from app.engine.archetype_effects import (
    ArchetypeClassifier,
    PlayerArchetype,
    get_archetype_modifiers,
)


class TestArchetypeClassification:
    """Test player archetype classification."""

    def test_field_general_classification(self):
        """QB with 90+ accuracy = Field General."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 92
        player.throw_accuracy_mid = 91

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.FIELD_GENERAL

    def test_field_general_requires_position(self):
        """Field General only for QBs."""
        player = MagicMock()
        player.position = "WR"
        player.throw_accuracy_short = 92
        player.throw_accuracy_mid = 91
        # Need to set these so Speed Merchant check doesn't fail on MagicMock comparisons
        player.speed = 70
        player.acceleration = 70
        player.strength = 70
        player.awareness = 70

        archetype = ArchetypeClassifier.classify(player)
        assert archetype != PlayerArchetype.FIELD_GENERAL

    def test_speed_merchant_classification(self):
        """Speed 90+ and Acceleration 88+ = Speed Merchant."""
        player = MagicMock()
        player.position = "WR"
        player.speed = 95
        player.acceleration = 92

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.SPEED_MERCHANT

    def test_trench_warlord_classification(self):
        """High strength and awareness = Trench Warlord."""
        player = MagicMock()
        player.position = "OT"
        player.strength = 90
        player.awareness = 85
        # Set other attributes to low values so it doesn't match Speed Merchant first
        player.speed = 70
        player.acceleration = 70
        player.throw_accuracy_short = 0
        player.throw_accuracy_mid = 0

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.TRENCH_WARLORD

    def test_standard_fallback(self):
        """Players not meeting thresholds = Standard."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 80
        player.throw_accuracy_mid = 78
        player.speed = 70
        player.acceleration = 70
        player.strength = 60
        player.awareness = 60

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.STANDARD


class TestArchetypeEffects:
    """Test archetype effect application."""

    def test_field_general_3rd_down_boost(self):
        """Field General gets +20% on 3rd down."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 92
        player.throw_accuracy_mid = 91
        player.last_name = "Manning"

        context = {"down": 3}

        mods = get_archetype_modifiers(player, context)

        assert mods["archetype"] == "Field General"
        assert mods["conversion_modifier"] == 1.20
        assert mods["has_audible"] is True

    def test_field_general_no_boost_on_other_downs(self):
        """Field General boost only on 3rd down."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 92
        player.throw_accuracy_mid = 91

        context = {"down": 1}

        mods = get_archetype_modifiers(player, context)

        assert mods["archetype"] == "Field General"
        assert mods["conversion_modifier"] == 1.0  # No boost

    def test_speed_merchant_breakaway_boost(self):
        """Speed Merchant gets +25% breakaway chance."""
        player = MagicMock()
        player.position = "WR"
        player.speed = 95
        player.acceleration = 92
        player.last_name = "Hill"

        context = {}

        mods = get_archetype_modifiers(player, context)

        assert mods["archetype"] == "Speed Merchant"
        assert mods["breakaway_modifier"] == 1.25

    def test_effects_contain_narrative(self):
        """Effects should include narrative when triggered."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 92
        player.throw_accuracy_mid = 91
        player.last_name = "Brady"

        context = {"down": 3}

        mods = get_archetype_modifiers(player, context)

        assert mods["narrative"] is not None
        assert "Brady" in mods["narrative"]
