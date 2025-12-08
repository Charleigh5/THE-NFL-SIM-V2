#!/usr/bin/env python3
"""
Playbook Module
===============
Manages offensive and defensive concepts, formations, and play design.

Phase 9: Playbook & AI
- Formation definitions
- Play concepts (West Coast, Air Raid, etc.)
- Personnel groupings
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class PlayType(str, Enum):
    """Category of play."""
    RUN = "RUN"
    PASS = "PASS"
    PLAY_ACTION = "PLAY_ACTION"
    SCREEN = "SCREEN"
    TRICK = "TRICK"


class Formation(str, Enum):
    """Offensive formations."""
    SINGLEBACK = "SINGLEBACK"
    I_FORM = "I_FORM"
    SHOTGUN = "SHOTGUN"
    PISTOL = "PISTOL"
    EMPTY = "EMPTY"
    WILDCAT = "WILDCAT"


class DefensiveScheme(str, Enum):
    """Defensive alignments."""
    BASE_4_3 = "4-3"
    BASE_3_4 = "3-4"
    NICKEL = "NICKEL"
    DIME = "DIME"
    PREVENT = "PREVENT"
    GOAL_LINE = "GOAL_LINE"


class Concept(str, Enum):
    """Offensive philosophies."""
    WEST_COAST = "WEST_COAST"      # Short, timing routes
    AIR_RAID = "AIR_RAID"          # Spread, vertical
    POWER_RUN = "POWER_RUN"        # Physical, downhill
    ZONE_RUN = "ZONE_RUN"          # Stretch, cutback
    RPO = "RPO"                    # Run-Pass Option


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Personnel:
    """Personnel grouping (e.g., 11 = 1 RB, 1 TE)."""
    name: str
    rb_count: int
    te_count: int
    wr_count: int

    @property
    def code(self) -> str:
        """Returns '11' for 1RB 1TE."""
        return f"{self.rb_count}{self.te_count}"


@dataclass
class Play:
    """A single play in the playbook."""
    play_id: str
    name: str
    play_type: PlayType
    formation: Formation
    concept: Concept
    personnel: Personnel

    # Effectiveness ratings
    vs_man_coverage: int = 50
    vs_zone_coverage: int = 50
    vs_blitz: int = 50

    # Metadata
    risk_level: int = 5  # 1-10 (Higher = More risk)
    avg_yards: float = 5.0


@dataclass
class Playbook:
    """Collection of plays for a team."""
    team_id: str
    plays: Dict[str, Play] = field(default_factory=dict)
    primary_concept: Concept = Concept.WEST_COAST

    def add_play(self, play: Play):
        self.plays[play.play_id] = play

    def get_plays_by_situation(
        self,
        down: int,
        distance: int,
        field_position: int
    ) -> List[Play]:
        """
        Filter plays suitable for the situation.
        """
        suitable = []

        for play in self.plays.values():
            # Short yardage: Any run
            if distance <= 3:
                if play.play_type == PlayType.RUN:
                    suitable.append(play)
            # Long yardage: Passing
            elif distance >= 10:
                if play.play_type in [PlayType.PASS, PlayType.SCREEN]:
                    suitable.append(play)
            # Medium: Mix
            else:
                suitable.append(play)

        return suitable[:10] # Return top 10


# ============================================================================
# PLAYBOOK GENERATOR
# ============================================================================

class PlaybookGenerator:
    """
    Factory to create default playbooks.
    """

    @staticmethod
    def generate_west_coast(team_id: str) -> Playbook:
        """Generate a West Coast offense playbook."""
        pb = Playbook(team_id, primary_concept=Concept.WEST_COAST)

        # Personnel groups
        personnel_11 = Personnel("11 Personnel", 1, 1, 3)
        personnel_12 = Personnel("12 Personnel", 1, 2, 2)

        # Example Plays
        plays = [
            Play(
                "WC_SLANT_FLAT", "Slant-Flat Combo", PlayType.PASS,
                Formation.SHOTGUN, Concept.WEST_COAST, personnel_11,
                vs_man_coverage=70, vs_zone_coverage=60, avg_yards=6.5
            ),
            Play(
                "INSIDE_ZONE", "Inside Zone", PlayType.RUN,
                Formation.SHOTGUN, Concept.ZONE_RUN, personnel_11,
                vs_man_coverage=50, vs_zone_coverage=55, avg_yards=4.2
            ),
            Play(
                "MESH_CONCEPT", "Mesh Cross", PlayType.PASS,
                Formation.SHOTGUN, Concept.WEST_COAST, personnel_11,
                vs_man_coverage=80, vs_zone_coverage=50, avg_yards=7.0
            ),
        ]

        for p in plays:
            pb.add_play(p)

        return pb

    @staticmethod
    def generate_air_raid(team_id: str) -> Playbook:
        """Generate an Air Raid offense playbook."""
        pb = Playbook(team_id, primary_concept=Concept.AIR_RAID)

        personnel_10 = Personnel("10 Personnel", 1, 0, 4)

        plays = [
            Play(
                "FOUR_VERTS", "Four Verticals", PlayType.PASS,
                Formation.SHOTGUN, Concept.AIR_RAID, personnel_10,
                vs_man_coverage=65, vs_zone_coverage=85, avg_yards=12.0, risk_level=7
            ),
            Play(
                "SHALLOW_CROSS", "Shallow Cross", PlayType.PASS,
                Formation.SHOTGUN, Concept.AIR_RAID, personnel_10,
                vs_man_coverage=75, vs_zone_coverage=55, avg_yards=8.5
            ),
        ]

        for p in plays:
            pb.add_play(p)

        return pb
