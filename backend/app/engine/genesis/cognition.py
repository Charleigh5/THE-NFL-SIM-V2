#!/usr/bin/env python3
"""
S2 Cognition Engine - GENESIS Biological
=========================================
Cognitive processing model for player decision-making.

Phase 2: GENESIS Biological Player Modeling
- OODA Loop (Observe-Orient-Decide-Act) timing
- Vision cone and field awareness
- Processing speed affects read progression
- Stress/pressure cognitive degradation

Context7 Best Practices:
- Dataclasses for state
- Pure functions for calculations
- No side effects in core logic
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math


# ============================================================================
# ENUMS
# ============================================================================

class CognitiveState(str, Enum):
    """Current cognitive state of a player."""
    RELAXED = "RELAXED"         # Pre-snap, no pressure
    FOCUSED = "FOCUSED"         # Normal play conditions
    STRESSED = "STRESSED"       # Under moderate pressure
    PANICKED = "PANICKED"       # Extreme pressure, mistakes likely
    FLOW = "FLOW"               # Peak performance state


class ReadPhase(str, Enum):
    """Current phase of read progression."""
    PRE_SNAP = "PRE_SNAP"       # Reading defense alignment
    POST_SNAP = "POST_SNAP"     # Initial read after snap
    FIRST_READ = "FIRST_READ"   # Looking at primary receiver
    SECOND_READ = "SECOND_READ" # Checking second option
    SCRAMBLE = "SCRAMBLE"       # Looking to run or dump off
    PANIC = "PANIC"             # Throwing it away or taking sack


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class OODAState:
    """
    OODA Loop (Observe-Orient-Decide-Act) timing state.

    Each phase has a time cost in milliseconds.
    """
    observe_time_ms: float = 100.0    # Time to gather visual info
    orient_time_ms: float = 80.0      # Time to process and understand
    decide_time_ms: float = 60.0      # Time to make decision
    act_time_ms: float = 40.0         # Time to initiate action

    @property
    def total_loop_time_ms(self) -> float:
        """Total time for one OODA loop iteration."""
        return (
            self.observe_time_ms +
            self.orient_time_ms +
            self.decide_time_ms +
            self.act_time_ms
        )

    @property
    def total_loop_time_s(self) -> float:
        """Total time in seconds."""
        return self.total_loop_time_ms / 1000.0

    def apply_cognition_modifier(self, s2_score: float) -> 'OODAState':
        """
        Apply S2 cognition score modifier to OODA times.

        Higher S2 scores = faster processing.
        S2 of 100 = baseline, 130 = ~25% faster, 70 = ~30% slower
        """
        modifier = 100.0 / max(s2_score, 50.0)  # Prevent division issues
        return OODAState(
            observe_time_ms=self.observe_time_ms * modifier,
            orient_time_ms=self.orient_time_ms * modifier,
            decide_time_ms=self.decide_time_ms * modifier,
            act_time_ms=self.act_time_ms,  # Physical action is not cognitive
        )


@dataclass
class VisionCone:
    """
    Player's field of vision for awareness calculations.
    """
    fov_degrees: float = 120.0       # Field of view in degrees
    focus_zone_degrees: float = 20.0  # High-detail central zone
    peripheral_degradation: float = 0.7  # Accuracy outside focus zone
    facing_angle: float = 0.0        # Current facing direction (0 = upfield)

    def can_see_target(
        self,
        player_pos: Tuple[float, float],
        target_pos: Tuple[float, float]
    ) -> Tuple[bool, float]:
        """
        Check if target is within vision cone.

        Returns:
            Tuple of (is_visible, detection_quality 0.0-1.0)
        """
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]

        # Calculate angle to target
        angle_to_target = math.degrees(math.atan2(dy, dx))

        # Normalize relative to facing
        relative_angle = abs(angle_to_target - self.facing_angle)
        if relative_angle > 180:
            relative_angle = 360 - relative_angle

        # Check if within FOV
        half_fov = self.fov_degrees / 2
        if relative_angle > half_fov:
            return False, 0.0

        # Calculate detection quality
        if relative_angle <= self.focus_zone_degrees / 2:
            quality = 1.0
        else:
            # Linear degradation in peripheral vision
            peripheral_range = half_fov - (self.focus_zone_degrees / 2)
            peripheral_distance = relative_angle - (self.focus_zone_degrees / 2)
            quality = 1.0 - (peripheral_distance / peripheral_range) * (1 - self.peripheral_degradation)

        return True, max(0.0, min(1.0, quality))


@dataclass
class CognitiveProfile:
    """
    Complete cognitive model for a player.
    """
    # Base attributes (from BiometricProfile)
    s2_cognition_score: float = 100.0
    reaction_time_ms: float = 250.0
    processing_speed: float = 100.0  # Percentile

    # Current state
    state: CognitiveState = CognitiveState.FOCUSED
    stress_level: float = 0.0  # 0-100
    focus_level: float = 50.0  # 0-100

    # Vision
    vision: VisionCone = field(default_factory=VisionCone)

    # OODA loop state
    ooda: OODAState = field(default_factory=OODAState)

    # Read progression (QB-specific)
    current_read: ReadPhase = ReadPhase.PRE_SNAP
    read_timer_ms: float = 0.0
    reads_completed: int = 0

    def get_effective_ooda(self) -> OODAState:
        """Get OODA times adjusted for current conditions."""
        base = self.ooda.apply_cognition_modifier(self.s2_cognition_score)

        # Stress slows processing
        stress_modifier = 1.0 + (self.stress_level / 100.0) * 0.5

        # High focus speeds processing
        focus_modifier = 1.0 - (self.focus_level / 200.0)  # 0.5x at max focus

        combined_modifier = stress_modifier * focus_modifier

        return OODAState(
            observe_time_ms=base.observe_time_ms * combined_modifier,
            orient_time_ms=base.orient_time_ms * combined_modifier,
            decide_time_ms=base.decide_time_ms * combined_modifier,
            act_time_ms=base.act_time_ms,
        )

    def update_state_from_stress(self) -> None:
        """Update cognitive state based on stress level."""
        if self.stress_level < 20 and self.focus_level > 70:
            self.state = CognitiveState.FLOW
        elif self.stress_level < 30:
            self.state = CognitiveState.RELAXED
        elif self.stress_level < 50:
            self.state = CognitiveState.FOCUSED
        elif self.stress_level < 75:
            self.state = CognitiveState.STRESSED
        else:
            self.state = CognitiveState.PANICKED

    def add_stress(self, amount: float) -> None:
        """Add stress (e.g., from pressure, bad play)."""
        self.stress_level = min(100.0, self.stress_level + amount)
        self.update_state_from_stress()

    def reduce_stress(self, amount: float) -> None:
        """Reduce stress (e.g., completed pass, timeout)."""
        self.stress_level = max(0.0, self.stress_level - amount)
        self.update_state_from_stress()


# ============================================================================
# COGNITION ENGINE
# ============================================================================

class CognitionEngine:
    """
    Engine for processing player cognitive decisions.

    Handles:
    - Read progression timing for QBs
    - Decision delay calculations
    - Stress and pressure effects
    - Vision-based awareness
    """

    def __init__(self, profile: Optional[CognitiveProfile] = None):
        self.profile = profile or CognitiveProfile()

    def calculate_decision_delay(
        self,
        complexity: float = 1.0,
        under_pressure: bool = False,
    ) -> float:
        """
        Calculate time needed to make a decision.

        Args:
            complexity: 1.0 = normal, higher = harder decision
            under_pressure: True if defenders nearby

        Returns:
            Decision time in seconds
        """
        ooda = self.profile.get_effective_ooda()

        # Base decision time
        base_time = ooda.total_loop_time_s

        # Complexity modifier
        complexity_factor = 0.5 + (complexity * 0.5)

        # Pressure adds time if stressed
        pressure_factor = 1.0
        if under_pressure:
            pressure_factor = 1.0 + (self.profile.stress_level / 200.0)

        return base_time * complexity_factor * pressure_factor

    def process_read_progression(
        self,
        elapsed_ms: float,
        defenders_nearby: int = 0,
        open_receiver_quality: Optional[List[float]] = None,
    ) -> Tuple[ReadPhase, int, bool]:
        """
        Process QB read progression for one time step.

        Args:
            elapsed_ms: Time since last call
            defenders_nearby: Number of defenders in face
            open_receiver_quality: Quality scores for each receiver (0-1)

        Returns:
            Tuple of (current_phase, reads_completed, should_throw)
        """
        if open_receiver_quality is None:
            open_receiver_quality = []

        self.profile.read_timer_ms += elapsed_ms

        ooda = self.profile.get_effective_ooda()
        time_per_read = ooda.total_loop_time_ms

        # Pressure speeds up decisions (but may cause mistakes)
        if defenders_nearby > 0:
            time_per_read *= 0.8
            self.profile.add_stress(elapsed_ms * 0.01 * defenders_nearby)

        # Check if we've completed another read
        reads_now = int(self.profile.read_timer_ms / time_per_read)
        new_reads = reads_now - self.profile.reads_completed

        if new_reads > 0:
            self.profile.reads_completed = reads_now

            # Update read phase
            if reads_now == 0:
                self.profile.current_read = ReadPhase.POST_SNAP
            elif reads_now == 1:
                self.profile.current_read = ReadPhase.FIRST_READ
            elif reads_now == 2:
                self.profile.current_read = ReadPhase.SECOND_READ
            elif reads_now >= 3:
                self.profile.current_read = ReadPhase.SCRAMBLE

        # Check if we should throw
        should_throw = False
        if self.profile.reads_completed > 0 and open_receiver_quality:
            # Look at receivers up to current read
            available = open_receiver_quality[:self.profile.reads_completed]
            if available:
                best_option = max(available)
                # Throw if receiver is clearly open or under heavy pressure
                threshold = 0.7 - (self.profile.stress_level / 200.0)
                if best_option > threshold:
                    should_throw = True

        # Panic check
        if self.profile.stress_level > 80:
            self.profile.current_read = ReadPhase.PANIC

        return (
            self.profile.current_read,
            self.profile.reads_completed,
            should_throw,
        )

    def reset_for_new_play(self) -> None:
        """Reset state for a new play."""
        self.profile.current_read = ReadPhase.PRE_SNAP
        self.profile.read_timer_ms = 0.0
        self.profile.reads_completed = 0
        self.profile.reduce_stress(10.0)  # Some stress relief between plays

    def can_see_player(
        self,
        own_position: Tuple[float, float],
        target_position: Tuple[float, float],
    ) -> Tuple[bool, float]:
        """
        Check if this player can see another player.

        Returns:
            Tuple of (can_see, detection_quality)
        """
        return self.profile.vision.can_see_target(own_position, target_position)
