"""
VALIDATION Package
==================
Statistical validation and calibration systems.

Phase 11: Validation
- Stats Validator
- Simulation Calibrator
"""

from .stats_validator import (
    ValidationEngine,
    ValidationResult,
    StatRange,
    NFLBenchmarks,
)

from .calibrator import (
    SimulationCalibrator,
    CalibrationTarget,
    CalibrationResult,
)

__all__ = [
    # Validator
    "ValidationEngine", "ValidationResult", "StatRange", "NFLBenchmarks",
    # Calibrator
    "SimulationCalibrator", "CalibrationTarget", "CalibrationResult",
]
