#!/usr/bin/env python3
"""
Simulation Calibrator Module
============================
Tunes simulation parameters to match real-world distributions.

Phase 11: Validation
- Parameter tuning
- Outcome distribution matching
- Auto-calibration
"""

from dataclasses import dataclass


@dataclass
class CalibrationTarget:
    """A parameter to calibrate."""
    name: str
    current_value: float
    target_value: float
    min_bound: float
    max_bound: float

    @property
    def error(self) -> float:
        """Current error from target."""
        return abs(self.current_value - self.target_value)

    @property
    def error_pct(self) -> float:
        """Error as percentage."""
        return (self.error / self.target_value * 100) if self.target_value != 0 else 0


@dataclass
class CalibrationResult:
    """Output of calibration run."""
    iterations: int
    converged: bool
    final_error: float
    adjustments: dict[str, float]


class SimulationCalibrator:
    """
    Auto-tunes simulation parameters.

    Uses gradient descent to minimize stat error.
    """

    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.targets: dict[str, CalibrationTarget] = {}

    def add_target(self, target: CalibrationTarget):
        """Register a calibration target."""
        self.targets[target.name] = target

    def calculate_adjustment(self, target: CalibrationTarget) -> float:
        """
        Calculate how much to adjust a parameter.

        Simple proportional control.
        """
        error = target.target_value - target.current_value
        adjustment = error * self.learning_rate

        # Clamp to bounds
        new_value = target.current_value + adjustment
        if new_value < target.min_bound:
            adjustment = target.min_bound - target.current_value
        elif new_value > target.max_bound:
            adjustment = target.max_bound - target.current_value

        return adjustment

    def run_calibration(self, max_iterations: int = 100, tolerance: float = 0.01) -> CalibrationResult:
        """
        Run calibration loop until convergence.
        """
        adjustments = {}
        avg_error = 0.0  # Initialize to handle empty targets case

        for iteration in range(max_iterations):
            total_error = 0.0

            for name, target in self.targets.items():
                adjustment = self.calculate_adjustment(target)
                target.current_value += adjustment
                adjustments[name] = adjustment
                total_error += target.error_pct

            avg_error = total_error / len(self.targets) if self.targets else 0

            if avg_error < tolerance:
                return CalibrationResult(
                    iterations=iteration + 1,
                    converged=True,
                    final_error=avg_error,
                    adjustments=adjustments
                )

        return CalibrationResult(
            iterations=max_iterations,
            converged=False,
            final_error=avg_error,
            adjustments=adjustments
        )

    def get_tuned_parameters(self) -> dict[str, float]:
        """
        Get all current parameter values.
        """
        return {name: target.current_value for name, target in self.targets.items()}
