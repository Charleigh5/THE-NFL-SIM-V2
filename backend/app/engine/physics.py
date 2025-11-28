import math
from pydantic import BaseModel

class Vector3(BaseModel):
    x: float
    y: float
    z: float

class BallPhysics:
    GRAVITY = 9.81
    AIR_DENSITY = 1.225 # kg/m^3 at sea level
    BALL_AREA = 0.014 # approx cross-sectional area of football in m^2
    BALL_MASS = 0.41 # kg

    @staticmethod
    def calculate_trajectory(v0: float, angle_deg: float, spin_rate: float = 0.0, spiral_efficiency: float = 1.0):
        """
        Calculate ball position over time.
        v0: Initial velocity (m/s)
        angle_deg: Launch angle in degrees
        spin_rate: RPM (affects stability)
        spiral_efficiency: 0.0 (Duck) to 1.0 (Perfect Spiral). Affects Drag Coefficient (Cd).
        """
        angle_rad = math.radians(angle_deg)
        vx = v0 * math.cos(angle_rad)
        vy = v0 * math.sin(angle_rad)
        
        # Drag Coefficient based on spiral
        # Tight spiral (1.0) -> Cd ~ 0.15
        # Wobbly duck (0.0) -> Cd ~ 0.6
        cd = 0.6 - (0.45 * spiral_efficiency)
        
        dt = 0.1 # Time step
        t = 0
        x, y = 0, 0
        trajectory = []
        
        while y >= 0:
            # Drag Force: Fd = 0.5 * rho * v^2 * Cd * A
            v = math.sqrt(vx**2 + vy**2)
            fd = 0.5 * BallPhysics.AIR_DENSITY * (v**2) * cd * BallPhysics.BALL_AREA
            
            # Drag Acceleration: a = F/m
            ad = fd / BallPhysics.BALL_MASS
            
            # Components of drag acceleration (opposing motion)
            ax = -(ad * (vx/v))
            ay = -BallPhysics.GRAVITY - (ad * (vy/v))
            
            # Update Velocity
            vx += ax * dt
            vy += ay * dt
            
            # Update Position
            x += vx * dt
            y += vy * dt
            
            t += dt
            trajectory.append({"t": round(t, 2), "x": round(x, 2), "y": round(y, 2)})
            
        return trajectory

    @staticmethod
    def apply_magnus_effect(velocity: Vector3, spin_vector: Vector3) -> Vector3:
        """
        Calculate Magnus force vector.
        F_magnus = S * (w x v)
        """
        # Simplified Magnus coefficient
        S = 0.0004 
        
        # Cross product of spin and velocity
        fx = S * (spin_vector.y * velocity.z - spin_vector.z * velocity.y)
        fy = S * (spin_vector.z * velocity.x - spin_vector.x * velocity.z)
        fz = S * (spin_vector.x * velocity.y - spin_vector.y * velocity.x)
        
        return Vector3(x=fx, y=fy, z=fz)
