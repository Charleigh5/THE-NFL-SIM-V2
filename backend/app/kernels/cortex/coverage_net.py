from app.kernels.core.ecs_manager import Component
from app.kernels.core.ecs_manager import Component
from typing import Dict, Tuple, List

class CoverageNet(Component):
    """
    Simulates the NGS/AWS Coverage Responsibility Models.
    In a real implementation, this would interface with a Neural Network (ONNX/PyTorch).
    Here, we simulate the logic.
    """
    
    def identify_targeted_defender(self, pass_trajectory: Dict, defenders: List[Dict]) -> str:
        """
        Model 1: Targeted Defender Identification.
        Finds the defender most responsible for the catch point.
        """
        # Simplified: Find closest defender to ball arrival point
        closest_defender = None
        min_dist = float('inf')
        
        target_x, target_y = pass_trajectory['arrival_x'], pass_trajectory['arrival_y']
        
        for defender in defenders:
            dist = ((defender['x'] - target_x)**2 + (defender['y'] - target_y)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closest_defender = defender['id']
                
        return closest_defender

    def identify_matchups(self, receivers: List[Dict], defenders: List[Dict]) -> Dict[str, str]:
        """
        Model 2: Matchup Identification.
        Who is covering whom?
        """
        matchups = {}
        # Simplified Man-Match logic
        for rx in receivers:
            # Find closest defender
            closest_def = min(defenders, key=lambda d: ((d['x']-rx['x'])**2 + (d['y']-rx['y'])**2)**0.5)
            matchups[rx['id']] = closest_def['id']
            
        return matchups

    def identify_zone_responsibility(self, defender: Dict, scheme: str) -> str:
        """
        Model 3: Coverage Assignment Identification.
        What zone is this player responsible for?
        """
        if scheme == "COVER_3":
            if defender['position'] == "CB":
                return "Deep Third"
            elif defender['position'] == "LB":
                return "Hook Curl"
        elif scheme == "COVER_2":
            if defender['position'] == "CB":
                return "Flat"
            elif defender['position'] == "S":
                return "Deep Half"
                
        return "Man"
