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
    CollisionResult,
    PhysicsState,
    PositionPhysics,
    Vector2,
    Vector3,
    calculate_acceleration,
    calculate_change_of_direction_time,
    calculate_deceleration,
    calculate_g_force,
    # Functions
    forty_to_yards_per_second,
    resolve_momentum_collision,
    speed_rating_to_forty,
)
from .defensive_back import (
    BreakType,
    CoverageType,
    DBPhysicsConfig,
    DBState,
    DefensiveBackPhysics,
)
from .offensive_line import (
    BlockerState,
    BlockType,
    GapResponsibility,
    OffensiveLinePhysics,
    OLPhysicsConfig,
)
from .pass_rush import (
    BlockerStance,
    PassRushConfig,
    PassRushPhysics,
    PassRushRep,
    RushMove,
)
from .quarterback import (
    PocketState,
    QBPhysicsConfig,
    QBState,
    QuarterbackPhysics,
    ThrowResult,
    ThrowType,
)
from .running_back import (
    ContactType,
    CutMove,
    CutType,
    RBPhysicsConfig,
    RBState,
    RunningBackPhysics,
    TackleAttempt,
)
from .wide_receiver import (
    CatchAttempt,
    CatchType,
    RouteType,
    WideReceiverPhysics,
    WRPhysicsConfig,
    WRState,
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
