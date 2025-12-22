import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PlayCommand
from app.engine.event_bus import EventType

class TestSafetyScenarios:

    @pytest.fixture
    def resolver(self):
        return PlayResolver(rng=MagicMock())

    def test_check_for_safety_home_offense_safety(self, resolver):
        """Test safety detection for Home offense (own endzone at 0)."""
        command = MagicMock(spec=PlayCommand)
        command.possession = "home"
        command.start_yard_line = 5
        command.play_id = "TEST_PLAY"
        command.defense_team_id = "AWAY_TEAM"

        # Loss of 6 yards from 5 yard line -> -1 -> Safety
        is_safety, clamped_yards = resolver._check_for_safety(command, -6)

        assert is_safety is True
        assert clamped_yards == -5 # Should be clamped to -start_yard

    def test_check_for_safety_away_offense_safety(self, resolver):
        """Test safety detection for Away offense (own endzone at 100)."""
        command = MagicMock(spec=PlayCommand)
        command.possession = "away"
        command.start_yard_line = 95
        command.play_id = "TEST_PLAY"
        command.defense_team_id = "HOME_TEAM"

        # Loss of 6 yards from 95 (5 yards out) -> 101 -> Safety
        # Note: Direction is positive for Home (0->100), negative for Away logic in Orchestrator?
        # Wait, the logic in _check_for_safety uses:
        # Away: if start_yard - yards_gained >= 100.
        # If yards_gained is NEGATIVE (loss), e.g. -6.
        # 95 - (-6) = 101 >= 100. Correct.

        is_safety, clamped_yards = resolver._check_for_safety(command, -6)

        assert is_safety is True
        assert clamped_yards == -5 # (100 - 95) * -1 = -5.

    def test_check_for_safety_home_offense_safe(self, resolver):
        """Test NO safety for Home offense."""
        command = MagicMock(spec=PlayCommand)
        command.possession = "home"
        command.start_yard_line = 5

        # Loss of 4 yards -> 1. Safe.
        is_safety, clamped_yards = resolver._check_for_safety(command, -4)

        assert is_safety is False
        assert clamped_yards == -4

    def test_check_for_safety_away_offense_safe(self, resolver):
        """Test NO safety for Away offense."""
        command = MagicMock(spec=PlayCommand)
        command.possession = "away"
        command.start_yard_line = 95

        # Loss of 4 yards -> 99. Safe.
        is_safety, clamped_yards = resolver._check_for_safety(command, -4)

        assert is_safety is False
        assert clamped_yards == -4

    @patch("app.orchestrator.play_resolver.EventBus.publish")
    def test_safety_event_logging(self, mock_publish, resolver):
        """Test that SAFETY event is published."""
        command = MagicMock(spec=PlayCommand)
        command.possession = "home"
        command.start_yard_line = 1
        command.defense_team_id = "DEFENSE_ID"
        command.play_id = "SACK_PLAY"

        resolver.current_match_context = MagicMock()
        resolver.current_match_context.season = 2025
        resolver.current_match_context.week = 10
        resolver.current_match_context.game_id = "GAME_ID"

        resolver._check_for_safety(command, -2)

        mock_publish.assert_called_once()
        args, _ = mock_publish.call_args
        assert args[0] == EventType.SAFETY
        assert args[1]["game_id"] == "GAME_ID"
        assert args[1]["scoring_team_id"] == "DEFENSE_ID"

