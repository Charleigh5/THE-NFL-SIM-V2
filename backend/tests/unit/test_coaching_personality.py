from app.services.coaching_personality import (
    PERSONALITY_PROFILES,
    CoachingPersonality,
    create_playcaller_config,
    get_personality_for_coach,
    get_situational_modifiers,
)


class TestPersonalityProfiles:
    """Tests for coaching personality definitions."""

    def test_conservative_low_aggression(self):
        """Old School coaches have low aggression."""
        profile = PERSONALITY_PROFILES[CoachingPersonality.OLD_SCHOOL]
        assert profile.aggression == 0.15
        assert profile.run_pass_ratio == 0.65  # Run-heavy

    def test_gambler_high_aggression(self):
        """Gambler (Riverboat) coaches are very aggressive."""
        profile = PERSONALITY_PROFILES[CoachingPersonality.RIVERBOAT]
        assert profile.aggression == 0.80
        assert profile.run_pass_ratio == 0.45

    def test_balanced_middle_ground(self):
        """CEO coaches are balanced."""
        profile = PERSONALITY_PROFILES[CoachingPersonality.CEO]
        assert profile.aggression == 0.40
        assert profile.run_pass_ratio == 0.50


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

    def test_moderate_aggression_is_offensive_guru(self):
        """70-79 aggression = Offensive Guru."""
        personality = get_personality_for_coach(aggression_rating=75)
        assert personality == CoachingPersonality.GURU_OFF

    def test_low_aggression_is_old_school(self):
        """20-29 aggression = Old School."""
        personality = get_personality_for_coach(aggression_rating=25)
        assert personality == CoachingPersonality.OLD_SCHOOL


class TestPlayCallerIntegration:
    """Tests for PlayCaller config generation."""

    def test_create_config_ceo(self):
        """Create balanced config for CEO."""
        config = create_playcaller_config(
            personality=CoachingPersonality.CEO,
            score_diff=0,
            time_remaining=3600,
            is_home=True,
            quarter=1
        )

        assert "aggression" in config
        assert "run_pass_ratio" in config
        assert 0.35 <= config["aggression"] <= 0.55

    def test_create_config_analytics_trailing(self):
        """Analytics trailing should be very aggressive."""
        config = create_playcaller_config(
            personality=CoachingPersonality.ANALYTICS,
            score_diff=-14,
            time_remaining=600,
            is_home=False,
            quarter=4
        )

        # Should be capped at 1.0
        assert config["aggression"] <= 1.0
        # Should be very pass-heavy
        assert config["run_pass_ratio"] < 0.45
