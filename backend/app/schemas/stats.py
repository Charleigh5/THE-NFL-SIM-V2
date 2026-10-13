"""
Unified Stats Schemas
=====================
Pydantic V2 schemas for player stats, position-specific breakdowns,
league leaders (standard and expanded), and team stats.
"""

from enum import StrEnum
from typing import Any

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


class PositionType(StrEnum):
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
    games_started: int | None = None
    approximate_value: float | None = None

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

    completion_percentage: float | None = None
    yards_per_attempt: float | None = None
    adjusted_yards_per_attempt: float | None = None
    net_yards_per_attempt: float | None = None
    adjusted_net_yards_per_attempt: float | None = None
    touchdown_percentage: float | None = None
    interception_percentage: float | None = None
    sack_percentage: float | None = None
    passer_rating: float | None = None

    fantasy_points: float | None = None
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
    longest_rush: int | None = None

    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: int | None = None
    targets: int | None = None

    yards_from_scrimmage: int | None = None
    total_touchdowns: int | None = None
    yards_per_rush: float | None = None
    yards_per_reception: float | None = None
    receptions_per_game: float | None = None

    fumbles: int = 0
    fumbles_lost: int = 0

    fantasy_points: float | None = None
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
    longest_reception: int | None = None
    targets: int | None = None

    yards_per_reception: float | None = None
    receptions_per_game: float | None = None
    catch_percentage: float | None = None
    yards_per_target: float | None = None
    air_yards: int | None = None
    yards_after_catch: int | None = None

    pass_blocking_snaps: int | None = None
    run_blocking_snaps: int | None = None
    pressures_allowed: int | None = None
    penalties: int = 0

    rushing_attempts: int = 0
    rushing_yards: int = 0
    rushing_touchdowns: int = 0

    fumbles: int = 0
    fumbles_lost: int = 0

    fantasy_points: float | None = None
    two_point_conversions: int = 0


class TightEndStat(PlayerStat):
    """Comprehensive tight end statistics"""

    receptions: int = 0
    receiving_yards: int = 0
    receiving_touchdowns: int = 0
    longest_reception: int | None = None
    targets: int | None = None

    pancake_blocks: int | None = None
    blocking_efficiency: float | None = None

    yards_per_reception: float | None = None
    receptions_per_game: float | None = None
    catch_percentage: float | None = None

    fantasy_points: float | None = None
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
    pass_blocking_efficiency: float | None = None

    run_blocking_grade: float | None = None
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
    pressure_rate: float | None = None
    pass_rush_win_rate: float | None = None

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

    targets_in_coverage: int | None = None
    receptions_allowed: int | None = None
    yards_allowed: int | None = None
    interceptions: int = 0
    passes_defensed: int = 0
    passer_rating_allowed: float | None = None

    forced_fumbles: int = 0
    fumbles_recovered: int = 0
    defensive_touchdowns: int = 0


class DefensiveBackStat(PlayerStat):
    """Comprehensive defensive back statistics"""

    targets: int = 0
    receptions_allowed: int = 0
    yards_allowed: int = 0
    touchdowns_allowed: int = 0
    completion_percentage_allowed: float | None = None
    yards_per_coverage_snap: float | None = None
    passer_rating_allowed: float | None = None

    interceptions: int = 0
    passes_defensed: int = 0
    interception_return_yards: int = 0
    interception_return_touchdowns: int = 0

    tackles_total: int = 0
    tackles_solo: int = 0
    tackles_assist: int = 0
    missed_tackles: int = 0
    missed_tackle_percentage: float | None = None

    forced_fumbles: int = 0
    fumbles_recovered: int = 0
    defensive_touchdowns: int = 0


class KickerStat(PlayerStat):
    """Comprehensive kicker statistics"""

    field_goals_attempted: int = 0
    field_goals_made: int = 0
    field_goal_percentage: float | None = None
    longest_field_goal: int | None = None

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
    extra_point_percentage: float | None = None

    points: int = 0
    kickoffs: int = 0
    touchbacks: int = 0
    touchback_percentage: float | None = None


class PunterStat(PlayerStat):
    """Comprehensive punter statistics"""

    punts: int = 0
    punting_yards: int = 0
    yards_per_punt: float | None = None
    longest_punt: int | None = None
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

    yards_per_kickoff_return: float | None = None
    yards_per_punt_return: float | None = None
    fair_catches: int = 0


# ============================================================================
# LEAGUE LEADERS & TEAM STATS
# ============================================================================


class LeagueLeaders(BaseModel):
    """Unified league leaders supporting both basic categories and expanded metrics."""

    passing_yards: list[Any] = Field(default_factory=list)
    passing_tds: list[Any] | None = Field(default_factory=list)
    rushing_yards: list[Any] = Field(default_factory=list)
    rushing_tds: list[Any] | None = Field(default_factory=list)
    receiving_yards: list[Any] = Field(default_factory=list)
    receiving_tds: list[Any] | None = Field(default_factory=list)

    # Expanded / alternative metric fields
    passing_touchdowns: list[Any] | None = None
    passer_rating: list[Any] | None = None
    completion_percentage: list[Any] | None = None
    adjusted_net_yards_per_attempt: list[Any] | None = None
    rushing_touchdowns: list[Any] | None = None
    yards_per_carry: list[Any] | None = None
    receiving_touchdowns: list[Any] | None = None
    receptions: list[Any] | None = None
    yards_per_reception: list[Any] | None = None
    sacks: list[Any] | None = None
    interceptions: list[Any] | None = None
    total_tackles: list[Any] | None = None
    passes_defensed: list[Any] | None = None
    forced_fumbles: list[Any] | None = None
    field_goal_percentage: list[Any] | None = None
    punting_average: list[Any] | None = None
    kickoff_return_yards: list[Any] | None = None
    punt_return_yards: list[Any] | None = None
    passer_rating_against: list[Any] | None = None
    pressure_rate: list[Any] | None = None
    tackle_efficiency: list[Any] | None = None
    fantasy_points: list[Any] | None = None

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
    third_down_conversion_rate: float | None = None
    red_zone_efficiency: float | None = None

    points_allowed: int = 0
    total_yards_allowed: int = 0
    passing_yards_allowed: int = 0
    rushing_yards_allowed: int = 0
    takeaways: int = 0
    sacks: int = 0
    interceptions: int = 0

    field_goal_percentage: float | None = None
    punt_return_average: float | None = None
    kickoff_return_average: float | None = None

    strength_of_schedule: float | None = None
    simple_rating_system: float | None = None
    expected_wins: float | None = None
    turnover_margin: int | None = None

    model_config = ConfigDict(from_attributes=True)
