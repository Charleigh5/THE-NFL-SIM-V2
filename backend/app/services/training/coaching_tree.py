#!/usr/bin/env python3
"""
Coaching Tree Module
====================
Handles coach skills, mentorship, and coordinator progression.

Phase 7: Training & Development
- Skill Tree nodes and unlocking
- Coordinator bonuses
- Hire/Fire logic assistance
"""

from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================

class CoachRole(str, Enum):
    """Coaching staff roles."""
    HEAD_COACH = "HEAD_COACH"
    OFFENSIVE_COORD = "OFFENSIVE_COORD"
    DEFENSIVE_COORD = "DEFENSIVE_COORD"
    SPECIAL_TEAMS = "SPECIAL_TEAMS"
    POSITION_COACH = "POSITION_COACH"


class SkillCategory(str, Enum):
    """Category of coaching skills."""
    OFFENSE = "OFFENSE"
    DEFENSE = "DEFENSE"
    TEAM_MANAGEMENT = "TEAM_MANAGEMENT"
    SCOUTING = "SCOUTING"
    PLAYER_DEVELOPMENT = "PLAYER_DEVELOPMENT"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class CoachSkill:
    """A specific unlockable skill."""
    id: str
    name: str
    category: SkillCategory
    max_rank: int
    current_rank: int = 0
    description: str = ""
    cost_per_rank: int = 10

    @property
    def bonus_value(self) -> float:
        """Current bonus multiplier (e.g. 1.05 for 5%)."""
        return 1.0 + (0.05 * self.current_rank)


@dataclass
class CoachState:
    """Coach's career state."""
    coach_id: str
    role: CoachRole
    level: int = 1
    xp: int = 0
    xp_to_next: int = 1000
    points_available: int = 0
    skills: dict[str, CoachSkill] = field(default_factory=dict)

    # Track specialty
    archetype: str = "Standard" # e.g. "QB Guru"


# ============================================================================
# COACHING ENGINE
# ============================================================================

class CoachingEngine:
    """
    Manages coach progression and skill trees.
    """

    def __init__(self):
        self._init_skill_registry()

    def _init_skill_registry(self):
        """Define available skills."""
        self.skill_registry = {
            "QB_WHISPERER": {
                "name": "QB Whisperer",
                "category": SkillCategory.OFFENSE,
                "desc": "Increases QB XP gain in training."
            },
            "TRENCH_WARFARE": {
                "name": "Trench Warfare",
                "category": SkillCategory.OFFENSE,
                "desc": "Boosts OL/DL blocking/shedding."
            },
            "SECONDARY_GURU": {
                "name": "Secondary Guru",
                "category": SkillCategory.DEFENSE,
                "desc": "Increases DB coverage ratings."
            },
            "SCOUTING_EYE": {
                "name": "Eagle Eye",
                "category": SkillCategory.SCOUTING,
                "desc": "Unlocks 50% more scouting info."
            },
            "MASTER_MOTIVATOR": {
                "name": "Master Motivator",
                "category": SkillCategory.TEAM_MANAGEMENT,
                "desc": "Reduces morale penalties from losses."
            },
        }

    def create_coach(self, coach_id: str, role: CoachRole) -> CoachState:
        """Initialize a new coach."""
        coach = CoachState(coach_id=coach_id, role=role)
        # Populate skills from registry
        for sid, data in self.skill_registry.items():
            coach.skills[sid] = CoachSkill(
                id=sid,
                name=data["name"],
                category=data["category"],
                max_rank=3,
                description=data["desc"]
            )
        return coach

    def award_xp(self, coach: CoachState, amount: int) -> bool:
        """
        Give coach XP. Returns True if leveled up.
        """
        coach.xp += amount
        leveled = False
        while coach.xp >= coach.xp_to_next:
            coach.xp -= coach.xp_to_next
            coach.level += 1
            coach.points_available += 1
            coach.xp_to_next = int(coach.xp_to_next * 1.1)
            leveled = True
        return leveled

    def purchase_skill(self, coach: CoachState, skill_id: str) -> bool:
        """
        Spend point to upgrade skill.
        """
        if skill_id not in coach.skills:
            return False

        skill = coach.skills[skill_id]

        if coach.points_available < 1:
            return False

        if skill.current_rank >= skill.max_rank:
            return False

        skill.current_rank += 1
        coach.points_available -= 1
        return True

    def get_staff_bonuses(self, staff: list[CoachState]) -> dict[str, float]:
        """
        Aggregate bonuses from entire coaching staff.

        Coordinator bonuses stack with Head Coach.
        """
        bonuses = {}
        for coach in staff:
            for skill in coach.skills.values():
                if skill.current_rank > 0:
                    current = bonuses.get(skill.id, 1.0)
                    # Additive stacking of the bonus percentage
                    # If current is 1.05 and new is 1.05, result is 1.10
                    bonus_pct = skill.bonus_value - 1.0
                    bonuses[skill.id] = current + bonus_pct

        return bonuses
