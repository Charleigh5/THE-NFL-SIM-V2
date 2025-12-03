from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from enum import Enum

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
    games_started: Optional[int] = None  # Made optional since not always available
    approximate_value: Optional[float] = None  # AV metric

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
    completion_percentage: Optional[float] = None
    yards_per_attempt: Optional[float] = None
    adjusted_yards_per_attempt: Optional[float] = None
    net_yards_per_attempt: Optional[float] = None
    adjusted_net_yards_per_attempt: Optional[float] = None
    touchdown_percentage: Optional[float] = None
    interception_percentage: Optional[float] = None
    sack_percentage: Optional[float] = None
    passer_rating: Optional[float] = None

    # Fantasy metrics
    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0
    fumbles: int = 0
    fumbles_lost: int = 0

class RunningBackStat(PlayerStat):
    """Comprehensive running back statistics"""
    # Rushing stats
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0
    longest_rush: Optional[int] = None

    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: Optional[int] = None
    targets: Optional[int] = None

    # Combined metrics
    yards_from_scrimmage: Optional[int] = None
    total_touchdowns: Optional[int] = None
    yards_per_rush: Optional[float] = None
    yards_per_reception: Optional[float] = None
    receptions_per_game: Optional[float] = None

    # Fumble stats
    fumbles: int = 0
    fumbles_lost: int = 0

    # Fantasy metrics
    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0

class WideReceiverStat(PlayerStat):
    """Comprehensive wide receiver statistics"""
    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: Optional[int] = None
    targets: Optional[int] = None

    # Advanced metrics
    yards_per_reception: Optional[float] = None
    receptions_per_game: Optional[float] = None
    catch_percentage: Optional[float] = None
    yards_per_target: Optional[float] = None
    air_yards: Optional[int] = None
    yards_after_catch: Optional[int] = None

    # Rushing stats (for WR who get occasional carries)
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0

    # Fumble stats
    fumbles: int = 0
    fumbles_lost: int = 0

    # Fantasy metrics
    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0

class TightEndStat(PlayerStat):
    """Comprehensive tight end statistics"""
    # Receiving stats
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: Optional[int] = None
    targets: Optional[int] = None

    # Blocking stats
    pancake_blocks: Optional[int] = None
    blocking_efficiency: Optional[float] = None

    # Advanced metrics
    yards_per_reception: Optional[float] = None
    receptions_per_game: Optional[float] = None
    catch_percentage: Optional[float] = None

    # Fantasy metrics
    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0

class OffensiveLineStat(PlayerStat):
    """Comprehensive offensive line statistics"""
    # Pass protection stats
    sacks_allowed: int = 0
    quarterback_hits_allowed: int = 0
    hurries_allowed: int = 0

    # Run blocking stats
    pancake_blocks: Optional[int] = None
    run_block_win_rate: Optional[float] = None

    # Advanced metrics
    pass_block_win_rate: Optional[float] = None
    pressure_rate_allowed: Optional[float] = None
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
    pressure_rate: Optional[float] = None
    run_stop_percentage: Optional[float] = None
    pass_rush_win_rate: Optional[float] = None
    tackle_efficiency: Optional[float] = None

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
    tackle_efficiency: Optional[float] = None
    coverage_snaps: Optional[int] = None
    run_defense_snaps: Optional[int] = None
    blitz_rate: Optional[float] = None
    completion_percentage_allowed: Optional[float] = None

class DefensiveBackStat(PlayerStat):
    """Comprehensive defensive back statistics"""
    # Standard defensive stats
    total_tackles: int = 0
    solo_tackles: int = 0
    assisted_tackles: int = 0
    interceptions: int = 0
    passes_defensed: int = 0
    interception_return_yards: Optional[int] = None
    interception_return_touchdowns: int = 0
    forced_fumbles: int = 0
    fumble_recoveries: int = 0

    # Advanced metrics
    target_rate: Optional[float] = None
    completion_percentage_allowed: Optional[float] = None
    yards_per_target_allowed: Optional[float] = None
    passer_rating_when_targeted: Optional[float] = None
    coverage_snaps: Optional[int] = None

class KickerStat(PlayerStat):
    """Comprehensive kicker statistics"""
    # Field goal stats
    field_goals_attempted: int = 0
    field_goals_made: int = 0
    field_goal_percentage: Optional[float] = None
    longest_field_goal: Optional[int] = None

    # Extra point stats
    extra_points_attempted: int = 0
    extra_points_made: int = 0
    extra_point_percentage: Optional[float] = None

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
    yards_per_punt: Optional[float] = None
    longest_punt: Optional[int] = None
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
    yards_per_kickoff_return: Optional[float] = None
    yards_per_punt_return: Optional[float] = None
    fair_catches: int = 0

class LeagueLeaders(BaseModel):
    """Expanded league leaders with comprehensive position-specific metrics"""
    # Passing leaders
    passing_yards: List[PlayerStat]
    passing_touchdowns: List[PlayerStat]
    passer_rating: List[PlayerStat]
    completion_percentage: List[PlayerStat]
    adjusted_net_yards_per_attempt: List[PlayerStat]

    # Rushing leaders
    rushing_yards: List[PlayerStat]
    rushing_touchdowns: List[PlayerStat]
    yards_per_carry: List[PlayerStat]

    # Receiving leaders
    receiving_yards: List[PlayerStat]
    receiving_touchdowns: List[PlayerStat]
    receptions: List[PlayerStat]
    yards_per_reception: List[PlayerStat]

    # Defensive leaders
    sacks: List[PlayerStat]
    interceptions: List[PlayerStat]
    total_tackles: List[PlayerStat]
    passes_defensed: List[PlayerStat]
    forced_fumbles: List[PlayerStat]

    # Special teams leaders
    field_goal_percentage: List[PlayerStat]
    punting_average: List[PlayerStat]
    kickoff_return_yards: List[PlayerStat]
    punt_return_yards: List[PlayerStat]

    # Advanced metrics leaders
    passer_rating_against: List[PlayerStat]
    pressure_rate: List[PlayerStat]
    tackle_efficiency: List[PlayerStat]
    fantasy_points: List[PlayerStat]

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
    third_down_conversion_rate: Optional[float] = None
    red_zone_efficiency: Optional[float] = None

    # Defensive stats
    points_allowed: int = 0
    total_yards_allowed: int = 0
    passing_yards_allowed: int = 0
    rushing_yards_allowed: int = 0
    takeaways: int = 0
    sacks: int = 0
    interceptions: int = 0

    # Special teams stats
    field_goal_percentage: Optional[float] = None
    punt_return_average: Optional[float] = None
    kickoff_return_average: Optional[float] = None

    # Advanced metrics
    strength_of_schedule: Optional[float] = None
    simple_rating_system: Optional[float] = None
    expected_wins: Optional[float] = None
    turnover_margin: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
