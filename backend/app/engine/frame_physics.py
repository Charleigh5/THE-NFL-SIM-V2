"""
60Hz Frame Physics Engine
=========================
Phase 4: Frame-based simulation at 60 frames per second.

This module provides deterministic, frame-by-frame physics simulation
for NFL plays, enabling:
- Precise collision detection
- Reproducible outcomes via checksums
- Statistical validation against real NFL data

Architecture:
- Each play runs for up to MAX_PLAY_DURATION seconds
- Physics updated at FRAMES_PER_SECOND rate
- Frame data can be exported for replay/validation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import math
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS (B-061, B-062)
# =============================================================================

FRAMES_PER_SECOND = 60  # 60Hz tick rate
MAX_PLAY_DURATION = 10.0  # Maximum play duration in seconds
DELTA_T = 1.0 / FRAMES_PER_SECOND  # Time per frame (~16.67ms)
MAX_FRAMES = int(FRAMES_PER_SECOND * MAX_PLAY_DURATION)  # 600 frames

# Physics constants (yards/second)
MAX_PLAYER_SPEED = 10.0  # ~21 mph (elite speed)
ACCELERATION_RATE = 5.0  # Yards/s²
DECELERATION_RATE = 8.0  # Yards/s² (braking is faster)

# Collision detection
TACKLE_RADIUS = 1.5  # Yards - contact distance
CATCH_RADIUS = 2.0  # Yards - ball catch distance

# Field dimensions (in yards)
FIELD_LENGTH = 100.0
FIELD_WIDTH = 53.33


class PlayerState(str, Enum):
    """Current state of a player in the simulation."""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    BLOCKING = "BLOCKING"
    RUSHING = "RUSHING"  # Pass rush
    COVERING = "COVERING"  # Coverage
    ROUTE_RUNNING = "ROUTE_RUNNING"
    TACKLING = "TACKLING"
    TACKLED = "TACKLED"
    CATCHING = "CATCHING"
    HAS_BALL = "HAS_BALL"


class PlayOutcome(str, Enum):
    """Possible outcomes for a play."""
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    SACK = "SACK"
    INTERCEPTION = "INTERCEPTION"
    FUMBLE = "FUMBLE"
    TOUCHDOWN = "TOUCHDOWN"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Vector2D:
    """2D position/velocity vector."""
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self) -> "Vector2D":
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def distance_to(self, other: "Vector2D") -> float:
        return (self - other).magnitude()

    def to_dict(self) -> dict:
        return {"x": round(self.x, 3), "y": round(self.y, 3)}


@dataclass
class PhysicsPlayer:
    """Player state in the physics simulation."""
    player_id: int
    position: Vector2D
    velocity: Vector2D = field(default_factory=lambda: Vector2D(0, 0))
    target_position: Optional[Vector2D] = None
    state: PlayerState = PlayerState.IDLE
    has_ball: bool = False
    is_offense: bool = True
    max_speed: float = 8.0  # Yards/second based on speed rating

    # Attributes (0-100 scale)
    speed_rating: int = 70
    acceleration_rating: int = 70
    agility_rating: int = 70
    tackle_rating: int = 50

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "position": self.position.to_dict(),
            "velocity": self.velocity.to_dict(),
            "state": self.state.value,
            "has_ball": self.has_ball,
            "is_offense": self.is_offense
        }


@dataclass
class PhysicsBall:
    """Ball state in the physics simulation."""
    position: Vector2D = field(default_factory=lambda: Vector2D(0, 0))
    velocity: Vector2D = field(default_factory=lambda: Vector2D(0, 0))
    height: float = 0.0  # Yards above ground
    is_in_air: bool = False
    is_loose: bool = False  # Fumble
    carrier_id: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "position": self.position.to_dict(),
            "height": round(self.height, 3),
            "is_in_air": self.is_in_air,
            "is_loose": self.is_loose,
            "carrier_id": self.carrier_id
        }


@dataclass
class PhysicsFrame:
    """Single frame of physics state."""
    frame_id: int
    timestamp: float  # Seconds since play start
    players: List[PhysicsPlayer]
    ball: PhysicsBall
    events: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "frame_id": self.frame_id,
            "timestamp": round(self.timestamp, 4),
            "players": [p.to_dict() for p in self.players],
            "ball": self.ball.to_dict(),
            "events": self.events
        }


@dataclass
class Collision:
    """Record of collision between players."""
    frame_id: int
    player1_id: int
    player2_id: int
    collision_type: str  # "TACKLE", "BLOCK", "CONTACT"
    impact_force: float  # For injury calculation


@dataclass
class PhysicsPlayResult:
    """Final result of physics simulation."""
    outcome: PlayOutcome
    yards_gained: float
    frames: List[PhysicsFrame]
    collisions: List[Collision]
    duration: float  # Actual play duration
    checksum: str  # Merkle tree hash for validation

    def to_dict(self) -> dict:
        return {
            "outcome": self.outcome.value,
            "yards_gained": round(self.yards_gained, 1),
            "frame_count": len(self.frames),
            "collision_count": len(self.collisions),
            "duration": round(self.duration, 3),
            "checksum": self.checksum
        }


# =============================================================================
# PHYSICS ENGINE
# =============================================================================

class FramePhysicsEngine:
    """
    60Hz Frame-based Physics Engine.

    Simulates a single play frame-by-frame for deterministic,
    reproducible results.
    """

    def __init__(self, rng: Any):
        self.rng = rng
        self.frames: List[PhysicsFrame] = []
        self.collisions: List[Collision] = []
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.play_outcome = PlayOutcome.IN_PROGRESS
        self.line_of_scrimmage = 0.0

        # Player registry
        self.players: Dict[int, PhysicsPlayer] = {}
        self.ball = PhysicsBall()

    def initialize_play(
        self,
        offense: List[Any],
        defense: List[Any],
        line_of_scrimmage: float,
        play_type: str = "PASS"
    ) -> None:
        """
        Initialize player positions for a play.

        Args:
            offense: Offensive player models
            defense: Defensive player models
            line_of_scrimmage: Yard line (0-100)
            play_type: "PASS" or "RUN"
        """
        self.line_of_scrimmage = line_of_scrimmage
        self.frames = []
        self.collisions = []
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.play_outcome = PlayOutcome.IN_PROGRESS
        self.players = {}

        # Position offense (simplified formation)
        for i, player in enumerate(offense or []):
            pos = self._get_offensive_position(i, player, line_of_scrimmage)
            max_speed = self._calculate_max_speed(player)

            self.players[player.id] = PhysicsPlayer(
                player_id=player.id,
                position=pos,
                is_offense=True,
                max_speed=max_speed,
                speed_rating=getattr(player, "speed", 70),
                acceleration_rating=getattr(player, "acceleration", 70),
                agility_rating=getattr(player, "agility", 70),
            )

        # Position defense
        for i, player in enumerate(defense or []):
            pos = self._get_defensive_position(i, player, line_of_scrimmage)
            max_speed = self._calculate_max_speed(player)

            self.players[player.id] = PhysicsPlayer(
                player_id=player.id,
                position=pos,
                is_offense=False,
                max_speed=max_speed,
                speed_rating=getattr(player, "speed", 70),
                tackle_rating=getattr(player, "tackle", 50),
            )

        # Position ball with QB (or center for run)
        qb = next((p for p in self.players.values() if p.is_offense), None)
        if qb:
            self.ball = PhysicsBall(
                position=Vector2D(qb.position.x, qb.position.y),
                carrier_id=qb.player_id
            )
            qb.has_ball = True

    def _get_offensive_position(
        self,
        index: int,
        player: Any,
        los: float
    ) -> Vector2D:
        """Get starting position for offensive player."""
        position = getattr(player, "position", "").upper()

        # Simple formation positioning
        positions = {
            "QB": Vector2D(los - 5, FIELD_WIDTH / 2),
            "RB": Vector2D(los - 7, FIELD_WIDTH / 2 - 2),
            "FB": Vector2D(los - 6, FIELD_WIDTH / 2 + 2),
            "WR": Vector2D(los, FIELD_WIDTH / 2 + (10 if index % 2 == 0 else -10)),
            "TE": Vector2D(los - 1, FIELD_WIDTH / 2 + 5),
            "LT": Vector2D(los - 1, FIELD_WIDTH / 2 - 4),
            "LG": Vector2D(los - 1, FIELD_WIDTH / 2 - 2),
            "C": Vector2D(los - 1, FIELD_WIDTH / 2),
            "RG": Vector2D(los - 1, FIELD_WIDTH / 2 + 2),
            "RT": Vector2D(los - 1, FIELD_WIDTH / 2 + 4),
        }

        # Match position prefix
        for pos_key, pos_val in positions.items():
            if position.startswith(pos_key):
                return pos_val

        # Default fallback
        return Vector2D(los - 3, FIELD_WIDTH / 2 + (index * 2 - 5))

    def _get_defensive_position(
        self,
        index: int,
        player: Any,
        los: float
    ) -> Vector2D:
        """Get starting position for defensive player."""
        position = getattr(player, "position", "").upper()

        # Simple defensive positioning
        if "DT" in position or "NT" in position:
            return Vector2D(los + 1, FIELD_WIDTH / 2 + (index % 2 - 0.5) * 2)
        elif "DE" in position or "LE" in position or "RE" in position:
            return Vector2D(los + 1, FIELD_WIDTH / 2 + (5 if "R" in position else -5))
        elif "MLB" in position or "ILB" in position:
            return Vector2D(los + 4, FIELD_WIDTH / 2)
        elif "LB" in position:
            return Vector2D(los + 4, FIELD_WIDTH / 2 + (index % 2 - 0.5) * 8)
        elif "CB" in position:
            return Vector2D(los + 2, FIELD_WIDTH / 2 + (15 if index % 2 == 0 else -15))
        elif "S" in position or "SS" in position or "FS" in position:
            return Vector2D(los + 12, FIELD_WIDTH / 2 + (5 if "S" in position else -5))

        # Default
        return Vector2D(los + 3, FIELD_WIDTH / 2 + (index * 2 - 5))

    def _calculate_max_speed(self, player: Any) -> float:
        """Calculate max speed in yards/second from speed rating."""
        speed_rating = getattr(player, "speed", 70)
        # Scale: 60 rating = 7 yds/s, 100 rating = 10 yds/s
        return 7.0 + (speed_rating - 60) * 0.075

    # =========================================================================
    # FRAME LOOP (B-063)
    # =========================================================================

    def execute_play(self) -> PhysicsPlayResult:
        """
        Execute the full play simulation at 60Hz.

        Returns:
            PhysicsPlayResult with all frames and outcome
        """
        logger.debug("Starting 60Hz physics simulation")

        # Record initial frame
        self._record_frame(events=["SNAP"])

        # Main simulation loop
        while not self._is_play_over() and self.current_frame < MAX_FRAMES:
            self.current_frame += 1
            self.elapsed_time = self.current_frame * DELTA_T

            # B-065: Update physics
            self._update_physics(DELTA_T)

            # B-064: Detect collisions
            collisions = self._detect_collisions()

            # Process collision effects
            events = self._process_collisions(collisions)

            # Record frame
            self._record_frame(events=events)

        # B-067: Generate final result
        return self._generate_play_result()

    # =========================================================================
    # PHYSICS UPDATE (B-065)
    # =========================================================================

    def _update_physics(self, delta_t: float) -> None:
        """
        Update all player and ball positions for one frame.

        Uses simple kinematics with acceleration towards target.
        """
        for player in self.players.values():
            if player.state == PlayerState.TACKLED:
                # Stopped movement
                player.velocity = Vector2D(0, 0)
                continue

            # Move towards target if set
            if player.target_position:
                direction = (player.target_position - player.position).normalized()

                # Accelerate towards target
                accel_rate = ACCELERATION_RATE * (player.acceleration_rating / 100.0)
                player.velocity = player.velocity + (direction * accel_rate * delta_t)

                # Cap at max speed
                if player.velocity.magnitude() > player.max_speed:
                    player.velocity = player.velocity.normalized() * player.max_speed

                # Check if reached target
                if player.position.distance_to(player.target_position) < 0.5:
                    player.target_position = None
            else:
                # Decelerate if no target
                speed = player.velocity.magnitude()
                if speed > 0.1:
                    decel = min(speed, DECELERATION_RATE * delta_t)
                    player.velocity = player.velocity.normalized() * (speed - decel)
                else:
                    player.velocity = Vector2D(0, 0)

            # Update position
            player.position = player.position + (player.velocity * delta_t)

            # Boundary checks
            player.position.x = max(0, min(FIELD_LENGTH, player.position.x))
            player.position.y = max(0, min(FIELD_WIDTH, player.position.y))

        # Update ball position
        if self.ball.carrier_id:
            carrier = self.players.get(self.ball.carrier_id)
            if carrier:
                self.ball.position = Vector2D(carrier.position.x, carrier.position.y)
        elif self.ball.is_in_air:
            # Simple projectile physics
            self.ball.position = self.ball.position + (self.ball.velocity * delta_t)
            self.ball.height = max(0, self.ball.height + (self.ball.velocity.y * delta_t))

            # Gravity effect on height
            self.ball.height -= 9.8 * delta_t  # Simplified

            if self.ball.height <= 0:
                self.ball.height = 0
                self.ball.is_in_air = False

    # =========================================================================
    # COLLISION DETECTION (B-064)
    # =========================================================================

    def _detect_collisions(self) -> List[Collision]:
        """
        Detect player-to-player collisions this frame.

        Returns list of collisions between offensive and defensive players.
        """
        collisions = []

        offense_players = [p for p in self.players.values() if p.is_offense]
        defense_players = [p for p in self.players.values() if not p.is_offense]

        for off_player in offense_players:
            for def_player in defense_players:
                distance = off_player.position.distance_to(def_player.position)

                # Check for tackle contact
                if distance < TACKLE_RADIUS:
                    # Calculate impact force based on velocities
                    relative_velocity = (off_player.velocity - def_player.velocity).magnitude()
                    impact_force = relative_velocity * 100  # Arbitrary scale

                    collision_type = "CONTACT"
                    if off_player.has_ball and def_player.state != PlayerState.BLOCKING:
                        collision_type = "TACKLE"
                    elif off_player.state == PlayerState.BLOCKING:
                        collision_type = "BLOCK"

                    collision = Collision(
                        frame_id=self.current_frame,
                        player1_id=off_player.player_id,
                        player2_id=def_player.player_id,
                        collision_type=collision_type,
                        impact_force=impact_force
                    )
                    collisions.append(collision)

        return collisions

    def _process_collisions(self, collisions: List[Collision]) -> List[str]:
        """Process collisions and update player states."""
        events = []

        for collision in collisions:
            self.collisions.append(collision)

            if collision.collision_type == "TACKLE":
                off_player = self.players.get(collision.player1_id)
                def_player = self.players.get(collision.player2_id)

                if off_player and off_player.has_ball:
                    # Tackle attempt - check if successful
                    tackle_rating = def_player.tackle_rating if def_player else 50
                    agility_rating = off_player.agility_rating

                    # Simple probability: tackle_rating / (tackle_rating + agility_rating)
                    tackle_prob = tackle_rating / (tackle_rating + agility_rating + 1)

                    if self.rng.random() < tackle_prob:
                        off_player.state = PlayerState.TACKLED
                        off_player.has_ball = False
                        self.play_outcome = PlayOutcome.COMPLETE
                        events.append(f"TACKLE:{def_player.player_id if def_player else 0}")

        return events

    # =========================================================================
    # PLAY TERMINATION (B-066)
    # =========================================================================

    def _is_play_over(self) -> bool:
        """
        Check if play should end.

        Returns True if:
        - Ball carrier is tackled
        - Incomplete pass
        - Turnover
        - Touchdown
        - Out of bounds
        """
        if self.play_outcome != PlayOutcome.IN_PROGRESS:
            return True

        # Check for touchdown
        ball_carrier = next(
            (p for p in self.players.values() if p.has_ball),
            None
        )
        if ball_carrier and ball_carrier.position.x >= FIELD_LENGTH:
            self.play_outcome = PlayOutcome.TOUCHDOWN
            return True

        # Check for safety (ball in endzone going backwards)
        if ball_carrier and ball_carrier.position.x <= 0:
            self.play_outcome = PlayOutcome.COMPLETE  # Safety handled elsewhere
            return True

        # Check for out of bounds
        if ball_carrier and (ball_carrier.position.y <= 0 or ball_carrier.position.y >= FIELD_WIDTH):
            self.play_outcome = PlayOutcome.OUT_OF_BOUNDS
            return True

        # Check if ball hit ground (incomplete pass)
        if self.ball.is_in_air and self.ball.height <= 0:
            self.play_outcome = PlayOutcome.INCOMPLETE
            return True

        return False

    def _record_frame(self, events: Optional[List[str]] = None) -> None:
        """Record current state as a frame."""
        frame = PhysicsFrame(
            frame_id=self.current_frame,
            timestamp=self.elapsed_time,
            players=[
                PhysicsPlayer(
                    player_id=p.player_id,
                    position=Vector2D(p.position.x, p.position.y),
                    velocity=Vector2D(p.velocity.x, p.velocity.y),
                    state=p.state,
                    has_ball=p.has_ball,
                    is_offense=p.is_offense,
                    max_speed=p.max_speed
                )
                for p in self.players.values()
            ],
            ball=PhysicsBall(
                position=Vector2D(self.ball.position.x, self.ball.position.y),
                height=self.ball.height,
                is_in_air=self.ball.is_in_air,
                is_loose=self.ball.is_loose,
                carrier_id=self.ball.carrier_id
            ),
            events=events or []
        )
        self.frames.append(frame)

    # =========================================================================
    # RESULT GENERATION (B-067)
    # =========================================================================

    def _generate_play_result(self) -> PhysicsPlayResult:
        """Generate final play result from frame data."""
        # Calculate yards gained
        yards_gained = 0.0
        ball_carrier = next(
            (p for p in self.players.values() if p.has_ball or p.state == PlayerState.TACKLED),
            None
        )
        if ball_carrier:
            yards_gained = ball_carrier.position.x - self.line_of_scrimmage

        # B-068: Generate checksum
        checksum = self._generate_checksum()

        return PhysicsPlayResult(
            outcome=self.play_outcome,
            yards_gained=yards_gained,
            frames=self.frames,
            collisions=self.collisions,
            duration=self.elapsed_time,
            checksum=checksum
        )

    # =========================================================================
    # CHECKSUM GENERATION (B-068)
    # =========================================================================

    def _generate_checksum(self) -> str:
        """
        Generate Merkle tree hash of frame data for validation.

        This enables replay verification and ensures determinism.
        """
        # Hash each frame
        frame_hashes = []
        for frame in self.frames:
            frame_data = json.dumps(frame.to_dict(), sort_keys=True)
            frame_hash = hashlib.sha256(frame_data.encode()).hexdigest()
            frame_hashes.append(frame_hash)

        # Build Merkle tree (simplified - just hash all frame hashes together)
        combined = "".join(frame_hashes)
        merkle_root = hashlib.sha256(combined.encode()).hexdigest()[:16]

        return merkle_root
