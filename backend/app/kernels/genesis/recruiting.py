from app.kernels.core.ecs_manager import Component
from typing import Dict, List, Optional
from pydantic import Field

class RecruitingProfile(Component):
    # Directive 14: Pre-Draft Interviews (Scheme Fit)
    scheme_fit_score: float = 0.0 # 0.0 - 1.0
    interview_notes: List[str] = Field(default_factory=list)
    
    # Directive 19: Qualitative Scouting Reports
    scouting_report: str = ""

    def conduct_interview(self, team_scheme: str, player_archetype: str) -> float:
        """
        Directive 14: Assess scheme fit.
        """
        fit = 0.5
        if team_scheme == player_archetype:
            fit = 1.0
        elif team_scheme == "Spread" and player_archetype == "Power":
            fit = 0.2
            
        self.scheme_fit_score = fit
        self.interview_notes.append(f"Scheme Fit assessed as {fit:.2f}")
        return fit

class WorkoutEngine(Component):
    # Directive 13: Specialized Recruiting Workouts
    workout_results: Dict[str, float] = {}

    def run_workout(self, drill_type: str, player_attributes: Dict[str, float]):
        """
        Directive 13: Simulates a workout to reveal true attributes.
        """
        if drill_type == "40_Yard_Dash":
            # Simulate 40 time based on Speed + Variance
            true_speed = player_attributes.get("Speed", 70)
            # 99 Speed = 4.24, 70 Speed = 4.60
            time = 4.24 + ((99 - true_speed) * 0.015)
            self.workout_results["40_Yard_Dash"] = round(time, 2)
