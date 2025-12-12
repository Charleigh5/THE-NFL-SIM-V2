#!/usr/bin/env python3
"""
Scouting Service
================
Service layer for managing scouting operations, prospect reports,
and fog-of-war integration with the Draft Assistant.

Wraps ScoutingEngine for persistence and team-specific caching.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.scouting.scout import (
    ScoutingEngine,
    ScoutProfile,
    ScoutingReport,
    ScoutRegion,
    ScoutSpecialty,
    KnowledgeTier
)


@dataclass
class ScoutAssignment:
    """Tracks a scout assigned to a prospect."""
    scout_id: str
    prospect_id: str
    assigned_date: datetime
    visits: int = 1
    is_complete: bool = False


@dataclass
class TeamScoutingState:
    """Scouting state for a team."""
    team_id: int
    scouts: Dict[str, ScoutProfile] = field(default_factory=dict)
    assignments: Dict[str, ScoutAssignment] = field(default_factory=dict)
    reports: Dict[str, ScoutingReport] = field(default_factory=dict)
    budget_remaining: int = 100  # Scouting points per draft cycle


class ScoutingService:
    """
    Manages scouting operations for teams.

    Provides:
    - Scout hiring and assignment
    - Fog-of-war report generation
    - Integration with Draft Assistant
    """

    def __init__(self, db: Session = None):
        self.db = db
        self.engine = ScoutingEngine()
        self._team_states: Dict[int, TeamScoutingState] = {}

    def get_team_state(self, team_id: int) -> TeamScoutingState:
        """Get or create scouting state for a team."""
        if team_id not in self._team_states:
            self._team_states[team_id] = TeamScoutingState(team_id=team_id)
            self._initialize_default_scouts(team_id)
        return self._team_states[team_id]

    def _initialize_default_scouts(self, team_id: int):
        """Create default scouts for a new team."""
        state = self._team_states[team_id]

        # Every team starts with 3 scouts
        default_scouts = [
            ScoutProfile(
                scout_id=f"{team_id}_scout_1",
                name="National Scout",
                region=ScoutRegion.NATIONAL,
                specialty=ScoutSpecialty.GENERALIST,
                efficiency=60,
                accuracy=65,
            ),
            ScoutProfile(
                scout_id=f"{team_id}_scout_2",
                name="Regional Scout",
                region=ScoutRegion.EAST,
                specialty=ScoutSpecialty.QB_GURU,
                efficiency=70,
                accuracy=75,
            ),
            ScoutProfile(
                scout_id=f"{team_id}_scout_3",
                name="Area Scout",
                region=ScoutRegion.WEST,
                specialty=ScoutSpecialty.ATHLETICISM,
                efficiency=55,
                accuracy=80,
            ),
        ]

        for scout in default_scouts:
            state.scouts[scout.scout_id] = scout

    def assign_scout(
        self,
        team_id: int,
        scout_id: str,
        prospect_id: str
    ) -> Optional[ScoutAssignment]:
        """
        Assign a scout to evaluate a prospect.

        Args:
            team_id: Team making the assignment
            scout_id: Scout to assign
            prospect_id: Prospect to evaluate

        Returns:
            ScoutAssignment if successful, None otherwise
        """
        state = self.get_team_state(team_id)

        # Validate scout exists
        if scout_id not in state.scouts:
            return None

        # Check if already assigned
        assignment_key = f"{scout_id}_{prospect_id}"
        if assignment_key in state.assignments:
            # Add another visit
            state.assignments[assignment_key].visits += 1
            return state.assignments[assignment_key]

        # Create new assignment
        assignment = ScoutAssignment(
            scout_id=scout_id,
            prospect_id=prospect_id,
            assigned_date=datetime.now(),
            visits=1
        )
        state.assignments[assignment_key] = assignment

        return assignment

    def generate_report(
        self,
        team_id: int,
        prospect_id: str,
        true_attributes: Dict[str, int]
    ) -> Optional[ScoutingReport]:
        """
        Generate or update scouting report for a prospect.

        Args:
            team_id: Team requesting report
            prospect_id: Prospect ID
            true_attributes: Actual prospect attributes (hidden from user)

        Returns:
            ScoutingReport with fog-of-war applied
        """
        state = self.get_team_state(team_id)

        # Find best scout assigned to this prospect
        best_scout = None
        total_visits = 0

        for key, assignment in state.assignments.items():
            if assignment.prospect_id == prospect_id:
                scout = state.scouts.get(assignment.scout_id)
                if scout and (best_scout is None or scout.accuracy > best_scout.accuracy):
                    best_scout = scout
                total_visits += assignment.visits

        # If no scout assigned, return minimal info
        if not best_scout:
            return self._generate_unknown_report(prospect_id)

        # Generate report using engine
        report = self.engine.generate_report(
            true_attributes=true_attributes,
            scout=best_scout,
            visits=total_visits
        )
        report.player_id = prospect_id

        # Cache report
        state.reports[prospect_id] = report

        return report

    def _generate_unknown_report(self, prospect_id: str) -> ScoutingReport:
        """Create a report with all attributes unknown."""
        report = ScoutingReport(
            player_id=prospect_id,
            scout_id="NONE",
            completion_percentage=0.0
        )
        # All attributes will be empty/unknown
        return report

    def get_report(self, team_id: int, prospect_id: str) -> Optional[ScoutingReport]:
        """Get cached report for a prospect."""
        state = self.get_team_state(team_id)
        return state.reports.get(prospect_id)

    def get_all_reports(self, team_id: int) -> List[ScoutingReport]:
        """Get all scouting reports for a team."""
        state = self.get_team_state(team_id)
        return list(state.reports.values())

    def get_formatted_report(
        self,
        team_id: int,
        prospect_id: str,
        true_attributes: Dict[str, int]
    ) -> Dict[str, str]:
        """
        Get user-friendly formatted report.

        Returns attributes as display strings based on knowledge tier.
        E.g., "???" for unknown, "B" for solid, "85" for exact.
        """
        report = self.generate_report(team_id, prospect_id, true_attributes)

        if not report:
            return {"error": "No scouting data available"}

        return self.engine.format_for_display(report)

    def apply_fog_of_war(
        self,
        team_id: int,
        prospect_id: str,
        true_attributes: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Apply fog-of-war to prospect attributes for Draft Assistant.

        Returns:
            Dict with visible attributes and their certainty levels
        """
        report = self.generate_report(team_id, prospect_id, true_attributes)

        if not report or report.completion_percentage == 0:
            # Completely unknown - return basic bio only
            return {
                "scouted": False,
                "completion": 0,
                "attributes": {},
                "message": "This prospect has not been scouted"
            }

        # Build visible attributes with certainty
        visible = {}
        for attr, (value, error, tier) in report.attributes.items():
            visible[attr] = {
                "value": value if tier in [KnowledgeTier.EXACT, KnowledgeTier.PARTIAL] else None,
                "range": (value - error, value + error) if tier != KnowledgeTier.UNKNOWN else None,
                "tier": tier.value,
                "display": self.engine.format_for_display(report).get(attr, "???")
            }

        return {
            "scouted": True,
            "completion": report.completion_percentage,
            "attributes": visible,
            "strengths": report.strengths,
            "weaknesses": report.weaknesses
        }
