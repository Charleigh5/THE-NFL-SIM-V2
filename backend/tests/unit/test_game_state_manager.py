"""
Unit tests for GameStateManager.
"""

import pytest
from app.orchestrator.game_state_manager import GameStateManager


class TestGameStateManager:
    """Tests for the GameStateManager class."""

    def test_initial_state(self):
        """Test that initial state is correct."""
        state = GameStateManager()

        assert state.quarter == 1
        assert state.time_left == "15:00"
        assert state.home_score == 0
        assert state.away_score == 0
        assert state.possession == "home"
        assert state.down == 1
        assert state.distance == 10
        assert state.yard_line == 25
        assert state.home_timeouts == 3
        assert state.away_timeouts == 3

    def test_time_left_seconds(self):
        """Test time_left_seconds property."""
        state = GameStateManager(time_left="12:30")
        assert state.time_left_seconds == 12 * 60 + 30

        state.time_left = "00:00"
        assert state.time_left_seconds == 0

    def test_update_clock(self):
        """Test clock updates correctly."""
        state = GameStateManager(time_left="10:00")

        state.update_clock(30)
        assert state.time_left == "09:30"

        state.update_clock(90)
        assert state.time_left == "08:00"

    def test_update_clock_minimum(self):
        """Test clock doesn't go below zero."""
        state = GameStateManager(time_left="00:10")

        state.update_clock(20)
        assert state.time_left == "00:00"

    def test_advance_quarter(self):
        """Test quarter advancement."""
        state = GameStateManager(quarter=1, time_left="00:00")

        state.advance_quarter()

        assert state.quarter == 2
        assert state.time_left == "15:00"

    def test_update_score_home(self):
        """Test scoring for home team."""
        state = GameStateManager()

        state.update_score("home", 7)
        assert state.home_score == 7

        state.update_score("home", 3)
        assert state.home_score == 10

    def test_update_score_away(self):
        """Test scoring for away team."""
        state = GameStateManager()

        state.update_score("away", 7)
        assert state.away_score == 7

    def test_update_yard_line_home(self):
        """Test yard line update for home possession."""
        state = GameStateManager(possession="home", yard_line=25)

        state.update_yard_line(10)
        assert state.yard_line == 35

        state.update_yard_line(-5)
        assert state.yard_line == 30

    def test_update_yard_line_away(self):
        """Test yard line update for away possession."""
        state = GameStateManager(possession="away", yard_line=75)

        state.update_yard_line(10)  # Away gains, moves toward 0
        assert state.yard_line == 65

    def test_update_yard_line_bounds(self):
        """Test yard line stays in bounds."""
        state = GameStateManager(possession="home", yard_line=95)

        state.update_yard_line(20)  # Would be 115
        assert state.yard_line == 100

        state.possession = "away"
        state.update_yard_line(150)  # Would be -50
        assert state.yard_line == 0

    def test_update_downs_first_down(self):
        """Test first down conversion."""
        state = GameStateManager(down=2, distance=7)

        result = state.update_downs(10)

        assert result is True
        assert state.down == 1
        assert state.distance == 10

    def test_update_downs_no_first_down(self):
        """Test down advancement without first down."""
        state = GameStateManager(down=1, distance=10)

        result = state.update_downs(3)

        assert result is False
        assert state.down == 2
        assert state.distance == 7

    def test_handle_turnover(self):
        """Test turnover handling."""
        state = GameStateManager(possession="home", down=3, distance=5)

        state.handle_turnover()

        assert state.possession == "away"
        assert state.down == 1
        assert state.distance == 10

    def test_handle_touchdown(self):
        """Test touchdown handling."""
        state = GameStateManager(possession="home", home_score=0)

        state.handle_touchdown()

        assert state.home_score == 7
        assert state.yard_line == 25
        assert state.down == 1
        assert state.possession == "away"

    def test_use_timeout_success(self):
        """Test successful timeout use."""
        state = GameStateManager(home_timeouts=2)

        result = state.use_timeout("home")

        assert result is True
        assert state.home_timeouts == 1

    def test_use_timeout_failure(self):
        """Test timeout failure when none remaining."""
        state = GameStateManager(away_timeouts=0)

        result = state.use_timeout("away")

        assert result is False
        assert state.away_timeouts == 0

    def test_get_score_diff(self):
        """Test score differential calculation."""
        state = GameStateManager(home_score=21, away_score=14, possession="home")
        assert state.get_score_diff() == 7

        state.possession = "away"
        assert state.get_score_diff() == -7

    def test_get_distance_to_goal(self):
        """Test distance to goal calculation."""
        state = GameStateManager(yard_line=75, possession="home")
        assert state.get_distance_to_goal() == 25

        state.possession = "away"
        assert state.get_distance_to_goal() == 75

    def test_is_quarter_over(self):
        """Test quarter end detection."""
        state = GameStateManager(time_left="00:05")
        assert state.is_quarter_over() is False

        state.time_left = "00:00"
        assert state.is_quarter_over() is True

    def test_is_game_over(self):
        """Test game end detection."""
        state = GameStateManager(quarter=4, time_left="00:00", home_score=21, away_score=14)
        assert state.is_game_over() is True

        # Tied regulation ends go to overtime, not game over
        state_tied = GameStateManager(quarter=4, time_left="00:00", home_score=14, away_score=14)
        assert state_tied.is_game_over() is False

        state.quarter = 3
        assert state.is_game_over() is False

    def test_reset(self):
        """Test state reset."""
        state = GameStateManager(
            quarter=4, time_left="02:00", home_score=28,
            away_score=21, possession="away", down=3
        )

        state.reset()

        assert state.quarter == 1
        assert state.home_score == 0
        assert state.possession == "home"

    def test_to_dict(self):
        """Test dictionary export."""
        state = GameStateManager(quarter=2, home_score=14)

        result = state.to_dict()

        assert result["quarter"] == 2
        assert result["home_score"] == 14
        assert "yard_line" in result

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "quarter": 3,
            "home_score": 21,
            "away_score": 17,
            "possession": "away"
        }

        state = GameStateManager.from_dict(data)

        assert state.quarter == 3
        assert state.home_score == 21
        assert state.possession == "away"
