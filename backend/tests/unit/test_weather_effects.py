import pytest
from app.models.weather import GameWeather, PrecipitationType, FieldCondition
from app.engine.weather_effects import WeatherEffects

def test_passing_modifiers_clear_weather():
    weather = GameWeather(
        temperature=70,
        wind_speed=0,
        precipitation_type=PrecipitationType.NONE.value,
        field_condition=FieldCondition.DRY.value
    )
    effects = WeatherEffects(weather)
    acc, dist = effects.get_passing_modifiers()
    assert acc == 1.0
    assert dist == 1.0

def test_passing_modifiers_heavy_wind():
    weather = GameWeather(
        temperature=70,
        wind_speed=20, # 10 over threshold
        precipitation_type=PrecipitationType.NONE.value
    )
    effects = WeatherEffects(weather)
    acc, dist = effects.get_passing_modifiers()
    # Accuracy: -1% per mph over 10 -> -10% -> 0.9
    # Distance: -0.5% per mph over 10 -> -5% -> 0.95
    assert acc == pytest.approx(0.9)
    assert dist == pytest.approx(0.95)

def test_passing_modifiers_rain():
    weather = GameWeather(
        temperature=70,
        wind_speed=0,
        precipitation_type=PrecipitationType.RAIN.value
    )
    effects = WeatherEffects(weather)
    acc, dist = effects.get_passing_modifiers()
    assert acc == 0.9
    assert dist == 1.0

def test_fumble_modifier_wet():
    weather = GameWeather(
        field_condition=FieldCondition.WET.value,
        temperature=70
    )
    effects = WeatherEffects(weather)
    mod = effects.get_fumble_probability_modifier()
    assert mod == 1.2

def test_fatigue_modifier_heat():
    weather = GameWeather(
        temperature=95, # 10 over 85
        humidity=0.5,
        field_condition=FieldCondition.DRY.value
    )
    effects = WeatherEffects(weather)
    mod = effects.get_fatigue_multiplier()
    # 1.0 + (10 * 0.02) = 1.2
    assert mod == pytest.approx(1.2)
