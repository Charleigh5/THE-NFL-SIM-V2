"""
Unit tests for The Closer trait (Phase 11: True-to-Life RPG).
Tests crunch time activation and pressure/fatigue immunity effects.
"""
from app.services.trait_service import TRAIT_CATALOG, TraitService


class TestTheCloserTrait:
    """Test suite for The Closer trait mechanics."""

    def test_the_closer_exists_in_catalog(self):
        """Verify The Closer trait is properly defined in TRAIT_CATALOG."""
        trait = TRAIT_CATALOG.get("the_closer")
        assert trait is not None
        assert trait.name == "The Closer"
        assert "CRUNCH_TIME" in trait.activation_triggers
        assert trait.effects.get("pressure_immunity") == 1.0
        assert trait.effects.get("fatigue_override") == 1.0
        assert trait.tier == "ELITE"

    def test_crunch_time_4th_quarter_close_game(self):
        """Test crunch time activates in 4th quarter with <5 min and close score."""
        context = {
            "quarter": 4,
            "time_remaining": 180,  # 3 minutes remaining
            "score_differential": 7,  # Down by 7
        }
        assert TraitService.check_crunch_time(context) is True

    def test_crunch_time_not_active_early_game(self):
        """Test crunch time does NOT activate in 1st quarter."""
        context = {
            "quarter": 1,
            "time_remaining": 600,
            "score_differential": 3,
        }
        assert TraitService.check_crunch_time(context) is False

    def test_crunch_time_not_active_blowout(self):
        """Test crunch time does NOT activate when score differential > 8."""
        context = {
            "quarter": 4,
            "time_remaining": 120,  # 2 minutes
            "score_differential": 21,  # Blowout
        }
        assert TraitService.check_crunch_time(context) is False

    def test_crunch_time_not_active_too_much_time(self):
        """Test crunch time does NOT activate with >5 min remaining."""
        context = {
            "quarter": 4,
            "time_remaining": 600,  # 10 minutes
            "score_differential": 3,
        }
        assert TraitService.check_crunch_time(context) is False

    def test_crunch_time_overtime_always_active(self):
        """Test crunch time ALWAYS activates in overtime regardless of score."""
        context = {
            "quarter": 5,  # OT
            "time_remaining": 900,  # Full OT period
            "score_differential": 0,  # Tied (irrelevant for OT)
        }
        assert TraitService.check_crunch_time(context) is True

    def test_trait_activation_with_crunch_time(self):
        """Test The Closer trait activates during crunch time."""
        trait = TRAIT_CATALOG.get("the_closer")
        context = {
            "quarter": 4,
            "time_remaining": 120,
            "score_differential": 6,
        }
        assert TraitService.check_trait_activation(trait, context) is True

    def test_trait_does_not_activate_outside_crunch_time(self):
        """Test The Closer trait does NOT activate outside crunch time."""
        trait = TRAIT_CATALOG.get("the_closer")
        context = {
            "quarter": 2,
            "time_remaining": 300,
            "score_differential": 3,
        }
        assert TraitService.check_trait_activation(trait, context) is False

    def test_crunch_time_edge_case_exactly_5_minutes(self):
        """Test boundary condition: exactly 5 minutes (300 seconds) is included."""
        context = {
            "quarter": 4,
            "time_remaining": 300,  # Exactly 5 min
            "score_differential": 7,
        }
        assert TraitService.check_crunch_time(context) is True

    def test_crunch_time_edge_case_exactly_8_points(self):
        """Test boundary condition: exactly 8 point differential is included."""
        context = {
            "quarter": 4,
            "time_remaining": 180,
            "score_differential": 8,  # Exactly 8
        }
        assert TraitService.check_crunch_time(context) is True

    def test_crunch_time_edge_case_9_points_excluded(self):
        """Test boundary condition: 9 point differential is excluded."""
        context = {
            "quarter": 4,
            "time_remaining": 180,
            "score_differential": 9,  # 9 points
        }
        assert TraitService.check_crunch_time(context) is False
