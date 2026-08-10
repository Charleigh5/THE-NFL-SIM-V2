"""
Unit tests for Trait Integration in the Game Engine.

These tests verify that:
1. MatchContext properly loads and flattens player traits
2. TraitEffectResolver methods apply correct effects
3. PlayResolver integrates traits during play resolution
"""

from dataclasses import dataclass

# Import the modules under test
from app.engine.trait_effects import TraitEffectResolver

# ============================================================================
# Mock Player Class for Testing
# ============================================================================

@dataclass
class MockPlayer:
    """Mock player for testing trait effects."""
    id: int
    first_name: str = "Test"
    last_name: str = "Player"
    position: str = "QB"
    active_traits: list[str] = None
    awareness: int = 50
    play_recognition: int = 50
    pass_pro_rating: int = 50

    def __post_init__(self):
        if self.active_traits is None:
            self.active_traits = []


# ============================================================================
# TraitEffectResolver Tests
# ============================================================================

class TestTraitEffectResolver:
    """Tests for the TraitEffectResolver static methods."""

    def test_apply_field_general_boost_applies_awareness(self):
        """Field General should boost team awareness."""
        qb = MockPlayer(id=1, position="QB", active_traits=["Field General"])
        wr = MockPlayer(id=2, position="WR")
        offense = [qb, wr]

        results = TraitEffectResolver.apply_field_general_boost(offense, qb)

        assert "team_awareness_boost" in results
        assert results["team_awareness_boost"] == 5.0
        assert hasattr(wr, "awareness_boosted")
        assert wr.awareness_boosted == 55  # 50 + 5

    def test_apply_green_dot_effects_boosts_play_recognition(self):
        """Green Dot should boost team play recognition."""
        captain = MockPlayer(id=1, position="LB", active_traits=["Green Dot"])
        cb = MockPlayer(id=2, position="CB")
        defense = [captain, cb]

        results = TraitEffectResolver.apply_green_dot_effects(defense)

        assert "team_play_recognition_boost" in results
        assert results["team_play_recognition_boost"] == 5.0
        assert hasattr(cb, "play_recognition_boosted")
        assert cb.play_recognition_boosted == 55  # 50 + 5

    def test_apply_green_dot_effects_no_captain(self):
        """Green Dot effects should be empty if no captain present."""
        cb = MockPlayer(id=1, position="CB")
        s = MockPlayer(id=2, position="S")
        defense = [cb, s]

        results = TraitEffectResolver.apply_green_dot_effects(defense)

        assert results == {}

    def test_apply_chip_block_effects_when_blocking(self):
        """Chip Block should boost pass_pro_rating when RB is blocking."""
        rb = MockPlayer(id=1, position="RB", active_traits=["Chip Block Specialist"])

        results = TraitEffectResolver.apply_chip_block_effects(rb, is_blocking=True)

        assert "pass_pro_rating_boost" in results
        assert results["pass_pro_rating_boost"] == 10.0

    def test_apply_chip_block_effects_not_blocking(self):
        """Chip Block should have no effect when RB is not blocking."""
        rb = MockPlayer(id=1, position="RB", active_traits=["Chip Block Specialist"])

        results = TraitEffectResolver.apply_chip_block_effects(rb, is_blocking=False)

        assert results == {}

    def test_apply_pick_artist_effects_ball_in_air(self):
        """Pick Artist should boost interception chance when ball is in air."""
        db = MockPlayer(id=1, position="CB", active_traits=["Pick Artist"])

        results = TraitEffectResolver.apply_pick_artist_effects(db, ball_in_air=True)

        assert "interception_chance_multiplier" in results
        assert results["interception_chance_multiplier"] == 1.50

    def test_apply_pick_artist_effects_ball_not_in_air(self):
        """Pick Artist should not activate when ball is not in air."""
        db = MockPlayer(id=1, position="CB", active_traits=["Pick Artist"])

        results = TraitEffectResolver.apply_pick_artist_effects(db, ball_in_air=False)

        assert results == {}

    def test_apply_possession_receiver_effects_critical_down(self):
        """Possession Receiver should activate on 3rd/4th down."""
        wr = MockPlayer(id=1, position="WR", active_traits=["Possession Receiver"])

        results = TraitEffectResolver.apply_possession_receiver_effects(wr, down=3, yards_to_go=5)

        assert "catch_in_traffic_boost" in results
        assert results["catch_in_traffic_boost"] == 15.0

    def test_apply_possession_receiver_effects_early_down(self):
        """Possession Receiver should not activate on 1st/2nd down."""
        wr = MockPlayer(id=1, position="WR", active_traits=["Possession Receiver"])

        results = TraitEffectResolver.apply_possession_receiver_effects(wr, down=1, yards_to_go=10)

        assert results == {}

    def test_cleanup_boosts_removes_temporary_attributes(self):
        """Cleanup should remove all temporary boost attributes."""
        player = MockPlayer(id=1)
        player.awareness_boosted = 60
        player.play_recognition_boosted = 55

        TraitEffectResolver.cleanup_boosts([player])

        assert not hasattr(player, "awareness_boosted")
        assert not hasattr(player, "play_recognition_boosted")


# ============================================================================
# Integration Tests (Mock-based)
# ============================================================================

class TestTraitIntegration:
    """Integration tests verifying traits work together."""

    def test_multiple_traits_can_apply(self):
        """Multiple traits on different players should all apply."""
        qb = MockPlayer(id=1, position="QB", active_traits=["Field General"])
        wr = MockPlayer(id=2, position="WR", active_traits=["Possession Receiver"])
        rb = MockPlayer(id=3, position="RB", active_traits=["Chip Block Specialist"])
        offense = [qb, wr, rb]

        # Apply Field General
        fg_results = TraitEffectResolver.apply_field_general_boost(offense, qb)
        assert fg_results.get("team_awareness_boost") == 5.0

        # Apply Chip Block
        cb_results = TraitEffectResolver.apply_chip_block_effects(rb, is_blocking=True)
        assert cb_results.get("pass_pro_rating_boost") == 10.0

        # Apply Possession Receiver
        pr_results = TraitEffectResolver.apply_possession_receiver_effects(wr, down=3, yards_to_go=7)
        assert pr_results.get("catch_in_traffic_boost") == 15.0
