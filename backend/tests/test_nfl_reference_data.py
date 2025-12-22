import pytest
from app.core.nfl_reference_data import HISTORICAL_SALARY_CAPS, SPECIAL_PLAYS, FOURTH_DOWN_ANALYTICS, SALARY_CAP_CAGR
from app.services.empire.salary_cap import SalaryCapEngine
from app.services.playbook.coaching_ai import CoachingAIService
from app.data.coaches import CoachingPhilosophy
from app.services.playbook.types import GameSituation

def test_salary_cap_completeness():
    """Verify historical caps cover the expected range."""
    # Should have 1994 to 2025 (32 years)
    for year in range(1994, 2026):
        assert year in HISTORICAL_SALARY_CAPS

    # 2010 should be None (uncapped)
    assert HISTORICAL_SALARY_CAPS[2010] is None
    # 2025 should be 279.2M
    assert HISTORICAL_SALARY_CAPS[2025] == 279_200_000

def test_salary_cap_cagr():
    """Verify CAGR is correct."""
    assert SALARY_CAP_CAGR == 0.0697

def test_salary_cap_engine_historical():
    """Test SalaryCapEngine using historical data."""
    engine = SalaryCapEngine()

    # Test lookup for 2024
    assert engine.get_historical_cap(2024) == 255_400_000

    # Test season cap for 2023
    assert engine.get_cap_for_season(2023) == 224_800_000

    # Test projection forward
    projections = engine.project_cap(279_200_000, 2)
    expected_2026 = int(279_200_000 * 1.0697)
    assert projections[0] == expected_2026

def test_special_plays_data():
    """Verify special plays reference data."""
    assert "TUSH_PUSH" in SPECIAL_PLAYS
    assert "FLEA_FLICKER" in SPECIAL_PLAYS
    assert SPECIAL_PLAYS["TUSH_PUSH"].success_rate_avg > 0.8
    assert SPECIAL_PLAYS["TUSH_PUSH"].epa_value == 0.25

def test_coaching_ai_4th_down_analytics():
    """Test coaching AI uses analytics data with archetype logic."""
    # Analytics Disciple archetype (fourth_down_aggression >= 60)
    philosophy = CoachingPhilosophy(
        aggressiveness=65,
        run_pass_ratio=50,
        fourth_down_aggression=65  # Explicitly set for Analytics Disciple
    )
    ai = CoachingAIService(philosophy)

    # 4th & 1 should be a 'go' for Analytics Disciple (goes on 4th & 1 always)
    situation_4th_1 = GameSituation(
        down=4,
        distance=1,
        field_position=50,
        score_diff=0,
        quarter=1,
        time_remaining=900
    )
    assert ai.should_go_for_it_4th_down(situation_4th_1) is True

    # Late game desperation should trigger override (ALL archetypes)
    situation_desperate = GameSituation(
        down=4,
        distance=10,
        field_position=20, # Deep in own half
        score_diff=-14,
        quarter=4,
        time_remaining=120
    )
    assert ai.should_go_for_it_4th_down(situation_desperate) is True

def test_coaching_ai_4th_down_optimal_zone():
    """Test coaching AI archetypes in various field positions."""
    # THE GAMBLER archetype (fourth_down_aggression >= 75)
    gambler_philosophy = CoachingPhilosophy(
        aggressiveness=80,
        run_pass_ratio=50,
        fourth_down_aggression=80
    )
    gambler_ai = CoachingAIService(gambler_philosophy)

    # Gambler should go for 4th & 2 past their own 30
    situation_own_45 = GameSituation(
        down=4,
        distance=2,
        field_position=45,  # Own 45 (past own 30)
        score_diff=0,
        quarter=2,
        time_remaining=300
    )
    assert gambler_ai.should_go_for_it_4th_down(situation_own_45) is True

    # CONSERVATIVE archetype (fourth_down_aggression < 40)
    conservative_philosophy = CoachingPhilosophy(
        aggressiveness=25,
        run_pass_ratio=60,
        fourth_down_aggression=25
    )
    conservative_ai = CoachingAIService(conservative_philosophy)

    # Conservative should NOT go for 4th & 1 at midfield - only at goal line
    situation_midfield = GameSituation(
        down=4,
        distance=1,
        field_position=50,
        score_diff=0,
        quarter=2,
        time_remaining=300
    )
    assert conservative_ai.should_go_for_it_4th_down(situation_midfield) is False

    # Conservative SHOULD go for 4th & Goal from the 1 (field_position > 97)
    situation_goal_line = GameSituation(
        down=4,
        distance=1,
        field_position=99,  # 1-yard line
        score_diff=0,
        quarter=2,
        time_remaining=300
    )
    assert conservative_ai.should_go_for_it_4th_down(situation_goal_line) is True
