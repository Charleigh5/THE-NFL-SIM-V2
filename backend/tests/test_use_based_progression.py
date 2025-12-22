"""
Test Use-Based Skill Progression
=================================

Unit tests for Skyrim-style use-based progression system.
Tests follow AAA pattern with comprehensive coverage.
"""
import pytest
from unittest.mock import MagicMock
from dataclasses import dataclass
from typing import Optional, Dict

from app.services.use_based_progression import (
    UseBasedProgression,
    ActionType,
    ACTION_XP_AWARDS,
    DEV_TRAIT_MULTIPLIERS,
    get_age_multiplier,
    get_xp_threshold,
)


# =============================================================================
# MOCK PLAYER FIXTURE
# =============================================================================

@dataclass
class MockPlayer:
    """Mock player for testing progression."""
    id: int = 1
    age: int = 25
    development_trait: str = "NORMAL"
    attribute_xp: Optional[Dict[str, int]] = None

    # Attributes that can be improved
    throw_accuracy_short: int = 70
    throw_accuracy_mid: int = 68
    throw_accuracy_deep: int = 65
    throw_power: int = 72
    awareness: int = 60
    pocket_presence: int = 55
    throw_on_the_run: int = 58

    agility: int = 75
    acceleration: int = 80
    speed: int = 85
    juke_move: int = 70
    break_tackle: int = 65
    trucking: int = 60
    stiff_arm: int = 62

    catching: int = 50
    catch_in_traffic: int = 48
    route_running: int = 55

    tackle: int = 70
    pursuit: int = 72
    pass_rush: int = 75
    power_moves: int = 68
    finesse_moves: int = 65
    play_recognition: int = 62
    hit_power: int = 70

    man_coverage: int = 60
    zone_coverage: int = 65

    run_block: int = 70
    pass_block: int = 68
    strength: int = 75

    kick_power: int = 80
    kick_accuracy: int = 78

    def __post_init__(self):
        if self.attribute_xp is None:
            self.attribute_xp = {}


@pytest.fixture
def young_star_player():
    """Young player with Star dev trait (fast learner)."""
    return MockPlayer(
        id=1,
        age=22,
        development_trait="STAR",
        throw_accuracy_deep=70,
        awareness=55,
    )


@pytest.fixture
def veteran_normal_player():
    """Veteran player with Normal dev trait (slow learner)."""
    return MockPlayer(
        id=2,
        age=32,
        development_trait="NORMAL",
        pass_rush=85,
        tackle=82,
    )


@pytest.fixture
def superstar_rb():
    """Superstar RB for rushing action tests."""
    return MockPlayer(
        id=3,
        age=25,
        development_trait="SUPERSTAR",
        speed=92,
        agility=90,
        break_tackle=85,
    )


# =============================================================================
# ACTION XP AWARD TESTS
# =============================================================================

class TestActionXPAwards:
    """Tests for UseBasedProgression.award_action_xp."""

    def test_pass_completion_awards_xp(self, young_star_player):
        """Short pass completion should award XP to throw_accuracy_short."""
        # Arrange
        player = young_star_player

        # Act
        gains = UseBasedProgression.award_action_xp(
            player,
            ActionType.PASS_COMPLETION_SHORT,
            {}
        )

        # Assert
        assert len(gains) > 0
        accuracy_gain = next((g for g in gains if g.attribute_name == "throw_accuracy_short"), None)
        assert accuracy_gain is not None
        assert accuracy_gain.base_xp == 3
        assert accuracy_gain.final_xp > accuracy_gain.base_xp  # Multiplied by dev trait

    def test_deep_pass_awards_more_xp(self, young_star_player):
        """Deep passes should award more XP than short passes."""
        player = young_star_player

        short_gains = UseBasedProgression.award_action_xp(
            player, ActionType.PASS_COMPLETION_SHORT, {}
        )
        deep_gains = UseBasedProgression.award_action_xp(
            player, ActionType.PASS_COMPLETION_DEEP, {}
        )

        short_xp = sum(g.final_xp for g in short_gains)
        deep_xp = sum(g.final_xp for g in deep_gains)

        assert deep_xp > short_xp

    def test_sack_awards_pass_rush_xp(self, veteran_normal_player):
        """Sack should award significant XP to pass_rush."""
        player = veteran_normal_player

        gains = UseBasedProgression.award_action_xp(
            player, ActionType.SACK, {}
        )

        pass_rush_gain = next((g for g in gains if g.attribute_name == "pass_rush"), None)
        assert pass_rush_gain is not None
        assert pass_rush_gain.base_xp == 5  # High value for impact play

    def test_interception_awards_coverage_xp(self):
        """Interception should boost zone_coverage significantly."""
        player = MockPlayer(id=5, zone_coverage=70)

        gains = UseBasedProgression.award_action_xp(
            player, ActionType.INTERCEPTION, {}
        )

        zone_gain = next((g for g in gains if g.attribute_name == "zone_coverage"), None)
        assert zone_gain is not None
        assert zone_gain.base_xp == 5


# =============================================================================
# MULTIPLIER TESTS
# =============================================================================

class TestMultipliers:
    """Tests for dev trait, age, and context multipliers."""

    def test_superstar_gets_1_5x_multiplier(self, superstar_rb):
        """Superstar players get 1.5x XP."""
        player = superstar_rb

        gains = UseBasedProgression.award_action_xp(
            player, ActionType.RUSHING_GAIN, {}
        )

        agility_gain = next((g for g in gains if g.attribute_name == "agility"), None)
        assert agility_gain is not None
        # Base XP is 1, should be 1.5 (rounded to 1 due to int conversion)
        # Combined with age multiplier of 1.0
        assert agility_gain.final_xp >= 1
        assert agility_gain.multipliers_applied["dev_trait"] == 1.5

    def test_young_player_learns_faster(self):
        """Players under 24 get bonus from both phase (Ascension) and age (young)."""
        # New behavior: combines phase + development modifiers
        # Age 21 with DEFAULT position: phase=ASCENSION (1.25) + dev_mod(0.8-1.2) -> avg
        mult = get_age_multiplier(21)
        assert mult > 1.0  # Young players definitely learn faster
        assert mult < 1.5  # But not excessively so

    def test_prime_player_baseline(self):
        """Players 25-30 in PRIME phase get moderate multiplier."""
        # Age 25 is PRIME phase (1.0) but still young dev (1.0) -> 1.0
        assert get_age_multiplier(25) == pytest.approx(1.0, rel=0.15)
        # Age 28 is PRIME phase but older dev (0.8) -> avg around 0.9
        assert get_age_multiplier(28) == pytest.approx(0.9, rel=0.15)

    def test_veteran_learns_slower(self):
        """Players over 30 get reduced learning from both phase and age."""
        # Age 31+ is DECLINE phase (0.75) + old dev (0.5) -> avg 0.625
        assert get_age_multiplier(31) < 0.8
        # Age 35 is same bracket as 31 - both DECLINE + 31+ dev
        assert get_age_multiplier(35) <= get_age_multiplier(31)

    def test_red_zone_context_bonus(self, young_star_player):
        """Red zone plays get 1.5x context bonus."""
        player = young_star_player

        normal_gains = UseBasedProgression.award_action_xp(
            player, ActionType.TOUCHDOWN_PASS, {}
        )

        # Reset XP
        player.attribute_xp = {}

        red_zone_gains = UseBasedProgression.award_action_xp(
            player, ActionType.TOUCHDOWN_PASS, {"red_zone": True}
        )

        normal_xp = sum(g.final_xp for g in normal_gains)
        red_zone_xp = sum(g.final_xp for g in red_zone_gains)

        assert red_zone_xp > normal_xp
        # Int rounding can cause small variations - allow 20% tolerance
        assert red_zone_xp == pytest.approx(normal_xp * 1.5, rel=0.2)

    def test_goal_line_context_bonus(self, superstar_rb):
        """Goal line plays get 2.0x context bonus."""
        player = superstar_rb

        normal_gains = UseBasedProgression.award_action_xp(
            player, ActionType.RUSHING_TD, {}
        )
        normal_xp = sum(g.final_xp for g in normal_gains)

        player.attribute_xp = {}

        goal_line_gains = UseBasedProgression.award_action_xp(
            player, ActionType.RUSHING_TD, {"goal_line": True}
        )
        goal_line_xp = sum(g.final_xp for g in goal_line_gains)

        assert goal_line_xp == pytest.approx(normal_xp * 2.0, rel=0.1)


# =============================================================================
# LEVEL-UP TESTS
# =============================================================================

class TestLevelUp:
    """Tests for attribute level-up logic."""

    def test_low_rating_levels_up_with_100_xp(self):
        """Attributes under 60 need 100 XP to level up."""
        assert get_xp_threshold(50) == 100
        assert get_xp_threshold(59) == 100

    def test_mid_rating_needs_more_xp(self):
        """Mid-tier ratings need more XP."""
        assert get_xp_threshold(65) == 150
        assert get_xp_threshold(75) == 250

    def test_high_rating_needs_much_more_xp(self):
        """High ratings have substantial XP requirements."""
        # 80-84 = 400, 85-89 = 600
        assert get_xp_threshold(82) == 400
        assert get_xp_threshold(85) == 600
        assert get_xp_threshold(88) == 600

    def test_elite_rating_very_hard_to_improve(self):
        """Elite ratings (90+) are very hard to improve."""
        # 90-94 = 1000, 95-99 = 2000
        assert get_xp_threshold(90) == 1000
        assert get_xp_threshold(92) == 1000
        assert get_xp_threshold(95) == 2000
        assert get_xp_threshold(98) == 2000

    def test_level_up_applies_when_threshold_reached(self):
        """Attribute increases by 1 when XP threshold reached."""
        player = MockPlayer(
            id=10,
            awareness=55,  # Needs 100 XP to level up
            attribute_xp={"awareness": 100}
        )

        levelups = UseBasedProgression.check_and_apply_levelups(player)

        assert len(levelups) == 1
        assert levelups[0].attribute_name == "awareness"
        assert levelups[0].old_value == 55
        assert levelups[0].new_value == 56
        assert player.awareness == 56
        assert player.attribute_xp["awareness"] == 0  # XP consumed

    def test_excess_xp_rolls_over(self):
        """XP above threshold carries over to next level."""
        player = MockPlayer(
            id=11,
            tackle=59,  # Needs 100 XP
            attribute_xp={"tackle": 150}
        )

        UseBasedProgression.check_and_apply_levelups(player)

        assert player.tackle == 60
        assert player.attribute_xp["tackle"] == 50  # 150 - 100 = 50 remaining

    def test_multiple_level_ups_at_once(self):
        """Can gain multiple levels if enough XP accumulated."""
        player = MockPlayer(
            id=12,
            speed=55,  # Needs 100 XP each
            attribute_xp={"speed": 250}  # Enough for 2 levels
        )

        levelups = UseBasedProgression.check_and_apply_levelups(player)

        assert len(levelups) == 2
        assert player.speed == 57  # 55 + 2
        assert player.attribute_xp["speed"] == 50  # 250 - 100 - 100 = 50

    def test_cannot_exceed_99(self):
        """Attributes cap at 99."""
        player = MockPlayer(
            id=13,
            kick_accuracy=98,
            attribute_xp={"kick_accuracy": 5000}  # Way more than needed
        )

        levelups = UseBasedProgression.check_and_apply_levelups(player)

        assert player.kick_accuracy == 99  # Capped
        assert len(levelups) == 1


# =============================================================================
# INTEGRATION TEST
# =============================================================================

class TestProgressionIntegration:
    """Full workflow integration tests."""

    def test_full_game_progression_workflow(self, superstar_rb):
        """Simulate multiple plays and progression over a game."""
        player = superstar_rb
        # Reset XP before test
        player.attribute_xp = {}

        # Simulate several successful runs
        for _ in range(5):
            UseBasedProgression.award_action_xp(
                player, ActionType.RUSHING_GAIN, {}
            )

        # One big run
        UseBasedProgression.award_action_xp(
            player, ActionType.BIG_RUN, {}
        )

        # Two broken tackles
        for _ in range(2):
            UseBasedProgression.award_action_xp(
                player, ActionType.BROKEN_TACKLE, {}
            )

        # Check progression summary
        summary = UseBasedProgression.get_progression_summary(player)

        # Verify XP was accumulated for key attributes
        assert len(summary) > 0

        # Check that relevant attributes got XP
        # From RUSHING_GAIN: agility, acceleration
        # From BIG_RUN: speed, acceleration, agility
        # From BROKEN_TACKLE: break_tackle, trucking, strength
        assert player.attribute_xp.get("agility", 0) > 0
        assert player.attribute_xp.get("acceleration", 0) > 0
