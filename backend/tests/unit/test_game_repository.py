"""
Unit tests for GameRepository.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.orchestrator.game_repository import GameRepository
from app.schemas.play import PlayResult


class TestGameRepository:
    """Tests for the GameRepository class."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        db = AsyncMock()
        db.execute = AsyncMock()
        db.commit = AsyncMock()
        db.rollback = AsyncMock()
        db.add = MagicMock()
        return db

    @pytest.fixture
    def repo(self, mock_db):
        """Create a GameRepository instance."""
        return GameRepository(mock_db)

    @pytest.fixture
    def sample_history(self):
        """Create sample play history."""
        return [
            PlayResult(
                yards_gained=10,
                is_touchdown=False,
                is_turnover=False,
                description="Pass complete for 10 yards",
                headline=None,
                injuries=[],
                passer_id=1,
                receiver_id=2
            ),
            PlayResult(
                yards_gained=5,
                is_touchdown=False,
                is_turnover=False,
                description="Rush for 5 yards",
                headline=None,
                injuries=[],
                rusher_id=3
            ),
            PlayResult(
                yards_gained=25,
                is_touchdown=True,
                is_turnover=False,
                description="Touchdown pass!",
                headline=None,
                injuries=[],
                passer_id=1,
                receiver_id=2
            ),
        ]

    def test_aggregate_stats_passing(self, repo, sample_history):
        """Test passing stats aggregation."""
        result = repo._aggregate_stats(sample_history)

        # Passer (ID 1)
        assert 1 in result
        assert result[1]["pass_attempts"] == 2
        assert result[1]["pass_completions"] == 2
        assert result[1]["pass_yards"] == 35  # 10 + 25
        assert result[1]["pass_tds"] == 1

    def test_aggregate_stats_rushing(self, repo, sample_history):
        """Test rushing stats aggregation."""
        result = repo._aggregate_stats(sample_history)

        # Rusher (ID 3)
        assert 3 in result
        assert result[3]["rush_attempts"] == 1
        assert result[3]["rush_yards"] == 5

    def test_aggregate_stats_receiving(self, repo, sample_history):
        """Test receiving stats aggregation."""
        result = repo._aggregate_stats(sample_history)

        # Receiver (ID 2)
        assert 2 in result
        assert result[2]["targets"] == 2
        assert result[2]["receptions"] == 2
        assert result[2]["rec_yards"] == 35
        assert result[2]["rec_tds"] == 1

    def test_aggregate_stats_empty_history(self, repo):
        """Test aggregation with empty history."""
        result = repo._aggregate_stats([])
        assert result == {}

    @pytest.mark.asyncio
    async def test_save_game_progress(self, repo, mock_db):
        """Test saving game progress."""
        # Setup mock game
        mock_game = MagicMock()
        mock_game.game_data = {}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_game
        mock_db.execute.return_value = mock_result

        state = {
            "home_score": 14,
            "away_score": 7,
            "quarter": 2,
            "time_left": "05:00"
        }

        await repo.save_game_progress(game_id=1, state=state, history=[])

        assert mock_game.home_score == 14
        assert mock_game.away_score == 7
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_game_progress_no_game_id(self, repo, mock_db):
        """Test that save is skipped when no game ID."""
        await repo.save_game_progress(game_id=None, state={}, history=[])

        mock_db.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_finalize_game(self, repo, mock_db):
        """Test game finalization."""
        mock_game = MagicMock()
        mock_game.is_played = False
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_game
        mock_db.execute.return_value = mock_result

        result = await repo.finalize_game(game_id=1)

        assert mock_game.is_played is True
        mock_db.commit.assert_called_once()
        assert result == mock_game

    @pytest.mark.asyncio
    async def test_finalize_game_not_found(self, repo, mock_db):
        """Test finalization when game not found."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        result = await repo.finalize_game(game_id=999)

        assert result is None
