#!/usr/bin/env python3
"""
Test Growth Curves (RPG-003)
============================
Verifies position-specific aging curves, XP multipliers, and regression logic.
"""

import pytest
from app.services.training.growth_curves import GrowthCurveEngine, GrowthCurveType
from app.services.training.progression import ProgressionEngine, PlayerProgressionState, DevTrait, ProgressionPhase

class TestGrowthCurveEngine:
    """Tests independent curve keys."""

    def test_rookie_xp_bump(self):
        """Rookies (21-22) should get significant XP boost regardless of position."""
        rb_mult = GrowthCurveEngine.get_xp_multiplier(21, "RB")
        qb_mult = GrowthCurveEngine.get_xp_multiplier(22, "QB")

        assert rb_mult == 1.5
        assert qb_mult == 1.5

    def test_rb_cliff(self):
        """RBs should regress sharply after 28."""
        # Age 26 = Prime
        prime_score = GrowthCurveEngine.get_regression_score(26, "RB")
        assert prime_score == 0

        # Age 29 = Regression
        decline_score = GrowthCurveEngine.get_regression_score(29, "RB")
        assert decline_score > 0
        assert decline_score >= 20 # Significant penalty

    def test_qb_longevity(self):
        """QBs should not regress at 32."""
        score = GrowthCurveEngine.get_regression_score(32, "QB")
        assert score == 0 # Still prime/stable

    def test_xp_multiplier_declines(self):
        """Veterans earn less XP."""
        # WR at 32 is past prime
        vet_mult = GrowthCurveEngine.get_xp_multiplier(32, "WR")
        assert vet_mult < 1.0
        assert vet_mult == 0.5


class TestProgressionIntegration:
    """Tests integration into ProgressionService."""

    @pytest.fixture
    def engine(self):
        return ProgressionEngine()

    def test_apply_xp_rookie(self, engine):
        """Rookie should get 1.5x boost on applied XP."""
        state = PlayerProgressionState(
            player_id="p1", age=21, position="RB",
            current_xp=0, level=75, dev_trait=DevTrait.NORMAL,
            xp_to_next_level=1000
        )

        # 100 base XP * 1.5 (Rookie) * 1.0 (Normal Dev) = 150
        new_state, _ = engine.apply_xp(state, 100)
        assert new_state.current_xp == 150

    def test_regression_calculation_physicals(self, engine):
        """Old RB should lose physical stats primarily."""
        attrs = {
            "speed": 90,
            "acceleration": 90,
            "awareness": 90
        }

        # Force a high regression scenario (RB age 32)
        # Score = (32 - 27) * 12 = 60
        # 60% chance per physical stat to drop

        # We run this multiple times or seed specifically,
        # but to keep it simple we check if *possible* losses occur.
        # Physics engine randomness makes exact assert hard without mocking.
        # We will trust the engine returns - values.

        regressed = engine.calculate_regression("RB", 35, attrs)

        # At age 35, RB should definitely regress something
        assert len(regressed) > 0
        assert "speed" in regressed or "acceleration" in regressed

        # Check that losses are negative integers
        for val in regressed.values():
            assert val < 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
