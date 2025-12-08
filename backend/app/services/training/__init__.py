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
    TrainingCampEngine,
    CampDay,
    CampResult,
    DrillType,
    TrainingIntensity,
    DrillConfig,
)

from .progression import (
    ProgressionEngine,
    PlayerProgressionState,
    ProgressionPhase,
    DevTrait,
)

from .coaching_tree import (
    CoachingEngine,
    CoachState,
    CoachSkill,
    CoachRole,
    SkillCategory,
)

__all__ = [
    # Camp
    "TrainingCampEngine", "CampDay", "CampResult",
    "DrillType", "TrainingIntensity", "DrillConfig",
    # Progression
    "ProgressionEngine", "PlayerProgressionState",
    "ProgressionPhase", "DevTrait",
    # Coaching
    "CoachingEngine", "CoachState", "CoachSkill",
    "CoachRole", "SkillCategory",
]
