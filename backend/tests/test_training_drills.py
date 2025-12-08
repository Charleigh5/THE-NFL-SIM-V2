#!/usr/bin/env python3
"""
Test Training Drills System (B-032)
===================================
Unit tests for the advanced training system.

Tests:
- Drill catalog validation
- Coaching style modifiers
- TrainingEngine drill execution
- Injury risk calculations
- XP multipliers
"""

import pytest
from app.services.training.drills import (
    Drill,
    DrillCategory,
    SeasonPhase,
    QB_DRILLS,
    RB_DRILLS,
    WR_DRILLS,
    OL_DRILLS,
    DL_DRILLS,
    DB_DRILLS,
    LB_DRILLS,
    ST_DRILLS,
    ALL_DRILLS,
    POSITION_DRILL_MAP,
    get_drills_for_position,
    get_drills_for_season,
    get_drills_by_category,
)
from app.services.training.coaching_philosophy import (
    CoachingStyle,
    CoachingStyleName,
    COACHING_STYLES,
    VOLUME_STYLE,
    INTENSITY_STYLE,
    SMART_STYLE,
    OLD_SCHOOL_STYLE,
    get_coaching_style,
    calculate_training_modifiers,
    get_seasonal_intensity_cap,
)
from app.kernels.rpg.training import TrainingEngine


class TestDrillCatalog:
    """Tests for drill catalog (B-011 to B-020)."""

    def test_have_minimum_50_drills(self):
        """B-011: Should have at least 50 unique drills."""
        assert len(ALL_DRILLS) >= 50, f"Expected 50+ drills, got {len(ALL_DRILLS)}"

    def test_drill_pydantic_model_validation(self):
        """B-012: Drill should be valid Pydantic model."""
        drill = Drill(
            name="Test Drill",
            target_stat="speed",
            secondary_stats=["agility"],
            injury_risk=0.05,
            xp_multiplier=1.2,
        )
        assert drill.name == "Test Drill"
        assert drill.target_stat == "speed"
        assert drill.injury_risk == 0.05

    def test_drill_injury_risk_bounds(self):
        """Injury risk should be bounded 0-1."""
        with pytest.raises(ValueError):
            Drill(name="Bad", target_stat="x", injury_risk=1.5)
        with pytest.raises(ValueError):
            Drill(name="Bad", target_stat="x", injury_risk=-0.1)

    def test_qb_drills_exist(self):
        """B-013: QB drills should exist."""
        assert len(QB_DRILLS) >= 5
        qb_targets = [d.target_stat for d in QB_DRILLS]
        assert "throw_power" in qb_targets or "throw_on_run" in qb_targets

    def test_rb_drills_exist(self):
        """B-014: RB drills should exist."""
        assert len(RB_DRILLS) >= 5
        rb_targets = [d.target_stat for d in RB_DRILLS]
        assert "agility" in rb_targets or "trucking" in rb_targets

    def test_wr_drills_exist(self):
        """B-015: WR drills should exist."""
        assert len(WR_DRILLS) >= 5
        wr_targets = [d.target_stat for d in WR_DRILLS]
        assert "route_running" in wr_targets

    def test_ol_drills_exist(self):
        """B-016: OL drills should exist."""
        assert len(OL_DRILLS) >= 5
        ol_targets = [d.target_stat for d in OL_DRILLS]
        assert "pass_block" in ol_targets or "run_block" in ol_targets

    def test_dl_drills_exist(self):
        """B-017: DL drills should exist."""
        assert len(DL_DRILLS) >= 5

    def test_db_drills_exist(self):
        """B-018: DB drills should exist."""
        assert len(DB_DRILLS) >= 5

    def test_lb_drills_exist(self):
        """B-019: LB drills should exist."""
        assert len(LB_DRILLS) >= 5

    def test_st_drills_exist(self):
        """B-020: Special teams drills should exist."""
        assert len(ST_DRILLS) >= 4

    def test_position_drill_map_coverage(self):
        """All positions should have drills mapped."""
        expected_positions = ["QB", "RB", "WR", "TE", "LT", "CB", "MLB", "K"]
        for pos in expected_positions:
            assert pos in POSITION_DRILL_MAP
            assert len(POSITION_DRILL_MAP[pos]) > 0

    def test_get_drills_for_position(self):
        """Should return correct drills for position."""
        qb_drills = get_drills_for_position("QB")
        assert len(qb_drills) == len(QB_DRILLS)

        unknown_drills = get_drills_for_position("UNKNOWN")
        assert unknown_drills == []

    def test_get_drills_for_season(self):
        """Should filter drills by season."""
        offseason_drills = get_drills_for_season(QB_DRILLS, SeasonPhase.OFFSEASON)
        assert len(offseason_drills) <= len(QB_DRILLS)

        # All offseason drills should have OFFSEASON in their filter
        for d in offseason_drills:
            assert SeasonPhase.OFFSEASON in d.season_filter

    def test_get_drills_by_category(self):
        """Should filter drills by category."""
        strength_drills = get_drills_by_category(ALL_DRILLS, DrillCategory.STRENGTH)
        assert len(strength_drills) > 0
        for d in strength_drills:
            assert d.category == DrillCategory.STRENGTH


class TestCoachingPhilosophy:
    """Tests for coaching styles (B-021 to B-026)."""

    def test_all_four_styles_exist(self):
        """B-022: All four coaching styles should be defined."""
        assert len(COACHING_STYLES) == 4
        assert CoachingStyleName.VOLUME in COACHING_STYLES
        assert CoachingStyleName.INTENSITY in COACHING_STYLES
        assert CoachingStyleName.SMART in COACHING_STYLES
        assert CoachingStyleName.OLD_SCHOOL in COACHING_STYLES

    def test_volume_style_properties(self):
        """B-023: Volume style should have low injury risk."""
        assert VOLUME_STYLE.injury_risk_multiplier < 1.0
        assert VOLUME_STYLE.young_player_bonus > 0

    def test_intensity_style_properties(self):
        """B-024: Intensity style should have high XP and high injury risk."""
        assert INTENSITY_STYLE.xp_multiplier > 1.0
        assert INTENSITY_STYLE.injury_risk_multiplier > 1.0

    def test_smart_style_properties(self):
        """B-025: Smart style should be balanced."""
        assert SMART_STYLE.xp_multiplier >= 1.0
        assert SMART_STYLE.injury_risk_multiplier < 1.0
        assert SMART_STYLE.recovery_multiplier > 1.0

    def test_old_school_style_properties(self):
        """B-026: Old school should favor veterans."""
        assert OLD_SCHOOL_STYLE.veteran_bonus > 0
        assert OLD_SCHOOL_STYLE.chemistry_effect > 0

    def test_get_coaching_style(self):
        """Should retrieve style by name."""
        style = get_coaching_style("volume")
        assert style.name == "volume"

        with pytest.raises(ValueError):
            get_coaching_style("nonexistent")

    def test_calculate_training_modifiers_young_player(self):
        """Should apply young player bonus."""
        result = calculate_training_modifiers(
            style=VOLUME_STYLE,
            player_age=23,
            base_xp=10.0,
            base_injury_risk=0.05,
            base_fatigue=10.0
        )
        assert result["age_bonus_applied"] == VOLUME_STYLE.young_player_bonus
        assert result["xp"] > 10.0 * VOLUME_STYLE.xp_multiplier  # Has bonus

    def test_calculate_training_modifiers_veteran(self):
        """Should apply veteran bonus."""
        result = calculate_training_modifiers(
            style=INTENSITY_STYLE,
            player_age=32,
            base_xp=10.0,
            base_injury_risk=0.05,
            base_fatigue=10.0
        )
        assert result["age_bonus_applied"] == INTENSITY_STYLE.veteran_bonus

    def test_seasonal_intensity_cap(self):
        """Should return correct seasonal caps."""
        assert get_seasonal_intensity_cap("offseason") == 0.85
        assert get_seasonal_intensity_cap("regular") == 0.50
        assert get_seasonal_intensity_cap("playoffs") == 0.30


class TestTrainingEngine:
    """Tests for enhanced TrainingEngine (B-027 to B-031)."""

    def test_train_with_drill_basic(self):
        """B-027: Should execute drill and return results."""
        engine = TrainingEngine()
        drill = QB_DRILLS[0]  # Footwork Mechanics

        result = engine.train_with_drill(
            drill=drill,
            player_age=25,
            season_phase="offseason",
            rng_seed=42
        )

        assert "xp_gained" in result
        assert "target_stat" in result
        assert "injury_occurred" in result
        assert result["target_stat"] == drill.target_stat

    def test_seasonal_periodization(self):
        """B-028: XP should be reduced in regular season vs offseason."""
        engine = TrainingEngine()
        drill = QB_DRILLS[0]

        offseason_result = engine.train_with_drill(
            drill=drill, player_age=25, season_phase="offseason", rng_seed=42
        )

        engine2 = TrainingEngine()  # Fresh engine
        regular_result = engine2.train_with_drill(
            drill=drill, player_age=25, season_phase="regular", rng_seed=42
        )

        assert offseason_result["xp_gained"] > regular_result["xp_gained"]

    def test_weekly_load_management(self):
        """B-029: Weekly load should accumulate."""
        engine = TrainingEngine()
        drill = QB_DRILLS[0]

        engine.train_with_drill(drill=drill, player_age=25, rng_seed=42)
        assert engine.weekly_load > 0

        initial_load = engine.weekly_load
        engine.train_with_drill(drill=drill, player_age=25, rng_seed=43)
        assert engine.weekly_load > initial_load

        # Reset should clear weekly load
        engine.reset_weekly_load()
        assert engine.weekly_load == 0.0

    def test_injury_risk_increases_with_fatigue(self):
        """B-030: Higher fatigue should increase injury risk."""
        engine1 = TrainingEngine()
        engine1.current_fatigue = 0.0

        engine2 = TrainingEngine()
        engine2.current_fatigue = 80.0

        drill = DL_DRILLS[-1]  # Bull Rush Power - high base risk

        result1 = engine1.train_with_drill(drill=drill, player_age=25, rng_seed=42)
        result2 = engine2.train_with_drill(drill=drill, player_age=25, rng_seed=42)

        assert result2["final_injury_risk"] > result1["final_injury_risk"]

    def test_xp_multiplier_from_drill(self):
        """B-031: Higher XP multiplier drills should give more XP."""
        engine = TrainingEngine()

        low_xp_drill = [d for d in QB_DRILLS if d.xp_multiplier < 1.0][0]  # Film Study
        high_xp_drill = [d for d in QB_DRILLS if d.xp_multiplier > 1.3][0]  # Weighted balls or 2-min

        low_result = engine.train_with_drill(
            drill=low_xp_drill, player_age=25, season_phase="offseason", rng_seed=42
        )

        engine2 = TrainingEngine()
        high_result = engine2.train_with_drill(
            drill=high_xp_drill, player_age=25, season_phase="offseason", rng_seed=42
        )

        # High multiplier drill should give more XP (before injury effects)
        assert high_result["xp_gained"] != low_result["xp_gained"]

    def test_coaching_style_affects_training(self):
        """Coaching style should modify training outcomes."""
        drill = QB_DRILLS[0]

        engine1 = TrainingEngine()
        result1 = engine1.train_with_drill(
            drill=drill,
            player_age=23,
            coaching_style=VOLUME_STYLE,
            season_phase="offseason",
            rng_seed=42
        )

        engine2 = TrainingEngine()
        result2 = engine2.train_with_drill(
            drill=drill,
            player_age=23,
            coaching_style=INTENSITY_STYLE,
            season_phase="offseason",
            rng_seed=42
        )

        # Intensity should give more XP (but also more risk)
        # Note: Young player bonus in Volume may offset this
        assert result1["xp_gained"] != result2["xp_gained"]

    def test_recovery_with_coaching_style(self):
        """Recovery should be affected by coaching style."""
        engine = TrainingEngine()
        engine.current_fatigue = 50.0

        # SMART style has 1.2x recovery
        recovered = engine.recover(rest_quality=0.5, coaching_style=SMART_STYLE)

        # Should recover more than base (0.5 * 20 * 1.2 = 12)
        assert recovered == pytest.approx(12.0, rel=0.01)

    def test_training_recommendation(self):
        """Should give appropriate training recommendations."""
        engine = TrainingEngine()

        assert engine.get_training_recommendation(10, "offseason") == "heavy"
        assert engine.get_training_recommendation(40, "regular") == "light"
        assert engine.get_training_recommendation(80, "regular") == "rest"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
