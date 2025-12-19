#!/usr/bin/env python3
"""
Test Suite for Enhanced Combine with GENESIS Integration (B-045)
================================================================
Tests for Phase 2 combine modernization and biometric reveals.
"""

import pytest
from app.services.scouting.combine import (
    CombineResults,
    CombineSimulation,
    GenesisRevealData,
)
from app.engine.genesis.biometrics import BiometricProfile, generate_biometrics_for_position


class TestCombineResultsModernization:
    """Tests for B-037 to B-040: Modernized combine metrics."""

    def test_combine_results_no_bench_reps(self):
        """B-037: Verify bench_reps field is removed."""
        result = CombineResults(
            forty_yard=4.45,
            vertical_jump=36.0,
            broad_jump=120,
            three_cone=7.0,
            shuttle=4.2,
        )
        assert not hasattr(result, 'bench_reps') or 'bench_reps' not in result.__dict__

    def test_combine_results_has_power_clean(self):
        """B-038: Verify power_clean_max field exists."""
        result = CombineResults(
            forty_yard=4.45,
            vertical_jump=36.0,
            broad_jump=120,
            three_cone=7.0,
            shuttle=4.2,
            power_clean_max=315,
        )
        assert result.power_clean_max == 315

    def test_combine_results_has_gps_speed(self):
        """B-039: Verify gps_tracked_speed field exists."""
        result = CombineResults(
            forty_yard=4.45,
            vertical_jump=36.0,
            broad_jump=120,
            three_cone=7.0,
            shuttle=4.2,
            gps_tracked_speed=21.5,
        )
        assert result.gps_tracked_speed == 21.5

    def test_combine_results_has_position_agility(self):
        """B-040: Verify position_agility_score field exists."""
        result = CombineResults(
            forty_yard=4.45,
            vertical_jump=36.0,
            broad_jump=120,
            three_cone=7.0,
            shuttle=4.2,
            position_agility_score=85.5,
        )
        assert result.position_agility_score == 85.5

    def test_combine_results_has_medical_flags(self):
        """B-044: Verify medical_flags field exists."""
        result = CombineResults(
            forty_yard=4.45,
            vertical_jump=36.0,
            broad_jump=120,
            three_cone=7.0,
            shuttle=4.2,
            medical_flags=["ELEVATED_BODY_FAT"],
        )
        assert "ELEVATED_BODY_FAT" in result.medical_flags


class TestCombineSimulationModern:
    """Tests for modernized CombineSimulation.run_combine()."""

    def test_run_combine_generates_modern_metrics(self):
        """Verify run_combine generates all modern metrics."""
        sim = CombineSimulation()
        attributes = {"speed": 85, "strength": 75, "agility": 80, "acceleration": 82, "jumping": 78}

        result = sim.run_combine(attributes, "WR")

        # Modern metrics should be populated
        assert result.power_clean_max >= 135  # Minimum value
        assert result.gps_tracked_speed >= 14.0  # Minimum value
        assert 0 <= result.position_agility_score <= 100  # Clamped range

    def test_run_combine_speed_rating_affects_gps(self):
        """Higher speed rating should produce faster GPS speed."""
        sim = CombineSimulation()

        slow_attrs = {"speed": 50, "strength": 50, "agility": 50, "acceleration": 50, "jumping": 50}
        fast_attrs = {"speed": 99, "strength": 50, "agility": 50, "acceleration": 50, "jumping": 50}

        # Run multiple times and average to account for variance
        slow_speeds = [sim.run_combine(slow_attrs, "WR").gps_tracked_speed for _ in range(10)]
        fast_speeds = [sim.run_combine(fast_attrs, "WR").gps_tracked_speed for _ in range(10)]

        assert sum(fast_speeds) / 10 > sum(slow_speeds) / 10

    def test_run_combine_strength_affects_power_clean(self):
        """Higher strength rating should produce higher power clean."""
        sim = CombineSimulation()

        weak_attrs = {"speed": 50, "strength": 40, "agility": 50, "acceleration": 50, "jumping": 50}
        strong_attrs = {"speed": 50, "strength": 95, "agility": 50, "acceleration": 50, "jumping": 50}

        # Run multiple times and average
        weak_cleans = [sim.run_combine(weak_attrs, "DL").power_clean_max for _ in range(10)]
        strong_cleans = [sim.run_combine(strong_attrs, "DL").power_clean_max for _ in range(10)]

        assert sum(strong_cleans) / 10 > sum(weak_cleans) / 10


class TestGenesisRevealData:
    """Tests for B-041 to B-043: GENESIS biometric reveal at combine."""

    def test_genesis_reveal_data_from_profile(self):
        """B-041: Test creating reveal data from BiometricProfile."""
        profile = BiometricProfile(
            hand_size=10.0,
            wingspan=80.0,
            arm_length=34.0,
            s2_cognition_score=115.0,
            fast_twitch_percentage=70.0,
            reaction_time_ms=220.0,
            body_fat_percentage=10.0,
        )

        reveal = GenesisRevealData.from_biometric_profile(profile)

        assert reveal.hand_size == 10.0
        assert reveal.wingspan == 80.0
        assert reveal.s2_cognition_score == 115.0

    def test_genesis_reveal_hides_s2_when_requested(self):
        """B-043: S2 cognition can be hidden in reveal data."""
        profile = BiometricProfile(s2_cognition_score=125.0)

        reveal_hidden = GenesisRevealData.from_biometric_profile(profile, include_hidden=False)
        reveal_shown = GenesisRevealData.from_biometric_profile(profile, include_hidden=True)

        assert reveal_hidden.s2_cognition_score == 0.0
        assert reveal_shown.s2_cognition_score == 125.0


class TestCombineSimulationGenesisIntegration:
    """Tests for B-041 to B-044: CombineSimulation GENESIS integration."""

    def test_reveal_genesis_data_returns_data(self):
        """B-041: reveal_genesis_data returns GenesisRevealData."""
        sim = CombineSimulation()

        reveal = sim.reveal_genesis_data(player_id=1, position="QB")

        assert isinstance(reveal, GenesisRevealData)
        assert reveal.hand_size > 0
        assert reveal.wingspan > 0

    def test_reveal_genesis_data_includes_s2(self):
        """B-043: Reveal includes S2 cognition score."""
        sim = CombineSimulation()

        reveal = sim.reveal_genesis_data(player_id=2, position="QB")

        # QBs typically have higher S2 scores
        assert reveal.s2_cognition_score >= 85.0

    def test_reveal_genesis_data_caches_profile(self):
        """Biometric profile is cached for same player_id."""
        sim = CombineSimulation()

        reveal1 = sim.reveal_genesis_data(player_id=100, position="WR")
        reveal2 = sim.reveal_genesis_data(player_id=100, position="WR")

        # Same player should have same data
        assert reveal1.hand_size == reveal2.hand_size
        assert reveal1.s2_cognition_score == reveal2.s2_cognition_score

    def test_reveal_uses_provided_profile(self):
        """Can provide explicit BiometricProfile."""
        sim = CombineSimulation()
        custom_profile = BiometricProfile(
            hand_size=11.5,
            wingspan=85.0,
            s2_cognition_score=140.0,
        )

        reveal = sim.reveal_genesis_data(
            player_id=999,
            position="OT",
            biometric_profile=custom_profile
        )

        assert reveal.hand_size == 11.5
        assert reveal.s2_cognition_score == 140.0


class TestMedicalFlagsScreening:
    """Tests for B-044: Medical flags screening system."""

    def test_elevated_body_fat_flag(self):
        """High body fat triggers flag."""
        sim = CombineSimulation()
        profile = BiometricProfile(body_fat_percentage=22.0)

        flags = sim._screen_medical_flags(profile)

        assert "ELEVATED_BODY_FAT" in flags

    def test_low_body_fat_flag(self):
        """Very low body fat triggers flag."""
        sim = CombineSimulation()
        profile = BiometricProfile(body_fat_percentage=5.0)

        flags = sim._screen_medical_flags(profile)

        assert "LOW_BODY_FAT_RISK" in flags

    def test_cardiovascular_flags(self):
        """Poor cardiovascular metrics trigger flags."""
        sim = CombineSimulation()
        profile = BiometricProfile(
            resting_heart_rate=80.0,
            vo2_max=38.0,
            hrv_score=50.0,
        )

        flags = sim._screen_medical_flags(profile)

        assert "ELEVATED_RHR" in flags
        assert "LOW_AEROBIC_CAPACITY" in flags
        assert "LOW_HRV_RECOVERY" in flags

    def test_heat_sensitivity_flag(self):
        """Low heat tolerance triggers flag."""
        sim = CombineSimulation()
        profile = BiometricProfile(heat_tolerance=30.0)

        flags = sim._screen_medical_flags(profile)

        assert "HEAT_SENSITIVITY" in flags

    def test_cognitive_flags(self):
        """Low cognitive scores trigger flags."""
        sim = CombineSimulation()
        profile = BiometricProfile(
            s2_cognition_score=80.0,
            reaction_time_ms=300.0,
        )

        flags = sim._screen_medical_flags(profile)

        assert "COGNITIVE_PROCESSING_CONCERN" in flags
        assert "SLOW_REACTION_TIME" in flags

    def test_healthy_profile_no_flags(self):
        """Healthy profile should have no flags."""
        sim = CombineSimulation()
        profile = BiometricProfile(
            body_fat_percentage=12.0,
            resting_heart_rate=55.0,
            vo2_max=55.0,
            hrv_score=75.0,
            heat_tolerance=60.0,
            sweat_rate=1.5,
            s2_cognition_score=110.0,
            reaction_time_ms=220.0,
        )

        flags = sim._screen_medical_flags(profile)

        assert len(flags) == 0
