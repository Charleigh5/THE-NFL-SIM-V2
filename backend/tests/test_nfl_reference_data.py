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
    """Test coaching AI uses analytics data."""
    philosophy = CoachingPhilosophy(
        aggressiveness=50,
        run_pass_ratio=50
    )
    ai = CoachingAIService(philosophy)

    # 4th & 1 should always be a 'go' for 50 aggressiveness
    situation_4th_1 = GameSituation(
        down=4,
        distance=1,
        field_position=50,
        score_diff=0,
        quarter=1,
        time_remaining=900
    )
    assert ai.should_go_for_it_4th_down(situation_4th_1) is True

    # Late game desperation should trigger override
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
    """Test coaching AI in the optimal 'go zone'."""
    philosophy = CoachingPhilosophy(
        aggressiveness=60,  # Moderately aggressive
        run_pass_ratio=50
    )
    ai = CoachingAIService(philosophy)

    # 4th & 2 at midfield (in the go-for-it zone: 40-60)
    situation_midfield = GameSituation(
        down=4,
        distance=2,
        field_position=50,
        score_diff=0,
        quarter=2,
        time_remaining=300
    )

    # With 60 aggressiveness:
    # Aggression Score = 60
    # Distance Penalty = 2 * 8 = 16
    # Position Bonus = 30 (for midfield in 40-60 zone)
    # Consider Go Bonus = 15 (for distance <= 5)
    # Total probability = 60 - 16 + 30 + 15 = 89%
    import app.services.playbook.coaching_ai as coaching_ai
    with pytest.MonkeyPatch.context() as mp:
        # Roll of 60 should succeed (60 < 89)
        mp.setattr(coaching_ai.random, "uniform", lambda a, b: 60)
        result = ai.should_go_for_it_4th_down(situation_midfield)
        assert result is True

        # Roll of 95 should fail (95 > 89)
        mp.setattr(coaching_ai.random, "uniform", lambda a, b: 95)
        result = ai.should_go_for_it_4th_down(situation_midfield)
        assert result is False

