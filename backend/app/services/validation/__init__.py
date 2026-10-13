"""
VALIDATION Package
==================
Statistical validation and calibration systems.

Phase 11: Validation
- Stats Validator
- Simulation Calibrator
"""

from .calibrator import (
    CalibrationResult,
    CalibrationTarget,
    SimulationCalibrator,
)
from .stats_validator import (
    NFLBenchmarks,
    StatRange,
    ValidationEngine,
    ValidationResult,
)

__all__ = [
    # Validator
    "ValidationEngine",
    "ValidationResult",
    "StatRange",
    "NFLBenchmarks",
    # Calibrator
    "SimulationCalibrator",
    "CalibrationTarget",
    "CalibrationResult",
]
