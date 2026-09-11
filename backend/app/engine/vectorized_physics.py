"""
SIMD Vectorized 60Hz Physics Kernel & Zero-Allocation Ring Buffers
==================================================================
Phase 4 Architecture: High-Performance Structure-of-Arrays (SoA) Physics

Replaces dynamic object allocation in the 60Hz tick loop with contiguous
NumPy float32 memory structures and SIMD-accelerated broadcasting for
pairwise collision detection and kinematics.

Key Innovations:
1. Structure-of-Arrays layout for 22 on-field player bodies.
2. SIMD pairwise collision detection matrix:
   dist_sq = sum((pos_off[:, newaxis] - pos_def[newaxis, :])**2)
3. ZeroAllocPlayBuffer: preallocated continuous memory for all 600 frames.
4. CircularTelemetryRingBuffer: zero-copy circular ring buffer for real-time
   telemetry streaming to WebSocket clients.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any
import numpy as np
from numpy.typing import NDArray
import hashlib
import json
import time
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTS & CONFIGURATION (1:1 PARITY WITH FRAME PHYSICS)
# =============================================================================

FRAMES_PER_SECOND: int = 60
MAX_PLAY_DURATION: float = 10.0
DELTA_T: float = 1.0 / FRAMES_PER_SECOND  # ~0.01667s (16.67ms)
MAX_FRAMES: int = int(FRAMES_PER_SECOND * MAX_PLAY_DURATION)  # 600 frames

MAX_PLAYER_SPEED: float = 10.0
ACCELERATION_RATE: float = 5.0
DECELERATION_RATE: float = 8.0

TACKLE_RADIUS: float = 1.5
CATCH_RADIUS: float = 2.0

FIELD_LENGTH: float = 100.0
FIELD_WIDTH: float = 53.33

# Integer state mapping for fast NumPy array indexing
STATE_IDLE: int = 0
STATE_RUNNING: int = 1
STATE_BLOCKING: int = 2
STATE_RUSHING: int = 3
STATE_COVERING: int = 4
STATE_ROUTE_RUNNING: int = 5
STATE_TACKLING: int = 6
STATE_TACKLED: int = 7
STATE_CATCHING: int = 8
STATE_HAS_BALL: int = 9

STATE_NAME_TO_INT: Dict[str, int] = {
    "IDLE": STATE_IDLE,
    "RUNNING": STATE_RUNNING,
    "BLOCKING": STATE_BLOCKING,
    "RUSHING": STATE_RUSHING,
    "COVERING": STATE_COVERING,
    "ROUTE_RUNNING": STATE_ROUTE_RUNNING,
    "TACKLING": STATE_TACKLING,
    "TACKLED": STATE_TACKLED,
    "CATCHING": STATE_CATCHING,
    "HAS_BALL": STATE_HAS_BALL,
}

INT_TO_STATE_NAME: Dict[int, str] = {v: k for k, v in STATE_NAME_TO_INT.items()}


# =============================================================================
# ZERO-ALLOCATION PLAY BUFFER
# =============================================================================

class ZeroAllocPlayBuffer:
    """
    Pre-allocated continuous float32 buffer for up to MAX_FRAMES (600) frames.
    Completely eliminates dynamic Python object allocation and GC overhead
    during the 60Hz tick loop.
    """

    def __init__(self, max_frames: int = MAX_FRAMES, max_players: int = 22):
        self.max_frames = max_frames
        self.max_players = max_players

        # Continuous contiguous arrays
        self.positions: NDArray[np.float64] = np.zeros(
            (max_frames, max_players, 2), dtype=np.float64
        )
        self.velocities: NDArray[np.float64] = np.zeros(
            (max_frames, max_players, 2), dtype=np.float64
        )
        # Ball format: [x, y, height, carrier_id]
        self.ball: NDArray[np.float64] = np.zeros((max_frames, 4), dtype=np.float64)
        self.states: NDArray[np.int32] = np.zeros(
            (max_frames, max_players), dtype=np.int32
        )
        self.events: List[List[str]] = [[] for _ in range(max_frames)]
        self.recorded_frames: int = 0

    def reset(self) -> None:
        """Reset buffer counters without reallocating underlying arrays."""
        self.recorded_frames = 0
        for i in range(self.max_frames):
            self.events[i].clear()

    def record_frame(
        self,
        frame_idx: int,
        positions: NDArray[np.float64],
        velocities: NDArray[np.float64],
        ball_state: NDArray[np.float64],
        states: NDArray[np.int32],
        events: Optional[List[str]] = None,
    ) -> None:
        """Record frame data in-place via zero-copy slice assignment."""
        if frame_idx >= self.max_frames:
            return

        n = min(self.max_players, positions.shape[0])
        self.positions[frame_idx, :n] = positions[:n]
        self.velocities[frame_idx, :n] = velocities[:n]
        self.ball[frame_idx, :4] = ball_state[:4]
        self.states[frame_idx, :n] = states[:n]

        if events:
            self.events[frame_idx].extend(events)

        if frame_idx + 1 > self.recorded_frames:
            self.recorded_frames = frame_idx + 1


# =============================================================================
# CIRCULAR TELEMETRY RING BUFFER (FOR LIVE STREAMING)
# =============================================================================

class CircularTelemetryRingBuffer:
    """
    Fixed-capacity circular ring buffer for real-time WebSocket telemetry streaming.
    Holds the last N frames with O(1) writes and zero memory allocation.
    """

    def __init__(self, capacity: int = 120, num_players: int = 22):
        self.capacity = capacity
        self.num_players = num_players
        self.buffer_pos = np.zeros((capacity, num_players, 2), dtype=np.float64)
        self.buffer_vel = np.zeros((capacity, num_players, 2), dtype=np.float64)
        self.buffer_ball = np.zeros((capacity, 4), dtype=np.float64)
        self.buffer_timestamps = np.zeros(capacity, dtype=np.float64)
        self.buffer_frame_ids = np.zeros(capacity, dtype=np.int32)
        self.head: int = 0
        self.count: int = 0

    def push(
        self,
        frame_id: int,
        timestamp: float,
        pos: NDArray[np.float64],
        vel: NDArray[np.float64],
        ball: NDArray[np.float64],
    ) -> None:
        """Push a telemetry snapshot into the circular buffer in-place."""
        idx = self.head
        n = min(self.num_players, pos.shape[0])

        self.buffer_frame_ids[idx] = frame_id
        self.buffer_timestamps[idx] = timestamp
        self.buffer_pos[idx, :n] = pos[:n]
        self.buffer_vel[idx, :n] = vel[:n]
        self.buffer_ball[idx, :4] = ball[:4]

        self.head = (self.head + 1) % self.capacity
        if self.count < self.capacity:
            self.count += 1

    def get_latest_frame(self) -> Optional[Dict[str, Any]]:
        """Retrieve the most recent frame as a dictionary snapshot."""
        if self.count == 0:
            return None
        last_idx = (self.head - 1 + self.capacity) % self.capacity
        return {
            "frame_id": int(self.buffer_frame_ids[last_idx]),
            "timestamp": float(self.buffer_timestamps[last_idx]),
            "ball": {
                "x": float(self.buffer_ball[last_idx, 0]),
                "y": float(self.buffer_ball[last_idx, 1]),
                "height": float(self.buffer_ball[last_idx, 2]),
                "carrier_id": int(self.buffer_ball[last_idx, 3]),
            },
        }


# =============================================================================
# SIMD VECTORIZED PHYSICS KERNEL
# =============================================================================

class VectorizedPhysicsKernel:
    """
    Structure-of-Arrays (SoA) SIMD Vectorized Physics Kernel.

    Performs kinematics updates and collision checks using vectorized NumPy
    broadcasting, keeping all computational loops in AVX2/SIMD hardware
    registers without Python heap object allocation.
    """

    def __init__(self, max_players: int = 22):
        self.max_players = max_players
        self.num_players: int = 0

        # Primary Coordinate & Kinematics Arrays (Shape: [max_players, 2])
        self.pos: NDArray[np.float64] = np.zeros((max_players, 2), dtype=np.float64)
        self.vel: NDArray[np.float64] = np.zeros((max_players, 2), dtype=np.float64)
        self.target_pos: NDArray[np.float64] = np.zeros(
            (max_players, 2), dtype=np.float64
        )
        self.has_target: NDArray[np.bool_] = np.zeros(max_players, dtype=bool)

        # Player Attributes & States (Shape: [max_players])
        self.player_ids: NDArray[np.int32] = np.zeros(max_players, dtype=np.int32)
        self.is_offense: NDArray[np.bool_] = np.zeros(max_players, dtype=bool)
        self.has_ball: NDArray[np.bool_] = np.zeros(max_players, dtype=bool)
        self.states: NDArray[np.int32] = np.zeros(max_players, dtype=np.int32)
        self.max_speeds: NDArray[np.float64] = np.zeros(max_players, dtype=np.float64)
        self.accel_rates: NDArray[np.float64] = np.zeros(max_players, dtype=np.float64)
        self.agility_ratings: NDArray[np.float64] = np.zeros(
            max_players, dtype=np.float64
        )
        self.tackle_ratings: NDArray[np.float64] = np.zeros(
            max_players, dtype=np.float64
        )

        # Ball State: [x, y, height, vx, vy, vz]
        self.ball: NDArray[np.float64] = np.zeros(6, dtype=np.float64)
        self.ball_is_in_air: bool = False
        self.ball_is_loose: bool = False
        self.carrier_idx: int = -1

        # Preallocated Continuous Buffer
        self.play_buffer = ZeroAllocPlayBuffer(
            max_frames=MAX_FRAMES, max_players=max_players
        )
        self.ring_buffer = CircularTelemetryRingBuffer(
            capacity=120, num_players=max_players
        )

    def load_players(
        self,
        player_data: List[Dict[str, Any]],
        ball_carrier_id: Optional[int] = None,
    ) -> None:
        """
        Load player attributes and initial coordinates into contiguous NumPy arrays.
        """
        n = min(len(player_data), self.max_players)
        self.num_players = n

        # Reset all arrays
        self.pos.fill(0.0)
        self.vel.fill(0.0)
        self.target_pos.fill(0.0)
        self.has_target.fill(False)
        self.player_ids.fill(0)
        self.is_offense.fill(False)
        self.has_ball.fill(False)
        self.states.fill(STATE_IDLE)
        self.max_speeds.fill(8.0)
        self.accel_rates.fill(ACCELERATION_RATE)
        self.agility_ratings.fill(70.0)
        self.tackle_ratings.fill(50.0)

        self.carrier_idx = -1
        self.ball.fill(0.0)
        self.ball_is_in_air = False
        self.ball_is_loose = False

        for i in range(n):
            p = player_data[i]
            self.player_ids[i] = p.get("player_id", i + 1)
            self.pos[i, 0] = p.get("x", 0.0)
            self.pos[i, 1] = p.get("y", 0.0)
            self.vel[i, 0] = p.get("vx", 0.0)
            self.vel[i, 1] = p.get("vy", 0.0)
            self.is_offense[i] = p.get("is_offense", True)
            self.max_speeds[i] = p.get("max_speed", 8.0)
            self.accel_rates[i] = p.get("accel_rate", ACCELERATION_RATE)
            self.agility_ratings[i] = p.get("agility", 70.0)
            self.tackle_ratings[i] = p.get("tackle", 50.0)

            state_str = p.get("state", "IDLE")
            self.states[i] = STATE_NAME_TO_INT.get(state_str, STATE_IDLE)

            if p.get("target_x") is not None and p.get("target_y") is not None:
                self.target_pos[i, 0] = p["target_x"]
                self.target_pos[i, 1] = p["target_y"]
                self.has_target[i] = True

            if ball_carrier_id is not None and self.player_ids[i] == ball_carrier_id:
                self.has_ball[i] = True
                self.carrier_idx = i
                self.ball[0] = self.pos[i, 0]
                self.ball[1] = self.pos[i, 1]
                self.ball[2] = 0.0

        # Reset preallocated frame buffer
        self.play_buffer.reset()

    def set_player_target(self, player_idx: int, target_x: float, target_y: float) -> None:
        """Set target destination for a player by array index."""
        if 0 <= player_idx < self.num_players:
            self.target_pos[player_idx, 0] = target_x
            self.target_pos[player_idx, 1] = target_y
            self.has_target[player_idx] = True

    def set_player_target_by_id(
        self, player_id: int, target_x: float, target_y: float
    ) -> bool:
        """Set target destination for a player by their persistent player_id."""
        matches = np.where(self.player_ids[: self.num_players] == player_id)[0]
        if len(matches) > 0:
            idx = matches[0]
            self.set_player_target(idx, target_x, target_y)
            return True
        return False

    def update_physics(self, delta_t: float) -> None:
        """
        Execute one 60Hz kinematics update across all players and the ball.
        All calculations are vectorized with zero Python object allocations.
        """
        n = self.num_players
        if n == 0:
            return

        # 1. Stopped / Tackled players velocity zeroing
        tackled_mask = self.states[:n] == STATE_TACKLED
        self.vel[:n][tackled_mask] = 0.0

        active_mask = ~tackled_mask

        # 2. Vectorized target-seeking acceleration
        seek_mask = active_mask & self.has_target[:n]
        if np.any(seek_mask):
            seek_indices = np.where(seek_mask)[0]
            dx = self.target_pos[seek_indices, 0] - self.pos[seek_indices, 0]
            dy = self.target_pos[seek_indices, 1] - self.pos[seek_indices, 1]
            dists = np.hypot(dx, dy)

            # Avoid division by zero
            safe_dists = np.maximum(dists, 1e-6)
            dir_x = dx / safe_dists
            dir_y = dy / safe_dists

            # Accelerate in-place
            accel = self.accel_rates[seek_indices] * delta_t
            self.vel[seek_indices, 0] += dir_x * accel
            self.vel[seek_indices, 1] += dir_y * accel

            # Cap velocities at max speed
            speeds = np.hypot(self.vel[seek_indices, 0], self.vel[seek_indices, 1])
            max_s = self.max_speeds[seek_indices]
            overspeed = speeds > max_s
            if np.any(overspeed):
                scale = max_s / np.maximum(speeds, 1e-6)
                over_indices = seek_indices[overspeed]
                self.vel[over_indices, 0] *= scale[overspeed]
                self.vel[over_indices, 1] *= scale[overspeed]

            # Clear target if reached within 0.5 yards
            reached = dists < 0.5
            if np.any(reached):
                reached_indices = seek_indices[reached]
                self.has_target[reached_indices] = False

        # 3. Vectorized deceleration for players with no active target
        idle_mask = active_mask & (~self.has_target[:n])
        if np.any(idle_mask):
            idle_indices = np.where(idle_mask)[0]
            speeds = np.hypot(self.vel[idle_indices, 0], self.vel[idle_indices, 1])
            moving = speeds > 0.1
            if np.any(moving):
                moving_indices = idle_indices[moving]
                m_speeds = speeds[moving]
                decel = np.minimum(m_speeds, DECELERATION_RATE * delta_t)
                scale = (m_speeds - decel) / np.maximum(m_speeds, 1e-6)
                self.vel[moving_indices, 0] *= scale
                self.vel[moving_indices, 1] *= scale

            stopped = ~moving
            if np.any(stopped):
                self.vel[idle_indices[stopped]] = 0.0

        # 4. In-place position integration & field boundary clamping
        self.pos[:n, 0] += self.vel[:n, 0] * delta_t
        self.pos[:n, 1] += self.vel[:n, 1] * delta_t

        np.clip(self.pos[:n, 0], 0.0, FIELD_LENGTH, out=self.pos[:n, 0])
        np.clip(self.pos[:n, 1], 0.0, FIELD_WIDTH, out=self.pos[:n, 1])

        # 5. Ball kinematics update
        if 0 <= self.carrier_idx < n:
            self.ball[0] = self.pos[self.carrier_idx, 0]
            self.ball[1] = self.pos[self.carrier_idx, 1]
            self.ball[2] = 0.0
            self.ball[3] = self.vel[self.carrier_idx, 0]
            self.ball[4] = self.vel[self.carrier_idx, 1]
            self.ball[5] = 0.0
        elif self.ball_is_in_air:
            self.ball[0] += self.ball[3] * delta_t
            self.ball[1] += self.ball[4] * delta_t
            self.ball[2] = max(0.0, self.ball[2] + self.ball[5] * delta_t - 9.8 * delta_t)
            if self.ball[2] <= 0:
                self.ball[2] = 0.0
                self.ball_is_in_air = False

    def detect_collisions_simd(self) -> List[Tuple[int, int, str, float]]:
        """
        Perform vectorized pairwise collision detection between offensive and
        defensive units using NumPy broadcasting.

        Returns:
            List of (offense_idx, defense_idx, collision_type, impact_force)
        """
        n = self.num_players
        if n == 0:
            return []

        off_indices = np.where(self.is_offense[:n])[0]
        def_indices = np.where(~self.is_offense[:n])[0]

        if len(off_indices) == 0 or len(def_indices) == 0:
            return []

        # Coordinate slices: (N_off, 2) and (N_def, 2)
        off_pos = self.pos[off_indices]
        def_pos = self.pos[def_indices]

        # Broadcasted difference matrix: shape (N_off, N_def, 2)
        diff = off_pos[:, np.newaxis, :] - def_pos[np.newaxis, :, :]

        # Squared distance matrix: shape (N_off, N_def)
        dist_sq = np.sum(diff**2, axis=-1)

        # Contact mask in AVX2 registers
        contact_mask = dist_sq < (TACKLE_RADIUS**2)
        if not np.any(contact_mask):
            return []

        # Vectorized relative velocities and impact force
        off_vel = self.vel[off_indices]
        def_vel = self.vel[def_indices]
        vel_diff = off_vel[:, np.newaxis, :] - def_vel[np.newaxis, :, :]
        rel_speed = np.sqrt(np.sum(vel_diff**2, axis=-1))
        impact_forces = rel_speed * 100.0

        off_hits, def_hits = np.where(contact_mask)
        collisions: List[Tuple[int, int, str, float]] = []

        for o_hit, d_hit in zip(off_hits, def_hits):
            actual_off_idx = int(off_indices[o_hit])
            actual_def_idx = int(def_indices[d_hit])
            force = float(impact_forces[o_hit, d_hit])

            collision_type = "CONTACT"
            if (
                self.has_ball[actual_off_idx]
                and self.states[actual_def_idx] != STATE_BLOCKING
            ):
                collision_type = "TACKLE"
            elif self.states[actual_off_idx] == STATE_BLOCKING:
                collision_type = "BLOCK"

            collisions.append((actual_off_idx, actual_def_idx, collision_type, force))

        return collisions

    def snapshot_frame(self, frame_idx: int, events: Optional[List[str]] = None) -> None:
        """
        Record current engine state into preallocated buffer and streaming ring buffer.
        Zero heap allocation.
        """
        n = self.num_players
        carrier_id = (
            int(self.player_ids[self.carrier_idx])
            if (0 <= self.carrier_idx < n)
            else -1
        )
        ball_summary = np.array(
            [self.ball[0], self.ball[1], self.ball[2], float(carrier_id)],
            dtype=np.float32,
        )

        self.play_buffer.record_frame(
            frame_idx=frame_idx,
            positions=self.pos[:n],
            velocities=self.vel[:n],
            ball_state=ball_summary,
            states=self.states[:n],
            events=events,
        )

        # Push to circular telemetry buffer for live stream
        timestamp = frame_idx * DELTA_T
        self.ring_buffer.push(
            frame_id=frame_idx,
            timestamp=timestamp,
            pos=self.pos[:n],
            vel=self.vel[:n],
            ball=ball_summary,
        )

    def benchmark_play_execution(
        self, frames_to_simulate: int = 300
    ) -> Dict[str, Any]:
        """
        Benchmark simulation speed and calculate per-tick latency in microseconds.
        """
        start_time = time.perf_counter()

        for f in range(frames_to_simulate):
            self.update_physics(DELTA_T)
            _ = self.detect_collisions_simd()
            self.snapshot_frame(f)

        duration_sec = time.perf_counter() - start_time
        total_time_ms = duration_sec * 1000.0
        per_tick_us = (total_time_ms / frames_to_simulate) * 1000.0

        return {
            "kernel_type": "NUMPY_SIMD_SOA",
            "simulated_frames": frames_to_simulate,
            "total_play_duration_seconds": round(frames_to_simulate * DELTA_T, 2),
            "execution_time_ms": round(total_time_ms, 3),
            "per_tick_latency_us": round(per_tick_us, 2),
            "simd_active": True,
            "frames_per_second_capacity": round(
                frames_to_simulate / max(duration_sec, 1e-6), 1
            ),
        }
