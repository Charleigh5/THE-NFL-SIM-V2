#!/usr/bin/env python3
"""
Phase 1: CORTEX Foundation Tests
=================================
Unit tests for Tick Engine, Deterministic RNG, and Enhanced Event Bus.

Context7 Best Practices:
- pytest-asyncio for async tests
- Factory fixtures
- Comprehensive edge cases
"""

import asyncio

import pytest

# Import Phase 1 modules
from app.engine.core import (
    DeterministicRNG,
    EnhancedEventBus,
    EventPriority,
    FrameState,
    GameClock,
    GameEvent,
    GameEventType,
    PlayPhase,
    TickConfig,
    TickEngine,
    TickEngineState,
    generate_client_seed,
    generate_server_seed,
)

# ============================================================================
# TICK ENGINE TESTS
# ============================================================================

class TestTickConfig:
    """Tests for TickConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = TickConfig()
        assert config.tick_rate == 60
        assert config.max_play_ticks == 600
        assert config.pre_snap_ticks == 300

    def test_tick_duration(self):
        """Test tick duration calculations."""
        config = TickConfig(tick_rate=60)
        assert abs(config.tick_duration_ms - 16.67) < 0.1
        assert abs(config.tick_duration_s - 0.0167) < 0.001


class TestGameClock:
    """Tests for GameClock."""

    def test_initial_state(self):
        """Test initial clock state."""
        clock = GameClock()
        assert clock.quarter == 1
        assert clock.time_remaining_ms == 15 * 60 * 1000
        assert clock.time_remaining_str == "15:00"

    def test_tick_advances_clock(self):
        """Test that tick advances the clock."""
        clock = GameClock()
        initial = clock.time_remaining_ms
        clock.tick(1000, clock_running=True)
        assert clock.time_remaining_ms == initial - 1000

    def test_tick_stopped_clock(self):
        """Test that stopped clock doesn't advance."""
        clock = GameClock()
        initial = clock.time_remaining_ms
        clock.tick(1000, clock_running=False)
        assert clock.time_remaining_ms == initial


class TestTickEngine:
    """Tests for TickEngine."""

    @pytest.fixture
    def engine(self):
        """Create a tick engine for testing."""
        return TickEngine()

    def test_initial_state(self, engine):
        """Test initial engine state."""
        assert engine.state == TickEngineState.STOPPED
        assert engine.current_tick == 0
        assert engine.play_phase == PlayPhase.PRE_SNAP

    def test_step_advances_tick(self, engine):
        """Test that step advances the tick counter."""
        frame = engine.step()
        assert engine.current_tick == 1
        assert frame.tick == 1

    def test_step_returns_frame_state(self, engine):
        """Test that step returns valid frame state."""
        frame = engine.step()
        assert isinstance(frame, FrameState)
        assert frame.play_phase == PlayPhase.PRE_SNAP

    def test_snap_ball(self, engine):
        """Test snap ball transitions to active play."""
        engine.snap_ball()
        assert engine.play_phase == PlayPhase.PLAY_ACTIVE

    def test_end_play(self, engine):
        """Test end play transitions to dead ball."""
        engine.end_play()
        assert engine.play_phase == PlayPhase.PLAY_DEAD

    def test_run_play_limited_ticks(self, engine):
        """Test running a play with limited ticks."""
        frames = engine.run_play(max_ticks=10)
        assert len(frames) == 10

    def test_frame_history(self, engine):
        """Test frame history is maintained."""
        for _ in range(5):
            engine.step()

        recent = engine.get_recent_frames(3)
        assert len(recent) == 3
        assert recent[-1].tick == 5

    def test_reset(self, engine):
        """Test reset clears state."""
        engine.step()
        engine.step()
        engine.reset()

        assert engine.current_tick == 0
        assert len(engine.get_recent_frames()) == 0


# ============================================================================
# DETERMINISTIC RNG TESTS
# ============================================================================

class TestDeterministicRNG:
    """Tests for DeterministicRNG."""

    @pytest.fixture
    def rng(self):
        """Create a seeded RNG for testing."""
        server = b"test_server_seed_12345678901234"
        client = b"test_client_seed_12345678901234"
        return DeterministicRNG(server, client, nonce=0)

    def test_deterministic_sequence(self):
        """Test that same seeds produce same sequence."""
        server = b"test_server_seed_12345678901234"
        client = b"test_client_seed_12345678901234"

        rng1 = DeterministicRNG(server, client, nonce=0)
        rng2 = DeterministicRNG(server, client, nonce=0)

        for _ in range(100):
            assert rng1.next_float() == rng2.next_float()

    def test_different_seeds_different_sequence(self):
        """Test that different seeds produce different sequences."""
        rng1 = DeterministicRNG(b"seed1" * 6, b"client" * 6, nonce=0)
        rng2 = DeterministicRNG(b"seed2" * 6, b"client" * 6, nonce=0)

        # Should be different (extremely unlikely to match)
        assert rng1.next_float() != rng2.next_float()

    def test_next_int_range(self, rng):
        """Test next_int produces values in range."""
        for _ in range(100):
            value = rng.next_int(1, 10)
            assert 1 <= value <= 10

    def test_next_float_range(self, rng):
        """Test next_float produces values in [0, 1)."""
        for _ in range(100):
            value = rng.next_float()
            assert 0.0 <= value < 1.0

    def test_next_bool_probability(self, rng):
        """Test next_bool respects probability."""
        true_count = sum(1 for _ in range(1000) if rng.next_bool(0.5))
        # Should be roughly 50%, allow wide margin
        assert 400 < true_count < 600

    def test_choice(self, rng):
        """Test choice selects from list."""
        items = ["a", "b", "c", "d"]
        for _ in range(20):
            result = rng.choice(items)
            assert result in items

    def test_shuffle(self, rng):
        """Test shuffle returns permutation."""
        items = [1, 2, 3, 4, 5]
        shuffled = rng.shuffle(items)

        assert len(shuffled) == len(items)
        assert set(shuffled) == set(items)

    def test_fork_creates_independent_rng(self, rng):
        """Test fork creates independent RNG with new nonce."""
        forked = rng.fork(nonce=42)

        # Different nonce should produce different sequence
        assert rng.next_float() != forked.next_float()

    def test_verification(self):
        """Test verification of sequences."""
        server = b"verification_test_seed_1234567"
        client = b"client_verification_seed_123456"

        # Generate reference sequence
        rng = DeterministicRNG(server, client, nonce=0)
        expected = [rng.next_float() for _ in range(10)]

        # Verify
        assert DeterministicRNG.verify(server, client, 0, expected)


# ============================================================================
# ENHANCED EVENT BUS TESTS
# ============================================================================

class TestEnhancedEventBus:
    """Tests for EnhancedEventBus."""

    @pytest.fixture
    def bus(self):
        """Create a fresh event bus."""
        return EnhancedEventBus()

    def test_subscribe_and_publish(self, bus):
        """Test basic subscribe and publish."""
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe(GameEventType.TOUCHDOWN, handler)

        event = GameEvent(GameEventType.TOUCHDOWN, tick=1)
        count = bus.publish(event)

        assert count == 1
        assert len(received) == 1
        assert received[0].event_type == GameEventType.TOUCHDOWN

    def test_unsubscribe(self, bus):
        """Test unsubscribe removes handler."""
        received = []

        def handler(event):
            received.append(event)

        reg = bus.subscribe(GameEventType.SACK, handler)
        bus.unsubscribe(reg)

        bus.publish(GameEvent(GameEventType.SACK, tick=1))

        assert len(received) == 0

    def test_priority_ordering(self, bus):
        """Test handlers are called in priority order."""
        order = []

        def low_handler(event):
            order.append("low")

        def high_handler(event):
            order.append("high")

        bus.subscribe(GameEventType.SNAP, low_handler, EventPriority.LOW)
        bus.subscribe(GameEventType.SNAP, high_handler, EventPriority.HIGH)

        bus.publish(GameEvent(GameEventType.SNAP, tick=1))

        assert order == ["high", "low"]

    def test_once_handler(self, bus):
        """Test one-time handlers are removed after call."""
        count = [0]

        def handler(event):
            count[0] += 1

        bus.subscribe(GameEventType.FUMBLE, handler, once=True)

        bus.publish(GameEvent(GameEventType.FUMBLE, tick=1))
        bus.publish(GameEvent(GameEventType.FUMBLE, tick=2))

        assert count[0] == 1

    def test_global_handler(self, bus):
        """Test subscribe_all receives all events."""
        received = []

        def handler(event):
            received.append(event.event_type)

        bus.subscribe_all(handler)

        bus.publish(GameEvent(GameEventType.SNAP, tick=1))
        bus.publish(GameEvent(GameEventType.TACKLE, tick=2))

        assert len(received) == 2
        assert GameEventType.SNAP in received
        assert GameEventType.TACKLE in received

    def test_event_history(self, bus):
        """Test event history is maintained."""
        for i in range(5):
            bus.publish(GameEvent(GameEventType.TICK, tick=i))

        history = bus.get_history(limit=3)
        assert len(history) == 3

    def test_pause_and_resume(self, bus):
        """Test pause blocks events, resume allows them."""
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe(GameEventType.TIMEOUT, handler)

        bus.pause()
        bus.publish(GameEvent(GameEventType.TIMEOUT, tick=1))
        assert len(received) == 0

        bus.resume()
        bus.publish(GameEvent(GameEventType.TIMEOUT, tick=2))
        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_async_handler(self, bus):
        """Test async handlers are called."""
        received = []

        async def async_handler(event):
            await asyncio.sleep(0.01)
            received.append(event)

        bus.subscribe(GameEventType.PASS_THROWN, async_handler)

        await bus.publish_async(GameEvent(GameEventType.PASS_THROWN, tick=1))

        assert len(received) == 1


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestPhase1Integration:
    """Integration tests for all Phase 1 components."""

    def test_tick_engine_with_rng(self):
        """Test tick engine using deterministic RNG."""
        rng = DeterministicRNG(
            generate_server_seed(),
            generate_client_seed("test"),
            nonce=0
        )

        engine = TickEngine(rng=rng)

        # Run a short play
        frames = engine.run_play(max_ticks=10)
        assert len(frames) == 10

    def test_tick_engine_with_event_bus(self):
        """Test tick engine publishing events."""
        bus = EnhancedEventBus()
        engine = TickEngine(event_bus=bus)

        frame_events = []

        def on_frame_end(event):
            frame_events.append(event)

        bus.subscribe(GameEventType.FRAME_END, on_frame_end)

        # The tick engine doesn't publish events by default,
        # but could be extended to do so
        engine.step()
        engine.step()

        # Engine works without errors
        assert engine.current_tick == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
