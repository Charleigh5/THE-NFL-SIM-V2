
import pytest
from unittest.mock import MagicMock
from app.models.player import Player
from app.engine.trait_effects import TraitEffectResolver

class TestRPGTraitEffects:

    def test_green_dot_boosts_defense(self):
        # Setup Defense
        captain = MagicMock(spec=Player)
        captain.id = 1
        captain.position = "LB"
        captain.active_traits = ["Green Dot"]
        captain.play_recognition = 80

        player2 = MagicMock(spec=Player)
        player2.id = 2
        player2.position = "CB"
        player2.active_traits = []
        player2.play_recognition = 70

        defense = [captain, player2]

        # Apply Effects
        results = TraitEffectResolver.apply_green_dot_effects(defense)

        # Verify
        assert results["team_play_recognition_boost"] == 5.0
        assert getattr(player2, "play_recognition_boosted") == 75
        # Captain doesn't boost himself in this simplified logic, or maybe he does?
        # The code says `if player.id != captain.id`. So he is NOT boosted.
        assert not hasattr(captain, "play_recognition_boosted")

    def test_pick_artist_effects(self):
        cb = MagicMock(spec=Player)
        cb.active_traits = ["Pick Artist"]

        # Ball NOT in air
        results = TraitEffectResolver.apply_pick_artist_effects(cb, ball_in_air=False)
        assert results == {}

        # Ball IN air
        results = TraitEffectResolver.apply_pick_artist_effects(cb, ball_in_air=True)
        assert results["interception_chance_multiplier"] == 1.50
        assert results["catch_radius_boost"] == 0.30

    def test_chip_block_effects(self):
        rb = MagicMock(spec=Player)
        rb.active_traits = ["Chip Block Specialist"]

        # Not blocking
        results = TraitEffectResolver.apply_chip_block_effects(rb, is_blocking=False)
        assert results == {}

        # Blocking
        results = TraitEffectResolver.apply_chip_block_effects(rb, is_blocking=True)
        assert results["pass_pro_rating_boost"] == 10.0
        assert results["edge_rusher_slow_effect"] == 0.15

    def test_possession_receiver_effects(self):
        wr = MagicMock(spec=Player)
        wr.active_traits = ["Possession Receiver"]

        # 1st Down (Not Critical)
        results = TraitEffectResolver.apply_possession_receiver_effects(wr, down=1, yards_to_go=10)
        assert results == {}

        # 3rd Down (Critical)
        results = TraitEffectResolver.apply_possession_receiver_effects(wr, down=3, yards_to_go=5)
        assert results["catch_in_traffic_boost"] == 15.0
        assert results["drop_chance_reduction"] == 0.30

    def test_cleanup_boosts(self):
        p1 = MagicMock(spec=Player)
        p1.play_recognition_boosted = 85

        TraitEffectResolver.cleanup_boosts([p1])

        with pytest.raises(AttributeError):
             _ = p1.play_recognition_boosted
