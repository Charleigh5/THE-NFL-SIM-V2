"""
Tests for Archetype Effects System
===================================
Tests the harmonized 7 canonical player archetypes and game impact cascades.
"""

import pytest
from unittest.mock import MagicMock
from app.engine.archetype_effects import (
    PlayerArchetype,
    ArchetypeClassifier,
    ArchetypeEffectApplicator,
    get_archetype_modifiers,
    ARCHETYPE_EFFECTS
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

    def test_sorcerer_classification(self):
        """QB with 90+ throw power and 88+ deep accuracy = Sorcerer."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 80
        player.throw_accuracy_mid = 80
        player.throw_power = 95
        player.throw_accuracy_deep = 90

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.SORCERER

    def test_alpha_dog_classification(self):
        """CB/WR with 88+ press and man coverage = Alpha Dog."""
        player = MagicMock()
        player.position = "CB"
        player.press = 92
        player.man_coverage = 90

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.ALPHA_DOG

    def test_weapon_classification(self):
        """Speed 90+ and Acceleration 88+ = Weapon."""
        player = MagicMock()
        player.position = "WR"
        player.speed = 95
        player.acceleration = 92

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.WEAPON

    def test_freak_classification(self):
        """EDGE/LB with 85+ strength and 80+ tackle = Freak."""
        player = MagicMock()
        player.position = "EDGE"
        player.strength = 88
        player.tackle = 84
        player.speed = 75
        player.acceleration = 75

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.FREAK

    def test_technician_classification(self):
        """High strength and awareness = Technician."""
        player = MagicMock()
        player.position = "OT"
        player.strength = 90
        player.awareness = 85
        player.speed = 70
        player.acceleration = 70
        player.tackle = 50

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.TECHNICIAN

    def test_workhorse_classification(self):
        """RB with 85+ stamina and carrying = Workhorse."""
        player = MagicMock()
        player.position = "RB"
        player.stamina = 90
        player.carrying = 88
        player.speed = 80
        player.acceleration = 80

        archetype = ArchetypeClassifier.classify(player)
        assert archetype == PlayerArchetype.WORKHORSE

    def test_field_general_requires_position(self):
        """Field General only for QBs."""
        player = MagicMock()
        player.position = "WR"
        player.throw_accuracy_short = 92
        player.throw_accuracy_mid = 91
        player.speed = 70
        player.acceleration = 70
        player.strength = 70
        player.awareness = 70
        player.press = 70
        player.man_coverage = 70

        archetype = ArchetypeClassifier.classify(player)
        assert archetype != PlayerArchetype.FIELD_GENERAL

    def test_standard_fallback(self):
        """Players not meeting thresholds = Standard."""
        player = MagicMock()
        player.position = "QB"
        player.throw_accuracy_short = 80
        player.throw_accuracy_mid = 78
        player.throw_power = 80
        player.throw_accuracy_deep = 80
        player.speed = 70
        player.acceleration = 70
        player.strength = 60
        player.awareness = 60
        player.press = 50
        player.man_coverage = 50
        player.tackle = 50

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

    def test_weapon_breakaway_boost(self):
        """Weapon gets +25% breakaway chance."""
        player = MagicMock()
        player.position = "WR"
        player.speed = 95
        player.acceleration = 92
        player.last_name = "Hill"

        context = {}

        mods = get_archetype_modifiers(player, context)

        assert mods["archetype"] in ["Weapon", "Speed Merchant"]
        assert mods["breakaway_modifier"] == 1.25

    def test_technician_run_boost(self):
        """Technician gets +10% conversion boost on run plays."""
        player = MagicMock()
        player.position = "OT"
        player.strength = 90
        player.awareness = 85
        player.speed = 70
        player.acceleration = 70
        player.tackle = 50

        context = {"play_type": "run"}

        mods = get_archetype_modifiers(player, context)

        assert mods["archetype"] == "Technician"
        assert mods["conversion_modifier"] == 1.10
        assert mods["intimidation"] == 1.3

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
