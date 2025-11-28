from app.kernels.core.ecs_manager import Component
from enum import Enum
from typing import Dict, List

class PersonnelGrouping(str, Enum):
    P11 = "11 Personnel" # 1 RB, 1 TE, 3 WR
    P12 = "12 Personnel" # 1 RB, 2 TE, 2 WR
    P21 = "21 Personnel" # 2 RB, 1 TE, 2 WR
    P10 = "10 Personnel" # 1 RB, 0 TE, 4 WR
    P13 = "13 Personnel" # 1 RB, 3 TE, 1 WR

class OffensiveScheme(str, Enum):
    SPREAD = "Shotgun Spread"
    WIDE_ZONE = "Wide Zone / Shanahan"
    AIR_RAID = "Air Raid"
    POWER_RUN = "Power Run"

class DefensiveScheme(str, Enum):
    BASE_43 = "4-3 Defense"
    BASE_34 = "3-4 Defense"
    NICKEL = "Nickel"
    DIME = "Dime"
    PREVENT = "Prevent"

class StrategyEngine(Component):
    current_personnel: PersonnelGrouping = PersonnelGrouping.P11
    current_off_scheme: OffensiveScheme = OffensiveScheme.SPREAD
    current_def_scheme: DefensiveScheme = DefensiveScheme.NICKEL
    
    def get_schematic_multiplier(self, off_play_type: str, def_play_type: str) -> float:
        """
        The Rock-Paper-Scissors Logic.
        Returns a multiplier for the offense (1.0 = Neutral, >1.0 = Advantage, <1.0 = Disadvantage).
        """
        multiplier = 1.0
        
        # Example RPS Logic
        if off_play_type == "INSIDE_ZONE":
            if def_play_type == "RUN_COMMIT":
                multiplier = 0.75 # Defense Hard Counter
            elif def_play_type == "PASS_COMMIT":
                multiplier = 1.25 # Offense Advantage
                
        if off_play_type == "VERTICALS":
            if def_play_type == "COVER_3":
                multiplier = 1.25 # Seam routes exploit Cover 3
            elif def_play_type == "PREVENT":
                multiplier = 0.50 # Hard Counter
                
        return multiplier

    def resolve_matchup(self, personnel: PersonnelGrouping, def_scheme: DefensiveScheme) -> float:
        """
        Evaluates personnel vs defensive front.
        """
        # Nickel is standard against 11 Personnel
        if personnel == PersonnelGrouping.P11 and def_scheme == DefensiveScheme.NICKEL:
            return 1.0 # Neutral
            
        # Heavy Run (13/21) vs Dime = Smash
        if personnel in [PersonnelGrouping.P13, PersonnelGrouping.P21] and def_scheme == DefensiveScheme.DIME:
            return 1.5 # Massive Run Advantage
            
        return 1.0
