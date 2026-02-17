"""
GENESIS Engine Module
=====================
Biological player modeling for the NFL Sim Engine.

Phase 2: Biological Systems
- Biometrics (physical measurements, muscle fiber composition)
- Cognition (S2 score, OODA loop, vision cone)
- Fatigue (4-compartment energy system)
- Injury (body part hierarchy, chronic wear, G-force calculations)
"""

from .biometrics import (
    POSITION_BIOMETRIC_RANGES,
    BiometricProfile,
    BodyType,
    FiberType,
    generate_biometrics_for_position,
)
from .cognition import (
    CognitionEngine,
    CognitiveProfile,
    CognitiveState,
    OODAState,
    ReadPhase,
    VisionCone,
)
from .fatigue import (
    ActivityLevel,
    EnergyCompartment,
    FatigueEngine,
    FatigueLevel,
    FatigueState,
)
from .injury import (
    BodyPart,
    BodyRegion,
    ChronicWear,
    Injury,
    InjuryEngine,
    InjuryProfile,
    InjurySeverity,
    InjuryType,
)

__all__ = [
    # Biometrics
    "BiometricProfile",
    "BodyType",
    "FiberType",
    "POSITION_BIOMETRIC_RANGES",
    "generate_biometrics_for_position",
    # Cognition
    "CognitionEngine",
    "CognitiveProfile",
    "CognitiveState",
    "ReadPhase",
    "OODAState",
    "VisionCone",
    # Fatigue
    "FatigueEngine",
    "FatigueState",
    "FatigueLevel",
    "ActivityLevel",
    "EnergyCompartment",
    # Injury
    "InjuryEngine",
    "InjuryProfile",
    "Injury",
    "InjuryType",
    "InjurySeverity",
    "BodyPart",
    "BodyRegion",
    "ChronicWear",
]
