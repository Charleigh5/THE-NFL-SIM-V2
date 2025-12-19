"""
Tests for Playbook Familiarity System
=====================================
Comprehensive tests for B-048 through B-060.
"""

import pytest
from app.services.playbook.familiarity import (
    PlaybookFamiliarity,
    PlayFamiliarity,
    FamiliarityManager,
    FamiliarityTier,
    BASE_LEARNING_RATE,
    VETERAN_LEARNING_MULTIPLIER,
    MIN_EXECUTION_PENALTY,
    MAX_EXECUTION_PENALTY,
    INITIAL_FAMILIARITY,
    SCHEME_CHANGE_PENALTY,
    FAMILIARITY_THRESHOLD_MASTERY,
)


class TestPlayFamiliarity:
    """Tests for PlayFamiliarity dataclass."""

    def test_initial_values(self):
        """B-050: Verify initial play knowledge storage."""
        play = PlayFamiliarity(play_id="SLANT_FLAT")
        assert play.play_id == "SLANT_FLAT"
        assert play.familiarity == INITIAL_FAMILIARITY
        assert play.times_executed == 0
        assert play.times_successful == 0

    def test_success_rate_zero_executions(self):
        """Success rate should be 0 with no executions."""
        play = PlayFamiliarity(play_id="TEST")
        assert play.success_rate == 0.0

    def test_success_rate_calculation(self):
        """Success rate should calculate correctly."""
        play = PlayFamiliarity(
            play_id="TEST",
            times_executed=10,
            times_successful=7
        )
        assert play.success_rate == 0.7

    def test_tier_unknown(self):
        """Tier should be UNKNOWN for low familiarity."""
        play = PlayFamiliarity(play_id="TEST", familiarity=0.05)
        assert play.tier == FamiliarityTier.UNKNOWN

    def test_tier_mastery(self):
        """Tier should be MASTERY for high familiarity."""
        play = PlayFamiliarity(play_id="TEST", familiarity=0.98)
        assert play.tier == FamiliarityTier.MASTERY


class TestPlaybookFamiliarity:
    """Tests for PlaybookFamiliarity component."""

    @pytest.fixture
    def rookie_player(self):
        """Rookie player with 0 years experience."""
        return PlaybookFamiliarity(player_id=1, experience_years=0)

    @pytest.fixture
    def veteran_player(self):
        """Veteran player with 8 years experience."""
        return PlaybookFamiliarity(player_id=2, experience_years=8)

    # --- B-051: Execution Penalty Tests ---

    def test_execution_penalty_unknown_play(self, rookie_player):
        """B-051: Unknown plays should have minimum penalty (0.7)."""
        penalty = rookie_player.calculate_execution_penalty("UNKNOWN_PLAY")
        assert penalty >= MIN_EXECUTION_PENALTY
        assert penalty < MAX_EXECUTION_PENALTY

    def test_execution_penalty_mastered_play(self, veteran_player):
        """B-051: Mastered plays should have near-max penalty (1.0)."""
        # Manually set high familiarity
        veteran_player.play_knowledge["MASTERED"] = PlayFamiliarity(
            play_id="MASTERED",
            familiarity=0.99
        )
        penalty = veteran_player.calculate_execution_penalty("MASTERED")
        assert penalty > 0.95
        assert penalty <= MAX_EXECUTION_PENALTY

    def test_execution_penalty_bounds(self, rookie_player):
        """B-051: Penalty should always be in 0.7-1.0 range."""
        for fam in [0.0, 0.1, 0.5, 0.9, 1.0]:
            rookie_player.play_knowledge["TEST"] = PlayFamiliarity(
                play_id="TEST",
                familiarity=fam
            )
            penalty = rookie_player.calculate_execution_penalty("TEST")
            assert MIN_EXECUTION_PENALTY <= penalty <= MAX_EXECUTION_PENALTY

    # --- B-052: Learn Play Tests ---

    def test_learn_play_increases_familiarity(self, rookie_player):
        """B-052: Learning a play should increase familiarity."""
        initial = rookie_player.get_familiarity("NEW_PLAY")
        rookie_player.learn_play("NEW_PLAY", success=True)
        after = rookie_player.get_familiarity("NEW_PLAY")
        assert after > initial

    def test_learn_play_tracks_executions(self, rookie_player):
        """B-052: Learning should track execution count."""
        rookie_player.learn_play("PLAY_A", success=True)
        rookie_player.learn_play("PLAY_A", success=False)
        rookie_player.learn_play("PLAY_A", success=True)

        assert rookie_player.play_knowledge["PLAY_A"].times_executed == 3
        assert rookie_player.play_knowledge["PLAY_A"].times_successful == 2

    def test_learn_play_success_bonus(self, rookie_player):
        """B-052: Successful plays should learn faster."""
        # Create two identical players
        player_success = PlaybookFamiliarity(player_id=10, experience_years=3)
        player_fail = PlaybookFamiliarity(player_id=11, experience_years=3)

        player_success.learn_play("PLAY_X", success=True)
        player_fail.learn_play("PLAY_X", success=False)

        assert player_success.get_familiarity("PLAY_X") > player_fail.get_familiarity("PLAY_X")

    # --- B-053: Veteran Bonus Tests ---

    def test_veteran_learns_faster(self, rookie_player, veteran_player):
        """B-053: Veterans should learn 1.5x faster than base rate."""
        rookie_player.learn_play("SLANT", success=True)
        veteran_player.learn_play("SLANT", success=True)

        rookie_gain = rookie_player.get_familiarity("SLANT") - INITIAL_FAMILIARITY
        veteran_gain = veteran_player.get_familiarity("SLANT") - INITIAL_FAMILIARITY

        # Veteran should gain more than rookie
        assert veteran_gain > rookie_gain
        # Should be approximately 1.5x / 0.8x = ~1.875x difference
        ratio = veteran_gain / rookie_gain if rookie_gain > 0 else 0
        assert ratio > 1.5  # At least 50% faster

    # --- B-054: Scheme Change Tests ---

    def test_scheme_change_penalty(self, veteran_player):
        """B-054: Scheme change should reduce familiarity."""
        # Build up familiarity
        veteran_player.current_scheme = "WEST_COAST"
        veteran_player.play_knowledge["WC_SLANT"] = PlayFamiliarity(
            play_id="WC_SLANT",
            familiarity=0.80
        )

        # Change scheme
        veteran_player.apply_scheme_change_penalty("AIR_RAID")

        # Familiarity should be reduced
        new_familiarity = veteran_player.get_familiarity("WC_SLANT")
        expected = 0.80 * (1.0 - SCHEME_CHANGE_PENALTY)
        assert abs(new_familiarity - expected) < 0.01

    def test_scheme_change_no_penalty_same_scheme(self, veteran_player):
        """B-054: Same scheme should not penalize."""
        veteran_player.current_scheme = "WEST_COAST"
        veteran_player.play_knowledge["WC_SLANT"] = PlayFamiliarity(
            play_id="WC_SLANT",
            familiarity=0.80
        )

        veteran_player.apply_scheme_change_penalty("WEST_COAST")

        assert veteran_player.get_familiarity("WC_SLANT") == 0.80

    # --- Serialization Tests ---

    def test_to_dict(self, rookie_player):
        """Serialization should include all relevant data."""
        rookie_player.learn_play("PLAY_A", success=True)
        data = rookie_player.to_dict()

        assert data["player_id"] == 1
        assert data["experience_years"] == 0
        assert "plays" in data
        assert "PLAY_A" in data["plays"]
        assert data["plays"]["PLAY_A"]["tier"] == FamiliarityTier.UNKNOWN.value


class TestFamiliarityManager:
    """Tests for FamiliarityManager service."""

    @pytest.fixture
    def manager(self):
        return FamiliarityManager()

    def test_get_or_create_new(self, manager):
        """Should create new familiarity for unknown player."""
        fam = manager.get_or_create(player_id=100, experience_years=5)
        assert fam.player_id == 100
        assert fam.experience_years == 5

    def test_get_or_create_existing(self, manager):
        """Should return existing familiarity for known player."""
        fam1 = manager.get_or_create(player_id=100)
        fam1.learn_play("TEST", success=True)

        fam2 = manager.get_or_create(player_id=100)
        assert fam2.get_familiarity("TEST") > INITIAL_FAMILIARITY

    def test_team_execution_modifier(self, manager):
        """Should average execution modifiers for team."""
        # Create players with different familiarity levels
        p1 = manager.get_or_create(player_id=1)
        p2 = manager.get_or_create(player_id=2)

        p1.play_knowledge["PLAY"] = PlayFamiliarity(play_id="PLAY", familiarity=0.9)
        p2.play_knowledge["PLAY"] = PlayFamiliarity(play_id="PLAY", familiarity=0.1)

        modifier = manager.calculate_team_execution_modifier([1, 2], "PLAY")

        # Should be between individual modifiers
        m1 = p1.calculate_execution_penalty("PLAY")
        m2 = p2.calculate_execution_penalty("PLAY")
        assert min(m1, m2) <= modifier <= max(m1, m2)

    def test_apply_learning_batch(self, manager):
        """Should apply learning to multiple players."""
        manager.get_or_create(player_id=1)
        manager.get_or_create(player_id=2)
        manager.get_or_create(player_id=3)

        manager.apply_learning_batch([1, 2, 3], "BATCH_PLAY", success=True)

        for pid in [1, 2, 3]:
            fam = manager._players[pid].get_familiarity("BATCH_PLAY")
            assert fam > INITIAL_FAMILIARITY


class TestIntegrationScenarios:
    """Real-world integration tests."""

    def test_rookie_season_learning_curve(self):
        """Simulate rookie learning plays over a season."""
        rookie = PlaybookFamiliarity(player_id=99, experience_years=0)

        # Simulate 17 games x ~10 plays per game = 170 plays
        play_id = "INSIDE_ZONE"
        for _ in range(170):
            success = True  # Assume mostly successful
            rookie.learn_play(play_id, success=success)

        # After a full season, should be proficient
        assert rookie.get_familiarity(play_id) > 0.75
        assert rookie.play_knowledge[play_id].tier in [
            FamiliarityTier.PROFICIENT,
            FamiliarityTier.MASTERY
        ]

    def test_scheme_change_recovery(self):
        """Simulate recovery after scheme change."""
        player = PlaybookFamiliarity(player_id=10, experience_years=6)
        player.current_scheme = "4-3"

        # Build up familiarity
        for _ in range(50):
            player.learn_play("ZONE_BLITZ", success=True)

        pre_change = player.get_familiarity("ZONE_BLITZ")

        # Scheme change
        player.apply_scheme_change_penalty("3-4")
        post_change = player.get_familiarity("ZONE_BLITZ")

        assert post_change < pre_change

        # Recover with practice
        for _ in range(30):
            player.learn_play("ZONE_BLITZ", success=True)

        recovered = player.get_familiarity("ZONE_BLITZ")
        assert recovered > post_change  # Should have recovered
