import math

class CollisionSystem:
    @staticmethod
    def resolve_tackle(runner_mass: float, runner_velocity: float, defender_mass: float, defender_velocity: float, angle_impact: float = 0.0) -> dict:
        """
        Physics-based tackle resolution using Momentum (p=mv).
        """
        # Momentum p = mv
        p_runner = runner_mass * runner_velocity
        p_defender = defender_mass * defender_velocity
        
        # Impact Force (Simplified Impulse)
        # Angle impact reduces effective defender momentum (0 = head on, 90 = side swipe)
        effective_p_defender = p_defender * math.cos(math.radians(angle_impact))
        
        impact_force = p_runner - effective_p_defender
        
        # Thresholds
        broken_tackle = False
        if impact_force > 50: # Arbitrary threshold for now
            broken_tackle = True
            
        return {
            "impact_force": round(impact_force, 2),
            "broken_tackle": broken_tackle,
            "runner_momentum_after": max(0, p_runner - effective_p_defender) if broken_tackle else 0
        }

class VisionAI:
    @staticmethod
    def calculate_safety_score(lane_vector: dict, defenders: list, blockers: list, dist_to_goal: float) -> float:
        """
        Calculate safety score for a running lane.
        Score = (GoalDist * W) - (DefProximity * W) + (BlockerLev * W)
        """
        score = 0.0
        
        # Distance to goal (closer is better, but we want to maximize gain, so maybe potential gain?)
        # Let's assume lane_vector points to a spot.
        
        # Proximity to Defenders (Negative)
        for d in defenders:
            dist = math.sqrt((d['x'] - lane_vector['x'])**2 + (d['y'] - lane_vector['y'])**2)
            if dist < 5:
                score -= (10 / (dist + 0.1)) # Inverse distance penalty
                
        # Blocker Leverage (Positive)
        for b in blockers:
            dist = math.sqrt((b['x'] - lane_vector['x'])**2 + (b['y'] - lane_vector['y'])**2)
            if dist < 3:
                score += 5
                
        return round(score, 2)
