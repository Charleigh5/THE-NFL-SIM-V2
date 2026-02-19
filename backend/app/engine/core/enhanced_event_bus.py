#!/usr/bin/env python3
"""
Enhanced Event Bus - CORTEX Foundation
=======================================
Async-capable, typed event bus for simulation events.

Features:
- Sync and async handler support
- Priority-based dispatch
- Event history for replay
- One-time handlers
"""

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Union

# ============================================================================
# EVENT TYPES
# ============================================================================

class EventPriority(int, Enum):
    """Priority levels for event handlers."""
    CRITICAL = 0
    HIGH = 10
    NORMAL = 50
    LOW = 90
    DEFERRED = 100


class GameEventType(str, Enum):
    """All game event types."""
    # Play Events
    SNAP = "SNAP"
    HANDOFF = "HANDOFF"
    PASS_THROWN = "PASS_THROWN"
    PASS_CAUGHT = "PASS_CAUGHT"
    PASS_INCOMPLETE = "PASS_INCOMPLETE"
    INTERCEPTION = "INTERCEPTION"
    FUMBLE = "FUMBLE"
    TACKLE = "TACKLE"
    SACK = "SACK"
    TOUCHDOWN = "TOUCHDOWN"
    SAFETY = "SAFETY"
    FIELD_GOAL = "FIELD_GOAL"

    # Clock Events
    QUARTER_END = "QUARTER_END"
    HALF_END = "HALF_END"
    GAME_END = "GAME_END"
    TIMEOUT = "TIMEOUT"
    TWO_MINUTE_WARNING = "TWO_MINUTE_WARNING"

    # Player Events
    PLAYER_INJURY = "PLAYER_INJURY"
    PLAYER_SUBSTITUTION = "PLAYER_SUBSTITUTION"
    PLAYER_FATIGUE = "PLAYER_FATIGUE"

    # Physics Events
    COLLISION = "COLLISION"
    BALL_TRAJECTORY = "BALL_TRAJECTORY"
    PLAYER_MOVEMENT = "PLAYER_MOVEMENT"

    # System Events
    TICK = "TICK"
    FRAME_START = "FRAME_START"
    FRAME_END = "FRAME_END"
    PLAY_START = "PLAY_START"
    PLAY_END = "PLAY_END"


# ============================================================================
# EVENT DATA CLASSES
# ============================================================================

@dataclass
class GameEvent:
    """Base class for all game events."""
    event_type: GameEventType
    tick: int
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize event for storage/replay."""
        return {
            "event_type": self.event_type.value,
            "tick": self.tick,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class PlayEvent(GameEvent):
    """Event during active play."""
    ball_carrier_id: str | None = None
    position_x: float = 0.0
    position_y: float = 0.0
    yards_gained: float = 0.0


@dataclass
class PlayerEvent(GameEvent):
    """Event related to a specific player."""
    player_id: str = ""
    team_id: str = ""
    severity: str = "minor"


@dataclass
class CollisionEvent(GameEvent):
    """Physics collision event."""
    entity1_id: str = ""
    entity2_id: str = ""
    impact_force: float = 0.0
    position_x: float = 0.0
    position_y: float = 0.0


# ============================================================================
# HANDLER TYPES
# ============================================================================

SyncHandler = Callable[[GameEvent], None]
AsyncHandler = Callable[[GameEvent], 'asyncio.Future[None]']
Handler = Union[SyncHandler, AsyncHandler]


@dataclass
class HandlerRegistration:
    """Registration info for an event handler."""
    handler: Handler
    priority: EventPriority
    event_types: set[GameEventType]
    is_async: bool
    once: bool = False


# ============================================================================
# ENHANCED EVENT BUS
# ============================================================================

class EnhancedEventBus:
    """
    Enhanced event bus with async support and typed events.
    """

    def __init__(self, history_size: int = 1000):
        self._handlers: dict[GameEventType, list[HandlerRegistration]] = {}
        self._global_handlers: list[HandlerRegistration] = []
        self._history: list[GameEvent] = []
        self._history_size = history_size
        self._paused = False
        self._event_count = 0

    def subscribe(
        self,
        event_types: GameEventType | list[GameEventType],
        handler: Handler,
        priority: EventPriority = EventPriority.NORMAL,
        once: bool = False,
    ) -> 'HandlerRegistration':
        """Subscribe to one or more event types."""
        if isinstance(event_types, GameEventType):
            event_types = [event_types]

        is_async = asyncio.iscoroutinefunction(handler)

        registration = HandlerRegistration(
            handler=handler,
            priority=priority,
            event_types=set(event_types),
            is_async=is_async,
            once=once,
        )

        for event_type in event_types:
            if event_type not in self._handlers:
                self._handlers[event_type] = []

            self._handlers[event_type].append(registration)
            self._handlers[event_type].sort(key=lambda r: r.priority)

        return registration

    def subscribe_all(
        self,
        handler: Handler,
        priority: EventPriority = EventPriority.LOW,
    ) -> HandlerRegistration:
        """Subscribe to all events."""
        is_async = asyncio.iscoroutinefunction(handler)

        registration = HandlerRegistration(
            handler=handler,
            priority=priority,
            event_types=set(),
            is_async=is_async,
        )

        self._global_handlers.append(registration)
        self._global_handlers.sort(key=lambda r: r.priority)

        return registration

    def unsubscribe(self, registration: HandlerRegistration) -> bool:
        """Remove a handler registration."""
        removed = False

        for event_type in registration.event_types:
            if event_type in self._handlers:
                if registration in self._handlers[event_type]:
                    self._handlers[event_type].remove(registration)
                    removed = True

        if registration in self._global_handlers:
            self._global_handlers.remove(registration)
            removed = True

        return removed

    def publish(self, event: GameEvent) -> int:
        """Publish an event synchronously."""
        if self._paused:
            return 0

        self._event_count += 1
        handlers_called = 0

        self._history.append(event)
        if len(self._history) > self._history_size:
            self._history.pop(0)

        handlers = list(self._handlers.get(event.event_type, []))
        handlers.extend(self._global_handlers)
        handlers.sort(key=lambda r: r.priority)

        to_remove: list[HandlerRegistration] = []

        for reg in handlers:
            try:
                if reg.is_async:
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(reg.handler(event))
                    except RuntimeError:
                        continue
                else:
                    reg.handler(event)

                handlers_called += 1

                if reg.once:
                    to_remove.append(reg)

            except Exception as e:
                print(f"Handler error for {event.event_type}: {e}")

        for reg in to_remove:
            self.unsubscribe(reg)

        return handlers_called

    async def publish_async(self, event: GameEvent) -> int:
        """Publish an event asynchronously."""
        if self._paused:
            return 0

        self._event_count += 1
        handlers_called = 0

        self._history.append(event)
        if len(self._history) > self._history_size:
            self._history.pop(0)

        handlers = list(self._handlers.get(event.event_type, []))
        handlers.extend(self._global_handlers)
        handlers.sort(key=lambda r: r.priority)

        to_remove: list[HandlerRegistration] = []
        tasks: list[asyncio.Task] = []

        for reg in handlers:
            try:
                if reg.is_async:
                    task = asyncio.create_task(reg.handler(event))
                    tasks.append(task)
                else:
                    reg.handler(event)

                handlers_called += 1

                if reg.once:
                    to_remove.append(reg)

            except Exception as e:
                print(f"Handler error for {event.event_type}: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        for reg in to_remove:
            self.unsubscribe(reg)

        return handlers_called

    def pause(self) -> None:
        """Pause event dispatch."""
        self._paused = True

    def resume(self) -> None:
        """Resume event dispatch."""
        self._paused = False

    def clear(self) -> None:
        """Clear all handlers."""
        self._handlers.clear()
        self._global_handlers.clear()

    def get_history(
        self,
        event_type: GameEventType | None = None,
        limit: int = 100,
    ) -> list[GameEvent]:
        """Get recent event history."""
        if event_type:
            filtered = [e for e in self._history if e.event_type == event_type]
            return filtered[-limit:]
        return self._history[-limit:]

    @property
    def event_count(self) -> int:
        """Total events published."""
        return self._event_count


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_default_bus: EnhancedEventBus | None = None


def get_event_bus() -> EnhancedEventBus:
    """Get the default event bus instance."""
    global _default_bus
    if _default_bus is None:
        _default_bus = EnhancedEventBus()
    return _default_bus


def reset_event_bus() -> None:
    """Reset the default event bus."""
    global _default_bus
    if _default_bus:
        _default_bus.clear()
    _default_bus = EnhancedEventBus()
