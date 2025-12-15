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
