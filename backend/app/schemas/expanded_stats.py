from enum import Enum

from pydantic import BaseModel, ConfigDict


class PositionType(str, Enum):
    """NFL Position Types"""
    QB = "Quarterback"
    RB = "Running Back"
    WR = "Wide Receiver"
    TE = "Tight End"
    OL = "Offensive Line"
    DL = "Defensive Line"
    LB = "Linebacker"
    DB = "Defensive Back"
    K = "Kicker"
    P = "Punter"
    ST = "Special Teams"

class PlayerStat(BaseModel):
    """Base player statistics with common fields"""
    player_id: int
    name: str
    team: str
    position: PositionType
    games_played: int
    games_started: int | None = None  # Made optional since not always available
    approximate_value: float | None = None  # AV metric

    model_config = ConfigDict(from_attributes=True)

class QuarterbackStat(PlayerStat):
    """Comprehensive quarterback statistics"""
    # Standard passing stats
    passing_attempts: int = 0
    completions: int = 0
    passing_yards: int = 0
    passing_touchdowns: int = 0
    interceptions: int = 0
    times_sacked: int = 0
    sack_yards_lost: int = 0

    # Rushing stats
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0

    # Advanced metrics
    completion_percentage: float | None = None
    yards_per_attempt: float | None = None
    adjusted_yards_per_attempt: float | None = None
    net_yards_per_attempt: float | None = None
    adjusted_net_yards_per_attempt: float | None = None
    touchdown_percentage: float | None = None
    interception_percentage: float | None = None
    sack_percentage: float | None = None
    passer_rating: float | None = None

    # Fantasy metrics
    fantasy_points: float | None = None
    two_point_conversions: int = 0
    fumbles: int = 0
    fumbles_lost: int = 0

class RunningBackStat(PlayerStat):
    """Comprehensive running back statistics"""
    # Rushing stats
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0
    longest_rush: int | None = None

    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: int | None = None
    targets: int | None = None

    # Combined metrics
    yards_from_scrimmage: int | None = None
    total_touchdowns: int | None = None
    yards_per_rush: float | None = None
    yards_per_reception: float | None = None
    receptions_per_game: float | None = None

    # Fumble stats
    fumbles: int = 0
    fumbles_lost: int = 0

    # Fantasy metrics
    fantasy_points: float | None = None
    two_point_conversions: int = 0

class WideReceiverStat(PlayerStat):
    """Comprehensive wide receiver statistics"""
    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: int | None = None
    targets: int | None = None

    # Advanced metrics
    yards_per_reception: float | None = None
    receptions_per_game: float | None = None
    catch_percentage: float | None = None
    yards_per_target: float | None = None
    air_yards: int | None = None
    yards_after_catch: int | None = None

    # Rushing stats (for WR who get occasional carries)
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0

    # Fumble stats
    fumbles: int = 0
    fumbles_lost: int = 0

    # Fantasy metrics
    fantasy_points: float | None = None
    two_point_conversions: int = 0

class TightEndStat(PlayerStat):
    """Comprehensive tight end statistics"""
    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: int | None = None
    targets: int | None = None

    # Blocking stats
    pancake_blocks: int | None = None
    blocking_efficiency: float | None = None

    # Advanced metrics
    yards_per_reception: float | None = None
    receptions_per_game: float | None = None
    catch_percentage: float | None = None

    # Fantasy metrics
    fantasy_points: float | None = None
    two_point_conversions: int = 0

class OffensiveLineStat(PlayerStat):
    """Comprehensive offensive line statistics"""
    # Pass protection stats
    sacks_allowed: int = 0
    quarterback_hits_allowed: int = 0
    hurries_allowed: int = 0

    # Run blocking stats
    pancake_blocks: int | None = None
    run_block_win_rate: float | None = None

    # Advanced metrics
    pass_block_win_rate: float | None = None
    pressure_rate_allowed: float | None = None
    penalties: int = 0

class DefensiveLineStat(PlayerStat):
    """Comprehensive defensive line statistics"""
    # Standard defensive stats
    total_tackles: int = 0
    solo_tackles: int = 0
    assisted_tackles: int = 0
    sacks: int = 0
    tackles_for_loss: int = 0
    quarterback_hits: int = 0
    forced_fumbles: int = 0
    fumble_recoveries: int = 0
    passes_defensed: int = 0

    # Advanced metrics
    pressure_rate: float | None = None
    run_stop_percentage: float | None = None
    pass_rush_win_rate: float | None = None
    tackle_efficiency: float | None = None

class LinebackerStat(PlayerStat):
    """Comprehensive linebacker statistics"""
    # Standard defensive stats
    total_tackles: int = 0
    solo_tackles: int = 0
    assisted_tackles: int = 0
    sacks: int = 0
    tackles_for_loss: int = 0
    interceptions: int = 0
    passes_defensed: int = 0
    forced_fumbles: int = 0
    fumble_recoveries: int = 0
    quarterback_hits: int = 0

    # Advanced metrics
    tackle_efficiency: float | None = None
    coverage_snaps: int | None = None
    run_defense_snaps: int | None = None
    blitz_rate: float | None = None
    completion_percentage_allowed: float | None = None

class DefensiveBackStat(PlayerStat):
    """Comprehensive defensive back statistics"""
    # Standard defensive stats
    total_tackles: int = 0
    solo_tackles: int = 0
    assisted_tackles: int = 0
    interceptions: int = 0
    passes_defensed: int = 0
    interception_return_yards: int | None = None
    interception_return_touchdowns: int = 0
    forced_fumbles: int = 0
    fumble_recoveries: int = 0

    # Advanced metrics
    target_rate: float | None = None
    completion_percentage_allowed: float | None = None
    yards_per_target_allowed: float | None = None
    passer_rating_when_targeted: float | None = None
    coverage_snaps: int | None = None

class KickerStat(PlayerStat):
    """Comprehensive kicker statistics"""
    # Field goal stats
    field_goals_attempted: int = 0
    field_goals_made: int = 0
    field_goal_percentage: float | None = None
    longest_field_goal: int | None = None

    # Extra point stats
    extra_points_attempted: int = 0
    extra_points_made: int = 0
    extra_point_percentage: float | None = None

    # Kickoff stats
    kickoffs: int = 0
    touchbacks: int = 0
    onside_kicks: int = 0
    onside_kicks_recovered: int = 0

class PunterStat(PlayerStat):
    """Comprehensive punter statistics"""
    # Punting stats
    punts: int = 0
    punting_yards: int = 0
    yards_per_punt: float | None = None
    longest_punt: int | None = None
    punts_inside_20: int = 0
    touchbacks: int = 0
    punts_blocked: int = 0

class SpecialTeamsStat(PlayerStat):
    """Comprehensive special teams statistics"""
    # Return stats
    kickoff_returns: int = 0
    kickoff_return_yards: int = 0
    kickoff_return_touchdowns: int = 0
    punt_returns: int = 0
    punt_return_yards: int = 0
    punt_return_touchdowns: int = 0

    # Coverage stats
    special_teams_tackles: int = 0
    blocked_kicks: int = 0

    # Advanced metrics
    yards_per_kickoff_return: float | None = None
    yards_per_punt_return: float | None = None
    fair_catches: int = 0

class LeagueLeaders(BaseModel):
    """Expanded league leaders with comprehensive position-specific metrics"""
    # Passing leaders
    passing_yards: list[PlayerStat]
    passing_touchdowns: list[PlayerStat]
    passer_rating: list[PlayerStat]
    completion_percentage: list[PlayerStat]
    adjusted_net_yards_per_attempt: list[PlayerStat]

    # Rushing leaders
    rushing_yards: list[PlayerStat]
    rushing_touchdowns: list[PlayerStat]
    yards_per_carry: list[PlayerStat]

    # Receiving leaders
    receiving_yards: list[PlayerStat]
    receiving_touchdowns: list[PlayerStat]
    receptions: list[PlayerStat]
    yards_per_reception: list[PlayerStat]

    # Defensive leaders
    sacks: list[PlayerStat]
    interceptions: list[PlayerStat]
    total_tackles: list[PlayerStat]
    passes_defensed: list[PlayerStat]
    forced_fumbles: list[PlayerStat]

    # Special teams leaders
    field_goal_percentage: list[PlayerStat]
    punting_average: list[PlayerStat]
    kickoff_return_yards: list[PlayerStat]
    punt_return_yards: list[PlayerStat]

    # Advanced metrics leaders
    passer_rating_against: list[PlayerStat]
    pressure_rate: list[PlayerStat]
    tackle_efficiency: list[PlayerStat]
    fantasy_points: list[PlayerStat]

class TeamStats(BaseModel):
    """Team-level statistics"""
    team_id: int
    team_name: str
    season: int
    wins: int
    losses: int
    ties: int

    # Offensive stats
    points_scored: int = 0
    total_yards: int = 0
    passing_yards: int = 0
    rushing_yards: int = 0
    turnovers: int = 0
    third_down_conversion_rate: float | None = None
    red_zone_efficiency: float | None = None

    # Defensive stats
    points_allowed: int = 0
    total_yards_allowed: int = 0
    passing_yards_allowed: int = 0
    rushing_yards_allowed: int = 0
    takeaways: int = 0
    sacks: int = 0
    interceptions: int = 0

    # Special teams stats
    field_goal_percentage: float | None = None
    punt_return_average: float | None = None
    kickoff_return_average: float | None = None

    # Advanced metrics
    strength_of_schedule: float | None = None
    simple_rating_system: float | None = None
    expected_wins: float | None = None
    turnover_margin: int | None = None

    model_config = ConfigDict(from_attributes=True)
