#!/usr/bin/env python3
"""
Phase 4: HIVE Environment Tests
================================
Unit tests for environment physics modules.

Context7 Best Practices:
- pytest fixtures for state setup
- Integration tests for combined effects
"""

import pytest
from typing import List

from app.engine.hive import (
    # Turf
    TurfGrid, TurfType, TurfCondition, WeatherEffect,
    # Equipment
    EquipmentPhysics, PlayerEquipment, CleatType, GloveType, HelmetType,
    # Weather
    WeatherPhysics, GameWeather, WindDirection, PrecipitationType,
)


# ============================================================================
# TURF GRID TESTS
# ============================================================================

class TestTurfGrid:
    """Tests for TurfGrid."""

    @pytest.fixture
    def grid(self):
        return TurfGrid(turf_type=TurfType.NATURAL_GRASS)

    def test_grid_initialization(self, grid):
        """Grid initializes with 100 zones at 100%."""
        assert len(grid.state.zones) == 10
        assert len(grid.state.zones[0]) == 10
        assert grid.state.average_integrity == 100.0

    def test_position_to_zone(self, grid):
        """Position conversion works correctly."""
        # Center of field, 50-yard line
        row, col = grid.position_to_zone(50, 0)
        assert row == 5
        assert col == 5

        # Left sideline, own endzone
        row, col = grid.position_to_zone(0, -26)
        assert row == 0
        assert col == 0

    def test_zone_degradation(self, grid):
        """Zones degrade when plays occur."""
        initial = grid.get_zone(5, 5).integrity

        grid.record_play(50, 55, 0, 5, is_run_play=True)

        # Zone should be degraded
        assert grid.get_zone(5, 5).integrity < initial

    def test_friction_calculation(self, grid):
        """Friction affected by integrity and weather."""
        base_friction = grid.get_friction(5, 5)

        # Damage the zone
        zone = grid.get_zone(5, 5)
        zone.degrade(50)

        damaged_friction = grid.get_friction(5, 5)
        assert damaged_friction < base_friction

    def test_weather_affects_friction(self, grid):
        """Weather modifies friction."""
        dry_friction = grid.get_friction(5, 5)

        grid.set_weather(WeatherEffect.WET)
        wet_friction = grid.get_friction(5, 5)

        assert wet_friction < dry_friction

    def test_injury_modifier(self, grid):
        """Damaged turf increases injury risk."""
        pristine_mod = grid.get_injury_modifier(5, 5)

        zone = grid.get_zone(5, 5)
        zone.degrade(70)

        damaged_mod = grid.get_injury_modifier(5, 5)
        assert damaged_mod > pristine_mod

    def test_weekly_recovery(self, grid):
        """Turf recovers between games."""
        zone = grid.get_zone(5, 5)
        zone.degrade(30)
        damaged = zone.integrity

        grid.weekly_recovery()

        assert zone.integrity > damaged

    def test_condition_states(self, grid):
        """Zone conditions update based on integrity."""
        zone = grid.get_zone(5, 5)

        assert zone.condition == TurfCondition.PRISTINE

        zone.degrade(40)
        assert zone.condition == TurfCondition.WORN

        zone.degrade(40)
        assert zone.condition == TurfCondition.DESTROYED

    def test_serialization(self, grid):
        """Grid serializes to dict."""
        data = grid.to_dict()

        assert "turf_type" in data
        assert "zones" in data
        assert len(data["zones"]) == 10


# ============================================================================
# EQUIPMENT TESTS
# ============================================================================

class TestEquipmentPhysics:
    """Tests for EquipmentPhysics."""

    @pytest.fixture
    def physics(self):
        return EquipmentPhysics()

    @pytest.fixture
    def skill_equipment(self):
        return PlayerEquipment(
            cleat_type=CleatType.MOLDED,
            cleat_cut="LOW",
            glove_type=GloveType.HIGH_GRIP,
        )

    def test_grip_modifier_base(self, physics, skill_equipment):
        """Base grip is calculated correctly."""
        grip = physics.get_grip_modifier(skill_equipment)
        assert 0.8 < grip < 1.2

    def test_detachable_cleats_better_in_rain(self, physics):
        """Detachable cleats perform better in bad weather."""
        molded = PlayerEquipment(cleat_type=CleatType.MOLDED)
        detachable = PlayerEquipment(cleat_type=CleatType.DETACHABLE)

        molded_wet = physics.get_grip_modifier(molded, weather="WET")
        detach_wet = physics.get_grip_modifier(detachable, weather="WET")

        assert detach_wet > molded_wet

    def test_agility_by_cut(self, physics):
        """Lower cut cleats improve agility."""
        low = PlayerEquipment(cleat_cut="LOW")
        high = PlayerEquipment(cleat_cut="HIGH")

        assert physics.get_agility_modifier(low) > physics.get_agility_modifier(high)

    def test_ankle_injury_by_cut(self, physics):
        """Higher cut cleats reduce ankle injury risk."""
        low = PlayerEquipment(cleat_cut="LOW")
        high = PlayerEquipment(cleat_cut="HIGH")

        assert physics.get_ankle_injury_modifier(low) > physics.get_ankle_injury_modifier(high)

    def test_catching_modifier(self, physics, skill_equipment):
        """High grip gloves improve catching."""
        no_glove = PlayerEquipment(glove_type=GloveType.NONE)

        with_gloves = physics.get_catching_modifier(skill_equipment)
        without = physics.get_catching_modifier(no_glove)

        assert with_gloves > without

    def test_high_grip_wet_penalty(self, physics):
        """High grip gloves lose effectiveness when wet."""
        equipment = PlayerEquipment(glove_type=GloveType.HIGH_GRIP)

        dry = physics.get_catching_modifier(equipment, weather="DRY")
        wet = physics.get_catching_modifier(equipment, weather="WET")

        assert wet < dry

    def test_helmet_protection(self, physics):
        """Better helmets provide more protection."""
        standard = PlayerEquipment(helmet_type=HelmetType.STANDARD)
        revolution = PlayerEquipment(helmet_type=HelmetType.REVOLUTION)

        assert physics.get_head_injury_reduction(revolution) > physics.get_head_injury_reduction(standard)

    def test_recommend_loadout(self, physics):
        """Equipment recommendation returns valid loadout."""
        loadout = physics.recommend_loadout("skill", "WET", "NATURAL")

        assert loadout.cleat_type == CleatType.DETACHABLE
        assert loadout.glove_type == GloveType.ALL_WEATHER


# ============================================================================
# WEATHER TESTS
# ============================================================================

class TestWeatherPhysics:
    """Tests for WeatherPhysics."""

    @pytest.fixture
    def physics(self):
        return WeatherPhysics()

    @pytest.fixture
    def calm_weather(self):
        return GameWeather(temperature_f=70, wind_speed_mph=0)

    @pytest.fixture
    def windy_weather(self):
        return GameWeather(
            temperature_f=50,
            wind_speed_mph=20,
            wind_direction=WindDirection.HEADWIND,
        )

    @pytest.fixture
    def rainy_weather(self):
        return GameWeather(
            temperature_f=55,
            precipitation=PrecipitationType.HEAVY_RAIN,
        )

    def test_dome_no_effects(self, physics):
        """Dome games have no weather effects."""
        weather = GameWeather(
            wind_speed_mph=30,
            precipitation=PrecipitationType.HEAVY_SNOW,
            is_dome=True,
        )

        dist, acc = physics.calculate_pass_wind_effect(weather, 0, 30)
        assert dist == 0 and acc == 0

    def test_headwind_reduces_distance(self, physics, windy_weather):
        """Headwind reduces pass distance."""
        dist, _ = physics.calculate_pass_wind_effect(windy_weather, 0, 40)
        assert dist < 0

    def test_tailwind_adds_distance(self, physics):
        """Tailwind adds to pass distance."""
        weather = GameWeather(
            wind_speed_mph=15,
            wind_direction=WindDirection.TAILWIND,
        )
        dist, _ = physics.calculate_pass_wind_effect(weather, 0, 40)
        assert dist > 0

    def test_crosswind_accuracy_penalty(self, physics):
        """Crosswind increases accuracy penalty."""
        crosswind = GameWeather(
            wind_speed_mph=15,
            wind_direction=WindDirection.CROSSWIND_LEFT,
        )
        headwind = GameWeather(
            wind_speed_mph=15,
            wind_direction=WindDirection.HEADWIND,
        )

        _, cross_acc = physics.calculate_pass_wind_effect(crosswind, 0, 30)
        _, head_acc = physics.calculate_pass_wind_effect(headwind, 0, 30)

        assert cross_acc > head_acc

    def test_hot_weather_stamina(self, physics):
        """Hot weather increases stamina drain."""
        hot = GameWeather(temperature_f=95)
        cool = GameWeather(temperature_f=60)

        hot_mod = physics.calculate_stamina_modifier(hot)
        cool_mod = physics.calculate_stamina_modifier(cool)

        assert hot_mod > cool_mod

    def test_cold_weather_stamina(self, physics):
        """Cold weather reduces stamina drain."""
        cold = GameWeather(temperature_f=20)

        mod = physics.calculate_stamina_modifier(cold)
        assert mod < 1.0

    def test_cramp_risk(self, physics):
        """Hot weather creates cramp risk."""
        hot = GameWeather(temperature_f=100, humidity_pct=80)

        risk = physics.calculate_cramp_risk(hot, player_fatigue=60)
        assert risk > 0

    def test_rain_ball_handling(self, physics, rainy_weather):
        """Rain decreases ball handling."""
        mod = physics.calculate_ball_handling_modifier(rainy_weather)
        assert mod < 1.0

    def test_visibility_in_snow(self, physics):
        """Snow decreases visibility."""
        snow = GameWeather(precipitation=PrecipitationType.HEAVY_SNOW)

        mod = physics.calculate_visibility_modifier(snow)
        assert mod < 1.0

    def test_combined_modifiers(self, physics, windy_weather):
        """Combined modifiers returns all effects."""
        mods = physics.get_combined_modifiers(windy_weather)

        assert "stamina_drain" in mods
        assert "ball_handling" in mods
        assert "visibility" in mods


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestHiveIntegration:
    """Integration tests for HIVE environment."""

    def test_weather_affects_turf(self):
        """Weather effect propagates to turf friction."""
        grid = TurfGrid(turf_type=TurfType.NATURAL_GRASS)

        dry_friction = grid.get_friction(5, 5)

        grid.set_weather(WeatherEffect.MUDDY)
        muddy_friction = grid.get_friction(5, 5)

        assert muddy_friction < dry_friction

    def test_equipment_turf_interaction(self):
        """Equipment modifiers interact with turf friction."""
        grid = TurfGrid(turf_type=TurfType.NATURAL_GRASS)
        equipment = EquipmentPhysics()
        player = PlayerEquipment(cleat_type=CleatType.DETACHABLE)

        turf_friction = grid.get_friction(5, 5)
        grip = equipment.get_grip_modifier(player, turf_friction)

        assert grip > 0

    def test_full_environment_calculation(self):
        """Full environment affects player performance."""
        # Setup
        grid = TurfGrid(turf_type=TurfType.NATURAL_GRASS)
        grid.set_weather(WeatherEffect.WET)

        weather = GameWeather(
            temperature_f=45,
            wind_speed_mph=15,
            wind_direction=WindDirection.HEADWIND,
            precipitation=PrecipitationType.LIGHT_RAIN,
        )

        weather_physics = WeatherPhysics()
        equipment_physics = EquipmentPhysics()

        # Calculate combined modifiers
        turf_friction = grid.get_friction(5, 5)
        injury_mod = grid.get_injury_modifier(5, 5)

        player = equipment_physics.recommend_loadout("skill", "WET", "NATURAL")
        grip = equipment_physics.get_grip_modifier(player, turf_friction, "WET")
        catching = equipment_physics.get_catching_modifier(player, "WET")

        weather_mods = weather_physics.get_combined_modifiers(weather)

        # All should be affected
        assert turf_friction < 1.0
        assert 0 < grip < 1.5
        assert weather_mods["ball_handling"] < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
