#!/usr/bin/env python3
"""
Phase 11: Validation Tests
==========================
Unit tests for validation and calibration modules.
"""

import pytest
from app.services.validation import (
    ValidationEngine, ValidationResult, NFLBenchmarks,
    SimulationCalibrator, CalibrationTarget,
)


class TestValidationEngine:
    """Tests for ValidationEngine."""

    @pytest.fixture
    def engine(self):
        return ValidationEngine()

    def test_validate_stat_pass(self, engine):
        """Valid stat within range passes."""
        result = engine.validate_stat("points_per_game", 24.0)

        assert result.passed
        assert result.stat_name == "points_per_game"

    def test_validate_stat_fail(self, engine):
        """Stat outside range fails."""
        result = engine.validate_stat("points_per_game", 5.0)  # Way too low

        assert not result.passed

    def test_validate_season(self, engine):
        """Validates multiple stats."""
        stats = {
            "points_per_game": 23.0,
            "yards_per_play": 5.5,
            "completion_pct": 66.0,
        }

        results = engine.validate_season(stats)
        assert len(results) == 3
        assert all(r.passed for r in results)

    def test_calibration_report(self, engine):
        """Generates calibration report."""
        results = [
            ValidationResult("test1", True, 50, (40, 60), 5, "PASS"),
            ValidationResult("test2", False, 100, (40, 60), 80, "FAIL"),
        ]

        report = engine.get_calibration_report(results)

        assert report["total_checks"] == 2
        assert report["passed"] == 1
        assert report["failed"] == 1
        assert "test2" in report["failed_stats"]


class TestSimulationCalibrator:
    """Tests for SimulationCalibrator."""

    @pytest.fixture
    def calibrator(self):
        return SimulationCalibrator(learning_rate=0.5)

    def test_add_target(self, calibrator):
        """Adds calibration target."""
        target = CalibrationTarget("pass_rate", 0.5, 0.65, 0.0, 1.0)
        calibrator.add_target(target)

        assert "pass_rate" in calibrator.targets

    def test_calculate_adjustment(self, calibrator):
        """Calculates correct adjustment."""
        target = CalibrationTarget("pass_rate", 0.5, 0.7, 0.0, 1.0)

        adjustment = calibrator.calculate_adjustment(target)

        # Error = 0.2, rate = 0.5 -> adj = 0.1
        assert adjustment == pytest.approx(0.1, abs=0.01)

    def test_run_calibration_converges(self, calibrator):
        """Calibration converges to target."""
        target = CalibrationTarget("td_rate", 0.04, 0.048, 0.01, 0.10)
        calibrator.add_target(target)

        result = calibrator.run_calibration(max_iterations=50, tolerance=1.0)

        # Should converge quickly with 0.5 learning rate
        assert result.final_error < 5  # Within 5% error

    def test_get_tuned_parameters(self, calibrator):
        """Returns current parameter values."""
        target = CalibrationTarget("int_rate", 0.02, 0.024, 0.01, 0.05)
        calibrator.add_target(target)

        params = calibrator.get_tuned_parameters()

        assert "int_rate" in params
        assert params["int_rate"] == 0.02


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
