"""
Domain Contracts & Typed Interfaces
===================================
Canonical domain models, value objects, and contracts for simulation engines.
"""

from app.schemas.society import (
    LockerRoomActionOption,
    LockerRoomConsequences,
    LockerRoomDialogueTurn,
    LockerRoomEventResponse,
    LockerRoomResolutionRequest,
    LockerRoomResolutionResponse,
    PlayerBackstory,
    PsychologicalDNA,
    TensionDelta,
)

__all__ = [
    "PsychologicalDNA",
    "PlayerBackstory",
    "TensionDelta",
    "LockerRoomDialogueTurn",
    "LockerRoomConsequences",
    "LockerRoomActionOption",
    "LockerRoomEventResponse",
    "LockerRoomResolutionRequest",
    "LockerRoomResolutionResponse",
]
