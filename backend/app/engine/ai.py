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

class QuarterbackAI:
    @staticmethod
    def calculate_pressure_score(qb_pos: dict, defenders: list) -> float:
        """
        Calculates aggregate pressure score on the QB.

        Args:
            qb_pos: dict with 'x', 'y' coordinates
            defenders: list of dicts/objects with 'x', 'y', 'pass_rush_power', 'is_blocked'
        """
        total_pressure = 0.0

        for d in defenders:
            # Skip if blocked (assuming 'is_blocked' flag is set by blocking engine)
            if isinstance(d, dict) and d.get('is_blocked', False):
                continue
            elif hasattr(d, 'is_blocked') and d.is_blocked:
                continue

            # Get coordinates
            d_x = d['x'] if isinstance(d, dict) else getattr(d, 'x', 0)
            d_y = d['y'] if isinstance(d, dict) else getattr(d, 'y', 0)

            dist = math.sqrt((d_x - qb_pos['x'])**2 + (d_y - qb_pos['y'])**2)

            # Only count significant pressure within 7 yards
            if dist < 7.0:
                # Get pass rush power (default 50)
                pr_power = 50
                if isinstance(d, dict):
                    pr_power = d.get('pass_rush_power', 50)
                elif hasattr(d, 'pass_rush_power'):
                    pr_power = d.pass_rush_power

                # Formula: (Power / 50) * (10 / (Distance + 1))
                # Example: Power 90, Dist 2 yards -> 1.8 * 3.33 = 6.0 pressure
                power_factor = pr_power / 50.0
                proximity_factor = 10.0 / (dist + 1.0)

                total_pressure += power_factor * proximity_factor

        return round(total_pressure, 2)

    @staticmethod
    def check_pressure_response(qb, pressure_score: float) -> str:
        """
        Determines QB's reaction to pressure based on pocket presence.

        Returns:
            str: "NORMAL", "SCRAMBLE", "THROW_AWAY", or "OBLIVIOUS"
        """
        # Threshold for feeling pressure
        if pressure_score < 5.0:
            return "NORMAL"

        # QB Attributes
        pocket_presence = getattr(qb, 'pocket_presence', 50)
        scramble_willingness = getattr(qb, 'scramble_willingness', 50)

        # 1. Sense Check: Does the QB realize the pressure?
        # Higher pocket presence = better chance to sense
        # Base chance 50% + (Presence - 50)%
        sense_chance = 0.50 + ((pocket_presence - 50) / 100.0)
        sense_chance = max(0.1, min(0.95, sense_chance))

        import random
        if random.random() > sense_chance:
            return "OBLIVIOUS" # Doesn't see it coming, high sack risk

        # 2. Reaction: Scramble vs Throw Away
        # Based on scramble willingness
        scramble_chance = scramble_willingness / 100.0

        if random.random() < scramble_chance:
            return "SCRAMBLE"
        else:
            return "THROW_AWAY"

