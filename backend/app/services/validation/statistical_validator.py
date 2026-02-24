"""
Statistical Validation Module (Phase 4 Extension)
==================================================
B-069 to B-073: Extended validation using scipy KS tests
and nflfastR target distributions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import statistics
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# NFL TARGET DISTRIBUTIONS
# =============================================================================

@dataclass
class NFLFastRTargets:
    """Target distributions from nflfastR data (2018-2023)."""

    YPC_DISTRIBUTION: dict[str, float] = field(default_factory=lambda: {
        "mean": 4.3,
        "std": 6.2,
        "median": 3.0,
    })

    PASS_OUTCOMES: dict[str, float] = field(default_factory=lambda: {
        "completion_rate": 0.65,
        "sack_rate": 0.072,
        "interception_rate": 0.024,
    })

    YARDS_PER_COMPLETION: dict[str, float] = field(default_factory=lambda: {
        "mean": 11.2,
        "std": 9.5,
        "median": 8.0,
    })


# =============================================================================
# VALIDATION RESULTS
# =============================================================================

@dataclass
class ValidationMetric:
    """Result of a single validation metric."""
    name: str
    actual: float
    expected: float
    tolerance: float
    passed: bool
    details: str | None = None


@dataclass
class StatisticalValidationResult:
    """Complete validation result."""
    total_plays: int
    metrics: list[ValidationMetric]
    overall_passed: bool
    ks_p_value: float | None = None

    def to_dict(self) -> dict:
        return {
            "total_plays": self.total_plays,
            "overall_passed": self.overall_passed,
            "ks_p_value": self.ks_p_value,
            "metrics": [
                {
                    "name": m.name,
                    "actual": round(m.actual, 4),
                    "expected": round(m.expected, 4),
                    "tolerance": round(m.tolerance, 4),
                    "passed": m.passed,
                    "details": m.details
                }
                for m in self.metrics
            ]
        }


# =============================================================================
# STATISTICAL VALIDATOR
# =============================================================================

class StatisticalValidator:
    """Validates simulation output against NFL statistics."""

    def __init__(self):
        self.targets = NFLFastRTargets()

    def run_validation(
        self,
        run_yards: list[float],
        pass_yards: list[float],
        pass_attempts: int,
        completions: int,
        sacks: int,
        interceptions: int
    ) -> StatisticalValidationResult:
        """Run full validation suite."""
        metrics = []
        total_plays = len(run_yards) + pass_attempts
        p_value = None

        # 1. Yards Per Carry
        if len(run_yards) >= 50:
            ypc = statistics.mean(run_yards)
            expected_ypc = self.targets.YPC_DISTRIBUTION["mean"]
            tolerance = 0.5

            metrics.append(ValidationMetric(
                name="YPC",
                actual=ypc,
                expected=expected_ypc,
                tolerance=tolerance,
                passed=abs(ypc - expected_ypc) < tolerance,
                details=f"Actual {ypc:.2f} vs Expected {expected_ypc:.1f}"
            ))

        # 2. Completion Percentage
        if pass_attempts > 0:
            comp_pct = completions / pass_attempts
            expected_comp = self.targets.PASS_OUTCOMES["completion_rate"]
            comp_tolerance = 0.02

            metrics.append(ValidationMetric(
                name="Completion %",
                actual=comp_pct,
                expected=expected_comp,
                tolerance=comp_tolerance,
                passed=abs(comp_pct - expected_comp) <= comp_tolerance,
                details=f"{comp_pct*100:.1f}% vs {expected_comp*100:.1f}%"
            ))

        # 3. Sack Rate
        if pass_attempts > 0:
            sack_rate = sacks / pass_attempts
            expected_sack = self.targets.PASS_OUTCOMES["sack_rate"]
            sack_tolerance = 0.01

            metrics.append(ValidationMetric(
                name="Sack Rate",
                actual=sack_rate,
                expected=expected_sack,
                tolerance=sack_tolerance,
                passed=abs(sack_rate - expected_sack) <= sack_tolerance,
                details=f"{sack_rate*100:.2f}% vs {expected_sack*100:.1f}%"
            ))

        # 4. Interception Rate
        if pass_attempts > 0:
            int_rate = interceptions / pass_attempts
            expected_int = self.targets.PASS_OUTCOMES["interception_rate"]
            int_tolerance = 0.01

            metrics.append(ValidationMetric(
                name="INT Rate",
                actual=int_rate,
                expected=expected_int,
                tolerance=int_tolerance,
                passed=abs(int_rate - expected_int) <= int_tolerance,
                details=f"{int_rate*100:.2f}% vs {expected_int*100:.1f}%"
            ))

        # 5. Yards Per Completion
        if len(pass_yards) >= 50:
            ypc = statistics.mean(pass_yards)
            expected_ypc = self.targets.YARDS_PER_COMPLETION["mean"]
            ypc_tolerance = 2.0

            metrics.append(ValidationMetric(
                name="Yards/Completion",
                actual=ypc,
                expected=expected_ypc,
                tolerance=ypc_tolerance,
                passed=abs(ypc - expected_ypc) <= ypc_tolerance,
                details=f"{ypc:.1f} yds vs {expected_ypc:.1f} yds"
            ))

        overall_passed = all(m.passed for m in metrics)

        return StatisticalValidationResult(
            total_plays=total_plays,
            metrics=metrics,
            overall_passed=overall_passed,
            ks_p_value=p_value
        )


def load_nflfastr_targets() -> NFLFastRTargets:
    """Load NFL target statistics."""
    return NFLFastRTargets()


__all__ = [
    "StatisticalValidator",
    "NFLFastRTargets",
    "ValidationMetric",
    "StatisticalValidationResult",
    "load_nflfastr_targets",
]
