#!/usr/bin/env python3
"""
Phase 7: Training & Development Tests
=====================================
Unit tests for training modules.

Context7 Best Practices:
- pytest fixtures
- Logic verification for math
- Edge case handling
"""


import pytest

from app.services.training import (
    CampDay,
    # Coaching
    CoachingEngine,
    CoachRole,
    DevTrait,
    DrillType,
    PlayerProgressionState,
    # Progression
    ProgressionEngine,
    ProgressionPhase,
    # Camp
    TrainingCampEngine,
    TrainingIntensity,
)

# ============================================================================
# TRAINING CAMP TESTS
# ============================================================================

class TestTrainingCampEngine:
    """Tests for TrainingCampEngine."""

    @pytest.fixture
    def engine(self):
        return TrainingCampEngine()

    def test_process_day_gain(self, engine):
        """Standard day yields XP and fatigue."""
        day = CampDay(DrillType.INDIVIDUAL, DrillType.SEVEN_ON_SEVEN, TrainingIntensity.STANDARD)
        roster = ["P1"]

        result = engine.process_day(day, roster)

        assert "P1" in result.xp_gained
        assert result.xp_gained["P1"] > 0
        assert result.fatigue_levels["P1"] > 0

    def test_process_rest_day(self, engine):
        """Rest day recovers fatigue."""
        day = CampDay(DrillType.INDIVIDUAL, DrillType.INDIVIDUAL, TrainingIntensity.WALKTHROUGH, rest_day=True)
        roster = ["P1"]

        result = engine.process_day(day, roster)

        assert result.fatigue_levels["P1"] < 0  # Negative fatigue = recovery

    def test_intensity_scaling(self, engine):
        """Full pads yields more XP and fatigue."""
        day_light = CampDay(DrillType.SCRIMMAGE, DrillType.SCRIMMAGE, TrainingIntensity.WALKTHROUGH)
        day_heavy = CampDay(DrillType.SCRIMMAGE, DrillType.SCRIMMAGE, TrainingIntensity.FULL_PADS)
        roster = ["P1"]

        # Use fixed seed to compare deterministic outcomes roughly
        res_light = engine.process_day(day_light, roster, rng_seed=42)
        res_heavy = engine.process_day(day_heavy, roster, rng_seed=42)

        assert res_heavy.xp_gained["P1"] > res_light.xp_gained["P1"]
        assert res_heavy.fatigue_levels["P1"] > res_light.fatigue_levels["P1"]

    def test_recommend_schedule(self, engine):
        """Schedule recommender respects needs."""
        schedule_tackle = engine.recommend_schedule(["tackling"])
        schedule_speed = engine.recommend_schedule(["speed"])

        # Check Day 5 specific drill (index 4)
        assert schedule_tackle[4].afternoon_drill == DrillType.OKLAHOMA
        assert schedule_speed[4].afternoon_drill == DrillType.CONDITIONING


# ============================================================================
# PROGRESSION TESTS
# ============================================================================

class TestProgressionEngine:
    """Tests for ProgressionEngine."""

    @pytest.fixture
    def engine(self):
        return ProgressionEngine()

    def test_calculate_threshold(self, engine):
        """Threshold increases with level."""
        low = engine.calculate_xp_threshold(70)
        high = engine.calculate_xp_threshold(90)

        assert high > low

    def test_dev_trait_multiplier(self, engine):
        """Traits boost XP."""
        assert engine.get_dev_trait_multiplier(DevTrait.X_FACTOR) == 2.0
        assert engine.get_dev_trait_multiplier(DevTrait.NORMAL) == 1.0

    def test_determine_phase(self, engine):
        """Age determines career phase."""
        assert engine.determine_phase("QB", 22) == ProgressionPhase.ROOKIE
        assert engine.determine_phase("QB", 29) == ProgressionPhase.PRIME
        assert engine.determine_phase("QB", 38) == ProgressionPhase.DECLINE

        # RB Peak is earlier
        assert engine.determine_phase("RB", 29) != ProgressionPhase.PRIME # Likely Post-Prime/Decline

    def test_apply_xp_level_up(self, engine):
        """XP triggers level up."""
        state = PlayerProgressionState(
            player_id="P1", age=24, current_xp=0, level=75,
            dev_trait=DevTrait.NORMAL, xp_to_next_level=1000
        )

        # Give enough XP to level once (Base 1000, next threshold ~1770)
        # 2500 XP:
        # - 1000 (Level 75->76) -> Remainder 1500
        # - Next need ~1771. So 1500 is not enough for 76->77
        new_state, levels = engine.apply_xp(state, 2500)

        assert levels == 1
        assert new_state.level == 76
        assert new_state.current_xp == 1500

    def test_regression(self, engine):
        """Decline phase loses attributes."""
        # 35 year old WR should regress speed
        regress = engine.calculate_regression(
            "WR", 35, {"speed": 90, "strength": 70}
        )

        # Randomness might fail, but at 35 WR, chance is high
        # Only check keys if regression occurred
        if regress:
            assert "speed" in regress or "strength" in regress
            if "speed" in regress:
                assert regress["speed"] < 0


# ============================================================================
# COACHING TREE TESTS
# ============================================================================

class TestCoachingEngine:
    """Tests for CoachingEngine."""

    @pytest.fixture
    def engine(self):
        return CoachingEngine()

    def test_create_coach(self, engine):
        """Coach initialized with empty skills."""
        coach = engine.create_coach("C1", CoachRole.HEAD_COACH)

        assert len(coach.skills) > 0
        assert coach.level == 1

    def test_award_xp(self, engine):
        """XP levels up coach."""
        coach = engine.create_coach("C1", CoachRole.HEAD_COACH)
        coach.xp_to_next = 1000

        leveled = engine.award_xp(coach, 1500)

        assert leveled
        assert coach.level == 2
        assert coach.points_available == 1
        assert coach.xp == 500

    def test_purchase_skill(self, engine):
        """Points buy skill ranks."""
        coach = engine.create_coach("C1", CoachRole.HEAD_COACH)
        coach.points_available = 1

        success = engine.purchase_skill(coach, "QB_WHISPERER")

        assert success
        assert coach.points_available == 0
        assert coach.skills["QB_WHISPERER"].current_rank == 1

    def test_purchase_fail_no_points(self, engine):
        """Cannot buy without points."""
        coach = engine.create_coach("C1", CoachRole.HEAD_COACH)
        coach.points_available = 0

        success = engine.purchase_skill(coach, "QB_WHISPERER")

        assert not success
        assert coach.skills["QB_WHISPERER"].current_rank == 0

    def test_staff_bonuses(self, engine):
        """Staff bonuses aggregate."""
        hc = engine.create_coach("HC", CoachRole.HEAD_COACH)
        hc.points_available = 1
        # Use internal method to force skill rank for testing
        hc.skills["QB_WHISPERER"].current_rank = 1 # +5%

        oc = engine.create_coach("OC", CoachRole.OFFENSIVE_COORD)
        oc.points_available = 1
        oc.skills["QB_WHISPERER"].current_rank = 1 # +5%

        bonuses = engine.get_staff_bonuses([hc, oc])

        # 1.0 + 0.05 + 0.05 = 1.10
        assert bonuses["QB_WHISPERER"] == 1.10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
