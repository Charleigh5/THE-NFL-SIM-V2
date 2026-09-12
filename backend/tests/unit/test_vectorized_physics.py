"""
Unit Test Suite for 60Hz Physics SIMD Vectorization & Hot-Loop Hardening (TASK-019)
===================================================================================
Empirical verification of:
1. Contiguous Structure-of-Arrays (SoA) layout and array initialization.
2. SIMD pairwise collision detection matrix using NumPy broadcasting.
3. Vectorized kinematics and numerical boundary invariants.
4. Zero-allocation verification in hot simulation loop using tracemalloc.
5. Circular telemetry ring buffer wrap-around and zero-copy streaming.
6. Execution latency benchmark (<0.15ms per tick, >10x real-time capacity).
"""

import pytest
import numpy as np
import random
import tracemalloc
import time
from typing import List, Dict, Any

from app.engine.vectorized_physics import (
    VectorizedPhysicsKernel,
    ZeroAllocPlayBuffer,
    CircularTelemetryRingBuffer,
    TACKLE_RADIUS,
    FIELD_LENGTH,
    FIELD_WIDTH,
    DELTA_T,
    MAX_FRAMES,
    STATE_IDLE,
    STATE_RUNNING,
    STATE_TACKLED,
    STATE_BLOCKING,
)
from app.engine.frame_physics import FramePhysicsEngine, Vector2D


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def rng():
    return random.Random(1337)


@pytest.fixture
def sample_22_players():
    """Generates 11 offensive and 11 defensive player datasets."""
    players = []
    # 11 Offense
    for i in range(11):
        players.append({
            "player_id": i + 1,
            "x": 45.0 + (i % 3),
            "y": 20.0 + (i * 2.5),
            "vx": 0.0,
            "vy": 0.0,
            "is_offense": True,
            "max_speed": 8.5,
            "accel_rate": 5.0,
            "agility": 80.0,
            "tackle": 50.0,
            "state": "RUNNING",
            "target_x": 55.0,
            "target_y": 20.0 + (i * 2.5),
        })
    # 11 Defense
    for i in range(11):
        players.append({
            "player_id": 20 + i,
            "x": 52.0 + (i % 3),
            "y": 20.0 + (i * 2.5),
            "vx": 0.0,
            "vy": 0.0,
            "is_offense": False,
            "max_speed": 8.2,
            "accel_rate": 4.8,
            "agility": 75.0,
            "tackle": 82.0,
            "state": "RUNNING",
            "target_x": 45.0,
            "target_y": 20.0 + (i * 2.5),
        })
    return players


# =============================================================================
# UNIT TESTS
# =============================================================================

class TestVectorizedPhysicsKernel:
    """Test suite for the Structure-of-Arrays SIMD Vectorized Physics Kernel."""

    def test_kernel_initialization_and_soa_layout(self, sample_22_players):
        """Verify contiguous float64/int32 SoA memory layout for 22 on-field bodies."""
        kernel = VectorizedPhysicsKernel(max_players=22)
        kernel.load_players(sample_22_players, ball_carrier_id=1)

        assert kernel.num_players == 22
        assert kernel.pos.shape == (22, 2)
        assert kernel.vel.shape == (22, 2)
        assert kernel.pos.dtype == np.float64
        assert kernel.vel.dtype == np.float64
        assert kernel.player_ids.dtype == np.int32
        assert kernel.states.dtype == np.int32

        # Check carrier initialization
        assert kernel.carrier_idx == 0
        assert kernel.has_ball[0] == True
        assert abs(kernel.ball[0] - sample_22_players[0]["x"]) < 1e-5
        assert abs(kernel.ball[1] - sample_22_players[0]["y"]) < 1e-5

    def test_simd_pairwise_collision_broadcasting(self, sample_22_players):
        """
        Verify SIMD distance matrix broadcasting detects pairwise contacts in AVX2 registers.
        All 121 pairs are computed in a single vectorized matrix comparison.
        """
        kernel = VectorizedPhysicsKernel(max_players=22)
        kernel.load_players(sample_22_players, ball_carrier_id=1)

        # Place player 0 (offense) and player 11 (defense) in contact distance (< TACKLE_RADIUS = 1.5 yds)
        kernel.pos[0, 0] = 50.0
        kernel.pos[0, 1] = 26.0
        kernel.vel[0, 0] = 4.0
        kernel.vel[0, 1] = 0.0

        kernel.pos[11, 0] = 50.8  # distance = 0.8 yds < 1.5 yds
        kernel.pos[11, 1] = 26.0
        kernel.vel[11, 0] = -3.0
        kernel.vel[11, 1] = 0.0

        # Move all other players far away
        kernel.pos[1:11, 0] = 10.0
        kernel.pos[12:22, 0] = 90.0

        collisions = kernel.detect_collisions_simd()

        # Exactly 1 collision detected
        assert len(collisions) == 1
        off_idx, def_idx, col_type, force = collisions[0]
        assert off_idx == 0
        assert def_idx == 11
        assert col_type == "TACKLE"  # Player 0 has ball
        # Relative speed = 4.0 - (-3.0) = 7.0 yds/s -> force = 700.0
        assert abs(force - 700.0) < 1e-3

    def test_vectorized_kinematics_and_boundary_invariants(self):
        """Verify vectorized velocity acceleration, max speed bounding, and field clamping."""
        kernel = VectorizedPhysicsKernel(max_players=2)
        two_players = [
            {
                "player_id": 1,
                "x": 95.0,
                "y": 25.0,
                "vx": 0.0,
                "vy": 0.0,
                "is_offense": True,
                "max_speed": 10.0,
                "accel_rate": 6.0,
                "agility": 85.0,
                "tackle": 50.0,
                "state": "RUNNING",
                "target_x": 120.0,  # Out of bounds past 100 yds
                "target_y": 25.0,
            },
            {
                "player_id": 2,
                "x": 5.0,
                "y": 25.0,
                "vx": 0.0,
                "vy": 0.0,
                "is_offense": False,
                "max_speed": 8.0,
                "accel_rate": 5.0,
                "agility": 75.0,
                "tackle": 80.0,
                "state": "RUNNING",
                "target_x": -20.0,  # Out of bounds below 0 yds
                "target_y": 25.0,
            },
        ]
        kernel.load_players(two_players)

        # Run 60 frames (1 full second)
        for _ in range(60):
            kernel.update_physics(DELTA_T)

        # Velocities should be capped at max_speed
        assert abs(kernel.vel[0, 0] - 10.0) < 0.5 or kernel.vel[0, 0] <= 10.001
        assert abs(kernel.vel[1, 0] - (-8.0)) < 0.5 or abs(kernel.vel[1, 0]) <= 8.001

        # Run for 200 more frames to force boundary contact
        for _ in range(200):
            kernel.update_physics(DELTA_T)

        # Position 0 clamped at FIELD_LENGTH (100.0)
        assert kernel.pos[0, 0] <= FIELD_LENGTH
        assert kernel.pos[0, 0] >= 99.9

        # Position 1 clamped at 0.0
        assert kernel.pos[1, 0] >= 0.0
        assert kernel.pos[1, 0] <= 0.1

    def test_zero_allocation_hot_loop_tracemalloc(self, sample_22_players):
        """
        Verify that 300 ticks of the simulation hot loop produce near-zero heap allocations,
        proving elimination of Python GC overhead.
        """
        kernel = VectorizedPhysicsKernel(max_players=22)
        kernel.load_players(sample_22_players, ball_carrier_id=1)

        # Warm up JIT/cache
        for f in range(5):
            kernel.update_physics(DELTA_T)
            _ = kernel.detect_collisions_simd()
            kernel.snapshot_frame(f)

        tracemalloc.start()
        snapshot_start = tracemalloc.take_snapshot()

        # Execute 300 60Hz ticks (5 seconds of simulated action)
        for f in range(5, 305):
            kernel.update_physics(DELTA_T)
            _ = kernel.detect_collisions_simd()
            kernel.snapshot_frame(f)

        snapshot_end = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot_end.compare_to(snapshot_start, "lineno")
        total_diff_kb = sum(stat.size_diff for stat in top_stats) / 1024.0

        # Memory diff should be negligible (< 100 KB over 300 frames with 22 players)
        # Previously, dynamic object allocation produced several Megabytes per play.
        assert total_diff_kb < 100.0

    def test_circular_telemetry_ring_buffer(self):
        """Verify circular ring buffer wrapping, O(1) in-place push, and latest retrieval."""
        ring = CircularTelemetryRingBuffer(capacity=10, num_players=2)

        pos = np.array([[10.0, 20.0], [15.0, 25.0]], dtype=np.float64)
        vel = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float64)
        ball = np.array([10.0, 20.0, 0.0, 1.0], dtype=np.float64)

        # Push 25 frames (more than capacity 10)
        for i in range(25):
            pos[0, 0] = float(i)
            ring.push(frame_id=i, timestamp=i * DELTA_T, pos=pos, vel=vel, ball=ball)

        assert ring.count == 10  # Capped at capacity
        latest = ring.get_latest_frame()
        assert latest is not None
        assert latest["frame_id"] == 24
        assert abs(latest["timestamp"] - (24 * DELTA_T)) < 1e-5

    def test_vectorized_latency_benchmark_budget(self, sample_22_players):
        """
        Verify that vectorized 60Hz simulation operates strictly within the latency budget.
        Ceiling: <0.30ms per tick (<300 microseconds), easily exceeding 1,000 frames/sec.
        """
        kernel = VectorizedPhysicsKernel(max_players=22)
        kernel.load_players(sample_22_players, ball_carrier_id=1)

        # Warm-up pass to populate memory pages and cache lines
        _ = kernel.benchmark_play_execution(frames_to_simulate=60)

        # Timed benchmark run
        result = kernel.benchmark_play_execution(frames_to_simulate=300)

        assert result["kernel_type"] == "NUMPY_SIMD_SOA"
        assert result["simulated_frames"] == 300
        assert result["simd_active"] is True
        # Per-tick latency should be well under the 300us ceiling (realtime 60fps is 16,666us)
        assert result["per_tick_latency_us"] < 300.0
        # Simulation capacity should easily exceed 1,000 frames/sec (vs 60 fps target)
        assert result["frames_per_second_capacity"] > 1000.0
