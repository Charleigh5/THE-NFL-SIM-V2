"""
CORTEX Core Module
==================
Core simulation components for the NFL Sim Engine.
Phase 1: Foundation (Tick Engine, RNG, Event Bus)
"""

from .deterministic_rng import (
    DeterministicRNG,
    RNGSeed,
    RNGState,
    generate_client_seed,
    generate_server_seed,
)
from .enhanced_event_bus import (
    CollisionEvent,
    EnhancedEventBus,
    EventPriority,
    GameEvent,
    GameEventType,
    HandlerRegistration,
    PlayerEvent,
    PlayEvent,
    get_event_bus,
    reset_event_bus,
)
from .tick_engine import (
    FrameState,
    GameClock,
    PlayPhase,
    TickConfig,
    TickEngine,
    TickEngineState,
    TickListener,
)

__all__ = [
    # Tick Engine
    "TickEngine",
    "TickConfig",
    "TickEngineState",
    "PlayPhase",
    "GameClock",
    "FrameState",
    "TickListener",
    # Deterministic RNG
    "DeterministicRNG",
    "RNGSeed",
    "RNGState",
    "generate_server_seed",
    "generate_client_seed",
    # Enhanced Event Bus
    "EnhancedEventBus",
    "GameEvent",
    "GameEventType",
    "EventPriority",
    "PlayEvent",
    "PlayerEvent",
    "CollisionEvent",
    "HandlerRegistration",
    "get_event_bus",
    "reset_event_bus",
]
