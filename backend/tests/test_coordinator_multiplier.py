"""
Tests for Coordinator Multiplier System
========================================
Tests the NFL Identity Blueprint coordinator IQ formula and integration.
"""

import pytest
from app.orchestrator.kernels.cortex_kernel import (
    CortexKernel,
    CoordinatorMultiplier,
    GameSituation
)


class TestCoordinatorMultiplier:
    """Test the coordinator IQ boost formula."""

    def test_neutral_at_75(self):
        """IQ 75 = 1.0x (neutral)."""
        boost = CoordinatorMultiplier.calculate_boost(75)
        assert boost == 1.0

    def test_boost_at_95(self):
        """IQ 95 = 1.1x (10% boost)."""
        boost = CoordinatorMultiplier.calculate_boost(95)
        assert boost == pytest.approx(1.1, rel=0.01)

    def test_penalty_at_55(self):
        """IQ 55 = 0.9x (10% penalty)."""
        boost = CoordinatorMultiplier.calculate_boost(55)
        assert boost == pytest.approx(0.9, rel=0.01)

    def test_max_boost_at_100(self):
        """IQ 100 = 1.125x."""
        boost = CoordinatorMultiplier.calculate_boost(100)
        assert boost == pytest.approx(1.125, rel=0.01)

    def test_min_boost_at_0(self):
        """IQ 0 = 0.625x."""
        boost = CoordinatorMultiplier.calculate_boost(0)
        assert boost == pytest.approx(0.625, rel=0.01)


class TestApplyToProbability:
    """Test probability modification."""

    def test_boost_applied_to_probability(self):
        """Probability should be multiplied by boost."""
        base_prob = 0.5
        intelligence = 95  # 1.1x boost

        modified = CoordinatorMultiplier.apply_to_probability(base_prob, intelligence)

        assert modified == pytest.approx(0.55, rel=0.01)

    def test_probability_clamped_to_1(self):
        """Probability should not exceed 1.0."""
        base_prob = 0.95
        intelligence = 100  # 1.125x boost

        modified = CoordinatorMultiplier.apply_to_probability(base_prob, intelligence)

        assert modified <= 1.0

    def test_probability_clamped_to_0(self):
        """Probability should not go below 0.0."""
        base_prob = 0.1
        intelligence = 0  # 0.625x boost

        modified = CoordinatorMultiplier.apply_to_probability(base_prob, intelligence)

        assert modified >= 0.0


class TestCortexKernelIntegration:
    """Test coordinator multiplier integration in CortexKernel."""

    def test_kernel_has_multiplier(self):
        """CortexKernel should have coordinator_multiplier attribute."""
        kernel = CortexKernel(seed=42)

        assert hasattr(kernel, "coordinator_multiplier")
        assert isinstance(kernel.coordinator_multiplier, CoordinatorMultiplier)

    def test_get_coordinator_boost(self):
        """get_coordinator_boost should return correct value."""
        kernel = CortexKernel(seed=42)

        boost = kernel.get_coordinator_boost(95)

        assert boost == pytest.approx(1.1, rel=0.01)

    def test_call_play_uses_intelligence(self):
        """call_play should accept intelligence in coach_philosophy."""
        kernel = CortexKernel(seed=42)

        situation = GameSituation(
            down=1,
            distance=10,
            field_position=25,
            time_remaining=600,
            score_differential=0,
            quarter=1
        )

        # Should not raise
        play = kernel.call_play(situation, {"intelligence": 95})

        assert play in ["RUN", "PASS_SHORT", "PASS_DEEP", "PUNT", "FG", "HAIL_MARY"]
