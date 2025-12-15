"""
Unit Tests for EloService

Tests the Elo rating calculation and update logic.
"""

import pytest
from app.services.elo_service import EloService


class TestEloService:
    """Test suite for EloService calculations."""

    def test_calculate_expected_outcome_equal_ratings(self):
        """Equal ratings should give 50% win probability."""
        expected = EloService.calculate_expected_outcome(1500, 1500)
        assert expected == pytest.approx(0.5, abs=0.001)

    def test_calculate_expected_outcome_higher_rated_favored(self):
        """Higher rated team should be favored."""
        expected = EloService.calculate_expected_outcome(1600, 1500)
        assert expected > 0.5
        assert expected < 1.0

    def test_calculate_expected_outcome_lower_rated_underdog(self):
        """Lower rated team should be underdog."""
        expected = EloService.calculate_expected_outcome(1400, 1500)
        assert expected < 0.5
        assert expected > 0.0

    def test_calculate_expected_outcome_large_difference(self):
        """Large rating difference should give extreme probabilities."""
        expected = EloService.calculate_expected_outcome(1800, 1400)
        assert expected > 0.9

    def test_update_ratings_winner_gains_loser_loses(self):
        """Winner should gain Elo, loser should lose Elo."""
        new_winner, new_loser = EloService.update_ratings(
            winner_elo=1500, loser_elo=1500, point_diff=10
        )
        assert new_winner > 1500
        assert new_loser < 1500

    def test_update_ratings_upset_gives_more_points(self):
        """Upset (lower rated team wins) should give more Elo change."""
        # Underdog wins
        underdog_win, favorite_loss = EloService.update_ratings(
            winner_elo=1400, loser_elo=1600, point_diff=7
        )

        # Favorite wins
        favorite_win, underdog_loss = EloService.update_ratings(
            winner_elo=1600, loser_elo=1400, point_diff=7
        )

        # Underdog gain should be more than favorite gain
        underdog_gain = underdog_win - 1400
        favorite_gain = favorite_win - 1600
        assert underdog_gain > favorite_gain

    def test_update_ratings_tie_moves_toward_equal(self):
        """Tie should move ratings toward each other."""
        elo_a, elo_b = EloService.update_ratings(
            winner_elo=1600, loser_elo=1400, point_diff=0, is_tie=True
        )

        # Higher rated team should drop
        assert elo_a < 1600
        # Lower rated team should rise
        assert elo_b > 1400

    def test_update_ratings_blowout_multiplier(self):
        """Blowout wins should have larger effect than close games."""
        blowout_win, blowout_loss = EloService.update_ratings(
            winner_elo=1500, loser_elo=1500, point_diff=35
        )

        close_win, close_loss = EloService.update_ratings(
            winner_elo=1500, loser_elo=1500, point_diff=3
        )

        blowout_change = blowout_win - 1500
        close_change = close_win - 1500
        assert blowout_change > close_change

    def test_get_win_probability_home_advantage(self):
        """Home team should have advantage in win probability."""
        home_prob, away_prob = EloService.get_win_probability(1500, 1500)

        # Home team should be favored when ratings are equal
        assert home_prob > 0.5
        assert away_prob < 0.5
        assert home_prob + away_prob == pytest.approx(1.0, abs=0.001)

    def test_margin_of_victory_multiplier_bounds(self):
        """MOV multiplier should be reasonable (1.0 to ~3.0)."""
        # Close game
        close_mult = EloService.calculate_margin_of_victory_multiplier(1500, 1500, 3)
        assert close_mult > 0.5
        assert close_mult < 5.0

        # Blowout
        blowout_mult = EloService.calculate_margin_of_victory_multiplier(1500, 1500, 42)
        assert blowout_mult > close_mult
        assert blowout_mult < 10.0

    def test_ratings_are_rounded(self):
        """Ratings should be rounded to 1 decimal place."""
        new_winner, new_loser = EloService.update_ratings(
            winner_elo=1500, loser_elo=1500, point_diff=7
        )

        # Check that both are rounded properly
        assert new_winner == round(new_winner, 1)
        assert new_loser == round(new_loser, 1)
