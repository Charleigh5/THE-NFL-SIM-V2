#!/usr/bin/env python3
"""
Statistical Validation Module
=============================
Validates simulation output against real NFL statistics.

Phase 11: Validation
- Expected value ranges
- Distribution validation
- Calibration checks
"""

import statistics
from dataclasses import dataclass

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class StatRange:
    """Expected range for a statistic."""
    name: str
    min_val: float
    max_val: float
    mean: float
    std_dev: float


@dataclass
class ValidationResult:
    """Result of a validation check."""
    stat_name: str
    passed: bool
    actual_value: float
    expected_range: tuple[float, float]
    deviation_pct: float
    message: str


# ============================================================================
# NFL STATISTICAL BENCHMARKS
# ============================================================================

class NFLBenchmarks:
    """
    Real NFL statistical benchmarks for validation.
    """

    # Per-game team averages (2023 season approximations)
    TEAM_STATS = {
        "points_per_game": StatRange("Points/Game", 14, 32, 22.5, 4.5),
        "yards_per_game": StatRange("Yards/Game", 280, 420, 340, 35),
        "pass_yards_per_game": StatRange("Pass Yards/Game", 180, 300, 230, 30),
        "rush_yards_per_game": StatRange("Rush Yards/Game", 80, 160, 115, 20),
        "turnovers_per_game": StatRange("Turnovers/Game", 0.5, 2.5, 1.3, 0.5),
    }

    # Per-play averages
    PLAY_STATS = {
        "yards_per_play": StatRange("Yards/Play", 4.5, 6.5, 5.4, 0.5),
        "yards_per_pass": StatRange("Yards/Pass", 6.0, 9.0, 7.2, 0.8),
        "yards_per_rush": StatRange("Yards/Rush", 3.5, 5.5, 4.3, 0.5),
        "completion_pct": StatRange("Completion %", 58, 72, 65, 4),
        "td_pct": StatRange("TD %", 3.5, 6.5, 4.8, 0.8),
        "int_pct": StatRange("INT %", 1.5, 3.5, 2.4, 0.5),
    }

    # Game-level
    GAME_STATS = {
        "total_plays": StatRange("Plays/Game", 55, 75, 64, 5),
        "time_of_possession": StatRange("TOP (min)", 25, 35, 30, 3),
        "third_down_pct": StatRange("3rd Down %", 30, 50, 40, 5),
    }


# ============================================================================
# VALIDATION ENGINE
# ============================================================================

class ValidationEngine:
    """
    Validates simulation statistics against NFL benchmarks.
    """

    def __init__(self):
        self.benchmarks = NFLBenchmarks()

    def validate_stat(self, stat_name: str, actual: float) -> ValidationResult:
        """
        Validate a single statistic.
        """
        # Find matching benchmark
        stat_range = None
        for category in [
            self.benchmarks.TEAM_STATS,
            self.benchmarks.PLAY_STATS,
            self.benchmarks.GAME_STATS,
        ]:
            if stat_name in category:
                stat_range = category[stat_name]
                break

        if not stat_range:
            return ValidationResult(
                stat_name=stat_name, passed=False, actual_value=actual,
                expected_range=(0, 0), deviation_pct=100,
                message=f"Unknown stat: {stat_name}"
            )

        # Check if in range
        in_range = stat_range.min_val <= actual <= stat_range.max_val

        # Calculate deviation from mean
        deviation = abs(actual - stat_range.mean)
        deviation_pct = (deviation / stat_range.mean) * 100 if stat_range.mean != 0 else 0

        # Standard deviation check (within 2 std devs is acceptable)
        within_std = deviation <= (2 * stat_range.std_dev)

        passed = in_range and within_std

        return ValidationResult(
            stat_name=stat_name,
            passed=passed,
            actual_value=actual,
            expected_range=(stat_range.min_val, stat_range.max_val),
            deviation_pct=deviation_pct,
            message=(
                f"{'PASS' if passed else 'FAIL'}: "
                f"{actual:.2f} vs expected {stat_range.mean:.2f}"
            )
        )

    def validate_season(self, season_stats: dict[str, float]) -> list[ValidationResult]:
        """
        Validate all stats from a simulated season.
        """
        results = []
        for stat_name, value in season_stats.items():
            result = self.validate_stat(stat_name, value)
            results.append(result)
        return results

    def get_calibration_report(self, results: list[ValidationResult]) -> dict:
        """
        Generate a calibration summary.
        """
        total = len(results)
        passed = sum(1 for r in results if r.passed)

        failed_stats = [r.stat_name for r in results if not r.passed]
        avg_deviation = statistics.mean([r.deviation_pct for r in results]) if results else 0

        return {
            "total_checks": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "avg_deviation_pct": avg_deviation,
            "failed_stats": failed_stats,
            "calibration_needed": len(failed_stats) > 0,
        }
