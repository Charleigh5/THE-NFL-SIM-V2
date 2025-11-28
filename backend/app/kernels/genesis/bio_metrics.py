from app.kernels.core.ecs_manager import Component
from typing import Dict, Optional
from pydantic import Field

class BiologicalProfile(Component):
    # Directive 1: Hard cap MaxAcceleration based on FastTwitchRatio
    fast_twitch_ratio: float = Field(default=0.5, ge=0.0, le=1.0) # 0.0 - 1.0 (Genetic Ceiling)
    max_acceleration_cap: float = 0.0
    
    # Directive 2: Hand Size Geopolitics
    hand_size_inches: float = Field(default=9.0, ge=7.0, le=12.0)
    
    # Directive 20: Wingspan Logic
    wingspan_inches: float = Field(default=75.0, ge=60.0, le=90.0)
    interaction_radius: float = 0.0

    def __init__(self, **data):
        super().__init__(**data)
        self.calculate_derived_metrics()

    def calculate_derived_metrics(self):
        # Directive 1 Logic
        # Example: 80% Fast Twitch = Cap of 99 Accel, 20% = Cap of 85 Accel
        self.max_acceleration_cap = 85.0 + (self.fast_twitch_ratio * 14.0)
        
        # Directive 20 Logic
        # Wingspan defines catch radius. Standard 75" = 1.0 meters radius
        self.interaction_radius = self.wingspan_inches / 75.0

    def calculate_fumble_risk(self, temperature_f: float) -> float:
        # Directive 2 Logic
        base_risk = 0.01
        if self.hand_size_inches < 9.0 and temperature_f < 32.0:
            base_risk *= 1.40 # 40% increase
        return base_risk

class AnatomyModel(Component):
    # Directive 6: Structural Integrity
    current_health: float = 100.0 # Temporary health
    chronic_wear: float = 0.0 # Permanent degradation (Directive 6)
    
    ligaments: Dict[str, Dict[str, float]] = Field(default_factory=lambda: {
        "ACL": {"integrity": 100.0, "stress": 0.0, "soft_tissue_limit": 85.0}, # Directive 7
        "MCL": {"integrity": 100.0, "stress": 0.0, "soft_tissue_limit": 90.0},
        "Achilles": {"integrity": 100.0, "stress": 0.0, "soft_tissue_limit": 80.0}
    })

    def apply_stress(self, torque_vector: float, body_part: str):
        # Directive 7: Physics-Based Injury
        if body_part in self.ligaments:
            lig = self.ligaments[body_part]
            lig["stress"] += torque_vector * 0.1
            
            # Check for failure
            if lig["stress"] > lig["soft_tissue_limit"]:
                lig["integrity"] = 0.0 # Snap
                self.current_health -= 50.0

class FatigueRegulator(Component):
    hrv: float = 100.0 # Heart Rate Variability
    lactic_acid: float = 0.0
    max_burst_capacity: float = 100.0
    
    # Directive: Climate Familiarity
    home_climate: str = "Neutral" # "Cold", "Warm", "Dome"

    def update_fatigue(self, exertion: float, current_temp_f: float):
        """
        Updates fatigue with Heat/Cold modifiers.
        """
        fatigue_mult = 1.0
        
        # Heat Fatigue: Cold teams tire faster in heat (>85F)
        if current_temp_f > 85.0 and self.home_climate == "Cold":
            fatigue_mult = 1.5 # 50% faster fatigue
            
        # Cold Stiffness: Warm teams struggle in cold (<32F)
        if current_temp_f < 32.0 and self.home_climate == "Warm":
            fatigue_mult = 1.2 # 20% faster fatigue due to stiffness
            
        self.lactic_acid += exertion * 0.5 * fatigue_mult
        self.hrv -= exertion * 0.2 * fatigue_mult
        
        # Burst capacity drops as lactic acid builds
        self.max_burst_capacity = max(0, 100 - self.lactic_acid)
