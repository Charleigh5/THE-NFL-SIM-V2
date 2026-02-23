"""
Elo Rating Service

Implements the Elo rating system for team power rankings.
The Elo system is a method for calculating the relative skill levels of teams.
Standard starting rating is 1500.
"""

import math

from sqlalchemy.orm import Session

from app.models.team import Team


class EloService:
    """
    Service for calculating and updating team Elo ratings.

    The Elo rating system is based on the following principles:
    1. Each team starts with a rating of 1500.
    2. After each game, ratings are adjusted based on the outcome.
    3. Beating a higher-rated team yields more points than beating a lower-rated team.
    4. The K-factor determines how much ratings change after each game.
    """

    # K-factor: How much ratings change per game.
    # NFL typically uses 20 for regular season, can be higher for playoffs.
    DEFAULT_K = 20.0

    # Home field advantage in Elo points (roughly 2.5 points in NFL)
    HOME_ADVANTAGE = 48.0  # ~3 point spread equivalent

    @staticmethod
    def calculate_expected_outcome(team_a_elo: float, team_b_elo: float) -> float:
        """
        Calculate the expected probability of team A winning.

        Uses the standard logistic curve formula:
        E_A = 1 / (1 + 10^((R_B - R_A) / 400))

        Args:
            team_a_elo: Current Elo rating of team A.
            team_b_elo: Current Elo rating of team B.

        Returns:
            Probability (0.0 to 1.0) of team A winning.
        """
        exponent = (team_b_elo - team_a_elo) / 400.0
        return 1.0 / (1.0 + math.pow(10, exponent))

    @staticmethod
    def calculate_margin_of_victory_multiplier(
        winner_elo: float, loser_elo: float, point_diff: int
    ) -> float:
        """
        Calculate a multiplier based on margin of victory.

        This prevents blowouts from having outsized effects while still
        rewarding decisive wins. Uses FiveThirtyEight's NFL formula.

        Args:
            winner_elo: Elo rating of the winning team.
            loser_elo: Elo rating of the losing team.
            point_diff: Absolute point differential (winner score - loser score).

        Returns:
            Margin of victory multiplier (typically 1.0 to 2.5).
        """
        # Natural log-based multiplier to dampen blowouts
        # Add 1 to point_diff to handle ties (point_diff = 0)
        log_multiplier = math.log(max(1, point_diff) + 1)

        # Adjustment for Elo difference (upsets get more credit)
        elo_diff = winner_elo - loser_elo
        elo_adjustment = 2.2 / (1.0 + 0.001 * elo_diff)

        return log_multiplier * elo_adjustment

    @staticmethod
    def update_ratings(
        winner_elo: float,
        loser_elo: float,
        point_diff: int,
        is_tie: bool = False,
        k_factor: float = None,
    ) -> tuple[float, float]:
        """
        Calculate new Elo ratings after a game.

        Args:
            winner_elo: Pre-game Elo rating of the winner.
            loser_elo: Pre-game Elo rating of the loser.
            point_diff: Margin of victory (0 for ties).
            is_tie: Whether the game ended in a tie.
            k_factor: Optional custom K-factor (default: 20).

        Returns:
            Tuple of (new_winner_elo, new_loser_elo).
        """
        k = k_factor if k_factor is not None else EloService.DEFAULT_K

        # Calculate expected outcomes
        expected_winner = EloService.calculate_expected_outcome(winner_elo, loser_elo)
        expected_loser = 1.0 - expected_winner

        if is_tie:
            # Ties: both teams get 0.5 as the actual outcome
            actual_winner = 0.5
            actual_loser = 0.5
            mov_multiplier = 1.0  # No MOV bonus for ties
        else:
            actual_winner = 1.0
            actual_loser = 0.0
            mov_multiplier = EloService.calculate_margin_of_victory_multiplier(
                winner_elo, loser_elo, point_diff
            )

        # Calculate rating changes
        winner_change = k * mov_multiplier * (actual_winner - expected_winner)
        loser_change = k * mov_multiplier * (actual_loser - expected_loser)

        new_winner_elo = winner_elo + winner_change
        new_loser_elo = loser_elo + loser_change

        return round(new_winner_elo, 1), round(new_loser_elo, 1)

    @classmethod
    def update_team_ratings(
        cls,
        db: Session,
        winner: Team,
        loser: Team,
        winner_score: int,
        loser_score: int,
    ) -> tuple[float, float]:
        """
        Update Elo ratings for two teams after a game.

        Args:
            db: Database session.
            winner: The winning Team object.
            loser: The losing Team object.
            winner_score: Points scored by the winner.
            loser_score: Points scored by the loser.

        Returns:
            Tuple of (new_winner_elo, new_loser_elo).
        """
        point_diff = winner_score - loser_score
        is_tie = point_diff == 0

        new_winner_elo, new_loser_elo = cls.update_ratings(
            winner_elo=winner.elo_rating or 1500.0,
            loser_elo=loser.elo_rating or 1500.0,
            point_diff=abs(point_diff),
            is_tie=is_tie,
        )

        # Update the team objects
        winner.elo_rating = new_winner_elo
        loser.elo_rating = new_loser_elo

        # Commit changes
        db.add(winner)
        db.add(loser)
        db.commit()

        return new_winner_elo, new_loser_elo

    @staticmethod
    def get_win_probability(home_team_elo: float, away_team_elo: float) -> tuple[float, float]:
        """
        Get the win probability for a matchup, including home field advantage.

        Args:
            home_team_elo: Elo rating of the home team.
            away_team_elo: Elo rating of the away team.

        Returns:
            Tuple of (home_win_prob, away_win_prob).
        """
        # Apply home field advantage
        adjusted_home_elo = home_team_elo + EloService.HOME_ADVANTAGE

        home_win_prob = EloService.calculate_expected_outcome(adjusted_home_elo, away_team_elo)
        away_win_prob = 1.0 - home_win_prob

        return round(home_win_prob, 3), round(away_win_prob, 3)
