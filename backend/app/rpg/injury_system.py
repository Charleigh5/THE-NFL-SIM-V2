from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from app.models.player import Player, InjuryStatus
from app.core.random_utils import DeterministicRNG
from app.core import injury_config as InjuryConfig
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

    # =========================================================================
    # NEW PROBABILITY MODEL METHODS (wrapping standalone functions)
    # =========================================================================

    def compute_play_injury_probability(
        self,
        player: Player,
        play_type: str = "STANDARD",
        fatigue_level: float = 0.0,
        medical_rating: int = 50,
    ) -> float:
        """
        Calculate injury probability for a specific play (class method).

        This wraps the standalone compute_play_injury_probability function
        for backward compatibility.
        """
        context = PlayContext(
            play_type=play_type,
            fatigue=fatigue_level,
            medical_staff_rating=medical_rating,
        )
        return compute_play_injury_probability(player, context, self.rng)

    def evaluate_post_play_injuries(
        self,
        play_context: Dict[str, Any],
        players_on_field: List[Player],
    ) -> List[Dict[str, Any]]:
        """
        Evaluate all players for injury after a play (class method).

        This wraps the standalone evaluate_post_play_injuries function
        for backward compatibility. Returns a list of dicts for API compatibility.
        """
        # Extract play type, considering sacked_player_id
        play_type = play_context.get("play_type", "STANDARD")
        sacked_player_id = play_context.get("sacked_player_id")

        results = []
        for player in players_on_field:
            # Use SACK play type for sacked player
            player_play_type = "SACK" if sacked_player_id == player.id else play_type

            context = PlayContext(
                play_type=player_play_type,
                fatigue=play_context.get("fatigue_level", 0.0),
                medical_staff_rating=play_context.get("medical_rating", 50),
            )

            # Calculate probability and check for injury
            prob = compute_play_injury_probability(player, context, self.rng)

            if self.rng.random() < prob:
                severity = generate_injury_severity(self.rng)
                injury_type, weeks = _determine_injury_details(severity, self.rng)

                toughness = get_player_toughness(player)
                has_ragknow = player_has_ragknow(player)
                can_play = InjuryConfig.can_play_through_injury(severity, toughness, has_ragknow)

                results.append({
                    "player_id": player.id,
                    "play_type": player_play_type,
                    "severity": severity,
                    "injury_type": injury_type,
                    "weeks_to_recovery": weeks,
                    "can_play_through": can_play,
                })

        return results

    def calculate_injured_performance_penalty(
        self,
        player: Player,
        has_ragknow: bool = False,
    ) -> Dict[str, int]:
        """
        Calculate performance penalties for playing through injury (class method).
        """
        severity = getattr(player, "injury_severity", 0)
        toughness = get_player_toughness(player)
        return calculate_injured_performance_penalty(severity, toughness, has_ragknow)

    def check_playing_injured_escalation(
        self,
        player: Player,
        has_ragknow: bool = False,
    ) -> bool:
        """
        Check if playing through injury causes it to worsen (class method).

        Returns True if injury escalated, False otherwise.
        Mutates player.injury_severity if escalation occurs.
        """
        severity = getattr(player, "injury_severity", 0)

        # Severity 8+ cannot be played through
        if severity >= 8:
            return False

        # Calculate escalation chance
        escalation_chance = InjuryConfig.INJURY_ESCALATION_BASE_CHANCE * severity
        if has_ragknow:
            escalation_chance *= 0.5

        if self.rng.random() < escalation_chance:
            increase = self.rng.randint(1, InjuryConfig.INJURY_ESCALATION_MAX_INCREASE)
            player.injury_severity = min(10, severity + increase)
            return True

        return False


# ============================================================================
# PLAY CONTEXT & INJURY EVENT DATACLASSES
# ============================================================================

@dataclass
class PlayContext:
    """
    Context information for a play, used for injury probability calculation.
    """
    play_type: str = "STANDARD"          # PASS_PLAY, RUN_PLAY, SACK, etc.
    fatigue: float = 0.0                  # Player's current fatigue (0-100)
    medical_staff_rating: int = 50        # Team's medical staff quality
    is_contact: bool = True               # Whether this was a contact play
    season: int = 0
    week: int = 0
    play_id: Optional[str] = None


@dataclass
class InjuryEvent:
    """
    Represents an injury that occurred during a play.
    """
    player_id: int
    severity: int                         # 1-10 severity scale
    injury_type: str = "Unknown"
    body_part: str = "Unknown"
    weeks_to_recovery: int = 0
    can_play_through: bool = False        # Based on toughness/Ragknow
    performance_penalties: Dict[str, int] = None

    def __post_init__(self):
        if self.performance_penalties is None:
            self.performance_penalties = {}


# ============================================================================
# CORE PROBABILITY FUNCTIONS
# ============================================================================

def compute_play_injury_probability(
    player: Player,
    play_context: PlayContext,
    rng: DeterministicRNG = None
) -> float:
    """
    Calculate injury probability for a specific play using multiplicative formula.

    Formula: Base × PlayType × Position × (Age × Durability × Fatigue × Medical)

    Args:
        player: The player to calculate injury probability for
        play_context: Context about the current play
        rng: Optional RNG for any stochastic elements

    Returns:
        Probability of injury (0.0 to 1.0)
    """
    # Base probability
    base = InjuryConfig.BASE_PLAY_INJURY_PROBABILITY

    # Play type multiplier
    play_type_mult = InjuryConfig.get_play_type_multiplier(play_context.play_type)

    # Position multiplier
    position = getattr(player, "position", "")
    position_mult = InjuryConfig.get_position_multiplier(position)

    # Player-specific factors
    age = getattr(player, "age", 25)
    age_mult = InjuryConfig.get_age_multiplier(age)

    durability = getattr(player, "injury_resistance", 70)
    durability_mult = InjuryConfig.get_durability_multiplier(durability)

    fatigue_mult = InjuryConfig.get_fatigue_multiplier(play_context.fatigue)

    medical_mult = InjuryConfig.get_medical_staff_multiplier(play_context.medical_staff_rating)

    # Combine all multipliers
    final_probability = (
        base *
        play_type_mult *
        position_mult *
        age_mult *
        durability_mult *
        fatigue_mult *
        medical_mult
    )

    # Cap at 95% maximum
    return min(0.95, max(0.0, final_probability))


def generate_injury_severity(rng: DeterministicRNG) -> int:
    """
    Generate an injury severity value (1-10) with weighted distribution.

    Distribution:
    - 1-3 (Minor): 60%
    - 4-7 (Moderate): 35%
    - 8-10 (Severe): 5%
    """
    roll = rng.random() if rng else random.random()

    if roll < 0.60:  # Minor
        return rng.randint(1, 3) if rng else random.randint(1, 3)
    elif roll < 0.95:  # Moderate
        return rng.randint(4, 7) if rng else random.randint(4, 7)
    else:  # Severe
        return rng.randint(8, 10) if rng else random.randint(8, 10)


def player_has_ragknow(player: Player) -> bool:
    """Check if a player has the Ragknow trait."""
    # Check active_traits list
    if hasattr(player, "active_traits") and "Ragknow" in getattr(player, "active_traits", []):
        return True
    # Check traits list
    if hasattr(player, "traits"):
        traits = getattr(player, "traits", [])
        for trait in traits:
            trait_name = getattr(trait, "name", trait) if not isinstance(trait, str) else trait
            if trait_name == "Ragknow":
                return True
    return False


def get_player_toughness(player: Player) -> int:
    """
    Get a player's effective toughness for injury play-through calculations.

    Uses injury_resistance as base with modifiers from age and traits.
    """
    base_toughness = getattr(player, "injury_resistance", 50)

    # Older players have more experience playing through pain
    age = getattr(player, "age", 25)
    if age >= 30:
        base_toughness += min(10, (age - 28) * 2)  # +2 per year over 28, max +10

    return min(100, max(0, base_toughness))


def calculate_injured_performance_penalty(
    severity: int,
    toughness: int = 50,
    has_ragknow: bool = False
) -> Dict[str, int]:
    """
    Calculate attribute penalties for playing through an injury.

    Args:
        severity: Injury severity (1-10)
        toughness: Player's toughness rating (0-100)
        has_ragknow: Whether player has the Ragknow trait

    Returns:
        Dictionary of attribute penalties (negative values)
    """
    # Ragknow ignores all penalties
    if has_ragknow:
        return {}

    # Get base penalties for this severity
    base_penalties = InjuryConfig.INJURY_PERFORMANCE_PENALTIES.get(severity, {})

    if not base_penalties:
        return {}

    # Calculate toughness reduction factor
    reduction_factor = InjuryConfig.calculate_toughness_penalty_reduction(toughness)

    # Apply reduction to each penalty
    adjusted_penalties = {}
    for stat, penalty in base_penalties.items():
        adjusted_penalty = int(penalty * reduction_factor)
        if adjusted_penalty != 0:
            adjusted_penalties[stat] = adjusted_penalty

    return adjusted_penalties


def apply_playing_injured_risk(
    player: Player,
    current_severity: int,
    rng: DeterministicRNG = None
) -> Optional[int]:
    """
    Check if playing through an injury causes it to worsen.

    Args:
        player: The injured player
        current_severity: Current injury severity (1-10)
        rng: Deterministic RNG for reproducibility

    Returns:
        New severity if injury worsened, None otherwise
    """
    # Severity 8+ cannot be played through
    if current_severity >= 8:
        return None

    # Calculate escalation chance: 2% per severity level
    escalation_chance = InjuryConfig.INJURY_ESCALATION_BASE_CHANCE * current_severity

    # Ragknow reduces escalation chance by 50%
    if player_has_ragknow(player):
        escalation_chance *= 0.5

    # Roll for escalation
    roll = rng.random() if rng else random.random()

    if roll < escalation_chance:
        # Injury worsened
        increase = rng.randint(1, InjuryConfig.INJURY_ESCALATION_MAX_INCREASE) if rng else random.randint(1, 2)
        new_severity = min(10, current_severity + increase)
        logger.info(f"Player {player.id} injury escalated from {current_severity} to {new_severity}")
        return new_severity

    return None


def evaluate_post_play_injuries(
    play_context: PlayContext,
    players_on_field: List[Player],
    rng: DeterministicRNG = None
) -> List[InjuryEvent]:
    """
    Evaluate all players on the field for potential injuries after a play.

    This function is called AFTER the play outcome is finalized to ensure
    simulation determinism - injuries do not affect the play in which they occur.

    Args:
        play_context: Context about the completed play
        players_on_field: List of players who participated in the play
        rng: Deterministic RNG for reproducibility

    Returns:
        List of InjuryEvent objects for any injuries that occurred
    """
    injuries = []
    injury_system = InjurySystem(seed=rng.randint(0, 1000000) if rng else None)

    for player in players_on_field:
        # Calculate injury probability
        probability = compute_play_injury_probability(player, play_context, rng)

        # Roll for injury
        roll = rng.random() if rng else random.random()

        if roll < probability:
            # Injury occurred!
            severity = generate_injury_severity(rng)

            # Check if player can play through
            toughness = get_player_toughness(player)
            has_ragknow = player_has_ragknow(player)
            can_play_through = InjuryConfig.can_play_through_injury(
                severity, toughness, has_ragknow
            )

            # Calculate performance penalties if playing through
            penalties = {}
            if can_play_through:
                penalties = calculate_injured_performance_penalty(
                    severity, toughness, has_ragknow
                )

            # Determine injury type and recovery time
            injury_type, weeks = _determine_injury_details(severity, rng)

            # Apply Ragknow recovery bonus
            if has_ragknow:
                weeks = int(weeks * InjuryConfig.RAGKNOW_RECOVERY_MULTIPLIER)

            injury_event = InjuryEvent(
                player_id=player.id,
                severity=severity,
                injury_type=injury_type,
                weeks_to_recovery=max(1, weeks),
                can_play_through=can_play_through,
                performance_penalties=penalties
            )

            injuries.append(injury_event)
            logger.info(
                f"Injury: Player {player.id} suffered {injury_type} "
                f"(severity {severity}), out {weeks} weeks. "
                f"Can play through: {can_play_through}"
            )

    return injuries


def _determine_injury_details(
    severity: int,
    rng: DeterministicRNG = None
) -> tuple:
    """
    Determine injury type and recovery weeks based on severity.

    Returns:
        Tuple of (injury_type: str, weeks_to_recovery: int)
    """
    if severity <= 3:
        injury_types = ["Minor Sprain", "Contusion", "Muscle Strain"]
        min_weeks, max_weeks = 1, 3
    elif severity <= 5:
        injury_types = ["Moderate Sprain", "Muscle Tear", "Hyperextension"]
        min_weeks, max_weeks = 2, 6
    elif severity <= 7:
        injury_types = ["Partial Ligament Tear", "Stress Fracture", "High Ankle Sprain"]
        min_weeks, max_weeks = 4, 10
    elif severity <= 9:
        injury_types = ["ACL Tear", "Complete Ligament Tear", "Fracture"]
        min_weeks, max_weeks = 8, 20
    else:
        injury_types = ["Severe ACL/MCL Tear", "Multiple Fractures", "Spinal Injury"]
        min_weeks, max_weeks = 16, 52

    # Select random injury type
    if rng:
        injury_type = injury_types[rng.randint(0, len(injury_types) - 1)]
        weeks = rng.randint(min_weeks, max_weeks)
    else:
        injury_type = random.choice(injury_types)
        weeks = random.randint(min_weeks, max_weeks)

    return injury_type, weeks


def apply_injury_event_to_player(player: Player, event: InjuryEvent, injury_system: InjurySystem = None):
    """
    Apply an InjuryEvent to a player's status.

    Args:
        player: The player to apply the injury to
        event: The injury event
        injury_system: Optional InjurySystem instance for recovery calculations
    """
    player.injury_severity = event.severity
    player.injury_type = event.injury_type
    player.weeks_to_recovery = event.weeks_to_recovery

    # Set status based on severity and can_play_through
    if event.can_play_through:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif event.severity <= 3:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif event.severity <= 7:
        player.injury_status = InjuryStatus.OUT
    else:
        player.injury_status = InjuryStatus.IR

    # Set recurrence risk
    player.injury_recurrence_risk = event.severity * 0.02

    logger.info(
        f"Applied injury to player {player.id}: {event.injury_type} "
        f"(severity {event.severity}), status: {player.injury_status.value}"
    )
