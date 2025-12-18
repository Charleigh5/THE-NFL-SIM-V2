import pytest
from unittest.mock import MagicMock
from app.services.playbook.types import GameSituation
from app.services.playbook.clock_management import ClockManagementAI, ClockStrategy
from app.services.playbook.coaching_ai import CoachingAIService
from app.data.coaches import CoachingPhilosophy

class TestClockManagementAI:
    @pytest.fixture
    def clock_ai(self):
        philosophy = CoachingPhilosophy()
        coaching_service = CoachingAIService(philosophy)
        return ClockManagementAI(coaching_service)

    def test_hurry_up_detection(self, clock_ai):
        # 4th Quarter, trailing, 2 mins left
        situation = GameSituation(
            quarter=4, time_remaining=120, down=1, distance=10,
            field_position=20, score_diff=-5
        )
        assert clock_ai.is_hurry_up_situation(situation) is True

        # 2nd Quarter, 30s left, close game
        situation = GameSituation(
            quarter=2, time_remaining=30, down=1, distance=10,
            field_position=20, score_diff=0
        )
        assert clock_ai.is_hurry_up_situation(situation) is True

        # 1st Quarter -> False
        situation.quarter = 1
        assert clock_ai.is_hurry_up_situation(situation) is False

    def test_spike_decision(self, clock_ai):
        # Hurry up context, running clock, no timeouts
        situation = GameSituation(
            quarter=4, time_remaining=20, down=1, distance=10,
            field_position=50, score_diff=-3
        )

        # Should spike if timeout = 0
        assert clock_ai.should_spike_ball(situation, timeouts_remaining=0) is True

        # Should NOT spike if timeouts available (usually)
        assert clock_ai.should_spike_ball(situation, timeouts_remaining=1) is False

        # Should NOT spike on 3rd down
        situation.down = 3
        assert clock_ai.should_spike_ball(situation, timeouts_remaining=0) is False

    def test_strategy_selection(self, clock_ai):
        # Kneel
        situation = GameSituation(
            quarter=4, time_remaining=40, down=1, distance=10,
            field_position=50, score_diff=3
        )
        assert clock_ai.get_clock_strategy(situation, 3) == ClockStrategy.KNEEL

        # Chew Clock
        situation = GameSituation(
            quarter=4, time_remaining=300, down=1, distance=10,
            field_position=50, score_diff=3
        )
        assert clock_ai.get_clock_strategy(situation, 3) == ClockStrategy.CHEW_CLOCK

    # =========================================================================
    # 2-MINUTE DRILL AI (AI-005) TESTS
    # =========================================================================

    def test_urgency_level_critical(self, clock_ai):
        """Test CRITICAL urgency in final seconds of 4th quarter."""
        situation = GameSituation(
            quarter=4, time_remaining=30, down=1, distance=10,
            field_position=50, score_diff=-7  # Trailing by TD
        )
        # 30 seconds left, 0 timeouts = CRITICAL
        from app.services.playbook.clock_management import UrgencyLevel
        assert clock_ai.get_urgency_level(situation, 0) == UrgencyLevel.CRITICAL

    def test_urgency_level_high(self, clock_ai):
        """Test HIGH urgency with some time remaining."""
        situation = GameSituation(
            quarter=4, time_remaining=90, down=1, distance=10,
            field_position=50, score_diff=-7
        )
        from app.services.playbook.clock_management import UrgencyLevel
        # 90 seconds + 0 timeouts = HIGH
        assert clock_ai.get_urgency_level(situation, 0) == UrgencyLevel.HIGH
        # 90 seconds + 2 timeouts (170 effective) = MEDIUM
        assert clock_ai.get_urgency_level(situation, 2) == UrgencyLevel.MEDIUM

    def test_urgency_level_low_when_winning(self, clock_ai):
        """Test LOW urgency when winning comfortably."""
        situation = GameSituation(
            quarter=4, time_remaining=60, down=1, distance=10,
            field_position=50, score_diff=21  # Winning by 3 TDs
        )
        from app.services.playbook.clock_management import UrgencyLevel
        assert clock_ai.get_urgency_level(situation, 0) == UrgencyLevel.LOW

    def test_two_minute_drill_context(self, clock_ai):
        """Test TwoMinuteDrillContext generation."""
        situation = GameSituation(
            quarter=4, time_remaining=45, down=1, distance=10,
            field_position=35, score_diff=-3  # Trailing, FG range
        )
        context = clock_ai.get_two_minute_drill_context(situation, 0)

        from app.services.playbook.clock_management import UrgencyLevel
        assert context.urgency_level == UrgencyLevel.CRITICAL
        assert context.favor_sideline_routes is True
        assert context.avoid_middle_field is True

    def test_play_adjustments_critical(self, clock_ai):
        """Test play adjustments in CRITICAL situations."""
        situation = GameSituation(
            quarter=4, time_remaining=30, down=1, distance=10,
            field_position=50, score_diff=-7
        )
        adjustments = clock_ai.get_play_adjustments(situation, 0)

        assert adjustments["urgency_level"] == "CRITICAL"
        assert adjustments["pass_probability_boost"] == 0.35
        assert adjustments["run_penalty"] == 0.4
        assert adjustments["max_play_clock_usage"] == 8

    def test_play_adjustments_normal(self, clock_ai):
        """Test play adjustments in normal situations."""
        situation = GameSituation(
            quarter=1, time_remaining=900, down=1, distance=10,
            field_position=50, score_diff=0
        )
        adjustments = clock_ai.get_play_adjustments(situation, 3)

        assert adjustments["urgency_level"] == "LOW"
        assert adjustments["pass_probability_boost"] == 0.0
        assert adjustments["max_play_clock_usage"] == 40

