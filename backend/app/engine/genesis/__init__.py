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
    BiometricProfile,
    BodyType,
    FiberType,
    POSITION_BIOMETRIC_RANGES,
    generate_biometrics_for_position,
)

from .cognition import (
    CognitionEngine,
    CognitiveProfile,
    CognitiveState,
    ReadPhase,
    OODAState,
    VisionCone,
)

from .fatigue import (
    FatigueEngine,
    FatigueState,
    FatigueLevel,
    ActivityLevel,
    EnergyCompartment,
)

from .injury import (
    InjuryEngine,
    InjuryProfile,
    Injury,
    InjuryType,
    InjurySeverity,
    BodyPart,
    BodyRegion,
    ChronicWear,
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
