"""
Unit tests for Age-Based Growth Curves (RPG-003).

Tests position-specific peak ages, XP multipliers, and attribute regression.
"""

import pytest
from app.services.age_curves import (
    get_age_modifier,
    get_development_rate_modifier,
    get_physical_regression,
    calculate_attribute_regression,
    get_player_phase,
    get_phase_xp_multiplier,
    POSITION_CURVES,
)


class TestPositionCurves:
    """Test position-specific age curves."""

    def test_rb_peaks_early(self):
        """RBs should peak at 24-27 and have steep decline."""
        curve = POSITION_CURVES["RB"]
        peak_start, peak_end, decline_rate = curve

        assert peak_start == 24
        assert peak_end == 27
        assert decline_rate == 0.05  # Steep decline

    def test_qb_peaks_late(self):
        """QBs should peak at 27-32 with slow decline."""
        curve = POSITION_CURVES["QB"]
        peak_start, peak_end, decline_rate = curve

        assert peak_start == 27
        assert peak_end == 32
        assert decline_rate == 0.02  # Slow decline

    def test_kicker_longest_prime(self):
        """Kickers should have the longest prime window."""
        curve = POSITION_CURVES["K"]
        peak_start, peak_end, decline_rate = curve

        assert peak_start == 28
        assert peak_end == 38  # 10 year prime window
        assert decline_rate == 0.015


class TestPlayerPhase:
    """Test career phase determination."""

    def test_rb_ascension_phase(self):
        """Young RB (age 22) should be in Ascension."""
        phase = get_player_phase("RB", 22)
        assert phase == "ASCENSION"

    def test_rb_prime_phase(self):
        """RB age 25 should be in Prime."""
        phase = get_player_phase("RB", 25)
        assert phase == "PRIME"

    def test_rb_decline_phase(self):
        """RB age 28 should be in Decline."""
        phase = get_player_phase("RB", 28)
        assert phase == "DECLINE"

    def test_qb_still_prime_at_29(self):
        """QB age 29 should still be in Prime."""
        phase = get_player_phase("QB", 29)
        assert phase == "PRIME"

    def test_qb_decline_at_33(self):
        """QB age 33 should be in Decline (prime ends at 32)."""
        phase = get_player_phase("QB", 33)
        assert phase == "DECLINE"


class TestXPMultipliers:
    """Test XP/development rate multipliers."""

    def test_young_player_learns_faster(self):
        """21-24 year olds should get 1.2x learning rate."""
        mult = get_development_rate_modifier(22)
        assert mult == 1.2

    def test_prime_player_steady_growth(self):
        """25-27 year olds should get 1.0x learning rate."""
        mult = get_development_rate_modifier(26)
        assert mult == 1.0

    def test_veteran_slower_gains(self):
        """28-30 year olds should get 0.8x learning rate."""
        mult = get_development_rate_modifier(29)
        assert mult == 0.8

    def test_old_veteran_minimal_gains(self):
        """31+ year olds should get 0.5x learning rate."""
        mult = get_development_rate_modifier(35)
        assert mult == 0.5

    def test_phase_xp_multiplier_ascension(self):
        """Ascension phase should give bonus XP."""
        mult = get_phase_xp_multiplier("RB", 22)
        assert mult == 1.25

    def test_phase_xp_multiplier_decline(self):
        """Decline phase should reduce XP gains."""
        mult = get_phase_xp_multiplier("RB", 29)
        assert mult == 0.75


class TestAgeModifier:
    """Test overall age performance modifier."""

    def test_prime_player_full_modifier(self):
        """Player in prime should have 1.0 modifier."""
        mod = get_age_modifier(27, "QB")
        assert mod == 1.0

    def test_young_player_still_developing(self):
        """Young player should have < 1.0 performance modifier."""
        mod = get_age_modifier(21, "RB")
        assert 0.85 <= mod < 1.0

    def test_old_player_declining(self):
        """Older player past prime should have declining modifier."""
        mod = get_age_modifier(32, "RB")
        assert mod < 1.0


class TestPhysicalRegression:
    """Test physical attribute regression."""

    def test_no_regression_young_player(self):
        """Players under 29 should have no physical regression."""
        reg = get_physical_regression(26, "RB")
        assert reg == 1.0

    def test_rb_faster_regression(self):
        """RBs should regress faster after 29."""
        reg_rb = get_physical_regression(32, "RB")
        reg_qb = get_physical_regression(32, "QB")

        assert reg_rb < reg_qb  # RB regresses more


class TestAttributeRegression:
    """Test the calculate_attribute_regression function."""

    def test_no_regression_in_prime(self):
        """Players in prime should have no regression."""
        attrs = {"speed": 88, "awareness": 85}
        regression = calculate_attribute_regression(25, "RB", attrs)

        assert len(regression) == 0

    def test_regression_targets_speed_first(self):
        """For old players, speed should be most likely to regress."""
        attrs = {
            "speed": 88,
            "acceleration": 86,
            "awareness": 85,
        }

        # With rng_value=0.1 (low), high-weight attrs should regress
        regression = calculate_attribute_regression(32, "RB", attrs, rng_value=0.1)

        # Speed has weight 1.0, should definitely regress
        if regression:
            assert "speed" in regression or "acceleration" in regression

    def test_awareness_rarely_regresses(self):
        """Awareness should almost never regress (weight 0.05)."""
        attrs = {"awareness": 90}

        # Even with low rng, awareness rarely regresses
        regression = calculate_attribute_regression(32, "QB", attrs, rng_value=0.8)

        assert "awareness" not in regression

    def test_floor_prevents_over_regression(self):
        """Attributes at 40 or below should not regress further."""
        attrs = {"speed": 40}
        regression = calculate_attribute_regression(35, "RB", attrs, rng_value=0.01)

        assert "speed" not in regression


class TestDevelopmentTraitBonus:
    """Test development trait multipliers."""

    def test_xfactor_double_learning(self):
        """X-Factor players should get 2x learning rate."""
        mult = get_development_rate_modifier(25, "XFACTOR")
        assert mult == 2.0

    def test_superstar_bonus(self):
        """Superstar players should get 1.5x learning rate."""
        mult = get_development_rate_modifier(25, "SUPERSTAR")
        assert mult == 1.5

    def test_star_bonus(self):
        """Star players should get 1.25x learning rate."""
        mult = get_development_rate_modifier(25, "STAR")
        assert mult == 1.25
