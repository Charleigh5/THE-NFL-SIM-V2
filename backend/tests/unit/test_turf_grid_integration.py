"""
Unit tests for 10x10 Turf Degradation Grid & Contact Physics (DEP-004).
"""

import pytest
from app.engine.hive.turf_grid import (
    TurfGrid,
    TurfType,
    TurfCondition,
    WeatherEffect,
    TurfGridConfig,
)


class TestTurfGridIntegration:
    """Tests for 10x10 field turf degradation and friction physics."""

    def test_initial_grid_is_pristine(self):
        """Newly created turf grid starts with 100% integrity across all 100 zones."""
        grid = TurfGrid(turf_type=TurfType.NATURAL_GRASS)
        assert grid.state.average_integrity == 100.0
        assert len(grid.state.zones) == 10
        assert len(grid.state.zones[0]) == 10

        # Check center zone
        zone = grid.get_zone(5, 5)
        assert zone.condition == TurfCondition.PRISTINE
        assert zone.integrity == 100.0

    def test_position_mapping_to_10x10_grid(self):
        """Yard line and lateral coordinates accurately resolve to row (0-9) and col (0-9)."""
        grid = TurfGrid()

        # Own 25 yard line, center hashes (0 lateral) -> row 2, col 5
        row, col = grid.position_to_zone(yard_line=25.0, lateral_position=0.0)
        assert row == 2
        assert col == 5

        # Opponent 15 yard line (yard_line=85.0), left numbers (-15.0) -> row 8, col 2
        row, col = grid.position_to_zone(yard_line=85.0, lateral_position=-15.0)
        assert row == 8
        assert col == 2

    def test_degradation_reduces_friction_and_increases_wear(self):
        """Repeated plays in a zone degrade integrity and reduce friction coefficient."""
        grid = TurfGrid(turf_type=TurfType.NATURAL_GRASS)
        base_friction = grid.get_friction(row=5, col=5)
        assert base_friction >= 0.80

        # Simulate 50 high-impact plays in center hash zone (row 5, col 5)
        zone = grid.get_zone(5, 5)
        for _ in range(50):
            zone.degrade(1.2)

        assert zone.integrity < 50.0
        assert zone.condition in [TurfCondition.DAMAGED, TurfCondition.DESTROYED]

        degraded_friction = grid.get_friction(row=5, col=5)
        assert degraded_friction < base_friction
        assert degraded_friction >= 0.40  # Respects physical minimum floor

    def test_weather_effects_on_turf_friction(self):
        """Wet and freezing conditions reduce friction multiplier."""
        grid_dry = TurfGrid(turf_type=TurfType.NATURAL_GRASS)
        grid_dry.state.weather_effect = WeatherEffect.DRY

        grid_frozen = TurfGrid(turf_type=TurfType.NATURAL_GRASS)
        grid_frozen.state.weather_effect = WeatherEffect.FROZEN

        dry_friction = grid_dry.get_friction(2, 2)
        frozen_friction = grid_frozen.get_friction(2, 2)

        assert frozen_friction < dry_friction
