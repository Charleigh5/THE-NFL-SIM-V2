"""
Test Age-Based Progression with Archetype Curves
=================================================

Unit tests for RPG-003 Age-Based Growth Curves with Position Archetypes.
Tests verify that Speed-dependent archetypes decline faster than Technique archetypes.
"""
import pytest
from app.services.age_curves import (
    PlayerArchetype,
    get_player_archetype,
    get_player_phase,
    get_phase_xp_multiplier,
    get_archetype_curve,
    ARCHETYPE_CURVES,
    POSITION_CURVES,
)


# =============================================================================
# ARCHETYPE DETECTION TESTS
# =============================================================================

class TestArchetypeDetection:
    """Tests for get_player_archetype function."""

    def test_qb_scrambler_high_speed(self):
        """QB with speed > 80 should be classified as Scrambler."""
        archetype = get_player_archetype("QB", {"speed": 85})
        assert archetype == PlayerArchetype.SCRAMBLER

    def test_qb_pocket_low_speed(self):
        """QB with speed <= 80 should be classified as Pocket."""
        archetype = get_player_archetype("QB", {"speed": 75})
        assert archetype == PlayerArchetype.POCKET

    def test_rb_speed_back(self):
        """RB with speed > 90 should be Speed Back."""
        archetype = get_player_archetype("RB", {"speed": 92, "trucking": 70})
        assert archetype == PlayerArchetype.SPEED_BACK

    def test_rb_power_back(self):
        """RB with trucking > 85 (and speed < 90) should be Power Back."""
        archetype = get_player_archetype("RB", {"speed": 85, "trucking": 88})
        assert archetype == PlayerArchetype.POWER_BACK

    def test_wr_deep_threat(self):
        """WR with speed > 93 should be Deep Threat."""
        archetype = get_player_archetype("WR", {"speed": 95, "route_running": 80})
        assert archetype == PlayerArchetype.DEEP_THREAT

    def test_wr_possession(self):
        """WR with route running > 85 (and speed < 93) should be Possession."""
        archetype = get_player_archetype("WR", {"speed": 88, "route_running": 90})
        assert archetype == PlayerArchetype.POSSESSION

    def test_cb_always_man_corner(self):
        """CB should always be classified as Man Corner (speed-dependent)."""
        archetype = get_player_archetype("CB", {"speed": 70})
        assert archetype == PlayerArchetype.MAN_CORNER

    def test_safety_zone_coverage(self):
        """Safety with zone > 85 should be Zone Safety."""
        archetype = get_player_archetype("S", {"zone_coverage": 88})
        assert archetype == PlayerArchetype.ZONE_SAFETY

    def test_lb_coverage(self):
        """LB with speed > 85 should be Coverage LB."""
        archetype = get_player_archetype("LB", {"speed": 87, "hit_power": 70})
        assert archetype == PlayerArchetype.COVERAGE_LB

    def test_lb_thumper(self):
        """LB with hit power > 85 (and speed < 85) should be Thumper."""
        archetype = get_player_archetype("LB", {"speed": 80, "hit_power": 88})
        assert archetype == PlayerArchetype.THUMPER_LB


# =============================================================================
# AGE PHASE TESTS
# =============================================================================

class TestAgePhases:
    """Tests for get_player_phase with archetypes."""

    def test_scrambler_prime_ends_at_29(self):
        """Scrambler QB should hit DECLINE at age 30."""
        phase = get_player_phase("QB", 30, PlayerArchetype.SCRAMBLER)
        assert phase == "DECLINE"

    def test_pocket_prime_until_34(self):
        """Pocket QB should still be in PRIME at age 34."""
        phase = get_player_phase("QB", 34, PlayerArchetype.POCKET)
        assert phase == "PRIME"

    def test_pocket_decline_at_35(self):
        """Pocket QB should hit DECLINE at age 35."""
        phase = get_player_phase("QB", 35, PlayerArchetype.POCKET)
        assert phase == "DECLINE"

    def test_speed_back_decline_at_27(self):
        """Speed Back RB should hit DECLINE at age 27."""
        phase = get_player_phase("RB", 27, PlayerArchetype.SPEED_BACK)
        assert phase == "DECLINE"

    def test_power_back_prime_until_29(self):
        """Power Back RB should still be in PRIME at age 29."""
        phase = get_player_phase("RB", 29, PlayerArchetype.POWER_BACK)
        assert phase == "PRIME"

    def test_zone_safety_prime_until_33(self):
        """Zone Safety should still be in PRIME at age 33."""
        phase = get_player_phase("S", 33, PlayerArchetype.ZONE_SAFETY)
        assert phase == "PRIME"


# =============================================================================
# XP MULTIPLIER TESTS
# =============================================================================

class TestXPMultipliers:
    """Tests for get_phase_xp_multiplier."""

    def test_young_player_ascension_bonus(self):
        """Young player in ASCENSION should get 1.25x XP."""
        multiplier = get_phase_xp_multiplier("RB", 22)
        assert multiplier == 1.25

    def test_prime_player_baseline(self):
        """Player in PRIME should get 1.0x XP."""
        multiplier = get_phase_xp_multiplier("WR", 27)
        assert multiplier == 1.0

    def test_decline_player_reduced(self):
        """Player in DECLINE should get 0.75x XP."""
        # CB hits decline at 29
        multiplier = get_phase_xp_multiplier("CB", 30)
        assert multiplier == 0.75


# =============================================================================
# ARCHETYPE CURVE TESTS
# =============================================================================

class TestArchetypeCurves:
    """Tests for get_archetype_curve."""

    def test_scrambler_curve_values(self):
        """Scrambler curve should be (25, 29, 0.04)."""
        curve = get_archetype_curve("QB", PlayerArchetype.SCRAMBLER)
        assert curve == (25, 29, 0.04)

    def test_pocket_curve_values(self):
        """Pocket curve should be (28, 34, 0.015)."""
        curve = get_archetype_curve("QB", PlayerArchetype.POCKET)
        assert curve == (28, 34, 0.015)

    def test_default_fallback(self):
        """Unknown archetype should fall back to position default."""
        curve = get_archetype_curve("OT", None)
        assert curve == POSITION_CURVES["OT"]

    def test_speed_back_severe_decline(self):
        """Speed Back should have highest decline rate (0.06)."""
        curve = get_archetype_curve("RB", PlayerArchetype.SPEED_BACK)
        assert curve[2] == 0.06  # decline_rate
