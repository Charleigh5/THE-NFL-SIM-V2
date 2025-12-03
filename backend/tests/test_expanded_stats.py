import pytest
from pydantic import ValidationError
from backend.app.schemas.expanded_stats import (
    PositionType,
    PlayerStat,
    QuarterbackStat,
    RunningBackStat,
    WideReceiverStat,
    TightEndStat,
    OffensiveLineStat,
    DefensiveLineStat,
    LinebackerStat,
    DefensiveBackStat,
    KickerStat,
    PunterStat,
    SpecialTeamsStat,
    LeagueLeaders,
    TeamStats
)
import datetime

class TestPositionType:
    """Test PositionType enum functionality"""

    def test_position_type_values(self):
        """Test that all expected position types are present"""
        expected_positions = [
            "Quarterback", "Running Back", "Wide Receiver", "Tight End",
            "Offensive Line", "Defensive Line", "Linebacker", "Defensive Back",
            "Kicker", "Punter", "Special Teams"
        ]

        actual_positions = [pos.value for pos in PositionType]
        assert set(expected_positions) == set(actual_positions)

    def test_position_type_enum_access(self):
        """Test enum access methods"""
        assert PositionType.QB.value == "Quarterback"
        assert PositionType.RB == PositionType("Running Back")

class TestPlayerStat:
    """Test base PlayerStat model"""

    def test_player_stat_creation(self):
        """Test basic player stat creation"""
        stat = PlayerStat(
            player_id=123,
            name="Test Player",
            team="TEST",
            position=PositionType.QB,
            games_played=16,
            games_started=15,
            approximate_value=12.5
        )

        assert stat.player_id == 123
        assert stat.name == "Test Player"
        assert stat.team == "TEST"
        assert stat.position == PositionType.QB
        assert stat.games_played == 16
        assert stat.games_started == 15
        assert stat.approximate_value == 12.5

    def test_player_stat_default_values(self):
        """Test default values for optional fields"""
        stat = PlayerStat(
            player_id=123,
            name="Test Player",
            team="TEST",
            position=PositionType.RB,
            games_played=10,
            games_started=8
            # approximate_value is optional
        )

        assert stat.approximate_value is None

    def test_player_stat_validation(self):
        """Test validation of required fields"""
        with pytest.raises(ValidationError):
            PlayerStat(
                name="Test Player",
                team="TEST",
                position=PositionType.WR,
                games_played=5
                # Missing player_id
            )

class TestQuarterbackStat:
    """Test QuarterbackStat model"""

    def test_qb_stat_creation(self):
        """Test comprehensive QB stat creation"""
        qb_stat = QuarterbackStat(
            player_id=1,
            name="Patrick Mahomes",
            team="KC",
            position=PositionType.QB,
            games_played=16,
            games_started=16,
            passing_attempts=580,
            completions=380,
            passing_yards=5000,
            passing_touchdowns=40,
            interceptions=12,
            times_sacked=25,
            sack_yards_lost=150,
            rushing_attempts=50,
            rushing_yards=250,
            rushing_touchdowns=2,
            fantasy_points=325.5,
            two_point_conversions=3,
            fumbles=5,
            fumbles_lost=2
        )

        assert qb_stat.passing_yards == 5000
        assert qb_stat.passer_rating is None  # Not calculated yet

    def test_qb_stat_default_calculated_fields(self):
        """Test that calculated fields are None by default"""
        qb_stat = QuarterbackStat(
            player_id=1,
            name="Test QB",
            team="TEST",
            position=PositionType.QB,
            games_played=1,
            passing_attempts=10,
            completions=5,
            passing_yards=50,
            passing_touchdowns=1,
            interceptions=0,
            times_sacked=1,
            sack_yards_lost=5
        )

        assert qb_stat.completion_percentage is None
        assert qb_stat.yards_per_attempt is None
        assert qb_stat.passer_rating is None

    def test_qb_stat_validation(self):
        """Test validation of QB-specific fields"""
        with pytest.raises(ValidationError):
            QuarterbackStat(
                player_id=1,
                name="Test QB",
                team="TEST",
                position=PositionType.QB,
                games_played=1,
                passing_attempts=10,
                completions=15,  # More completions than attempts
                passing_yards=50,
                passing_touchdowns=1,
                interceptions=0,
                times_sacked=1,
                sack_yards_lost=5
            )

class TestRunningBackStat:
    """Test RunningBackStat model"""

    def test_rb_stat_creation(self):
        """Test comprehensive RB stat creation"""
        rb_stat = RunningBackStat(
            player_id=2,
            name="Christian McCaffrey",
            team="SF",
            position=PositionType.RB,
            games_played=16,
            games_started=16,
            rushing_attempts=280,
            rushing_yards=1400,
            rushing_touchdowns=12,
            longest_rush=65,
            receptions=80,
            receiving_yards=700,
            receiving_touchdowns=5,
            longest_reception=45,
            targets=100,
            yards_from_scrimmage=2100,
            total_touchdowns=17,
            yards_per_rush=5.0,
            yards_per_reception=8.75,
            receptions_per_game=5.0,
            fantasy_points=310.2,
            two_point_conversions=2,
            fumbles=3,
            fumbles_lost=1
        )

        assert rb_stat.yards_from_scrimmage == 2100
        assert rb_stat.total_touchdowns == 17

    def test_rb_stat_validation(self):
        """Test validation of RB-specific fields"""
        with pytest.raises(ValidationError):
            RunningBackStat(
                player_id=2,
                name="Test RB",
                team="TEST",
                position=PositionType.RB,
                games_played=1,
                rushing_attempts=10,
                rushing_yards=-5,  # Negative yards
                rushing_touchdowns=1,
                receptions=5,
                receiving_yards=50
            )

class TestWideReceiverStat:
    """Test WideReceiverStat model"""

    def test_wr_stat_creation(self):
        """Test comprehensive WR stat creation"""
        wr_stat = WideReceiverStat(
            player_id=3,
            name="Tyreek Hill",
            team="MIA",
            position=PositionType.WR,
            games_played=16,
            games_started=16,
            receptions=119,
            receiving_yards=1710,
            receiving_touchdowns=12,
            longest_reception=80,
            targets=160,
            yards_per_reception=14.37,
            receptions_per_game=7.44,
            catch_percentage=74.38,
            yards_per_target=10.69,
            air_yards=850,
            yards_after_catch=860,
            rushing_attempts=5,
            rushing_yards=45,
            rushing_touchdowns=1,
            fantasy_points=285.7,
            two_point_conversions=1,
            fumbles=2,
            fumbles_lost=1
        )

        assert wr_stat.receiving_yards == 1710
        assert wr_stat.yards_after_catch == 860

class TestTeamStats:
    """Test TeamStats model"""

    def test_team_stat_creation(self):
        """Test comprehensive team stat creation"""
        team_stat = TeamStats(
            team_id=1,
            team_name="Kansas City Chiefs",
            season=2023,
            wins=14,
            losses=3,
            ties=0,
            points_scored=496,
            total_yards=6500,
            passing_yards=4800,
            rushing_yards=1700,
            turnovers=18,
            third_down_conversion_rate=48.5,
            red_zone_efficiency=65.2,
            points_allowed=320,
            total_yards_allowed=5200,
            passing_yards_allowed=3500,
            rushing_yards_allowed=1700,
            takeaways=28,
            sacks=45,
            interceptions=18,
            field_goal_percentage=88.2,
            punt_return_average=10.3,
            kickoff_return_average=22.1,
            strength_of_schedule=0.512,
            simple_rating_system=12.4,
            expected_wins=12.8,
            turnover_margin=10
        )

        assert team_stat.wins == 14
        assert team_stat.simple_rating_system == 12.4

class TestLeagueLeaders:
    """Test LeagueLeaders model"""

    def test_league_leaders_creation(self):
        """Test league leaders structure"""
        # Create sample player stats
        qb1 = PlayerStat(player_id=1, name="QB1", team="TM1", position=PositionType.QB, games_played=16)
        qb2 = PlayerStat(player_id=2, name="QB2", team="TM2", position=PositionType.QB, games_played=16)

        rb1 = PlayerStat(player_id=3, name="RB1", team="TM3", position=PositionType.RB, games_played=16)
        rb2 = PlayerStat(player_id=4, name="RB2", team="TM4", position=PositionType.RB, games_played=16)

        leaders = LeagueLeaders(
            passing_yards=[qb1, qb2],
            rushing_yards=[rb1, rb2],
            passing_touchdowns=[qb1],
            rushing_touchdowns=[rb1],
            receiving_yards=[],
            receiving_touchdowns=[],
            receptions=[],
            yards_per_reception=[],
            sacks=[],
            interceptions=[],
            total_tackles=[],
            passes_defensed=[],
            forced_fumbles=[],
            field_goal_percentage=[],
            punting_average=[],
            kickoff_return_yards=[],
            punt_return_yards=[],
            passer_rating_against=[],
            pressure_rate=[],
            tackle_efficiency=[],
            fantasy_points=[]
        )

        assert len(leaders.passing_yards) == 2
        assert len(leaders.rushing_yards) == 2

class TestDataValidation:
    """Test data validation scenarios"""

    def test_negative_stat_values(self):
        """Test that negative values are handled appropriately"""
        # Some stats can be negative (like sack yards lost)
        qb_stat = QuarterbackStat(
            player_id=1,
            name="Test QB",
            team="TEST",
            position=PositionType.QB,
            games_played=1,
            passing_attempts=10,
            completions=5,
            passing_yards=50,
            passing_touchdowns=1,
            interceptions=0,
            times_sacked=3,
            sack_yards_lost=-25  # Negative value is valid
        )
        assert qb_stat.sack_yards_lost == -25

    def test_zero_values(self):
        """Test that zero values are handled correctly"""
        rb_stat = RunningBackStat(
            player_id=2,
            name="Test RB",
            team="TEST",
            position=PositionType.RB,
            games_played=1,
            rushing_attempts=0,  # Zero attempts
            rushing_yards=0,
            rushing_touchdowns=0,
            receptions=0,
            receiving_yards=0
        )
        assert rb_stat.rushing_attempts == 0
        assert rb_stat.receiving_yards == 0

class TestModelInheritance:
    """Test model inheritance and polymorphism"""

    def test_player_stat_inheritance(self):
        """Test that position-specific models inherit from PlayerStat"""
        qb = QuarterbackStat(
            player_id=1,
            name="Test QB",
            team="TEST",
            position=PositionType.QB,
            games_played=1,
            passing_attempts=10
        )

        # Should have all PlayerStat fields
        assert hasattr(qb, 'player_id')
        assert hasattr(qb, 'name')
        assert hasattr(qb, 'team')
        assert hasattr(qb, 'position')
        assert hasattr(qb, 'games_played')

        # Should have QB-specific fields
        assert hasattr(qb, 'passing_attempts')
        assert hasattr(qb, 'completions')

    def test_polymorphic_behavior(self):
        """Test that different position models can be used interchangeably"""
        players = [
            QuarterbackStat(player_id=1, name="QB", team="TM1", position=PositionType.QB, games_played=1, passing_attempts=10),
            RunningBackStat(player_id=2, name="RB", team="TM2", position=PositionType.RB, games_played=1, rushing_attempts=5),
            WideReceiverStat(player_id=3, name="WR", team="TM3", position=PositionType.WR, games_played=1, receptions=3)
        ]

        # All should be instances of PlayerStat
        for player in players:
            assert isinstance(player, PlayerStat)

        # But maintain their specific types
        assert isinstance(players[0], QuarterbackStat)
        assert isinstance(players[1], RunningBackStat)
        assert isinstance(players[2], WideReceiverStat)

class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_maximum_values(self):
        """Test handling of very large values"""
        qb_stat = QuarterbackStat(
            player_id=1,
            name="Test QB",
            team="TEST",
            position=PositionType.QB,
            games_played=16,
            passing_attempts=1000,  # Very high attempt count
            completions=700,
            passing_yards=50000,  # Very high yardage
            passing_touchdowns=100,
            interceptions=5,
            times_sacked=100,
            sack_yards_lost=500
        )

        assert qb_stat.passing_yards == 50000
        assert qb_stat.passing_attempts == 1000

    def test_minimum_values(self):
        """Test handling of minimum valid values"""
        rb_stat = RunningBackStat(
            player_id=2,
            name="Test RB",
            team="TEST",
            position=PositionType.RB,
            games_played=1,
            rushing_attempts=1,  # Minimum attempt
            rushing_yards=1,  # Minimum positive yards
            rushing_touchdowns=0,
            receptions=0,
            receiving_yards=0
        )

        assert rb_stat.rushing_attempts == 1
        assert rb_stat.rushing_yards == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
