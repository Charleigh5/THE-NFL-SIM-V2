"""
Domain Contracts & Typed Interfaces
===================================
Canonical domain models, value objects, and contracts for simulation engines.
"""

from app.schemas.society import (
    PsychologicalDNA,
    PlayerBackstory,
    TensionDelta,
    LockerRoomDialogueTurn,
    LockerRoomConsequences,
    LockerRoomActionOption,
    LockerRoomEventResponse,
    LockerRoomResolutionRequest,
    LockerRoomResolutionResponse,
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
