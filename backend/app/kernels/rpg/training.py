from app.kernels.core.ecs_manager import Component
from typing import Dict
from pydantic import Field

class TrainingEngine(Component):
    # Directive 1: Weekly Practice Scheduling
    # Directive 2: Fatigue as Soft Cap
    current_fatigue: float = 0.0 # 0-100
    chronic_fatigue: float = 0.0 # Directive 4: Chronic Wear
    
    # Directive 9: Real-World Periodization
    intensity_schedule: Dict[str, float] = {
        "Monday": 0.0, "Tuesday": 0.0, "Wednesday": 0.8, 
        "Thursday": 0.6, "Friday": 0.3, "Saturday": 0.0, "Sunday": 1.0 # Game Day
    }

    def train_player(self, intensity: float, injury_risk_mult: float) -> float:
        """
        Returns XP gained.
        """
        # Directive 7: Fatigue Multiplier on Injury
        effective_fatigue = self.current_fatigue + self.chronic_fatigue
        
        # XP Gain logic
        xp_gain = intensity * 10.0
        
        # Fatigue Accumulation
        self.current_fatigue += intensity * 5.0
        if self.current_fatigue > 80.0:
            # Overworking leads to chronic issues
            self.chronic_fatigue += 1.0
            
        return xp_gain

    def recover(self, rest_quality: float):
        self.current_fatigue = max(0.0, self.current_fatigue - (rest_quality * 20.0))
