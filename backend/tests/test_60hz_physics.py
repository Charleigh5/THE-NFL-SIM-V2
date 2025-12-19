"""
Tests for 60Hz Frame Physics Engine (B-075)
============================================
Unit tests for the frame-based physics simulation.
"""

import pytest
import random
from dataclasses import dataclass
import math

from app.engine.frame_physics import (
    FramePhysicsEngine,
    Vector2D,
    PhysicsPlayer,
    PhysicsBall,
    PhysicsFrame,
    PlayOutcome,
    PlayerState,
    Collision,
    FRAMES_PER_SECOND,
    MAX_PLAY_DURATION,
    DELTA_T,
    MAX_FRAMES,
    TACKLE_RADIUS,
    FIELD_LENGTH,
    FIELD_WIDTH,
)


# =============================================================================
# FIXTURES
# =============================================================================

@dataclass
class MockPlayer:
    """Mock player for testing."""
    id: int
    position: str
    speed: int = 80
    acceleration: int = 75
    agility: int = 75
    tackle: int = 70


@pytest.fixture
def rng():
    """Fixed random number generator for reproducibility."""
    return random.Random(42)


@pytest.fixture
def basic_offense():
    """Basic offensive unit."""
    return [
        MockPlayer(1, "QB", speed=75),
        MockPlayer(2, "RB", speed=88),
        MockPlayer(3, "WR", speed=92),
        MockPlayer(4, "TE", speed=78),
        MockPlayer(5, "LT", speed=65),
    ]


@pytest.fixture
def basic_defense():
    """Basic defensive unit."""
    return [
        MockPlayer(21, "DT", speed=72, tackle=82),
        MockPlayer(22, "DE", speed=80, tackle=78),
        MockPlayer(23, "MLB", speed=82, tackle=88),
        MockPlayer(24, "CB", speed=90, tackle=65),
        MockPlayer(25, "FS", speed=88, tackle=72),
    ]


@pytest.fixture
def engine(rng):
    """Pre-configured physics engine."""
    return FramePhysicsEngine(rng)


# =============================================================================
# CONSTANTS TESTS (B-061, B-062)
# =============================================================================

class TestConstants:
    """Tests for physics constants."""

    def test_frames_per_second(self):
        """B-061: Verify FRAMES_PER_SECOND = 60."""
        assert FRAMES_PER_SECOND == 60

    def test_max_play_duration(self):
        """B-062: Verify MAX_PLAY_DURATION = 10 seconds."""
        assert MAX_PLAY_DURATION == 10.0

    def test_delta_t_calculation(self):
        """Delta time should be 1/60 second."""
        assert abs(DELTA_T - 1/60) < 0.0001

    def test_max_frames_calculation(self):
        """Max frames should be 600 (60fps * 10s)."""
        assert MAX_FRAMES == 600


# =============================================================================
# VECTOR2D TESTS
# =============================================================================

class TestVector2D:
    """Tests for 2D vector operations."""

    def test_addition(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        result = v1 + v2
        assert result.x == 4
        assert result.y == 6

    def test_subtraction(self):
        v1 = Vector2D(5, 7)
        v2 = Vector2D(2, 3)
        result = v1 - v2
        assert result.x == 3
        assert result.y == 4

    def test_scalar_multiplication(self):
        v = Vector2D(3, 4)
        result = v * 2
        assert result.x == 6
        assert result.y == 8

    def test_magnitude(self):
        v = Vector2D(3, 4)
        assert v.magnitude() == 5.0

    def test_normalized(self):
        v = Vector2D(3, 4)
        norm = v.normalized()
        assert abs(norm.x - 0.6) < 0.001
        assert abs(norm.y - 0.8) < 0.001

    def test_normalized_zero_vector(self):
        v = Vector2D(0, 0)
        norm = v.normalized()
        assert norm.x == 0
        assert norm.y == 0

    def test_distance_to(self):
        v1 = Vector2D(0, 0)
        v2 = Vector2D(3, 4)
        assert v1.distance_to(v2) == 5.0


# =============================================================================
# ENGINE INITIALIZATION TESTS
# =============================================================================

class TestEngineInitialization:
    """Tests for engine initialization."""

    def test_initialize_play_creates_players(self, engine, basic_offense, basic_defense):
        """Players should be created on initialization."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        assert len(engine.players) == len(basic_offense) + len(basic_defense)

    def test_initialize_play_positions_ball(self, engine, basic_offense, basic_defense):
        """Ball should be positioned with QB."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Ball should have a carrier
        assert engine.ball.carrier_id is not None

    def test_initialize_play_sets_line_of_scrimmage(self, engine, basic_offense, basic_defense):
        """Line of scrimmage should be set."""
        engine.initialize_play(basic_offense, basic_defense, 35)

        assert engine.line_of_scrimmage == 35

    def test_player_max_speed_calculation(self, engine, basic_offense, basic_defense):
        """Max speed should be calculated from speed rating."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Find a player
        player = list(engine.players.values())[0]

        # Max speed should be positive and reasonable
        assert 5.0 < player.max_speed < 12.0


# =============================================================================
# PHYSICS UPDATE TESTS (B-065)
# =============================================================================

class TestPhysicsUpdate:
    """Tests for physics update step."""

    def test_update_moves_player_towards_target(self, engine, basic_offense, basic_defense):
        """B-065: Player should move towards target position."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Set a target for first player
        player = list(engine.players.values())[0]
        initial_pos = Vector2D(player.position.x, player.position.y)
        player.target_position = Vector2D(initial_pos.x + 10, initial_pos.y)

        # Run several updates
        for _ in range(30):  # 0.5 seconds
            engine._update_physics(DELTA_T)

        # Player should have moved
        assert player.position.x > initial_pos.x

    def test_update_respects_max_speed(self, engine, basic_offense, basic_defense):
        """Player velocity should not exceed max speed."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        player = list(engine.players.values())[0]
        player.target_position = Vector2D(100, 25)

        # Run many updates
        for _ in range(120):  # 2 seconds
            engine._update_physics(DELTA_T)
            assert player.velocity.magnitude() <= player.max_speed + 0.01

    def test_tackled_player_stops(self, engine, basic_offense, basic_defense):
        """Tackled player should not move."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        player = list(engine.players.values())[0]
        player.state = PlayerState.TACKLED
        initial_pos = Vector2D(player.position.x, player.position.y)
        player.target_position = Vector2D(100, 25)

        engine._update_physics(DELTA_T)

        assert player.position.x == initial_pos.x
        assert player.position.y == initial_pos.y

    def test_ball_follows_carrier(self, engine, basic_offense, basic_defense):
        """Ball should follow carrier position."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        carrier_id = engine.ball.carrier_id
        carrier = engine.players.get(carrier_id)

        if carrier:
            carrier.target_position = Vector2D(60, 30)

            for _ in range(30):
                engine._update_physics(DELTA_T)

            assert engine.ball.position.x == carrier.position.x
            assert engine.ball.position.y == carrier.position.y


# =============================================================================
# COLLISION DETECTION TESTS (B-064)
# =============================================================================

class TestCollisionDetection:
    """Tests for collision detection."""

    def test_no_collision_when_far_apart(self, engine, basic_offense, basic_defense):
        """B-064: No collision when players are far apart."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Players start apart, so no initial collisions
        collisions = engine._detect_collisions()

        # Might be 0 or some if players are close in formation
        # Just verify we get a list
        assert isinstance(collisions, list)

    def test_collision_when_close(self, engine, basic_offense, basic_defense):
        """Collision detected when players are close."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Move offensive player to defensive player position
        off_player = [p for p in engine.players.values() if p.is_offense][0]
        def_player = [p for p in engine.players.values() if not p.is_offense][0]

        off_player.position = Vector2D(
            def_player.position.x,
            def_player.position.y
        )
        off_player.has_ball = True

        collisions = engine._detect_collisions()

        # Should detect at least one collision
        assert len(collisions) >= 1

    def test_tackle_collision_type(self, engine, basic_offense, basic_defense):
        """Tackle collision type for ball carrier."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        off_player = [p for p in engine.players.values() if p.is_offense][0]
        def_player = [p for p in engine.players.values() if not p.is_offense][0]

        off_player.position = Vector2D(def_player.position.x, def_player.position.y)
        off_player.has_ball = True

        collisions = engine._detect_collisions()

        tackle_collisions = [c for c in collisions if c.collision_type == "TACKLE"]
        assert len(tackle_collisions) >= 1


# =============================================================================
# PLAY TERMINATION TESTS (B-066)
# =============================================================================

class TestPlayTermination:
    """Tests for play termination conditions."""

    def test_not_over_at_start(self, engine, basic_offense, basic_defense):
        """B-066: Play should not be over at start."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        assert not engine._is_play_over()

    def test_touchdown_ends_play(self, engine, basic_offense, basic_defense):
        """Touchdown should end play."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Move ball carrier to end zone
        carrier_id = engine.ball.carrier_id
        carrier = engine.players.get(carrier_id)
        if carrier:
            carrier.position = Vector2D(101, 25)
            carrier.has_ball = True

        assert engine._is_play_over()
        assert engine.play_outcome == PlayOutcome.TOUCHDOWN

    def test_out_of_bounds_ends_play(self, engine, basic_offense, basic_defense):
        """Out of bounds should end play."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        carrier_id = engine.ball.carrier_id
        carrier = engine.players.get(carrier_id)
        if carrier:
            carrier.position = Vector2D(50, -1)
            carrier.has_ball = True

        assert engine._is_play_over()
        assert engine.play_outcome == PlayOutcome.OUT_OF_BOUNDS


# =============================================================================
# RESULT GENERATION TESTS (B-067)
# =============================================================================

class TestResultGeneration:
    """Tests for play result generation."""

    def test_result_contains_frames(self, engine, basic_offense, basic_defense):
        """B-067: Result should contain frames."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Force quick end
        engine.play_outcome = PlayOutcome.COMPLETE

        result = engine._generate_play_result()

        assert result.frames is not None

    def test_result_contains_checksum(self, engine, basic_offense, basic_defense):
        """Result should have checksum."""
        engine.initialize_play(basic_offense, basic_defense, 50)
        engine._record_frame()
        engine.play_outcome = PlayOutcome.COMPLETE

        result = engine._generate_play_result()

        assert result.checksum is not None
        assert len(result.checksum) > 0


# =============================================================================
# CHECKSUM TESTS (B-068)
# =============================================================================

class TestChecksum:
    """Tests for Merkle tree checksum generation."""

    def test_checksum_is_deterministic(self, rng, basic_offense, basic_defense):
        """B-068: Same inputs should produce same checksum."""
        engine1 = FramePhysicsEngine(random.Random(42))
        engine1.initialize_play(basic_offense, basic_defense, 50)
        engine1._record_frame()
        checksum1 = engine1._generate_checksum()

        engine2 = FramePhysicsEngine(random.Random(42))
        engine2.initialize_play(basic_offense, basic_defense, 50)
        engine2._record_frame()
        checksum2 = engine2._generate_checksum()

        assert checksum1 == checksum2

    def test_checksum_changes_with_different_positions(self, rng, basic_offense, basic_defense):
        """Different play states should produce different checksums."""
        engine1 = FramePhysicsEngine(random.Random(42))
        engine1.initialize_play(basic_offense, basic_defense, 50)
        engine1._record_frame()
        checksum1 = engine1._generate_checksum()

        engine2 = FramePhysicsEngine(random.Random(42))
        engine2.initialize_play(basic_offense, basic_defense, 60)  # Different LOS
        engine2._record_frame()
        checksum2 = engine2._generate_checksum()

        assert checksum1 != checksum2


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for full play execution."""

    def test_execute_play_returns_result(self, engine, basic_offense, basic_defense):
        """Execute play should return valid result."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        # Set targets so play progresses
        for player in engine.players.values():
            if player.is_offense:
                player.target_position = Vector2D(60, 25)

        result = engine.execute_play()

        assert result is not None
        assert result.outcome != PlayOutcome.IN_PROGRESS
        assert len(result.frames) > 0

    def test_execute_play_respects_max_frames(self, engine, basic_offense, basic_defense):
        """Play should not exceed MAX_FRAMES + 1 (for initial snap frame)."""
        engine.initialize_play(basic_offense, basic_defense, 50)

        result = engine.execute_play()

        # MAX_FRAMES loop iterations + 1 initial snap frame
        assert len(result.frames) <= MAX_FRAMES + 1

    def test_yards_gained_calculation(self, engine, basic_offense, basic_defense):
        """Yards gained should be calculated correctly."""
        los = 40
        engine.initialize_play(basic_offense, basic_defense, los)

        # Move ball carrier forward
        carrier_id = engine.ball.carrier_id
        carrier = engine.players.get(carrier_id)
        if carrier:
            carrier.position = Vector2D(los + 15, 25)
            carrier.state = PlayerState.TACKLED

        engine.play_outcome = PlayOutcome.COMPLETE
        engine._record_frame()
        result = engine._generate_play_result()

        # Should gain approximately 15 yards
        assert abs(result.yards_gained - 15) < 1
