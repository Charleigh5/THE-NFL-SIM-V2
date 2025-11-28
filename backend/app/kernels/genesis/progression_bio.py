from app.kernels.core.ecs_manager import Component
from typing import Dict, List
import math

class BioProgression(Component):
    # Directive 10: Stat-based Progression (Meritocracy)
    # Directive 11: Position/Age Decline Curves
    # Directive 16: Gradual Regression
    
    age: int = 22
    position: str = "RB"
    
    # Base decline start ages by position
    decline_starts: Dict[str, int] = {
        "RB": 26, "WR": 29, "QB": 35, "OL": 32, "DL": 30, "LB": 29, "DB": 29, "K": 38
    }

    def calculate_regression_impact(self) -> Dict[str, float]:
        """
        Directive 11 & 16: Calculates attribute penalties based on age curves.
        """
        decline_age = self.decline_starts.get(self.position, 30)
        
        if self.age <= decline_age:
            return {}
            
        years_over = self.age - decline_age
        
        # Exponential decay for physical traits
        physical_decay = -1.0 * (math.exp(years_over * 0.15) - 1.0)
        
        return {
            "Speed": physical_decay,
            "Acceleration": physical_decay,
            "Agility": physical_decay * 0.8
        }

    def apply_meritocracy_boost(self, performance_grade: float) -> float:
        """
        Directive 10: Stat-based Progression.
        Performance Grade (0.0 - 100.0) determines development speed.
        """
        if performance_grade > 90.0:
            return 1.5 # Super dev trait
        elif performance_grade > 75.0:
            return 1.1
        elif performance_grade < 60.0:
            return 0.5 # Stagnation
        return 1.0
