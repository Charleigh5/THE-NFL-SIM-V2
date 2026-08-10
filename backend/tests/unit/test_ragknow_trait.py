"""
Unit tests for the Ragknow trait.

Tests the legendary Ragknow trait that allows players to:
1. Play through injuries (severity 1-7) without performance penalties
2. Ignore permanent attribute degradation while injured
3. Recover 10% faster
"""

from unittest.mock import MagicMock

import pytest

from app.core import injury_config as InjuryConfig
from app.core.random_utils import DeterministicRNG
from app.models.player import Player
from app.rpg.injury_system import (
    apply_playing_injured_risk,
    calculate_injured_performance_penalty,
    get_player_toughness,
    player_has_ragknow,
)
from app.services.trait_service import TRAIT_CATALOG, TraitRarity


class TestRagknowTraitDefinition:
    """Tests for the Ragknow trait catalog entry."""

    def test_ragknow_exists_in_catalog(self):
        """Test that Ragknow trait is defined in the catalog."""
        assert "ragknow" in TRAIT_CATALOG

    def test_ragknow_is_legendary(self):
        """Test that Ragknow has legendary rarity."""
        ragknow = TRAIT_CATALOG["ragknow"]
        assert ragknow.rarity_tier == TraitRarity.LEGENDARY

    def test_ragknow_has_correct_effects(self):
        """Test that Ragknow has the required effects."""
        ragknow = TRAIT_CATALOG["ragknow"]

        assert ragknow.effects.get("ignore_injury_penalties") == 1.0
        assert ragknow.effects.get("max_playable_severity") == 7
        assert ragknow.effects.get("block_injury_degradation") == 1.0
        assert ragknow.effects.get("recovery_time_multiplier") == 0.90

    def test_ragknow_has_league_cap(self):
        """Test that Ragknow has a league-wide soft cap."""
        ragknow = TRAIT_CATALOG["ragknow"]
        assert ragknow.max_league_count == 3

    def test_ragknow_requires_veteran_status(self):
        """Test that Ragknow requires minimum experience."""
        ragknow = TRAIT_CATALOG["ragknow"]
        assert ragknow.min_experience == 5

    def test_ragknow_available_to_all_positions(self):
        """Test that Ragknow is position-agnostic."""
        ragknow = TRAIT_CATALOG["ragknow"]
        assert "ALL" in ragknow.position_requirements


class TestPlayerHasRagknow:
    """Tests for the player_has_ragknow helper function."""

    def test_player_without_ragknow(self):
        """Test that players without the trait return False."""
        player = MagicMock(spec=Player)
        player.active_traits = []
        player.traits = []

        assert player_has_ragknow(player) is False

    def test_player_with_ragknow_in_active_traits(self):
        """Test detection via active_traits list."""
        player = MagicMock(spec=Player)
        player.active_traits = ["Field General", "Ragknow"]
        player.traits = []

        assert player_has_ragknow(player) is True

    def test_player_with_ragknow_in_traits_list(self):
        """Test detection via traits list with objects."""
        player = MagicMock(spec=Player)
        player.active_traits = []

        ragknow_trait = MagicMock()
        ragknow_trait.name = "Ragknow"
        player.traits = [ragknow_trait]

        assert player_has_ragknow(player) is True

    def test_player_with_ragknow_string_in_traits(self):
        """Test detection via traits list with strings."""
        player = MagicMock(spec=Player)
        player.active_traits = []
        player.traits = ["Iron Man", "Ragknow"]

        assert player_has_ragknow(player) is True


class TestRagknowIgnoresPenalties:
    """Tests for Ragknow's ignore_injury_penalties effect."""

    def test_ragknow_no_performance_penalties(self):
        """Test that Ragknow holders have no attribute penalties."""
        # Severity 7 would normally have significant penalties
        penalties = calculate_injured_performance_penalty(
            severity=7,
            toughness=50,
            has_ragknow=True
        )

        assert penalties == {}

    def test_normal_player_has_penalties(self):
        """Test that normal players do have penalties."""
        penalties = calculate_injured_performance_penalty(
            severity=7,
            toughness=50,
            has_ragknow=False
        )

        assert len(penalties) > 0
        assert "speed" in penalties
        assert penalties["speed"] < 0  # Negative penalty

    def test_all_severity_levels_ignored(self):
        """Test that Ragknow ignores penalties at all severity levels."""
        for severity in range(1, 8):
            penalties = calculate_injured_performance_penalty(
                severity=severity,
                toughness=30,
                has_ragknow=True
            )
            assert penalties == {}, f"Severity {severity} should have no penalties"


class TestRagknowMaxPlayableSeverity:
    """Tests for Ragknow's max_playable_severity effect."""

    def test_ragknow_can_play_through_severity_7(self):
        """Test that Ragknow can play through highest playable severity."""
        can_play = InjuryConfig.can_play_through_injury(
            severity=7,
            toughness=30,  # Low toughness would normally block
            has_ragknow=True
        )

        assert can_play is True

    def test_ragknow_cannot_play_through_severity_8(self):
        """Test that even Ragknow can't play through severity 8+."""
        for severity in [8, 9, 10]:
            can_play = InjuryConfig.can_play_through_injury(
                severity=severity,
                toughness=100,
                has_ragknow=True
            )
            assert can_play is False, f"Severity {severity} should not be playable"

    def test_ragknow_bypasses_toughness_requirements(self):
        """Test that Ragknow ignores toughness thresholds."""
        # Normally severity 5 requires 85+ toughness
        can_play_normal = InjuryConfig.can_play_through_injury(
            severity=5,
            toughness=30,
            has_ragknow=False
        )
        can_play_ragknow = InjuryConfig.can_play_through_injury(
            severity=5,
            toughness=30,
            has_ragknow=True
        )

        assert can_play_normal is False
        assert can_play_ragknow is True


class TestRagknowEscalationReduction:
    """Tests for Ragknow's reduced injury escalation chance."""

    @pytest.fixture
    def player(self):
        player = MagicMock(spec=Player)
        player.id = 1
        player.injury_resistance = 70
        player.age = 30
        return player

    def test_ragknow_reduces_escalation(self, player):
        """Test that Ragknow reduces escalation chance by 50%."""
        # Set up player without Ragknow
        player.active_traits = []
        player.traits = []

        # Count escalations over many runs
        escalations_normal = 0
        escalations_ragknow = 0
        runs = 1000

        for i in range(runs):
            rng = DeterministicRNG(seed=i)
            result = apply_playing_injured_risk(player, current_severity=5, rng=rng)
            if result is not None:
                escalations_normal += 1

        # Now with Ragknow
        player.active_traits = ["Ragknow"]

        for i in range(runs):
            rng = DeterministicRNG(seed=i)
            result = apply_playing_injured_risk(player, current_severity=5, rng=rng)
            if result is not None:
                escalations_ragknow += 1

        # Ragknow should have roughly half the escalations
        # Allow 20% tolerance for RNG variance
        ratio = escalations_ragknow / max(1, escalations_normal)
        assert 0.3 < ratio < 0.7, f"Expected ~50% reduction, got ratio {ratio}"


class TestRagknowRecoveryBonus:
    """Tests for Ragknow's recovery time bonus."""

    def test_recovery_multiplier_value(self):
        """Test that recovery multiplier is 0.90 (10% faster)."""
        assert InjuryConfig.RAGKNOW_RECOVERY_MULTIPLIER == 0.90

    def test_recovery_applied_correctly(self):
        """Test that 10% reduction is applied to recovery time."""
        base_weeks = 10
        ragknow_weeks = int(base_weeks * InjuryConfig.RAGKNOW_RECOVERY_MULTIPLIER)

        assert ragknow_weeks == 9  # 10% reduction


class TestToughnessBasedPlayThrough:
    """Tests for the toughness-based play-through system (non-Ragknow)."""

    def test_low_toughness_minor_only(self):
        """Test that low toughness can only play through minor injuries."""
        # Low toughness (30) should only handle severity 1
        assert InjuryConfig.can_play_through_injury(1, toughness=30) is True
        assert InjuryConfig.can_play_through_injury(2, toughness=30) is False

    def test_high_toughness_more_injuries(self):
        """Test that high toughness can play through more injuries."""
        # High toughness (90) should handle up to severity 5
        assert InjuryConfig.can_play_through_injury(5, toughness=90) is True
        assert InjuryConfig.can_play_through_injury(6, toughness=90) is False

    def test_experience_increases_effective_toughness(self):
        """Test that older players have higher effective toughness."""
        young_player = MagicMock(spec=Player)
        young_player.injury_resistance = 70
        young_player.age = 24

        vet_player = MagicMock(spec=Player)
        vet_player.injury_resistance = 70
        vet_player.age = 34

        young_toughness = get_player_toughness(young_player)
        vet_toughness = get_player_toughness(vet_player)

        assert vet_toughness > young_toughness


class TestTraitRaritySystem:
    """Tests for the trait rarity system."""

    def test_legendary_traits_have_caps(self):
        """Test that legendary traits have max_league_count set."""
        legendary_traits = [
            key for key, trait in TRAIT_CATALOG.items()
            if trait.rarity_tier == TraitRarity.LEGENDARY
        ]

        for trait_key in legendary_traits:
            trait = TRAIT_CATALOG[trait_key]
            assert trait.max_league_count is not None, f"{trait_key} should have cap"
            assert trait.max_league_count <= 10, f"{trait_key} cap should be low"

    def test_rare_traits_exist(self):
        """Test that rare traits are defined."""
        rare_traits = [
            key for key, trait in TRAIT_CATALOG.items()
            if trait.rarity_tier == TraitRarity.RARE
        ]

        assert len(rare_traits) > 0

    def test_common_traits_no_cap(self):
        """Test that common traits don't have restrictive caps."""
        common_traits = [
            key for key, trait in TRAIT_CATALOG.items()
            if trait.rarity_tier == TraitRarity.COMMON
        ]

        for trait_key in common_traits:
            trait = TRAIT_CATALOG[trait_key]
            # Common traits should either have no cap or a very high one
            if trait.max_league_count is not None:
                assert trait.max_league_count >= 50
