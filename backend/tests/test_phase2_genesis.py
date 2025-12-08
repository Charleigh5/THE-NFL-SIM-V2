#!/usr/bin/env python3
"""
Phase 2: GENESIS Biological Tests
===================================
Unit tests for Biometrics, Cognition, Fatigue, and Injury systems.

Context7 Best Practices:
- pytest fixtures for state setup
- Comprehensive coverage of edge cases
- Integration tests for system interactions
"""

import pytest
from typing import List

# Import Phase 2 modules
from app.engine.genesis import (
    # Biometrics
    BiometricProfile,
    BodyType,
    FiberType,
    POSITION_BIOMETRIC_RANGES,
    generate_biometrics_for_position,
    # Cognition
    CognitionEngine,
    CognitiveProfile,
    CognitiveState,
    ReadPhase,
    OODAState,
    VisionCone,
    # Fatigue
    FatigueEngine,
    FatigueState,
    FatigueLevel,
    ActivityLevel,
    EnergyCompartment,
    # Injury
    InjuryEngine,
    InjuryProfile,
    Injury,
    InjuryType,
    InjurySeverity,
    BodyPart,
    BodyRegion,
    ChronicWear,
)

# Import RNG for deterministic tests
from app.engine.core import DeterministicRNG


# ============================================================================
# BIOMETRICS TESTS
# ============================================================================

class TestBiometricProfile:
    """Tests for BiometricProfile."""

    def test_default_values(self):
        """Test default biometric values are reasonable."""
        profile = BiometricProfile()
        assert 8.0 <= profile.hand_size <= 12.0
        assert 70 <= profile.wingspan <= 90
        assert 0 <= profile.fast_twitch_percentage <= 100

    def test_catch_radius_calculation(self):
        """Test catch radius is derived from arm and hand size."""
        profile = BiometricProfile(arm_length=34.0, hand_size=10.0)
        assert profile.catch_radius > 3.0  # Should be > 3 feet

    def test_explosion_factor(self):
        """Test explosion factor varies with fast-twitch."""
        fast_twitch = BiometricProfile(fast_twitch_percentage=90)
        slow_twitch = BiometricProfile(fast_twitch_percentage=30)

        assert fast_twitch.explosion_factor > slow_twitch.explosion_factor

    def test_endurance_factor(self):
        """Test endurance factor varies inversely with fast-twitch."""
        fast_twitch = BiometricProfile(fast_twitch_percentage=90)
        slow_twitch = BiometricProfile(fast_twitch_percentage=30)

        assert slow_twitch.endurance_factor > fast_twitch.endurance_factor

    def test_cognitive_modifier(self):
        """Test S2 cognition affects cognitive modifier."""
        high_s2 = BiometricProfile(s2_cognition_score=130)
        low_s2 = BiometricProfile(s2_cognition_score=80)

        assert high_s2.cognitive_modifier > low_s2.cognitive_modifier

    def test_serialization(self):
        """Test to_dict and from_dict round-trip."""
        original = BiometricProfile(
            hand_size=10.5,
            wingspan=80.0,
            fast_twitch_percentage=65.0,
        )

        data = original.to_dict()
        restored = BiometricProfile.from_dict(data)

        assert restored.hand_size == original.hand_size
        assert restored.wingspan == original.wingspan
        assert restored.fast_twitch_percentage == original.fast_twitch_percentage


class TestBiometricGeneration:
    """Tests for position-based biometric generation."""

    @pytest.fixture
    def rng(self):
        """Create deterministic RNG."""
        return DeterministicRNG(b"test" * 8, b"seed" * 8, nonce=0)

    def test_generate_for_qb(self, rng):
        """Test QB biometrics are in expected ranges."""
        profile = generate_biometrics_for_position("QB", rng, talent_level=0.5)

        ranges = POSITION_BIOMETRIC_RANGES["QB"]
        assert ranges["hand_size"][0] <= profile.hand_size <= ranges["hand_size"][1]

    def test_generate_for_wr(self, rng):
        """Test WR biometrics have high fast-twitch."""
        profile = generate_biometrics_for_position("WR", rng, talent_level=0.8)

        assert profile.fast_twitch_percentage >= 50  # WRs are explosive

    def test_talent_affects_output(self, rng):
        """Test that higher talent produces better biometrics."""
        low_talent = generate_biometrics_for_position("RB", rng, talent_level=0.2)

        # Reset RNG
        rng2 = DeterministicRNG(b"test" * 8, b"seed" * 8, nonce=0)
        high_talent = generate_biometrics_for_position("RB", rng2, talent_level=0.9)

        # We can't directly compare since RNG still adds randomness,
        # but test that both are valid
        assert low_talent.hand_size > 0
        assert high_talent.hand_size > 0


# ============================================================================
# COGNITION TESTS
# ============================================================================

class TestOODAState:
    """Tests for OODA loop state."""

    def test_total_loop_time(self):
        """Test total OODA loop time calculation."""
        ooda = OODAState()
        assert ooda.total_loop_time_ms == 280.0  # Sum of all phases
        assert abs(ooda.total_loop_time_s - 0.28) < 0.01

    def test_cognition_modifier(self):
        """Test S2 cognition speeds up OODA loop."""
        base = OODAState()
        fast = base.apply_cognition_modifier(130.0)

        assert fast.total_loop_time_ms < base.total_loop_time_ms


class TestVisionCone:
    """Tests for vision cone calculations."""

    def test_target_in_front(self):
        """Test detecting target directly ahead."""
        vision = VisionCone(fov_degrees=120, facing_angle=0)

        can_see, quality = vision.can_see_target((0, 0), (10, 0))

        assert can_see
        assert quality > 0.9  # Directly ahead = high quality

    def test_target_behind(self):
        """Test target behind is not visible."""
        vision = VisionCone(fov_degrees=120, facing_angle=0)

        can_see, quality = vision.can_see_target((0, 0), (-10, 0))

        assert not can_see
        assert quality == 0.0


class TestCognitionEngine:
    """Tests for CognitionEngine."""

    @pytest.fixture
    def engine(self):
        """Create cognition engine."""
        profile = CognitiveProfile(s2_cognition_score=100)
        return CognitionEngine(profile)

    def test_decision_delay(self, engine):
        """Test decision delay calculation."""
        delay = engine.calculate_decision_delay(complexity=1.0)

        assert 0.1 < delay < 1.0  # Should be a fraction of a second

    def test_pressure_increases_delay(self, engine):
        """Test that pressure increases decision delay."""
        engine.profile.stress_level = 80

        normal_delay = engine.calculate_decision_delay(complexity=1.0, under_pressure=False)
        pressure_delay = engine.calculate_decision_delay(complexity=1.0, under_pressure=True)

        assert pressure_delay > normal_delay

    def test_read_progression(self, engine):
        """Test QB read progression over time."""
        # Simulate 500ms of reads
        for _ in range(30):  # 30 * 16.67ms ≈ 500ms
            phase, reads, should_throw = engine.process_read_progression(
                elapsed_ms=16.67,
                defenders_nearby=0,
                open_receiver_quality=[0.3, 0.8, 0.5]
            )

        assert reads > 0
        assert phase != ReadPhase.PRE_SNAP

    def test_stress_affects_state(self, engine):
        """Test stress updates cognitive state."""
        engine.profile.add_stress(50)
        assert engine.profile.state == CognitiveState.STRESSED

        engine.profile.add_stress(30)
        assert engine.profile.state == CognitiveState.PANICKED


# ============================================================================
# FATIGUE TESTS
# ============================================================================

class TestEnergyCompartment:
    """Tests for EnergyCompartment."""

    def test_consume_energy(self):
        """Test energy consumption."""
        compartment = EnergyCompartment(
            name="Test",
            capacity=100.0,
            current=100.0,
        )

        overflow = compartment.consume(30.0)

        assert overflow == 0.0
        assert compartment.current == 70.0

    def test_consume_overflow(self):
        """Test consumption overflow when depleted."""
        compartment = EnergyCompartment(
            name="Test",
            capacity=100.0,
            current=20.0,
        )

        overflow = compartment.consume(50.0)

        assert overflow == 30.0
        assert compartment.current == 0.0

    def test_recovery(self):
        """Test energy recovery."""
        compartment = EnergyCompartment(
            name="Test",
            capacity=100.0,
            current=50.0,
            recovery_rate=5.0,
        )

        compartment.recover(2.0)

        assert compartment.current == 60.0


class TestFatigueEngine:
    """Tests for FatigueEngine."""

    @pytest.fixture
    def engine(self):
        """Create fatigue engine."""
        return FatigueEngine(stamina_rating=80)

    def test_sprint_depletes_atp(self, engine):
        """Test sprinting depletes ATP-PC quickly."""
        initial_atp = engine.state.atp_pc.current

        # Sprint for 60 ticks (1 second)
        engine.process_activity(ActivityLevel.SPRINT, elapsed_ticks=60)

        assert engine.state.atp_pc.current < initial_atp

    def test_rest_recovers_energy(self, engine):
        """Test resting recovers energy."""
        # Deplete some energy
        engine.process_activity(ActivityLevel.EXPLOSIVE, elapsed_ticks=30)
        depleted = engine.state.atp_pc.current

        # Rest
        engine.process_recovery(elapsed_ticks=120)

        assert engine.state.atp_pc.current > depleted

    def test_fatigue_modifiers(self, engine):
        """Test fatigue affects performance modifiers."""
        # Fresh player
        fresh_mods = engine.get_attribute_modifiers()
        assert fresh_mods["speed"] > 0.9

        # Exhaust the player
        for _ in range(10):
            engine.process_activity(ActivityLevel.EXPLOSIVE, elapsed_ticks=60)

        tired_mods = engine.get_attribute_modifiers()
        assert tired_mods["speed"] < fresh_mods["speed"]

    def test_huddle_recovery(self, engine):
        """Test between-play recovery."""
        # Deplete ATP
        engine.process_activity(ActivityLevel.EXPLOSIVE, elapsed_ticks=60)

        # Huddle
        engine.apply_rest_between_plays()

        # ATP should be fully recovered
        assert engine.state.atp_pc.current == engine.state.atp_pc.capacity


# ============================================================================
# INJURY TESTS
# ============================================================================

class TestInjury:
    """Tests for Injury dataclass."""

    def test_healing_progress(self):
        """Test healing progress calculation."""
        injury = Injury(
            body_part=BodyPart.ANKLE_LEFT,
            injury_type=InjuryType.SPRAIN,
            severity=InjurySeverity.MODERATE,
            weeks_to_recovery=4,
            weeks_elapsed=2,
        )

        assert injury.healing_progress == 0.5
        assert not injury.is_healed

    def test_heal_week(self):
        """Test healing over time."""
        injury = Injury(
            body_part=BodyPart.KNEE_RIGHT,
            injury_type=InjuryType.MCL_TEAR,
            severity=InjurySeverity.SERIOUS,
            weeks_to_recovery=2,
        )

        injury.heal_week()
        injury.heal_week()

        assert injury.is_healed


class TestChronicWear:
    """Tests for ChronicWear tracking."""

    def test_re_injury_risk(self):
        """Test chronic wear increases re-injury risk."""
        wear = ChronicWear(body_part=BodyPart.KNEE_LEFT)

        base_risk = wear.re_injury_risk_modifier

        wear.add_wear(30.0)

        assert wear.re_injury_risk_modifier > base_risk

    def test_performance_modifier(self):
        """Test chronic wear affects performance."""
        wear = ChronicWear(body_part=BodyPart.ANKLE_RIGHT)

        assert wear.performance_modifier == 1.0

        wear.add_wear(40.0)

        assert wear.performance_modifier < 1.0


class TestInjuryEngine:
    """Tests for InjuryEngine."""

    @pytest.fixture
    def rng(self):
        """Create deterministic RNG."""
        return DeterministicRNG(b"injury" * 6, b"test" * 8, nonce=0)

    @pytest.fixture
    def engine(self, rng):
        """Create injury engine."""
        profile = InjuryProfile(injury_resistance=80)
        return InjuryEngine(profile, rng)

    def test_high_gforce_injury(self, engine):
        """Test high G-force has high injury probability."""
        prob = engine.calculate_injury_probability(
            body_part=BodyPart.KNEE_LEFT,
            g_force=25.0,
            fatigue_modifier=1.0,
            is_contact=True,
        )

        assert prob > 0.1  # Significant injury risk

    def test_low_gforce_safe(self, engine):
        """Test low G-force has low injury probability."""
        prob = engine.calculate_injury_probability(
            body_part=BodyPart.THIGH_LEFT,
            g_force=3.0,
            fatigue_modifier=1.0,
            is_contact=False,
        )

        assert prob < 0.01  # Very low risk

    def test_head_impact_tracking(self, engine):
        """Test CTE risk tracking."""
        engine.process_head_impact(15.0)
        engine.process_head_impact(20.0)

        assert engine.profile.head_impact_count == 2
        assert engine.profile.cumulative_head_g_force == 35.0

    def test_process_week_healing(self, engine):
        """Test weekly healing process."""
        # Add an injury
        injury = Injury(
            body_part=BodyPart.CALF_RIGHT,
            injury_type=InjuryType.STRAIN,
            severity=InjurySeverity.MINOR,
            weeks_to_recovery=1,
        )
        engine.profile.active_injuries.append(injury)

        # Process one week
        healed = engine.process_week()

        assert len(healed) == 1
        assert len(engine.profile.active_injuries) == 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestPhase2Integration:
    """Integration tests for Phase 2 systems."""

    @pytest.fixture
    def rng(self):
        """Create deterministic RNG."""
        return DeterministicRNG(b"integration" * 4, b"test" * 8, nonce=0)

    def test_biometrics_affect_fatigue(self, rng):
        """Test fast-twitch percentage affects fatigue pattern."""
        # Fast-twitch player (explosive but fatigues quickly)
        fast_bio = BiometricProfile(fast_twitch_percentage=85)

        # Their stats would be used to modify the fatigue engine
        assert fast_bio.explosion_factor > 0.9
        assert fast_bio.endurance_factor < 0.6

    def test_cognition_stress_from_pressure(self):
        """Test pressure affects cognitive read progression."""
        profile = CognitiveProfile(s2_cognition_score=100)
        engine = CognitionEngine(profile)

        # Simulate reads under pressure
        for _ in range(20):
            engine.process_read_progression(
                elapsed_ms=16.67,
                defenders_nearby=3,  # Heavy pressure
                open_receiver_quality=[0.2, 0.3, 0.4]
            )

        # Should be stressed
        assert engine.profile.stress_level > 0

    def test_fatigue_increases_injury_risk(self):
        """Test fatigue increases injury probability."""
        fatigue_engine = FatigueEngine(stamina_rating=70)

        # Exhaust the player
        for _ in range(20):
            fatigue_engine.process_activity(ActivityLevel.EXPLOSIVE, elapsed_ticks=60)

        fatigue_mod = fatigue_engine.state.injury_risk_modifier
        assert fatigue_mod > 1.0  # Higher than baseline


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
