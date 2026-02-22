#!/usr/bin/env python3
"""
60Hz Tick Engine - CORTEX Foundation
=====================================
Core tick-based simulation engine for deterministic NFL gameplay.

Features:
- 60 ticks per second (16.67ms per tick)
- Deterministic frame snapshots
- ECS-compatible architecture
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

# ============================================================================
# INTERFACES (Protocols)
# ============================================================================


class TickListener(Protocol):
    """Protocol for objects that receive tick updates."""

    def on_tick(self, tick: int, delta_time: float) -> None:
        """Called each simulation tick."""
        ...


# ============================================================================
# ENUMS
# ============================================================================


class TickEngineState(str, Enum):
    """State of the tick engine."""

    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"


class PlayPhase(str, Enum):
    """Current phase within a play."""

    PRE_SNAP = "PRE_SNAP"
    SNAP = "SNAP"
    PLAY_ACTIVE = "PLAY_ACTIVE"
    TACKLE = "TACKLE"
    PLAY_DEAD = "PLAY_DEAD"


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class TickConfig:
    """Configuration for the tick engine."""

    tick_rate: int = 60  # Ticks per second
    max_play_ticks: int = 600  # 10 seconds max play duration
    pre_snap_ticks: int = 300  # 5 seconds pre-snap

    @property
    def tick_duration_ms(self) -> float:
        """Duration of one tick in milliseconds."""
        return 1000.0 / self.tick_rate

    @property
    def tick_duration_s(self) -> float:
        """Duration of one tick in seconds."""
        return 1.0 / self.tick_rate


@dataclass
class GameClock:
    """Tracks game time within simulation."""

    quarter: int = 1
    time_remaining_ms: int = 15 * 60 * 1000  # 15 minutes in ms
    play_clock_ms: int = 40 * 1000  # 40 seconds

    def tick(self, delta_ms: float, clock_running: bool = True) -> None:
        """Advance game clock by delta milliseconds."""
        if clock_running and self.time_remaining_ms > 0:
            self.time_remaining_ms = max(0, self.time_remaining_ms - int(delta_ms))

    @property
    def time_remaining_str(self) -> str:
        """Format time remaining as MM:SS."""
        total_seconds = self.time_remaining_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"


@dataclass
class FrameState:
    """Complete state of a single simulation frame."""

    tick: int
    timestamp: float
    play_phase: PlayPhase
    game_clock: GameClock
    entities: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "tick": self.tick,
            "timestamp": self.timestamp,
            "play_phase": self.play_phase.value,
            "game_clock": {
                "quarter": self.game_clock.quarter,
                "time_remaining_ms": self.game_clock.time_remaining_ms,
                "play_clock_ms": self.game_clock.play_clock_ms,
            },
            "entities": self.entities,
            "events": self.events,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FrameState":
        """Deserialize from dictionary."""
        return cls(
            tick=data["tick"],
            timestamp=data["timestamp"],
            play_phase=PlayPhase(data["play_phase"]),
            game_clock=GameClock(
                quarter=data["game_clock"]["quarter"],
                time_remaining_ms=data["game_clock"]["time_remaining_ms"],
                play_clock_ms=data["game_clock"]["play_clock_ms"],
            ),
            entities=data.get("entities", {}),
            events=data.get("events", []),
        )


# ============================================================================
# TICK ENGINE
# ============================================================================


class TickEngine:
    """
    Core 60Hz tick engine for NFL simulation.

    Executes game logic at a fixed time step, enabling:
    - Deterministic simulation
    - Frame-by-frame replay
    - Physics-based gameplay
    """

    def __init__(
        self,
        config: TickConfig | None = None,
        rng: Any | None = None,
        event_bus: Any | None = None,
    ):
        self.config = config or TickConfig()
        self.rng = rng
        self.event_bus = event_bus

        self.state = TickEngineState.STOPPED
        self.current_tick = 0
        self.game_clock = GameClock()
        self.play_phase = PlayPhase.PRE_SNAP

        self._listeners: list[TickListener] = []
        self._frame_history: list[FrameState] = []
        self._max_history = 600  # Store last 10 seconds

    def register_listener(self, listener: TickListener) -> None:
        """Register a tick listener."""
        self._listeners.append(listener)

    def unregister_listener(self, listener: TickListener) -> None:
        """Unregister a tick listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def step(self) -> FrameState:
        """Execute one simulation tick."""
        self.current_tick += 1
        delta_time = self.config.tick_duration_s

        # Update game clock
        clock_running = self.play_phase == PlayPhase.PLAY_ACTIVE
        self.game_clock.tick(self.config.tick_duration_ms, clock_running)

        # Notify listeners
        for listener in self._listeners:
            listener.on_tick(self.current_tick, delta_time)

        # Capture frame state
        frame = FrameState(
            tick=self.current_tick,
            timestamp=time.time(),
            play_phase=self.play_phase,
            game_clock=GameClock(
                quarter=self.game_clock.quarter,
                time_remaining_ms=self.game_clock.time_remaining_ms,
                play_clock_ms=self.game_clock.play_clock_ms,
            ),
        )

        # Store in history (circular buffer)
        self._frame_history.append(frame)
        if len(self._frame_history) > self._max_history:
            self._frame_history.pop(0)

        return frame

    def run_play(self, max_ticks: int | None = None) -> list[FrameState]:
        """Run a complete play simulation."""
        max_ticks = max_ticks or self.config.max_play_ticks
        self.state = TickEngineState.RUNNING
        self.play_phase = PlayPhase.PRE_SNAP

        play_frames: list[FrameState] = []

        for _ in range(max_ticks):
            if self.state != TickEngineState.RUNNING:
                break

            if self.play_phase == PlayPhase.PLAY_DEAD:
                break

            frame = self.step()
            play_frames.append(frame)

        self.state = TickEngineState.STOPPED
        return play_frames

    def snap_ball(self) -> None:
        """Transition from pre-snap to active play."""
        if self.play_phase == PlayPhase.PRE_SNAP:
            self.play_phase = PlayPhase.SNAP
            self.play_phase = PlayPhase.PLAY_ACTIVE

    def end_play(self) -> None:
        """End the current play."""
        self.play_phase = PlayPhase.PLAY_DEAD

    def get_frame(self, tick: int) -> FrameState | None:
        """Get a specific frame from history."""
        for frame in self._frame_history:
            if frame.tick == tick:
                return frame
        return None

    def get_recent_frames(self, count: int = 60) -> list[FrameState]:
        """Get the most recent N frames."""
        return self._frame_history[-count:]

    def reset(self) -> None:
        """Reset engine state for a new play."""
        self.current_tick = 0
        self.play_phase = PlayPhase.PRE_SNAP
        self._frame_history.clear()
