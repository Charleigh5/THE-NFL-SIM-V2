import pytest
from app.services.coaching_personality import (
    CoachingPersonality,
    PersonalityProfile,
    PERSONALITY_PROFILES,
    get_situational_modifiers,
    apply_personality_modifiers,
    get_personality_for_coach,
    create_playcaller_config,
)


class TestPersonalityProfiles:
    """Tests for coaching personality definitions."""

    def test_conservative_low_aggression(self):
        """Conservative coaches have low aggression."""
        profile = PERSONALITY_PROFILES[CoachingPersonality.CONSERVATIVE]
        assert profile.aggression == 0.20
        assert profile.run_pass_ratio == 0.55  # Run-heavy

    def test_gambler_high_aggression(self):
        """Gambler coaches are very aggressive."""
        profile = PERSONALITY_PROFILES[CoachingPersonality.GAMBLER]
        assert profile.aggression == 0.90
        assert profile.run_pass_ratio == 0.30  # Pass-heavy

    def test_balanced_middle_ground(self):
        """Balanced coaches are in the middle."""
        profile = PERSONALITY_PROFILES[CoachingPersonality.BALANCED]
        assert 0.4 <= profile.aggression <= 0.6
        assert 0.4 <= profile.run_pass_ratio <= 0.5


class TestSituationalModifiers:
    """Tests for game situation adjustments."""

    def test_home_field_boost(self):
        """Playing at home increases aggression."""
        mods = get_situational_modifiers(
            score_diff=0, time_remaining_seconds=3600,
            is_home=True, quarter=1
        )
        assert mods["aggression"] > 0

    def test_trailing_big_increases_aggression(self):
        """Losing by 14+ increases aggression significantly."""
        mods = get_situational_modifiers(
            score_diff=-17, time_remaining_seconds=1800,
            is_home=False, quarter=3
        )
        assert mods["aggression"] >= 0.20
        assert mods["run_ratio"] < 0  # More passing

    def test_leading_big_decreases_aggression(self):
        """Winning by 14+ decreases aggression."""
        mods = get_situational_modifiers(
            score_diff=21, time_remaining_seconds=1800,
            is_home=True, quarter=3
        )
        assert mods["aggression"] < 0
        assert mods["run_ratio"] > 0  # More running

    def test_late_game_trailing(self):
        """Final 5 minutes while trailing increases urgency."""
        mods = get_situational_modifiers(
            score_diff=-7, time_remaining_seconds=200,
            is_home=True, quarter=4
        )
        assert mods["aggression"] > 0.10


class TestPersonalityDetermination:
    """Tests for determining personality from coach attributes."""

    def test_high_aggression_is_gambler(self):
        """80+ aggression rating = Gambler personality."""
        personality = get_personality_for_coach(aggression_rating=85)
        assert personality == CoachingPersonality.GAMBLER

    def test_moderate_aggression_is_aggressive(self):
        """60-79 aggression = Aggressive personality."""
        personality = get_personality_for_coach(aggression_rating=65)
        assert personality == CoachingPersonality.AGGRESSIVE

    def test_low_aggression_is_conservative(self):
        """<40 aggression = Conservative personality."""
        personality = get_personality_for_coach(aggression_rating=30)
        assert personality == CoachingPersonality.CONSERVATIVE


class TestPlayCallerIntegration:
    """Tests for PlayCaller config generation."""

    def test_create_config_balanced(self):
        """Create balanced config for PlayCaller."""
        config = create_playcaller_config(
            personality=CoachingPersonality.BALANCED,
            score_diff=0,
            time_remaining=3600,
            is_home=True,
            quarter=1
        )

        assert "aggression" in config
        assert "run_pass_ratio" in config
        assert 0.4 <= config["aggression"] <= 0.6

    def test_create_config_gambler_trailing(self):
        """Gambler trailing should be very aggressive."""
        config = create_playcaller_config(
            personality=CoachingPersonality.GAMBLER,
            score_diff=-14,
            time_remaining=600,
            is_home=False,
            quarter=4
        )

        # Should be capped at 1.0
        assert config["aggression"] <= 1.0
        # Should be very pass-heavy
        assert config["run_pass_ratio"] < 0.30
