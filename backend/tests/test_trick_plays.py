import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import TrickPlayCommand
from app.core.nfl_reference_data import TRICK_PLAY_TABLE

class TestTrickPlays:

    @pytest.fixture
    def resolver(self):
        rng = MagicMock()
        rng.random.return_value = 0.5 # Default roll
        # Mock randint to return a safe value
        rng.randint.return_value = 10

        resolver = PlayResolver(rng=rng)

        # Mock Context
        mock_context = MagicMock()
        mock_context.home_team_awareness = 50
        mock_context.away_team_awareness = 50
        resolver.current_match_context = mock_context

        return resolver

    def test_configuration_loading(self):
        """Verify we can load basic config"""
        fake_punt = TRICK_PLAY_TABLE.get("FAKE_PUNT_RUN")
        assert fake_punt is not None
        assert fake_punt.name == "Fake Punt Run"
        assert fake_punt.base_success_rate > 0.3

    def test_confusion_calculation(self, resolver):
        """Verify confusion logic"""
        command = TrickPlayCommand(
            offense_players=[],
            defense_players=[],
            trick_type="FAKE_PUNT_RUN",
            is_home_team=True
        )

        # With default awareness (50 vs 50), confusion should be base + 0
        conf = resolver._calculate_trick_play_confusion(command)
        assert conf == 0.5 # Base for FAKE_PUNT_RUN is 0.5

        # Test High Awareness (Defense ready)
        # Using mock context
        resolver.current_match_context.away_team_awareness = 90
        # Awareness mod = (50 - 90) / 100 = -0.4
        conf = resolver._calculate_trick_play_confusion(command)
        assert conf == pytest.approx(0.1)

    def test_resolve_trick_play_success(self, resolver):
        """Verify success path"""
        command = TrickPlayCommand(
            offense_players=[],
            defense_players=[],
            trick_type="FAKE_PUNT_RUN",
            distance=5
        )

        # Mock RNG to force success
        # Config: Base 0.45 + Confusion 0.5 * 0.2 = 0.55 threshold?
        # Actually min/max clamp applies.

        resolver.rng.random.return_value = 0.01 # Very low roll = Success
        resolver.rng.randint.return_value = 15 # Gain

        result = resolver._resolve_trick_play(command)

        assert result.yards_gained == 15
        assert "TRICK PLAY!" in result.description
        assert "Fake Punt Run executed" in result.description
        assert not result.is_turnover

    def test_resolve_trick_play_failure(self, resolver):
        """Verify failure path"""
        command = TrickPlayCommand(
            offense_players=[],
            defense_players=[],
            trick_type="FAKE_PUNT_RUN",
            distance=5
        )

        # Force failure
        resolver.rng.random.return_value = 0.99

        result = resolver._resolve_trick_play(command)

        assert result.yards_gained < 0
        assert "Loss of" in result.description or "INTERCEPTED" in result.description

    def test_resolve_flea_flicker_turnover(self, resolver):
        """Verify turnover risk on high risk plays"""
        command = TrickPlayCommand(
            offense_players=[],
            defense_players=[],
            trick_type="FLEA_FLICKER"
        )

        # Force Failure (0.99)
        # Force Risk Check (0.01) -> Turnover
        resolver.rng.random.side_effect = [0.99, 0.01]

        result = resolver._resolve_trick_play(command)

        assert result.is_turnover
        assert "INTERCEPTED/FUMBLED" in result.description
