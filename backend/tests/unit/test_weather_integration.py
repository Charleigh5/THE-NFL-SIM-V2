import pytest
import math
from unittest.mock import MagicMock
from app.engine.weather_effects import WeatherEffects
from app.models.weather import GameWeather, PrecipitationType, FieldCondition
from app.orchestrator.play_commands import FieldGoalCommand, PuntCommand

class TestWeatherIntegration:
    """Test suite for weather effects integration."""

    def test_weather_effects_modifiers(self):
        """Test the WeatherEffects calculator directly."""
        # Test High Wind
        weather = GameWeather(wind_speed=20.0, temperature=75.0)
        effects = WeatherEffects(weather)
        acc_mod, dist_mod = effects.get_passing_modifiers()

        # 1% per mph over 10 -> 10 * 0.01 = 0.1 penalty
        assert acc_mod == pytest.approx(0.9, 0.01)
        # 0.5% per mph over 10 -> 10 * 0.005 = 0.05 penalty
        assert dist_mod == pytest.approx(0.95, 0.01)

        # Test Cold/Snow
        weather = GameWeather(
            precipitation_type=PrecipitationType.SNOW.value,
            temperature=10.0,
            field_condition=FieldCondition.SNOWY.value
        )
        effects = WeatherEffects(weather)

        # Fumble mod: 1.15 (Snowy) * 1.1 (Cold < 20) = 1.265
        fumble_mod = effects.get_fumble_probability_modifier()
        assert fumble_mod == pytest.approx(1.265, 0.01)

    def test_field_goal_weather_impact(self):
        """Test weather impact on field goal success."""
        # Setup context with bad weather for kicking
        weather_config = {
            "wind_speed": 20.0, # Strong wind
            "temperature": 30.0, # Freezing
            "precipitation_type": "Snow"
        }
        context = {"weather": weather_config}

        # 40 yard FG
        # Base success: 100 - (40-20)*2 = 60
        # Wind penalty: (20-10)*1.5 = 15
        # Cold penalty: 5
        # Precip penalty: 5
        # Expected success base: 60 - 15 - 5 - 5 = 35

        # This is probabilistic, so we can't assert the result,
        # but we can verify the code path doesn't crash
        cmd = FieldGoalCommand([], [], distance=40)

        # Mock RNG to force specific outcomes if needed,
        # but here we just check it runs
        rng = MagicMock()
        rng.randint.return_value = 50 # Would fail if threshold is 35

        result = cmd.execute(context, rng=rng)

        # With 35 thresh and 50 roll, should fail
        assert result.is_turnover
        assert "NO GOOD" in result.description
        assert "battling strong winds" in result.description

    def test_punt_weather_impact(self):
        """Test weather impact on punt distance."""
        weather_config = {
            "wind_speed": 20.0,
            "temperature": 75.0
        }
        context = {"weather": weather_config}

        cmd = PuntCommand([], [])
        rng = MagicMock()
        rng.randint.side_effect = [45, 5] # Distance, Return

        # Base distance 45
        # Wind penalty: (20-10)*0.5 = 5
        # Expected net: -(40 - 5) = -35

        result = cmd.execute(context, rng=rng)
        assert result.yards_gained == -35
