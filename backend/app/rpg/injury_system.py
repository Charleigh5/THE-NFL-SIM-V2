from app.models.player import Player, InjuryStatus
from app.core.random_utils import DeterministicRNG
import random
import logging

logger = logging.getLogger(__name__)

class InjurySystem:
    def __init__(self, seed: int = None):
        self.rng = DeterministicRNG(seed if seed is not None else random.randint(0, 1000000))

    def calculate_injury_risk_multiplier(self, training_staff_quality: int) -> float:
        """
        Calculate a risk multiplier based on training staff quality.
        Higher quality -> Lower risk.
        Quality 0 -> 1.2x
        Quality 50 -> 1.0x
        Quality 100 -> 0.8x
        """
        return 1.2 - (training_staff_quality / 100.0) * 0.4

    def apply_injury(self, player: Player, severity_roll: int, medical_rating: int = 50):
        """
        Apply an injury to a player based on a severity roll (0-100).
        Calculates severity (1-10), type, and recovery time.
        """
        # Calculate Severity (1-10)
        # 0-50: Minor (1-3)
        # 51-80: Moderate (4-7)
        # 81-100: Severe (8-10)

        if severity_roll <= 50:
            severity = self.rng.randint(1, 3)
            player.injury_type = "Minor Sprain" # Placeholder, could be more specific
            player.injury_status = InjuryStatus.QUESTIONABLE
        elif severity_roll <= 80:
            severity = self.rng.randint(4, 7)
            player.injury_type = "Muscle Tear"
            player.injury_status = InjuryStatus.OUT
        else:
            severity = self.rng.randint(8, 10)
            player.injury_type = "Major Fracture" # or Ligament Tear
            player.injury_status = InjuryStatus.IR

        player.injury_severity = severity

        # Calculate Recovery Weeks
        weeks = self.calculate_recovery_weeks(player, severity, medical_rating)
        player.weeks_to_recovery = weeks

        # Initial Recurrence Risk (Setback probability)
        # Higher severity = higher risk
        player.injury_recurrence_risk = severity * 0.02 # 2% per severity point initially (e.g. 20% for severity 10)

        logger.info(f"Player {player.id} injured: {player.injury_type} (Severity {severity}), Out for {weeks} weeks")

    def calculate_recovery_weeks(self, player: Player, severity: int, medical_rating: int = 50) -> int:
        """
        Calculate recovery time based on severity, age, and durability.
        """
        # Base weeks based on severity
        if severity <= 3:
            base_weeks = self.rng.randint(1, 4)
        elif severity <= 7:
            base_weeks = self.rng.randint(4, 12)
        else:
            base_weeks = self.rng.randint(12, 52)

        # Age Factor: Players over 30 recover slower
        age_factor = 1.0
        if player.age > 30:
            age_factor = 1.0 + ((player.age - 30) * 0.1) # +10% per year over 30

        # Durability Factor (Injury Resistance 0-100)
        # 100 resistance -> 0.5x time (Fast healer)
        # 50 resistance -> 1.0x time (Average)
        # 0 resistance -> 1.5x time (Slow healer)
        durability_factor = 1.5 - (player.injury_resistance / 100.0)

        final_weeks = int(base_weeks * age_factor * durability_factor)

        # Medical Staff Impact
        # Rating 0 -> 1.2x time
        # Rating 50 -> 1.0x time
        # Rating 100 -> 0.8x time
        medical_factor = 1.2 - (medical_rating / 100.0) * 0.4
        final_weeks = int(final_weeks * medical_factor)

        return max(1, final_weeks)

    def process_recovery_step(self, player: Player, medical_rating: int = 50):
        """
        Process one week of recovery.
        Check for setbacks.
        """
        if player.injury_status == InjuryStatus.ACTIVE:
            return

        # Check Setback
        # Medical rating reduces setback chance
        # Rating 100 -> 0.5x risk
        # Rating 0 -> 1.0x risk
        risk_modifier = 1.0 - (medical_rating / 200.0)

        if self.check_setback(player, risk_modifier):
            # Setback!
            added_weeks = self.rng.randint(1, 4)
            player.weeks_to_recovery += added_weeks
            # Increase recurrence risk for future checks
            player.injury_recurrence_risk += 0.05
            logger.info(f"Player {player.id} suffered a setback in rehab. Added {added_weeks} weeks.")
            return

        # Progress Recovery
        if player.weeks_to_recovery > 0:
            player.weeks_to_recovery -= 1

        if player.weeks_to_recovery <= 0:
            self.clear_injury(player)

    def check_setback(self, player: Player, risk_modifier: float = 1.0) -> bool:
        """
        Check if a setback occurs based on recurrence risk.
        """
        if player.weeks_to_recovery <= 0:
            return False

        roll = self.rng.random() # 0.0 to 1.0
        return roll < (player.injury_recurrence_risk * risk_modifier)

    def clear_injury(self, player: Player):
        """
        Clear injury status and apply potential permanent attribute degradation.
        """
        # Apply Permanent Damage
        self.apply_permanent_damage(player)

        player.injury_status = InjuryStatus.ACTIVE
        player.injury_type = None
        player.injury_severity = 0
        player.injury_recurrence_risk = 0.0
        logger.info(f"Player {player.id} recovered from injury.")

    def apply_permanent_damage(self, player: Player):
        """
        Degrade attributes based on severity and age.
        """
        # Only severe injuries or older players risk permanent damage
        risk_threshold = 7
        if player.age > 32:
            risk_threshold = 5

        if player.injury_severity >= risk_threshold:
            # Chance of degradation
            # Higher severity = higher chance
            chance = (player.injury_severity - risk_threshold + 1) * 0.2 # 20% per point over threshold

            if self.rng.random() < chance:
                logger.info(f"Player {player.id} suffered permanent attribute degradation.")
                # Determine stats to drop based on position or general physicals
                stats_to_drop = ["speed", "agility", "acceleration", "strength"]

                # Drop 1-3 stats
                num_stats = self.rng.randint(1, 3)
                for _ in range(num_stats):
                    stat = self.rng.choice(stats_to_drop)
                    current = getattr(player, stat)
                    # Drop by 1-3 points
                    drop = self.rng.randint(1, 3)
                    new_val = max(40, current - drop)
                    setattr(player, stat, new_val)

                # Also drop injury resistance permanently
                player.injury_resistance = max(0, player.injury_resistance - 5)
