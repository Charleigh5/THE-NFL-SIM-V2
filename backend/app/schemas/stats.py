"""
Unified Stats Schemas
=====================
Pydantic V2 schemas for player stats, position-specific breakdowns,
league leaders (standard and expanded), and team stats.
"""

from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, ConfigDict, Field, model_validator


# ============================================================================
# BASIC LEADER SCHEMAS
# ============================================================================

class PlayerLeader(BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    value: int | float
    stat_type: str  # "passing_yards", "rushing_yards", "receiving_yards"

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# POSITION TYPES & BASE STAT MODELS
# ============================================================================

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
    games_started: Optional[int] = None
    approximate_value: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class QuarterbackStat(PlayerStat):
    """Comprehensive quarterback statistics"""
    passing_attempts: int = 0
    completions: int = 0
    passing_yards: int = 0
    passing_touchdowns: int = 0
    interceptions: int = 0
    times_sacked: int = 0
    sack_yards_lost: int = 0

    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0

    completion_percentage: Optional[float] = None
    yards_per_attempt: Optional[float] = None
    adjusted_yards_per_attempt: Optional[float] = None
    net_yards_per_attempt: Optional[float] = None
    adjusted_net_yards_per_attempt: Optional[float] = None
    touchdown_percentage: Optional[float] = None
    interception_percentage: Optional[float] = None
    sack_percentage: Optional[float] = None
    passer_rating: Optional[float] = None

    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0
    fumbles: int = 0
    fumbles_lost: int = 0

    @model_validator(mode="after")
    def validate_qb_logic(self):
        if self.completions > self.passing_attempts:
            raise ValueError("Completions cannot exceed passing attempts")
        return self


class RunningBackStat(PlayerStat):
    """Comprehensive running back statistics"""
    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0
    longest_rush: Optional[int] = None

    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: Optional[int] = None
    targets: Optional[int] = None

    yards_from_scrimmage: Optional[int] = None
    total_touchdowns: Optional[int] = None
    yards_per_rush: Optional[float] = None
    yards_per_reception: Optional[float] = None
    receptions_per_game: Optional[float] = None

    fumbles: int = 0
    fumbles_lost: int = 0

    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0

    @model_validator(mode="after")
    def validate_rb_logic(self):
        if self.rushing_yards < 0:
            raise ValueError("Rushing yards cannot be negative in this context")
        return self


class WideReceiverStat(PlayerStat):
    """Comprehensive wide receiver statistics"""
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: Optional[int] = None
    targets: Optional[int] = None

    yards_per_reception: Optional[float] = None
    receptions_per_game: Optional[float] = None
    catch_percentage: Optional[float] = None
    yards_per_target: Optional[float] = None
    air_yards: Optional[int] = None
    yards_after_catch: Optional[int] = None

    pass_blocking_snaps: Optional[int] = None
    run_blocking_snaps: Optional[int] = None
    pressures_allowed: Optional[int] = None
    penalties: int = 0

    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0

    fumbles: int = 0
    fumbles_lost: int = 0

    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0


class TightEndStat(PlayerStat):
    """Comprehensive tight end statistics"""
    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: Optional[int] = None
    targets: Optional[int] = None

    pancake_blocks: Optional[int] = None
    blocking_efficiency: Optional[float] = None

    yards_per_reception: Optional[float] = None
    receptions_per_game: Optional[float] = None
    catch_percentage: Optional[float] = None

    fantasy_points: Optional[float] = None
    two_point_conversions: int = 0


class OffensiveLineStat(PlayerStat):
    """Comprehensive offensive line statistics"""
    snaps_played: int = 0
    pass_blocking_snaps: int = 0
    run_blocking_snaps: int = 0

    sacks_allowed: int = 0
    hits_allowed: int = 0
    hurries_allowed: int = 0
    pressures_allowed: int = 0
    pass_blocking_efficiency: Optional[float] = None

    run_blocking_grade: Optional[float] = None
    blown_blocks: int = 0

    penalties: int = 0
    false_starts: int = 0
    holding_penalties: int = 0


class DefensiveLineStat(PlayerStat):
    """Comprehensive defensive line statistics"""
    tackles_total: int = 0
    tackles_solo: int = 0
    tackles_assist: int = 0
    tackles_for_loss: int = 0
    sacks: float = 0.0

    quarterback_hits: int = 0
    hurries: int = 0
    pressures: int = 0
    pressure_rate: Optional[float] = None
    pass_rush_win_rate: Optional[float] = None

    forced_fumbles: int = 0
    fumbles_recovered: int = 0
    defensive_touchdowns: int = 0

    stops: int = 0
    batted_passes: int = 0


class LinebackerStat(PlayerStat):
    """Comprehensive linebacker statistics"""
    tackles_total: int = 0
    tackles_solo: int = 0
    tackles_assist: int = 0
    tackles_for_loss: int = 0
    sacks: float = 0.0

    quarterback_hits: int = 0
    pressures: int = 0

    targets_in_coverage: Optional[int] = None
    receptions_allowed: Optional[int] = None
    yards_allowed: Optional[int] = None
    interceptions: int = 0
    passes_defensed: int = 0
    passer_rating_allowed: Optional[float] = None

    forced_fumbles: int = 0
    fumbles_recovered: int = 0
    defensive_touchdowns: int = 0


class DefensiveBackStat(PlayerStat):
    """Comprehensive defensive back statistics"""
    targets: int = 0
    receptions_allowed: int = 0
    yards_allowed: int = 0
    touchdowns_allowed: int = 0
    completion_percentage_allowed: Optional[float] = None
    yards_per_coverage_snap: Optional[float] = None
    passer_rating_allowed: Optional[float] = None

    interceptions: int = 0
    passes_defensed: int = 0
    interception_return_yards: int = 0
    interception_return_touchdowns: int = 0

    tackles_total: int = 0
    tackles_solo: int = 0
    tackles_assist: int = 0
    missed_tackles: int = 0
    missed_tackle_percentage: Optional[float] = None

    forced_fumbles: int = 0
    fumbles_recovered: int = 0
    defensive_touchdowns: int = 0


class KickerStat(PlayerStat):
    """Comprehensive kicker statistics"""
    field_goals_attempted: int = 0
    field_goals_made: int = 0
    field_goal_percentage: Optional[float] = None
    longest_field_goal: Optional[int] = None

    fg_1_19_made: int = 0
    fg_1_19_att: int = 0
    fg_20_29_made: int = 0
    fg_20_29_att: int = 0
    fg_30_39_made: int = 0
    fg_30_39_att: int = 0
    fg_40_49_made: int = 0
    fg_40_49_att: int = 0
    fg_50_plus_made: int = 0
    fg_50_plus_att: int = 0

    extra_points_attempted: int = 0
    extra_points_made: int = 0
    extra_point_percentage: Optional[float] = None

    points: int = 0
    kickoffs: int = 0
    touchbacks: int = 0
    touchback_percentage: Optional[float] = None


class PunterStat(PlayerStat):
    """Comprehensive punter statistics"""
    punts: int = 0
    punting_yards: int = 0
    yards_per_punt: Optional[float] = None
    longest_punt: Optional[int] = None
    punts_inside_20: int = 0
    touchbacks: int = 0
    punts_blocked: int = 0


class SpecialTeamsStat(PlayerStat):
    """Comprehensive special teams statistics"""
    kickoff_returns: int = 0
    kickoff_return_yards: int = 0
    kickoff_return_touchdowns: int = 0
    punt_returns: int = 0
    punt_return_yards: int = 0
    punt_return_touchdowns: int = 0

    special_teams_tackles: int = 0
    blocked_kicks: int = 0

    yards_per_kickoff_return: Optional[float] = None
    yards_per_punt_return: Optional[float] = None
    fair_catches: int = 0


# ============================================================================
# LEAGUE LEADERS & TEAM STATS
# ============================================================================

class LeagueLeaders(BaseModel):
    """Unified league leaders supporting both basic categories and expanded metrics."""
    passing_yards: List[Any] = Field(default_factory=list)
    passing_tds: Optional[List[Any]] = Field(default_factory=list)
    rushing_yards: List[Any] = Field(default_factory=list)
    rushing_tds: Optional[List[Any]] = Field(default_factory=list)
    receiving_yards: List[Any] = Field(default_factory=list)
    receiving_tds: Optional[List[Any]] = Field(default_factory=list)

    # Expanded / alternative metric fields
    passing_touchdowns: Optional[List[Any]] = None
    passer_rating: Optional[List[Any]] = None
    completion_percentage: Optional[List[Any]] = None
    adjusted_net_yards_per_attempt: Optional[List[Any]] = None
    rushing_touchdowns: Optional[List[Any]] = None
    yards_per_carry: Optional[List[Any]] = None
    receiving_touchdowns: Optional[List[Any]] = None
    receptions: Optional[List[Any]] = None
    yards_per_reception: Optional[List[Any]] = None
    sacks: Optional[List[Any]] = None
    interceptions: Optional[List[Any]] = None
    total_tackles: Optional[List[Any]] = None
    passes_defensed: Optional[List[Any]] = None
    forced_fumbles: Optional[List[Any]] = None
    field_goal_percentage: Optional[List[Any]] = None
    punting_average: Optional[List[Any]] = None
    kickoff_return_yards: Optional[List[Any]] = None
    punt_return_yards: Optional[List[Any]] = None
    passer_rating_against: Optional[List[Any]] = None
    pressure_rate: Optional[List[Any]] = None
    tackle_efficiency: Optional[List[Any]] = None
    fantasy_points: Optional[List[Any]] = None

    model_config = ConfigDict(from_attributes=True)


class TeamStats(BaseModel):
    """Team-level statistics."""
    team_id: int
    team_name: str
    season: int
    wins: int
    losses: int
    ties: int

    points_scored: int = 0
    total_yards: int = 0
    passing_yards: int = 0
    rushing_yards: int = 0
    turnovers: int = 0
    third_down_conversion_rate: Optional[float] = None
    red_zone_efficiency: Optional[float] = None

    points_allowed: int = 0
    total_yards_allowed: int = 0
    passing_yards_allowed: int = 0
    rushing_yards_allowed: int = 0
    takeaways: int = 0
    sacks: int = 0
    interceptions: int = 0

    field_goal_percentage: Optional[float] = None
    punt_return_average: Optional[float] = None
    kickoff_return_average: Optional[float] = None

    strength_of_schedule: Optional[float] = None
    simple_rating_system: Optional[float] = None
    expected_wins: Optional[float] = None
    turnover_margin: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
