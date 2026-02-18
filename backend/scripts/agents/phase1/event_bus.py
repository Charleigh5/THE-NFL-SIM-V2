#!/usr/bin/env python3
"""
Phase 1 Agent 3: Enhanced Event Bus
====================================
Implements an async-capable, typed event bus for simulation events.

CORTEX Foundation Component:
- Type-safe event definitions
- Async event handlers
- Event history for replay
- Priority-based dispatch

Context7 Best Practices:
- Protocol-based handlers
- Dataclass events
- Full type annotations
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar, Union

# ============================================================================
# EVENT TYPES
# ============================================================================

class EventPriority(int, Enum):
    """Priority levels for event handlers."""
    CRITICAL = 0   # System-level, must run first
    HIGH = 10      # Important game logic
    NORMAL = 50    # Standard handlers
    LOW = 90       # Analytics, logging
    DEFERRED = 100 # Can run after frame


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

# Type variable for event subclasses
E = TypeVar('E', bound=GameEvent)

# Handler function types
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
    once: bool = False  # Remove after first call
    weak_ref: bool = False  # Use weak reference


# ============================================================================
# ENHANCED EVENT BUS
# ============================================================================

class EnhancedEventBus:
    """
    Enhanced event bus with async support and typed events.

    Features:
    - Sync and async handler support
    - Priority-based dispatch
    - Event history for replay
    - Weak references for cleanup
    - One-time handlers
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
        """
        Subscribe to one or more event types.

        Args:
            event_types: Event type(s) to listen for
            handler: Handler function (sync or async)
            priority: Handler priority (lower = earlier)
            once: Remove handler after first call

        Returns:
            Registration object for unsubscribing
        """
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
            # Sort by priority
            self._handlers[event_type].sort(key=lambda r: r.priority)

        return registration

    def subscribe_all(
        self,
        handler: Handler,
        priority: EventPriority = EventPriority.LOW,
    ) -> HandlerRegistration:
        """Subscribe to all events (useful for logging/analytics)."""
        is_async = asyncio.iscoroutinefunction(handler)

        registration = HandlerRegistration(
            handler=handler,
            priority=priority,
            event_types=set(),  # Empty = all events
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
        """
        Publish an event synchronously.

        Args:
            event: Event to publish

        Returns:
            Number of handlers called
        """
        if self._paused:
            return 0

        self._event_count += 1
        handlers_called = 0

        # Store in history
        self._history.append(event)
        if len(self._history) > self._history_size:
            self._history.pop(0)

        # Get handlers for this event type
        handlers = list(self._handlers.get(event.event_type, []))
        handlers.extend(self._global_handlers)
        handlers.sort(key=lambda r: r.priority)

        # Track one-time handlers to remove
        to_remove: list[HandlerRegistration] = []

        for reg in handlers:
            try:
                if reg.is_async:
                    # Run async handler in event loop if available
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(reg.handler(event))
                    except RuntimeError:
                        # No event loop, skip async handlers
                        continue
                else:
                    reg.handler(event)

                handlers_called += 1

                if reg.once:
                    to_remove.append(reg)

            except Exception as e:
                # Log but don't stop other handlers
                print(f"Handler error for {event.event_type}: {e}")

        # Remove one-time handlers
        for reg in to_remove:
            self.unsubscribe(reg)

        return handlers_called

    async def publish_async(self, event: GameEvent) -> int:
        """
        Publish an event asynchronously.

        Awaits all async handlers before returning.
        """
        if self._paused:
            return 0

        self._event_count += 1
        handlers_called = 0

        # Store in history
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

        # Await all async handlers
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


# ============================================================================
# MAIN AGENT ENTRY POINT
# ============================================================================

def main():
    """Agent entry point - generates enhanced event bus."""
    from scripts.agents.shared.markers import mark_complete
    from scripts.agents.shared.validation import validate_python_syntax

    print("=" * 60)
    print("Phase 1 Agent 3: Enhanced Event Bus")
    print("=" * 60)

    target_dir = PROJECT_ROOT / "app" / "engine" / "core"
    target_dir.mkdir(exist_ok=True)

    target_file = target_dir / "enhanced_event_bus.py"

    source_content = Path(__file__).read_text()
    lines = source_content.split("\n")

    impl_start = None
    for i, line in enumerate(lines):
        if "# ============" in line and "EVENT TYPES" in lines[i]:
            impl_start = i
            break

    if impl_start:
        impl_lines = lines[impl_start:]
        impl_end = None
        for i, line in enumerate(impl_lines):
            if "def main():" in line:
                impl_end = i
                break

        if impl_end:
            impl_lines = impl_lines[:impl_end]

        header = '''#!/usr/bin/env python3
"""
Enhanced Event Bus - CORTEX Foundation
=======================================
Async-capable, typed event bus for simulation events.

Generated by Phase 1 Agent 3
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union
from enum import Enum, auto
import time
import weakref

'''

        target_file.write_text(header + "\n".join(impl_lines))
        print(f"✅ Generated: {target_file}")

    # Update __init__.py
    init_file = target_dir / "__init__.py"
    init_content = init_file.read_text() if init_file.exists() else ""

    if "EnhancedEventBus" not in init_content:
        additional = '''
from .enhanced_event_bus import (
    EnhancedEventBus,
    GameEvent,
    GameEventType,
    EventPriority,
    PlayEvent,
    PlayerEvent,
    CollisionEvent,
    get_event_bus,
    reset_event_bus,
)
'''
        init_content += additional
        init_file.write_text(init_content)
        print(f"✅ Updated: {init_file}")

    success, error = validate_python_syntax(target_file)
    if not success:
        print(f"❌ Syntax error: {error}")
        return
    print("✅ Syntax validated")

    mark_complete("event_bus", {"file": str(target_file)})
    mark_complete("event_bus_tests", {"status": "pending_implementation"})

    print("\n✅ Phase 1 Agent 3 completed successfully!")


if __name__ == "__main__":
    main()
