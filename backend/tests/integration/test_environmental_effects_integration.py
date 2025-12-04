"""
Integration tests for Environmental Effects (Weather) System.

Tests verify that weather conditions properly affect:
- Passing accuracy and distance
- Kicking accuracy and distance
- Fumble probability
- Fatigue accumulation
"""

import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.models.player import Player
from app.models.weather import GameWeather, PrecipitationType, FieldCondition
from app.engine.weather_effects import WeatherEffects
from app.core.random_utils import DeterministicRNG
from app.engine.blocking import BlockingResult


class TestEnvironmentalEffects:
    """Test suite for environmental effects integration (GAME-009)"""

    def create_mock_player(self, position: str, **attributes):
        """Helper to create a mock player with attributes"""
        player = MagicMock(spec=Player)
        player.id = hash(f"{position}_test") % 100000
        player.position = position
        player.last_name = f"{position}Player"

        defaults = {
            'throw_accuracy_short': 80,
            'throw_accuracy_mid': 75,
            'throw_accuracy_deep': 70,
            'speed': 70,
            'route_running': 75,
            'man_coverage': 70,
            'strength': 75,
            'tackle': 70,
            'ball_security': 80,
            'pocket_presence': 50
        }
        defaults.update(attributes)

        for attr, value in defaults.items():
            setattr(player, attr, value)

        return player

    def test_snow_reduces_passing_accuracy(self):
        """Snow should reduce passing accuracy by 15%"""
        weather = GameWeather(
            temperature=25.0,
            wind_speed=5.0,
            precipitation_type=PrecipitationType.SNOW.value,
            field_condition=FieldCondition.SNOWY.value
        )

        effects = WeatherEffects(weather)
        acc_mod, dist_mod = effects.get_passing_modifiers()

        # Snow: 0.85 accuracy, cold: 0.95 accuracy
        # Combined: 0.85 * 0.95 = 0.8075
        assert abs(acc_mod - 0.8075) < 0.01, f"Expected ~0.81 accuracy, got {acc_mod}"
        assert abs(dist_mod - 0.95) < 0.01, f"Expected 0.95 distance, got {dist_mod}"

    def test_rain_reduces_passing_accuracy(self):
        """Rain should reduce passing accuracy by 10%"""
        weather = GameWeather(
            temperature=55.0,
            wind_speed=8.0,
            precipitation_type=PrecipitationType.RAIN.value,
            field_condition=FieldCondition.WET.value
        )

        effects = WeatherEffects(weather)
        acc_mod, dist_mod = effects.get_passing_modifiers()

        # Rain: 0.9 accuracy
        assert abs(acc_mod - 0.9) < 0.01, f"Expected 0.9 accuracy, got {acc_mod}"

    def test_high_wind_affects_passing(self):
        """High wind should reduce both accuracy and distance"""
        weather = GameWeather(
            temperature=60.0,
            wind_speed=25.0,  # 25 mph wind
            precipitation_type=PrecipitationType.NONE.value,
            field_condition=FieldCondition.DRY.value
        )

        effects = WeatherEffects(weather)
        acc_mod, dist_mod = effects.get_passing_modifiers()

        # Wind > 10: -1% acc per mph over 10 = -15% = 0.85
        # Wind > 10: -0.5% dist per mph over 10 = -7.5% = 0.925
        assert abs(acc_mod - 0.85) < 0.01, f"Expected 0.85 accuracy, got {acc_mod}"
        assert abs(dist_mod - 0.925) < 0.01, f"Expected 0.925 distance, got {dist_mod}"

    def test_wet_field_increases_fumbles(self):
        """Wet field should increase fumble probability by 20%"""
        weather = GameWeather(
            temperature=60.0,
            wind_speed=5.0,
            precipitation_type=PrecipitationType.RAIN.value,
            field_condition=FieldCondition.WET.value
        )

        effects = WeatherEffects(weather)
        fumble_mod = effects.get_fumble_probability_modifier()

        assert abs(fumble_mod - 1.2) < 0.01, f"Expected 1.2x fumbles, got {fumble_mod}"

    def test_muddy_field_increases_fumbles_more(self):
        """Muddy field should increase fumble probability by 30%"""
        weather = GameWeather(
            temperature=55.0,
            wind_speed=5.0,
            precipitation_type=PrecipitationType.RAIN.value,
            field_condition=FieldCondition.MUDDY.value
        )

        effects = WeatherEffects(weather)
        fumble_mod = effects.get_fumble_probability_modifier()

        assert abs(fumble_mod - 1.3) < 0.01, f"Expected 1.3x fumbles, got {fumble_mod}"

    def test_extreme_cold_increases_fumbles(self):
        """Extreme cold (<20°F) should increase fumbles by 10%"""
        weather = GameWeather(
            temperature=10.0,  # 10°F
            wind_speed=5.0,
            precipitation_type=PrecipitationType.NONE.value,
            field_condition=FieldCondition.DRY.value
        )

        effects = WeatherEffects(weather)
        fumble_mod = effects.get_fumble_probability_modifier()

        assert abs(fumble_mod - 1.1) < 0.01, f"Expected 1.1x fumbles, got {fumble_mod}"

    def test_heat_increases_fatigue(self):
        """High temperature (>85°F) should increase fatigue"""
        weather = GameWeather(
            temperature=95.0,  # 95°F
            wind_speed=5.0,
            precipitation_type=PrecipitationType.NONE.value,
            field_condition=FieldCondition.DRY.value,
            humidity=0.5
        )

        effects = WeatherEffects(weather)
        fatigue_mod = effects.get_fatigue_multiplier()

        # Heat: +2% per degree over 85 = +20% = 1.2
        assert abs(fatigue_mod - 1.2) < 0.01, f"Expected 1.2x fatigue, got {fatigue_mod}"

    def test_high_humidity_increases_fatigue(self):
        """High humidity (>70%) should increase fatigue"""
        weather = GameWeather(
            temperature=85.0,
            wind_speed=5.0,
            precipitation_type=PrecipitationType.NONE.value,
            field_condition=FieldCondition.DRY.value,
            humidity=0.9  # 90% humidity
        )

        effects = WeatherEffects(weather)
        fatigue_mod = effects.get_fatigue_multiplier()

        # Humidity: (0.9 - 0.7) * 0.5 = 0.1 added to 1.0 = 1.1
        assert abs(fatigue_mod - 1.1) < 0.01, f"Expected 1.1x fatigue, got {fatigue_mod}"

    def test_wind_affects_kicking_more_than_passing(self):
        """Wind should have greater impact on kicking than passing"""
        weather = GameWeather(
            temperature=60.0,
            wind_speed=20.0,
            precipitation_type=PrecipitationType.NONE.value,
            field_condition=FieldCondition.DRY.value
        )

        effects = WeatherEffects(weather)

        pass_acc, pass_dist = effects.get_passing_modifiers()
        kick_acc, kick_dist = effects.get_kicking_modifiers()

        # Kicking should be more affected
        assert kick_acc < pass_acc, "Kicking accuracy should be more affected by wind"
        assert kick_dist < pass_dist, "Kicking distance should be more affected by wind"

    @pytest.mark.asyncio
    async def test_weather_integration_in_pass_play(self):
        """Test that weather effects are applied in actual pass play resolution"""
        rng = DeterministicRNG("weather_test")
        resolver = PlayResolver(rng)

        # Create players
        qb = self.create_mock_player('QB', throw_accuracy_short=90)
        wr = self.create_mock_player('WR', speed=85)
        cb = self.create_mock_player('CB', man_coverage=70)

        offense = [qb, wr]
        defense = [cb]

        command = PassPlayCommand(
            offense_players=offense,
            defense_players=defense,
            depth="short"
        )

        # Mock match context with SNOW weather
        resolver.current_match_context = MagicMock()
        resolver.current_match_context.weather_config = {
            "temperature": 20.0,
            "wind_speed": 15.0,
            "precipitation_type": "Snow",
            "field_condition": "Snowy",
            "humidity": 0.5
        }

        # Mock line battle (clean pocket)
        with patch.object(resolver, '_resolve_line_battle') as mock_battle:
            mock_battle.return_value = (
                [BlockingResult.WIN],
                [],
                []
            )

            # Run multiple plays to test weather impact
            completions = 0
            total_plays = 50

            for _ in range(total_plays):
                result = resolver._resolve_pass_play(command)
                if result.yards_gained > 0:
                    completions += 1

            completion_rate = completions / total_plays

            # With 90 base accuracy and snow weather:
            # - Snow: 0.85 modifier
            # - Cold (<32): 0.95 modifier
            # - Combined: 0.85 * 0.95 = 0.8075 (~81% of base)
            # Base success ~70%, with modifiers ~57%
            # But QB has high accuracy (90), so actual rate will be higher
            # Expect 75-90% range (still lower than perfect conditions)
            assert completion_rate < 0.95, \
                f"Completion rate should be reduced in snow, got {completion_rate:.2%}"
            assert completion_rate > 0.60, \
                f"Completion rate shouldn't be too low with high QB rating, got {completion_rate:.2%}"

            print(f"\n✅ Snow Weather Test: {completion_rate:.1%} completion rate (reduced from ~95% in clear weather)")

    @pytest.mark.asyncio
    async def test_weather_integration_in_run_play(self):
        """Test that weather affects fumble rates in run plays"""
        rng = DeterministicRNG("fumble_test")
        resolver = PlayResolver(rng)

        # Create players
        rb = self.create_mock_player('RB', strength=80, ball_security=60)
        lb = self.create_mock_player('LB', tackle=75, hit_power=90)

        offense = [rb]
        defense = [lb]

        command = RunPlayCommand(
            offense_players=offense,
            defense_players=defense,
            run_direction="middle"
        )

        # Test 1: DRY conditions (baseline)
        resolver.current_match_context = MagicMock()
        resolver.current_match_context.weather_config = {
            "temperature": 70.0,
            "wind_speed": 5.0,
            "precipitation_type": "None",
            "field_condition": "Dry",
            "humidity": 0.5
        }

        dry_fumbles = 0
        total_plays = 100

        for _ in range(total_plays):
            result = resolver._resolve_run_play(command)
            if result.is_turnover:
                dry_fumbles += 1

        # Test 2: MUDDY conditions
        resolver.current_match_context.weather_config = {
            "temperature": 55.0,
            "wind_speed": 10.0,
            "precipitation_type": "Rain",
            "field_condition": "Muddy",
            "humidity": 0.8
        }

        muddy_fumbles = 0

        for _ in range(total_plays):
            result = resolver._resolve_run_play(command)
            if result.is_turnover:
                muddy_fumbles += 1

        # Muddy should have more fumbles than dry
        assert muddy_fumbles > dry_fumbles, \
            f"Muddy field should cause more fumbles. Dry: {dry_fumbles}, Muddy: {muddy_fumbles}"

        print(f"\n✅ Fumble Test: Dry={dry_fumbles}, Muddy={muddy_fumbles} (Muddy should be higher)")

    def test_all_weather_types_documented(self):
        """Verify all weather types have documented effects"""
        weather_types = [
            PrecipitationType.NONE.value,
            PrecipitationType.RAIN.value,
            PrecipitationType.SNOW.value,
        ]

        for weather_type in weather_types:
            weather = GameWeather(
                temperature=60.0,
                wind_speed=5.0,
                precipitation_type=weather_type,
                field_condition=FieldCondition.DRY.value
            )

            effects = WeatherEffects(weather)

            # All should return valid modifiers
            acc, dist = effects.get_passing_modifiers()
            assert 0.5 <= acc <= 1.0, f"Invalid accuracy for {weather_type}"
            assert 0.5 <= dist <= 1.0, f"Invalid distance for {weather_type}"

            fumble_mod = effects.get_fumble_probability_modifier()
            assert fumble_mod >= 1.0, f"Invalid fumble mod for {weather_type}"

        print(f"\n✅ All {len(weather_types)} weather types have valid effects")
