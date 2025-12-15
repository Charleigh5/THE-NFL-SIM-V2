import pytest
from unittest.mock import patch
from app.data.coaches import CoachingPhilosophy
from app.services.playbook.coaching_ai import CoachingAIService
from app.services.playbook.types import GameSituation

class TestCoachingAIService:
    @pytest.fixture
    def aggressive_coach(self):
        return CoachingPhilosophy(
            aggressiveness=80,
            fourth_down_aggression=90,
            clock_management_style="AGGRESSIVE",
            trick_play_frequency=25,
            two_pt_conversion_threshold=20
        )

    @pytest.fixture
    def conservative_coach(self):
        return CoachingPhilosophy(
            aggressiveness=20,
            fourth_down_aggression=10,
            clock_management_style="CONSERVATIVE",
            trick_play_frequency=0,
            two_pt_conversion_threshold=80
        )

    def test_get_adjusted_aggression_trailing(self, aggressive_coach):
        """Test aggression adjustment when trailing significantly."""
        service = CoachingAIService(aggressive_coach)
        situation = GameSituation(
            quarter=3,
            time_remaining=1800,
            down=1,
            distance=10,
            field_position=50,
            score_diff=-14
        )
        # Base 80, trailing > 7 (+10) = 90
        assert service.get_adjusted_aggression(situation) == 90

    def test_get_adjusted_aggression_leading_late(self, aggressive_coach):
        """Test aggression adjustment when leading late (should be conservative)."""
        service = CoachingAIService(aggressive_coach)
        situation = GameSituation(
            quarter=4,
            time_remaining=200,
            down=1,
            distance=10,
            field_position=50,
            score_diff=10 # Leading by 10
        )
        # Base 80
        # Leading > 7 -> -10 (70)
        # 4th Q Leading -> -15 (55)
        # Result 55?
        val = service.get_adjusted_aggression(situation)
        assert val < 80 # Should be lower than base
        assert val == 55

    @patch('random.uniform')
    def test_should_go_for_it_4th_down_aggressive(self, mock_random, aggressive_coach):
        """Test 4th down decision for aggressive coach."""
        mock_random.return_value = 50 # Roll 50

        service = CoachingAIService(aggressive_coach)
        situation = GameSituation(
            quarter=4,
            time_remaining=120,
            down=4,
            distance=2, # Penalty 20
            field_position=60, # Bonus 20
            score_diff=-5
        )
        # Probability = Agg(90) - Dist(20) + Pos(20) = 90
        # Roll 50 < 90 -> True
        assert service.should_go_for_it_4th_down(situation) is True

    @patch('random.uniform')
    def test_should_go_for_it_4th_long_conservative(self, mock_random, conservative_coach):
        """Test 4th down decision for conservative coach on long yardage."""
        mock_random.return_value = 10 # Low roll, but prob might be negative

        service = CoachingAIService(conservative_coach)
        situation = GameSituation(
            quarter=1,
            time_remaining=3000,
            down=4,
            distance=10, # Penalty 100
            field_position=40, # Bonus 20
            score_diff=0
        )
        # Probability = Agg(10) - Dist(100) + Pos(20) = -70
        # Roll 10 < -70 -> False
        assert service.should_go_for_it_4th_down(situation) is False

    def test_should_call_timeout_offense(self, aggressive_coach):
        """Test timeout logic for offense."""
        service = CoachingAIService(aggressive_coach)
        situation = GameSituation(
            quarter=2,
            time_remaining=100, # Under 3 mins
            down=1,
            distance=10,
            field_position=50,
            score_diff=-3 # Trailing
        )
        # Should call timeout to save time
        assert service.should_call_timeout(situation, is_offense=True) is True

    def test_should_call_timeout_defense_winning(self, aggressive_coach):
        """Defense shouldn't call timeout when winning comfortable."""
        service = CoachingAIService(aggressive_coach)
        situation = GameSituation(
            quarter=4,
            time_remaining=100,
            down=1,
            distance=10,
            field_position=50,
            score_diff=14 # Winning by 14
        )
        assert service.should_call_timeout(situation, is_offense=False) is False
