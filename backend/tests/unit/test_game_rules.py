
import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.game_state_manager import GameStateManager
from app.orchestrator.play_commands import TwoPointConversionCommand, RunPlayCommand, PassPlayCommand, PlayResult
from app.orchestrator.play_resolver import PlayResolver

class TestGameRules:

    @pytest.fixture
    def game_state(self):
        return GameStateManager()

    # --- GAME-011: Overtime Rules ---

    def test_overtime_transition(self, game_state):
        """Verify transition from Q4 to OT (Q5)."""
        game_state.quarter = 4
        game_state.time_left = "00:00"

        game_state.advance_quarter()

        assert game_state.quarter == 5
        assert game_state.time_left == "10:00"
        assert game_state.ot_possessions == 0
        assert game_state.is_overtime is True

    def test_regulation_end(self, game_state):
        """Verify game ends after Q4 if not tied."""
        game_state.quarter = 4
        game_state.time_left = "00:00"
        game_state.home_score = 24
        game_state.away_score = 21

        assert game_state.is_game_over() is True

    # --- GAME-012: 2-Point Conversion ---

    def test_two_point_conversion_wrapper(self):
        """Verify TwoPointConversionCommand wraps execution correctly."""
        # Setup context
        context = {"yard_line": 98} # 2 yards from goal (offense usually drives to 100 or 0)

        # Mock sub-command
        mock_sub_command = MagicMock()
        mock_sub_command.execute.return_value = PlayResult(
            yards_gained=2, is_touchdown=True, description="Conversion Good"
        )

        # Create 2pt command
        cmd = TwoPointConversionCommand(offense_players=[], defense_players=[])
        cmd.executed_command = mock_sub_command

        # Execute
        result = cmd.execute(context)

        # Verify
        mock_sub_command.execute.assert_called_once_with(context, None)
        assert result.is_touchdown is True
        assert result.description == "Conversion Good"

    def test_two_point_conversion_fallback(self):
        """Verify fallback if no sub-command provided."""
        cmd = TwoPointConversionCommand(offense_players=[], defense_players=[])
        result = cmd.execute({})

        assert result.is_touchdown is False
        assert "failed" in result.description


