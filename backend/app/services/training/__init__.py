"""
TRAINING Package
================
Player development and coaching systems.

Phase 7: Training & Development
- Training Camp (Drills, Intensity)
- Progression (XP, Aging, Dev Traits)
- Coaching Tree (Skills, Staff Bonuses)
"""

from .camp import (
    CampDay,
    CampResult,
    DrillConfig,
    DrillType,
    TrainingCampEngine,
    TrainingIntensity,
)
from .coaching_tree import (
    CoachingEngine,
    CoachRole,
    CoachSkill,
    CoachState,
    SkillCategory,
)
from .progression import (
    DevTrait,
    PlayerProgressionState,
    ProgressionEngine,
    ProgressionPhase,
)

__all__ = [
    # Camp
    "TrainingCampEngine",
    "CampDay",
    "CampResult",
    "DrillType",
    "TrainingIntensity",
    "DrillConfig",
    # Progression
    "ProgressionEngine",
    "PlayerProgressionState",
    "ProgressionPhase",
    "DevTrait",
    # Coaching
    "CoachingEngine",
    "CoachState",
    "CoachSkill",
    "CoachRole",
    "SkillCategory",
]
