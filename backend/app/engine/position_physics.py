"""
Position-Specific Physics Engine
================================
Physics formulas for each position based on ENHANCEMENT_REFERENCE.md specifications.

Key Concepts:
- QB: Vision cone (120° FOV), OODA loop delays, pressure accuracy degradation
- RB: Momentum-based tackles (not dice roll), balance/COG system
- WR: 4-phase separation calculation, catch radius
- CB: Press jam physics, hip flip mechanics

CITATION: ENHANCEMENT_REFERENCE.md - Position-Specific Physics Deep Dive
"""

import math
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# COMMON PHYSICS UTILITIES
# =============================================================================

@dataclass
class Vector2D:
    """2D vector for positional calculations."""
    x: float = 0.0
    y: float = 0.0

    def distance_to(self, other: 'Vector2D') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)


@dataclass
class PlayerPhysicsState:
    """Current physics state of a player."""
    position: Vector2D
    velocity: Vector2D
    mass: float            # in lbs
    momentum: float = 0.0  # mass * speed
    facing_angle: float = 0.0  # degrees, 0 = upfield


# =============================================================================
# QUARTERBACK PHYSICS
# =============================================================================

class QuarterbackPhysics:
    """
    QB-specific physics: vision, decision-making, throw trajectory.

    Key Features:
    - 120° vision cone with raycasting
    - OODA loop reaction delay based on Awareness rating
    - Pressure accuracy penalty (exponential after 1.8s)
    """

    VISION_CONE_ANGLE = 120  # degrees
    POCKET_COLLAPSE_THRESHOLD = 1.8  # seconds

    def __init__(self, ratings: dict[str, int]):
        self.arm_strength = ratings.get("throw_power", 80)
        self.awareness = ratings.get("awareness", 80)
        self.release_speed = ratings.get("release", 80)
        self.poise = ratings.get("poise", 80)

        # Derived values
        # Decision time: 0.5s at 100 AWR, 2.5s at 0 AWR
        self.decision_time = 2.5 * (1 - self.awareness / 100)
        self.panic_factor = 1 - (self.poise / 100)

    def is_in_vision_cone(
        self,
        qb_position: Vector2D,
        qb_facing: float,
        target_position: Vector2D,
    ) -> bool:
        """
        Check if target is within QB's 120° vision cone.

        Args:
            qb_position: QB's current position
            qb_facing: QB's facing angle in degrees (0 = upfield)
            target_position: Position to check

        Returns:
            True if target is visible
        """
        # Calculate angle to target
        dx = target_position.x - qb_position.x
        dy = target_position.y - qb_position.y
        angle_to_target = math.degrees(math.atan2(dy, dx))

        # Normalize angles
        angle_diff = abs(angle_to_target - qb_facing)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff

        return angle_diff <= (self.VISION_CONE_ANGLE / 2)

    def calculate_ooda_delay(self, time_elapsed: float) -> tuple[bool, float]:
        """
        Calculate OODA (Observe-Orient-Decide-Act) loop delay.

        Low-awareness QBs have processing latency that delays decisions.

        Args:
            time_elapsed: Time since snap

        Returns:
            (can_make_decision, time_remaining_to_decide)
        """
        if time_elapsed >= self.decision_time:
            return (True, 0.0)
        else:
            return (False, self.decision_time - time_elapsed)

    def calculate_pressure_penalty(self, time_in_pocket: float) -> float:
        """
        Calculate accuracy penalty from pressure.

        Penalty is exponential beyond the pocket collapse threshold (1.8s).
        Elite "poise" QBs resist pressure better.

        Args:
            time_in_pocket: Seconds since snap

        Returns:
            Accuracy multiplier (0.5 - 1.0)
        """
        if time_in_pocket <= self.POCKET_COLLAPSE_THRESHOLD:
            return 1.0

        # Exponential decay beyond threshold
        excess_time = time_in_pocket - self.POCKET_COLLAPSE_THRESHOLD
        base_penalty = 0.3 * (excess_time ** 2)

        # Poise reduces penalty
        panic_modifier = self.panic_factor
        final_penalty = base_penalty * panic_modifier

        return max(0.5, 1.0 - final_penalty)

    def calculate_throw_velocity(self, distance_yards: float) -> float:
        """
        Calculate ball velocity based on arm strength and distance.

        Arm strength 1-99 maps to 45-65 mph ball velocity.
        """
        base_velocity = 45 + (self.arm_strength / 99 * 20)  # 45-65 mph

        # Adjust for distance (deep balls require more)
        if distance_yards > 30:
            velocity_needed = base_velocity * min(1.0, distance_yards / 40)
        else:
            velocity_needed = base_velocity * 0.8  # Don't overthrow short

        return velocity_needed


# =============================================================================
# RUNNING BACK PHYSICS
# =============================================================================

class TackleOutcome(str, Enum):
    """Possible outcomes of a tackle attempt."""
    TACKLED = "TACKLED"
    BROKEN_TACKLE = "BROKEN_TACKLE"
    STIFF_ARM = "STIFF_ARM"
    WRAPPED_UP = "WRAPPED_UP"


@dataclass
class TackleResult:
    """Result of a tackle attempt."""
    outcome: TackleOutcome
    yards_after_contact: float = 0.0
    velocity_retained: float = 0.0
    fumble_occurred: bool = False


class RunningBackPhysics:
    """
    RB-specific physics: momentum-based tackles, balance, contact.

    Key Features:
    - Momentum-based tackle resolution (NOT dice roll)
    - Balance/center-of-gravity affects tackle resistance
    - Collision angle modifiers (head-on vs side vs behind)
    - G-force injury risk on sharp cuts
    """

    def __init__(self, ratings: dict[str, int], weight: float = 215.0):
        self.mass = weight
        self.break_tackle = ratings.get("break_tackle", 75)
        self.balance = ratings.get("balance", 75)
        self.trucking = ratings.get("trucking", 70)
        self.speed = ratings.get("speed", 85)
        self.stiff_arm = ratings.get("stiff_arm", 70)
        self.elusiveness = ratings.get("elusiveness", 75)

        # Derived values
        self.top_speed = 40 / (ratings.get("forty_time", 4.5))  # yards/second

    def resolve_tackle_attempt(
        self,
        defender_mass: float,
        defender_velocity: float,
        defender_tackle_rating: int,
        collision_angle: float,
        rb_velocity: float,
    ) -> TackleResult:
        """
        Physics-based tackle resolution using momentum transfer.

        NOT a dice roll - outcome determined by physics.

        Args:
            defender_mass: Defender weight in lbs
            defender_velocity: Defender speed at contact
            defender_tackle_rating: Defender's tackle rating
            collision_angle: 0-180° (0=head-on, 90=perpendicular, 180=from behind)
            rb_velocity: RB speed at contact

        Returns:
            TackleResult with outcome and yards after contact
        """
        # Calculate momentum
        rb_momentum = self.mass * rb_velocity
        defender_momentum = defender_mass * defender_velocity

        # Angle modifier (harder to tackle from behind)
        angle_modifier = self._get_angle_modifier(collision_angle)
        effective_defender_momentum = defender_momentum * angle_modifier

        # Balance threshold (lower COG = harder to tackle)
        balance_threshold = (self.balance / 100) * 50

        # Net momentum
        net_momentum = rb_momentum - (effective_defender_momentum * math.cos(math.radians(collision_angle)))

        # Tackle power calculation
        tackle_power = (defender_tackle_rating / 100) * defender_momentum * angle_modifier

        # RB resistance
        rb_resistance = (self.break_tackle / 100) * net_momentum + balance_threshold

        # Determine outcome
        if tackle_power < rb_resistance * 0.6:
            # Clean broken tackle
            return TackleResult(
                outcome=TackleOutcome.BROKEN_TACKLE,
                yards_after_contact=max(0, net_momentum * 0.1),
                velocity_retained=0.7,
            )
        elif tackle_power < rb_resistance * 1.2:
            # Stiff arm battle
            if self._simulate_stiff_arm_battle(defender_tackle_rating):
                return TackleResult(
                    outcome=TackleOutcome.STIFF_ARM,
                    yards_after_contact=2.0,
                    velocity_retained=0.5,
                )
            else:
                return TackleResult(
                    outcome=TackleOutcome.WRAPPED_UP,
                    yards_after_contact=0.5,
                    velocity_retained=0.0,
                )
        else:
            # Clean tackle
            fumble = self._check_fumble(tackle_power / max(1, rb_resistance))
            return TackleResult(
                outcome=TackleOutcome.TACKLED,
                yards_after_contact=0.0,
                velocity_retained=0.0,
                fumble_occurred=fumble,
            )

    def _get_angle_modifier(self, angle: float) -> float:
        """Get tackle power modifier based on collision angle."""
        if angle < 30:
            return 1.0        # Head-on, full tackle force
        elif angle < 60:
            return 0.85       # Glancing blow
        elif angle < 120:
            return 0.7        # Side tackle
        else:
            return 0.5        # Chase-down from behind

    def _simulate_stiff_arm_battle(self, defender_tackle: int) -> bool:
        """Simulate stiff arm success based on ratings."""
        import random
        stiff_arm_chance = self.stiff_arm / (self.stiff_arm + defender_tackle)
        return random.random() < stiff_arm_chance

    def _check_fumble(self, force_ratio: float) -> bool:
        """Check if big hit causes fumble."""
        import random
        # Base 2% fumble chance, increases with force ratio
        fumble_chance = 0.02 * force_ratio
        return random.random() < fumble_chance

    def calculate_cut_injury_risk(
        self,
        cut_angle: float,
        current_speed: float,
        field_traction: float,
    ) -> float:
        """
        Calculate ACL injury risk on sharp cuts.

        Based on biomechanics - high G-force cuts increase injury risk.

        Args:
            cut_angle: Degrees of direction change (0-90)
            current_speed: Current speed in yards/second
            field_traction: Field traction coefficient (0.4 = mud, 1.0 = dry)

        Returns:
            Injury probability (0.0 - 1.0)
        """
        # Maximum cut angle limited by physics
        max_cut = 90 * (self.elusiveness / 100)

        # Calculate lateral G-force
        effective_traction = field_traction * (1 - 0.3)  # Fatigue penalty
        lateral_g_force = (current_speed ** 2) / (2 * effective_traction)

        # ACL injury probability (non-contact)
        # Risk increases above 2.5G
        injury_risk = max(0, (lateral_g_force - 2.5) * 0.01)

        return min(0.05, injury_risk)  # Cap at 5%


# =============================================================================
# WIDE RECEIVER PHYSICS
# =============================================================================

class WideReceiverPhysics:
    """
    WR-specific physics: route running, separation, catch mechanics.

    Key Features:
    - 4-phase separation calculation (release, stem, break, vertical)
    - Catch radius based on height/jumping/hand size
    - Contested catch mechanics
    """

    def __init__(
        self,
        ratings: dict[str, int],
        height_inches: int = 72,
        hand_size: float = 9.5,
    ):
        self.route_running = ratings.get("route_running", 80)
        self.release = ratings.get("release", 75)
        self.acceleration = ratings.get("acceleration", 85)
        self.speed = ratings.get("speed", 88)
        self.catching = ratings.get("catching", 85)
        self.catch_in_traffic = ratings.get("catch_in_traffic", 75)
        self.spectacular_catch = ratings.get("spectacular_catch", 70)
        self.jumping = ratings.get("jumping", 80)

        self.height = height_inches
        self.hand_size = hand_size

        # Derived values
        self.top_speed = 40 / (ratings.get("forty_time", 4.45))
        self.catch_radius = self._calculate_catch_radius()

    def _calculate_catch_radius(self) -> float:
        """
        Calculate catch radius based on physical attributes.

        Height/jumping/hand size all contribute.
        """
        height_factor = (self.height - 66) / 12  # Normalized (66" = 0, 78" = 1)
        jump_factor = self.jumping / 100
        hand_factor = (self.hand_size - 8) / 2  # Normalized (8" = 0, 10" = 1)

        # Base radius + modifiers
        base_radius = 1.5  # yards
        return base_radius + (height_factor * 0.3) + (jump_factor * 0.2) + (hand_factor * 0.1)

    def calculate_separation(
        self,
        cb_acceleration: int,
        cb_speed: int,
        cb_press: int,
        cb_change_of_direction: int,
        route_break_angle: float,
        time_elapsed: float,
    ) -> float:
        """
        Calculate separation from CB at each route phase.

        4-Phase System:
        - Phase 1 (0-0.5s): Release off line
        - Phase 2 (0.5-1.5s): Route stem
        - Phase 3 (1.5-2.0s): Break point (critical!)
        - Phase 4 (2.0s+): Vertical race

        Args:
            cb_*: Cornerback ratings
            route_break_angle: Angle of route break (0-90°)
            time_elapsed: Time since snap

        Returns:
            Separation distance in yards
        """
        separation = 0.0

        # Phase 1: Release (0-0.5s)
        if time_elapsed < 0.5:
            release_battle = self.release - cb_press
            if release_battle > 0:
                separation = release_battle / 20  # Max 2yd advantage
            else:
                separation = release_battle / 30  # Jammed

        # Phase 2: Route stem (0.5-1.5s)
        elif time_elapsed < 1.5:
            speed_diff = self.acceleration - cb_acceleration
            separation += speed_diff * 0.1 * (time_elapsed - 0.5)

        # Phase 3: Break point (1.5-2.0s) - CRITICAL
        elif time_elapsed < 2.0:
            break_quality = (self.route_running / 100) * (route_break_angle / 90)
            cb_hip_flip = cb_change_of_direction / 100

            if break_quality > cb_hip_flip:
                separation += (break_quality - cb_hip_flip) * 8  # Up to 8yd
            else:
                separation += 1.0  # Minimal window

        # Phase 4: Vertical (2.0s+)
        else:
            top_speed_diff = self.top_speed - (40 / (4.4 + (100 - cb_speed) * 0.02))
            separation += top_speed_diff * (time_elapsed - 2.0)

        return max(0, separation)

    def attempt_catch(
        self,
        ball_distance: float,
        defender_distance: float,
        is_contested: bool,
    ) -> tuple[bool, str]:
        """
        Determine catch success.

        Args:
            ball_distance: Distance from WR to catch point
            defender_distance: Distance from nearest defender
            is_contested: Whether defender is jumping for ball

        Returns:
            (success, reason)
        """
        import random

        # Can't catch if out of reach
        if ball_distance > self.catch_radius:
            return (False, "out_of_reach")

        # Base catch probability
        base_catch = 0.95  # Elite baseline

        # Traffic penalty
        if defender_distance < 1.0:
            traffic_modifier = self.catch_in_traffic / 100
            traffic_penalty = (1.0 - traffic_modifier) * (1.0 - defender_distance)
        else:
            traffic_penalty = 0.0

        # Contested catch
        if is_contested:
            contested_modifier = self.spectacular_catch / 100
        else:
            contested_modifier = 1.0

        # Final probability
        catch_prob = base_catch * contested_modifier * (1 - traffic_penalty)

        if random.random() < catch_prob:
            return (True, "caught")
        else:
            reason = "tight_coverage" if traffic_penalty > 0.3 else "dropped"
            return (False, reason)


# =============================================================================
# CORNERBACK PHYSICS
# =============================================================================

class CornerbackPhysics:
    """
    CB-specific physics: press, coverage, ball skills.

    Key Features:
    - Press jam power calculation
    - Hip flip mechanics for route matching
    - Interception timing window
    """

    def __init__(self, ratings: dict[str, int]):
        self.press = ratings.get("press", 75)
        self.man_coverage = ratings.get("man_coverage", 80)
        self.zone_coverage = ratings.get("zone_coverage", 78)
        self.speed = ratings.get("speed", 88)
        self.acceleration = ratings.get("acceleration", 85)
        self.change_of_direction = ratings.get("change_of_direction", 80)
        self.ball_skills = ratings.get("ball_skills", 75)
        self.play_recognition = ratings.get("play_recognition", 78)
        self.strength = ratings.get("strength", 60)

    def execute_press_coverage(
        self,
        wr_release: int,
        wr_strength: int,
    ) -> tuple[float, float]:
        """
        Calculate press jam result.

        Args:
            wr_release: WR's release rating
            wr_strength: WR's strength rating

        Returns:
            (disruption_time, separation_penalty)
            - disruption_time: Seconds added to route
            - separation_penalty: Yards of separation lost/gained
        """
        # Jam power calculation
        jam_power = self.press * 0.6 + self.strength * 0.4
        wr_release_power = wr_release * 0.7 + wr_strength * 0.3

        jam_diff = jam_power - wr_release_power

        if jam_diff > 5:
            # Successful jam
            return (0.5, -3.5)  # Half second delay, 3.5yd less separation
        elif jam_diff > -5:
            # Stalemate
            return (0.2, -1.0)
        else:
            # Failed jam - WR clean release
            return (0.0, 2.0)  # WR gains 2yd advantage

    def calculate_hip_flip_time(self, route_break_angle: float) -> float:
        """
        Calculate time to flip hips on route break.

        CBs with poor COD get beaten on sharp breaks.

        Args:
            route_break_angle: 0-90° route break

        Returns:
            Time in seconds to complete hip flip
        """
        if route_break_angle <= 45:
            return 0.0  # No hip flip needed

        # Time = Base (0.6s at 0 COD) scaled by rating
        base_time = 0.6
        cod_factor = (100 - self.change_of_direction) / 100

        return base_time * cod_factor

    def attempt_interception(
        self,
        ball_distance: float,
        wr_distance_to_ball: float,
        ball_flight_time: float,
    ) -> tuple[bool, str]:
        """
        Attempt to intercept pass.

        Args:
            ball_distance: CB distance to catch point
            wr_distance_to_ball: WR distance to catch point
            ball_flight_time: Time until ball arrives

        Returns:
            (success, outcome)
        """
        import random

        # Read time based on play recognition
        read_delay = (100 - self.play_recognition) / 100 * 0.3

        # Time available to reach ball
        time_available = ball_flight_time - read_delay

        # Can CB reach the ball?
        closing_speed = self.speed / 10  # yards per second (simplified)
        can_reach = (ball_distance / closing_speed) <= time_available

        if not can_reach:
            return (False, "unreachable")

        # Timing window (±0.15s for clean catch)
        arrival_time = ball_distance / closing_speed
        timing_error = abs(arrival_time - ball_flight_time)

        if timing_error > 0.15:
            return (False, "poor_timing")

        # Contested catch calculation
        if wr_distance_to_ball < 1.0:
            # 50/50 ball
            cb_catch = self.ball_skills
            int_probability = 0.5 + (cb_catch / 100 - 0.5) * 0.3
        else:
            # CB alone at catch point
            int_probability = self.ball_skills / 100 * 0.9

        if random.random() < int_probability:
            return (True, "interception")
        else:
            return (False, "dropped_int" if wr_distance_to_ball > 1.0 else "contested")
