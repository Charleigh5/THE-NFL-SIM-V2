from sqlalchemy.orm import Session
from app.models.medical import BodyPart, InjuryEvent
from app.models.player import Player, InjuryStatus
import random

class MedicalService:
    def __init__(self, db: Session):
        self.db = db

    def initialize_body_health(self, player_id: int) -> BodyPart:
        """Create baseline health record for a player"""
        health = BodyPart(player_id=player_id)
        self.db.add(health)
        self.db.commit()
        return health

    def apply_game_wear(self, player: Player, snaps_played: int, position: str):
        """
        Calculate and apply wear & tear after a game.
        """
        if not player.body_health:
            self.initialize_body_health(player.id)

        health = player.body_health[0] # One-to-one list

        # Base wear calculation
        # RB/LB take more wear than WR/CB
        wear_multiplier = 1.0
        if position in ["RB", "LB", "DT", "OL"]:
            wear_multiplier = 1.5
        elif position in ["QB", "K", "P"]:
            wear_multiplier = 0.6

        wear_amount = (snaps_played * 0.15) * wear_multiplier

        # Apply to general wear
        health.general_wear = min(100, health.general_wear + wear_amount)

        # Randomly apply to specific body parts based on events (simulated)
        # e.g. 10% chance per 10 snaps to take a "hit" to a specific zone
        hits = snaps_played // 10
        for _ in range(hits):
            if random.random() < 0.3: # 30% chance of meaningful contact
                self._apply_hit_damage(health, position)

        self.db.commit()

    def _apply_hit_damage(self, health: BodyPart, position: str):
        """Logic to distribute damage to body parts"""
        part = random.choice(["head", "torso", "right_arm", "left_arm", "right_leg", "left_leg"])
        damage = random.uniform(0.5, 3.0) # Small micro-tears

        if part == "head":
            health.head_health = max(0, health.head_health - damage)
        elif part == "torso":
            health.torso_health = max(0, health.torso_health - damage)
        elif part == "right_arm":
            health.right_arm_health = max(0, health.right_arm_health - damage)
        elif part == "right_leg":
            health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty

    def process_weekly_recovery(self, player_id: int):
        """
        Recover health based on medical staff quality and rest.
        """
        player = self.db.query(Player).filter(Player.id == player_id).first()
        if not player or not player.body_health:
            return

        health = player.body_health[0]

        # Recovery rate
        recovery_rate = 5.0 # Base
        # Add modifier for Team Medical Staff (if we have access to team)

        health.general_wear = max(0, health.general_wear - recovery_rate * 2)
        health.right_leg_health = min(100, health.right_leg_health + recovery_rate)
        health.left_leg_health = min(100, health.left_leg_health + recovery_rate)
        # ... repeat for all parts

        self.db.commit()
