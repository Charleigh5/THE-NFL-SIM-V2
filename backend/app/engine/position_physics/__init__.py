"""
Position Physics Package
========================
Physics-based calculations for each position.

Phase 3: Position-Specific Physics
- QB: Throw trajectory, pressure timing
- RB: Momentum tackles, cut moves
- WR: Separation, catch probability
- DB: Press coverage, interceptions
- DL: Pass rush simulation
- OL: Blocking assignments, pocket shape
"""

from .base import (
    Vector2,
    Vector3,
    PhysicsState,
    CollisionResult,
    PositionPhysics,
    # Functions
    forty_to_yards_per_second,
    speed_rating_to_forty,
    calculate_acceleration,
    calculate_deceleration,
    calculate_change_of_direction_time,
    resolve_momentum_collision,
    calculate_g_force,
)

from .quarterback import (
    QuarterbackPhysics,
    QBState,
    QBPhysicsConfig,
    ThrowResult,
    ThrowType,
    PocketState,
)

from .running_back import (
    RunningBackPhysics,
    RBState,
    RBPhysicsConfig,
    TackleAttempt,
    CutMove,
    CutType,
    ContactType,
)

from .wide_receiver import (
    WideReceiverPhysics,
    WRState,
    WRPhysicsConfig,
    CatchAttempt,
    RouteType,
    CatchType,
)

from .defensive_back import (
    DefensiveBackPhysics,
    DBState,
    DBPhysicsConfig,
    CoverageType,
    BreakType,
)

from .pass_rush import (
    PassRushPhysics,
    PassRushRep,
    PassRushConfig,
    RushMove,
    BlockerStance,
)

from .offensive_line import (
    OffensiveLinePhysics,
    BlockerState,
    OLPhysicsConfig,
    BlockType,
    GapResponsibility,
)

__all__ = [
    # Base
    "Vector2", "Vector3", "PhysicsState", "CollisionResult", "PositionPhysics",
    "forty_to_yards_per_second", "speed_rating_to_forty",
    "calculate_acceleration", "calculate_deceleration",
    "calculate_change_of_direction_time", "resolve_momentum_collision",
    "calculate_g_force",
    # QB
    "QuarterbackPhysics", "QBState", "QBPhysicsConfig",
    "ThrowResult", "ThrowType", "PocketState",
    # RB
    "RunningBackPhysics", "RBState", "RBPhysicsConfig",
    "TackleAttempt", "CutMove", "CutType", "ContactType",
    # WR
    "WideReceiverPhysics", "WRState", "WRPhysicsConfig",
    "CatchAttempt", "RouteType", "CatchType",
    # DB
    "DefensiveBackPhysics", "DBState", "DBPhysicsConfig",
    "CoverageType", "BreakType",
    # DL
    "PassRushPhysics", "PassRushRep", "PassRushConfig",
    "RushMove", "BlockerStance",
    # OL
    "OffensiveLinePhysics", "BlockerState", "OLPhysicsConfig",
    "BlockType", "GapResponsibility",
]
