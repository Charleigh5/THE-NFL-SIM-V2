"""
Attribute Interaction Engine

Set 3: Advanced Cross-Attribute Effects System

This engine models complex interactions between player attributes in head-to-head
matchups. Unlike simple skill comparisons, these interactions create emergent
gameplay outcomes that reward strategic roster construction.

Examples:
- QB Hard Count vs DL Discipline (pre-snap mind games)
- WR Release vs CB Press (line-of-scrimmage battle)
- OL Anchor vs DL First Step (pass protection)
- RB Patience vs LB Run Fit (running game chess match)

The system uses a context-aware calculation that considers:
1. Primary attribute matchup (main skill vs counter-skill)
2. Secondary modifiers (awareness, experience)
3. Situational context (weather, game situation, fatigue)
4. Trait synergies (traits can modify interaction outcomes)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class InteractionType(str, Enum):
    """Categories of attribute interactions."""
    PRE_SNAP = "PRE_SNAP"           # Mind games before the play
    LINE_OF_SCRIMMAGE = "LOS"       # Initial contact/release battles
    PASS_PROTECTION = "PASS_PROT"   # OL vs DL blocking battles
    ROUTE_VS_COVERAGE = "ROUTE_COV" # WR routes vs DB coverage
    RUN_GAME = "RUN_GAME"           # RB vision vs LB gap integrity
    BALL_CARRIER = "BALL_CARRIER"   # YAC battles after catch/handoff
    SPECIAL_TEAMS = "SPECIAL"       # Kicking game interactions
    LEADERSHIP = "LEADERSHIP"       # Team-wide influence effects


class InteractionOutcome(str, Enum):
    """Possible outcomes of an attribute interaction."""
    DOMINANT_WIN = "DOMINANT_WIN"   # Clear victory (>15 point differential)
    WIN = "WIN"                      # Standard win (5-15 point differential)
    SLIGHT_WIN = "SLIGHT_WIN"       # Marginal win (1-5 point differential)
    NEUTRAL = "NEUTRAL"              # Even matchup
    SLIGHT_LOSS = "SLIGHT_LOSS"     # Marginal loss
    LOSS = "LOSS"                    # Standard loss
    DOMINANT_LOSS = "DOMINANT_LOSS" # Clear loss


@dataclass
class InteractionResult:
    """Result of an attribute interaction calculation."""
    interaction_type: InteractionType
    outcome: InteractionOutcome
    differential: float              # Raw rating differential after modifiers
    winner_boost: float              # Bonus applied to winner
    loser_penalty: float             # Penalty applied to loser
    narrative: str                   # Human-readable description
    modifiers_applied: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "interaction_type": self.interaction_type.value,
            "outcome": self.outcome.value,
            "differential": round(self.differential, 2),
            "winner_boost": round(self.winner_boost, 2),
            "loser_penalty": round(self.loser_penalty, 2),
            "narrative": self.narrative,
            "modifiers_applied": self.modifiers_applied
        }


@dataclass
class InteractionDefinition:
    """Defines how two attributes interact."""
    name: str
    interaction_type: InteractionType
    attacker_attr: str              # Primary attribute of the aggressor
    defender_attr: str              # Primary attribute of the defender
    secondary_attrs: List[str]      # Supporting attributes (weighted 25% each)
    positions_attacker: List[str]   # Positions that can use this as attacker
    positions_defender: List[str]   # Positions that can use this as defender
    base_importance: float          # How impactful this interaction is (0.5-2.0)
    situational_modifiers: Dict[str, float]  # Context-based adjustments
    narrative_templates: Dict[str, str]      # Templates for outcome descriptions


class AttributeInteractionEngine:
    """
    Engine for calculating complex cross-attribute effects.

    This is the brain behind strategic matchups in the simulation.
    It goes beyond simple A vs B comparisons to model the nuanced
    rock-paper-scissors nature of football positioning.
    """

    # Interaction Catalog - All defined matchup types
    INTERACTION_CATALOG: Dict[str, InteractionDefinition] = {}

    def __init__(self, rng: Any = None):
        """
        Initialize the Attribute Interaction Engine.

        Args:
            rng: DeterministicRNG instance for reproducible randomness
        """
        self.rng = rng
        self._initialize_catalog()
        logger.info("AttributeInteractionEngine initialized with %d interactions",
                   len(self.INTERACTION_CATALOG))

    def _initialize_catalog(self) -> None:
        """Initialize all interaction definitions."""

        # ═══════════════════════════════════════════════════════════════════
        # PRE-SNAP INTERACTIONS
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["hard_count_vs_discipline"] = InteractionDefinition(
            name="Hard Count vs Discipline",
            interaction_type=InteractionType.PRE_SNAP,
            attacker_attr="awareness",      # QB's ability to sell the hard count
            defender_attr="discipline",     # DL's ability to stay patient
            secondary_attrs=["experience", "play_recognition"],
            positions_attacker=["QB"],
            positions_defender=["DE", "DT", "LB"],
            base_importance=1.5,            # High impact - free play potential
            situational_modifiers={
                "HOME": 0.10,               # QB gets crowd noise advantage
                "AWAY": -0.05,              # Harder to sell on the road
                "LOUD_STADIUM": 0.15,       # More effective in loud venues
                "PLAYOFF": -0.10,           # Defenders more focused in playoffs
                "4TH_QUARTER_CLOSE": -0.15, # High stakes = more discipline
            },
            narrative_templates={
                "DOMINANT_WIN": "{qb} masterfully draws {defender} offsides with an Oscar-worthy hard count!",
                "WIN": "{qb}'s hard count freezes {defender} just long enough.",
                "SLIGHT_WIN": "{defender} nearly jumps but just holds on.",
                "NEUTRAL": "Both sides are locked in - no pre-snap advantage.",
                "SLIGHT_LOSS": "{defender} times the snap perfectly.",
                "LOSS": "{defender} blows through unblocked, anticipating the snap.",
                "DOMINANT_LOSS": "{defender} reads the hard count and jumps the snap for a devastating hit!"
            }
        )

        self.INTERACTION_CATALOG["coverage_disguise_vs_pre_snap_read"] = InteractionDefinition(
            name="Coverage Disguise vs Pre-Snap Read",
            interaction_type=InteractionType.PRE_SNAP,
            attacker_attr="coverage_disguise",
            defender_attr="awareness",
            secondary_attrs=["experience", "play_recognition"],
            positions_attacker=["LB", "S"],
            positions_defender=["QB"],
            base_importance=1.3,
            situational_modifiers={
                "3RD_DOWN": 0.20,           # More complex coverages on 3rd
                "RED_ZONE": 0.15,           # Condensed field = more deception
                "2_MINUTE": -0.10,          # Less time for complex disguises
            },
            narrative_templates={
                "DOMINANT_WIN": "{defender} shows Tampa 2 but drops into a perfect trap coverage!",
                "WIN": "{defender}'s disguise creates hesitation in the pocket.",
                "SLIGHT_WIN": "The coverage look is slightly misleading.",
                "NEUTRAL": "{qb} reads the defense correctly.",
                "SLIGHT_LOSS": "{qb} sees through the disguise.",
                "LOSS": "{qb} correctly identifies the coverage and audibles to the perfect play.",
                "DOMINANT_LOSS": "{qb} reads it like a book, finding the coverage hole immediately!"
            }
        )

        # ═══════════════════════════════════════════════════════════════════
        # LINE OF SCRIMMAGE INTERACTIONS
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["wr_release_vs_cb_press"] = InteractionDefinition(
            name="WR Release vs CB Press",
            interaction_type=InteractionType.LINE_OF_SCRIMMAGE,
            attacker_attr="release",
            defender_attr="press",
            secondary_attrs=["agility", "strength", "speed"],
            positions_attacker=["WR", "TE"],
            positions_defender=["CB", "S"],
            base_importance=1.4,
            situational_modifiers={
                "RAIN": -0.15,              # Slippery footing hurts release
                "SNOW": -0.20,              # Even worse
                "WIND": 0.05,               # Receiver might use wind for leverage
                "MAN_COVERAGE": 0.20,       # Press more impactful in man
                "ZONE": -0.10,              # Less direct matchup importance
            },
            narrative_templates={
                "DOMINANT_WIN": "{wr} destroys {cb} with a filthy release - untouched into the route!",
                "WIN": "{wr} wins off the line cleanly.",
                "SLIGHT_WIN": "{wr} fights through contact and gets into the route.",
                "NEUTRAL": "Physical battle at the line - neither gains advantage.",
                "SLIGHT_LOSS": "{cb}'s jam disrupts the timing.",
                "LOSS": "{cb} reroutes {wr} significantly.",
                "DOMINANT_LOSS": "{cb} absolutely smothers {wr} at the line - route is dead on arrival!"
            }
        )

        self.INTERACTION_CATALOG["te_block_release_vs_lb_coverage"] = InteractionDefinition(
            name="TE Block-Release vs LB Coverage",
            interaction_type=InteractionType.LINE_OF_SCRIMMAGE,
            attacker_attr="blocking_tenacity",  # Fake the block, then release
            defender_attr="play_recognition",
            secondary_attrs=["agility", "route_running", "awareness"],
            positions_attacker=["TE"],
            positions_defender=["LB"],
            base_importance=1.2,
            situational_modifiers={
                "PLAY_ACTION": 0.25,        # PA sells the block
                "GOAL_LINE": -0.10,         # Less room to work
            },
            narrative_templates={
                "DOMINANT_WIN": "{te} sells the block perfectly and slips out wide open!",
                "WIN": "{te} releases cleanly into the pattern.",
                "SLIGHT_WIN": "{lb} hesitates just enough for {te} to get separation.",
                "NEUTRAL": "{lb} stays with {te} through the release.",
                "SLIGHT_LOSS": "{lb} reads the play and sticks with {te}.",
                "LOSS": "{lb} is all over {te} from the snap.",
                "DOMINANT_LOSS": "{lb} blows up the play, denying any release!"
            }
        )

        # ═══════════════════════════════════════════════════════════════════
        # PASS PROTECTION INTERACTIONS
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["ol_anchor_vs_dl_first_step"] = InteractionDefinition(
            name="OL Anchor vs DL First Step",
            interaction_type=InteractionType.PASS_PROTECTION,
            attacker_attr="first_step",
            defender_attr="anchor",
            secondary_attrs=["strength", "agility", "pass_block", "pass_rush_power"],
            positions_attacker=["DE", "DT"],
            positions_defender=["OT", "OG", "C"],
            base_importance=1.8,            # Critical for pass protection
            situational_modifiers={
                "4TH_QUARTER": 0.10,        # DL gets boost from fatigue
                "LONG_DRIVE": 0.15,         # OL tiring = worse anchor
                "ROAD": 0.05,               # Crowd noise helps timing
                "RAIN": -0.10,              # Slippery = worse first step
            },
            narrative_templates={
                "DOMINANT_WIN": "{dl} explodes off the line and is in the backfield instantly!",
                "WIN": "{dl} wins the edge with a quick get-off.",
                "SLIGHT_WIN": "{dl} gains a half-step advantage.",
                "NEUTRAL": "Stalemate at the point of attack.",
                "SLIGHT_LOSS": "{ol} absorbs the rush and holds ground.",
                "LOSS": "{ol} stonewalls {dl} with perfect technique.",
                "DOMINANT_LOSS": "{ol} pancakes {dl} into the turf - no pass rush at all!"
            }
        )

        self.INTERACTION_CATALOG["ol_discipline_vs_dl_inside_move"] = InteractionDefinition(
            name="OL Discipline vs DL Inside Counter",
            interaction_type=InteractionType.PASS_PROTECTION,
            attacker_attr="pass_rush_finesse",
            defender_attr="discipline",
            secondary_attrs=["agility", "awareness", "pass_block"],
            positions_attacker=["DE", "DT"],
            positions_defender=["OT", "OG", "C"],
            base_importance=1.5,
            situational_modifiers={
                "3RD_AND_LONG": 0.15,       # Rushers more creative
                "DROP_BACK_PASS": 0.10,     # More time for counters
                "QUICK_PASS": -0.20,        # No time for counter moves
            },
            narrative_templates={
                "DOMINANT_WIN": "{dl} uses a devastating swim-rip combo to blow by {ol}!",
                "WIN": "{dl}'s counter move catches {ol} off balance.",
                "SLIGHT_WIN": "{dl} creates a rushing lane with a flashy move.",
                "NEUTRAL": "{ol} mirrors {dl}'s move effectively.",
                "SLIGHT_LOSS": "{ol} recovers nicely from the initial move.",
                "LOSS": "{ol} reads the counter and stays in front.",
                "DOMINANT_LOSS": "{ol} bats away the move and drives {dl} into the ground!"
            }
        )

        self.INTERACTION_CATALOG["rb_chip_vs_blitz_timing"] = InteractionDefinition(
            name="RB Chip Block vs LB Blitz Timing",
            interaction_type=InteractionType.PASS_PROTECTION,
            attacker_attr="blitz_timing",
            defender_attr="pass_pro_rating",
            secondary_attrs=["awareness", "speed", "strength"],
            positions_attacker=["LB"],
            positions_defender=["RB", "TE"],
            base_importance=1.3,
            situational_modifiers={
                "MAX_PROTECT": 0.25,        # RB committed to blocking
                "HOT_ROUTE": -0.15,         # RB releasing, less committed
            },
            narrative_templates={
                "DOMINANT_WIN": "{lb} times the blitz perfectly and flies by {rb} untouched!",
                "WIN": "{lb} gets a free run at the QB.",
                "SLIGHT_WIN": "{rb}'s chip slows {lb} but doesn't stop them.",
                "NEUTRAL": "{rb} and {lb} collide - both affected.",
                "SLIGHT_LOSS": "{rb} gets a solid chip on {lb}.",
                "LOSS": "{rb} stonewalls {lb} completely.",
                "DOMINANT_LOSS": "{rb} delivers a devastating chip that sends {lb} to the turf!"
            }
        )

        # ═══════════════════════════════════════════════════════════════════
        # ROUTE VS COVERAGE INTERACTIONS
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["route_running_vs_man_coverage"] = InteractionDefinition(
            name="Route Running vs Man Coverage",
            interaction_type=InteractionType.ROUTE_VS_COVERAGE,
            attacker_attr="route_running",
            defender_attr="man_coverage",
            secondary_attrs=["speed", "agility", "awareness"],
            positions_attacker=["WR", "TE", "RB"],
            positions_defender=["CB", "S", "LB"],
            base_importance=1.6,
            situational_modifiers={
                "CONCEPT_DEEP": 0.10,       # More time for route to develop
                "CONCEPT_SHORT": -0.10,     # Less separation opportunity
                "PRESS": -0.15,             # Already calculated in LOS
                "OFF_COVERAGE": 0.10,       # More room to work
            },
            narrative_templates={
                "DOMINANT_WIN": "{wr} runs a clinic on {cb} - wide open by 5 yards!",
                "WIN": "{wr} creates clear separation at the break.",
                "SLIGHT_WIN": "{wr} gains a step at the cut.",
                "NEUTRAL": "{cb} is stride for stride with {wr}.",
                "SLIGHT_LOSS": "{cb} anticipates the break and closes.",
                "LOSS": "{cb} blankets {wr} throughout the route.",
                "DOMINANT_LOSS": "{cb} jumps the route for an interception opportunity!"
            }
        )

        self.INTERACTION_CATALOG["ball_tracking_vs_throw_placement"] = InteractionDefinition(
            name="DB Ball Tracking vs QB Throw Placement",
            interaction_type=InteractionType.ROUTE_VS_COVERAGE,
            attacker_attr="throw_accuracy_mid",  # Will be dynamic based on depth
            defender_attr="ball_tracking",
            secondary_attrs=["awareness", "speed", "catching"],
            positions_attacker=["QB"],
            positions_defender=["CB", "S"],
            base_importance=1.4,
            situational_modifiers={
                "SUN_IN_EYES": 0.15,        # DB has trouble tracking
                "NIGHT_GAME": -0.05,        # Lighting more consistent
                "WIND": 0.20,               # Ball tracking harder in wind
            },
            narrative_templates={
                "DOMINANT_WIN": "{qb} throws a perfect back-shoulder fade - DB has no chance!",
                "WIN": "The ball placement puts {db} in a trailing position.",
                "SLIGHT_WIN": "Good throw placement, but {db} nearly adjusts.",
                "NEUTRAL": "Both the throw and coverage are contested.",
                "SLIGHT_LOSS": "{db} tracks the ball well and is in position.",
                "LOSS": "{db} reads the throw and makes a play on the ball.",
                "DOMINANT_LOSS": "{db} high-points the ball for an incredible interception!"
            }
        )

        # ═══════════════════════════════════════════════════════════════════
        # RUN GAME INTERACTIONS
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["rb_patience_vs_lb_run_fit"] = InteractionDefinition(
            name="RB Patience vs LB Run Fit",
            interaction_type=InteractionType.RUN_GAME,
            attacker_attr="patience",
            defender_attr="run_fit",
            secondary_attrs=["awareness", "speed", "agility", "play_recognition"],
            positions_attacker=["RB"],
            positions_defender=["LB"],
            base_importance=1.5,
            situational_modifiers={
                "INSIDE_RUN": 0.10,         # Patience more valuable inside
                "OUTSIDE_RUN": -0.10,       # Speed more important outside
                "GOAL_LINE": -0.20,         # No room for patience
            },
            narrative_templates={
                "DOMINANT_WIN": "{rb} waits for the hole to develop, then explodes through!",
                "WIN": "{rb}'s patience allows blockers to seal the lane.",
                "SLIGHT_WIN": "{rb} makes a subtle cut to find daylight.",
                "NEUTRAL": "Both {rb} and {lb} in position - contested yards.",
                "SLIGHT_LOSS": "{lb} fills the gap before {rb} can react.",
                "LOSS": "{lb} is in the hole immediately.",
                "DOMINANT_LOSS": "{lb} reads it perfectly and blows up the play in the backfield!"
            }
        )

        self.INTERACTION_CATALOG["ol_pull_vs_dl_gap_integrity"] = InteractionDefinition(
            name="OL Pull Speed vs DL Gap Integrity",
            interaction_type=InteractionType.RUN_GAME,
            attacker_attr="pull_speed",
            defender_attr="gap_integrity",
            secondary_attrs=["speed", "agility", "run_block", "block_shed"],
            positions_attacker=["OG", "C"],
            positions_defender=["DE", "DT", "LB"],
            base_importance=1.4,
            situational_modifiers={
                "POWER_SCHEME": 0.15,       # Pull is central to the play
                "ZONE_SCHEME": -0.10,       # Less pulling in zone
                "TRAP": 0.20,               # Misdirection helps the pull
            },
            narrative_templates={
                "DOMINANT_WIN": "{ol} gets out and creates a massive lane - convoy blocking!",
                "WIN": "{ol} kicks out the edge defender perfectly.",
                "SLIGHT_WIN": "{ol} gets enough to spring the runner.",
                "NEUTRAL": "{dl} and {ol} meet at the point of attack.",
                "SLIGHT_LOSS": "{dl} stays in lane and forces a cut.",
                "LOSS": "{dl} sheds the block and makes the tackle.",
                "DOMINANT_LOSS": "{dl} blows through the pull and stuffs the play!"
            }
        )

        # ═══════════════════════════════════════════════════════════════════
        # BALL CARRIER INTERACTIONS (YAC)
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["juke_vs_tackle"] = InteractionDefinition(
            name="Ball Carrier Jukes vs Open Field Tackle",
            interaction_type=InteractionType.BALL_CARRIER,
            attacker_attr="juke_efficiency",
            defender_attr="tackle",
            secondary_attrs=["agility", "speed", "awareness"],
            positions_attacker=["RB", "WR"],
            positions_defender=["CB", "S", "LB"],
            base_importance=1.3,
            situational_modifiers={
                "OPEN_FIELD": 0.20,         # More room for moves
                "SIDELINE": -0.15,          # Less room to operate
                "FATIGUE_HIGH": 0.15,       # Tackler more likely to miss
            },
            narrative_templates={
                "DOMINANT_WIN": "{bc} puts {defender} on skates with a filthy juke!",
                "WIN": "{bc} makes {defender} miss in space.",
                "SLIGHT_WIN": "{bc} spins out of the tackle attempt.",
                "NEUTRAL": "{defender} slows {bc} but doesn't bring them down.",
                "SLIGHT_LOSS": "{defender} wraps up but {bc} falls forward.",
                "LOSS": "Solid open field tackle by {defender}.",
                "DOMINANT_LOSS": "{defender} delivers a huge hit and forces a fumble!"
            }
        )

        # ═══════════════════════════════════════════════════════════════════
        # LEADERSHIP/TEAM INTERACTIONS
        # ═══════════════════════════════════════════════════════════════════

        self.INTERACTION_CATALOG["field_general_influence"] = InteractionDefinition(
            name="Field General Leadership Boost",
            interaction_type=InteractionType.LEADERSHIP,
            attacker_attr="awareness",      # QB's awareness creates the boost
            defender_attr="awareness",      # Opposition awareness resists
            secondary_attrs=["experience"],
            positions_attacker=["QB"],
            positions_defender=["LB"],      # Defensive captain counters
            base_importance=1.0,
            situational_modifiers={
                "HOME": 0.10,
                "LEAD": 0.15,
                "TRAILING_LATE": -0.20,
            },
            narrative_templates={
                "DOMINANT_WIN": "{qb} has the offense humming - everyone is on the same page!",
                "WIN": "{qb}'s leadership keeps the offense composed.",
                "SLIGHT_WIN": "The offense shows good execution.",
                "NEUTRAL": "Both units are playing disciplined football.",
                "SLIGHT_LOSS": "The defense's intensity is disrupting rhythm.",
                "LOSS": "{lb} has the defense playing with fire.",
                "DOMINANT_LOSS": "The defense is swarming - offense can't get anything going!"
            }
        )

    def calculate_interaction(
        self,
        interaction_name: str,
        attacker: Any,
        defender: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> InteractionResult:
        """
        Calculate the result of an attribute interaction.

        Args:
            interaction_name: Key from INTERACTION_CATALOG
            attacker: Player object with attributes (offense/aggressor role)
            defender: Player object with attributes (defense/resistance role)
            context: Game situation modifiers

        Returns:
            InteractionResult with calculated outcome
        """
        if interaction_name not in self.INTERACTION_CATALOG:
            logger.warning(f"Unknown interaction: {interaction_name}")
            return self._create_neutral_result(interaction_name)

        definition = self.INTERACTION_CATALOG[interaction_name]
        context = context or {}

        # Step 1: Get primary attributes
        attacker_primary = getattr(attacker, definition.attacker_attr, 50)
        defender_primary = getattr(defender, definition.defender_attr, 50)

        # Step 2: Calculate secondary attribute contributions (25% weight each, max 2)
        attacker_secondary_bonus = 0.0
        defender_secondary_bonus = 0.0

        for i, attr in enumerate(definition.secondary_attrs[:2]):
            attacker_val = getattr(attacker, attr, 50)
            defender_val = getattr(defender, attr, 50)

            attacker_secondary_bonus += (attacker_val - 50) * 0.25
            defender_secondary_bonus += (defender_val - 50) * 0.25

        # Step 3: Calculate situational modifiers
        situational_modifier = 0.0
        modifiers_applied = {}

        for situation, modifier in definition.situational_modifiers.items():
            if context.get(situation.lower(), False) or context.get(situation, False):
                situational_modifier += modifier
                modifiers_applied[situation] = modifier

        # Step 4: Experience modifier (veterans have edge in complex interactions)
        attacker_exp = getattr(attacker, 'experience', 0)
        defender_exp = getattr(defender, 'experience', 0)
        experience_modifier = (attacker_exp - defender_exp) * 0.5
        experience_modifier = max(-5, min(5, experience_modifier))

        if abs(experience_modifier) > 0:
            modifiers_applied["EXPERIENCE"] = experience_modifier

        # Step 5: Random variance (if RNG available)
        variance = 0.0
        if self.rng:
            # -3 to +3 variance
            variance = (self.rng.random() * 6) - 3
            modifiers_applied["VARIANCE"] = round(variance, 2)

        # Step 6: Calculate final differential
        attacker_total = (
            attacker_primary +
            attacker_secondary_bonus +
            (situational_modifier * 10) +  # Scale situational modifiers
            experience_modifier +
            variance
        )

        defender_total = (
            defender_primary +
            defender_secondary_bonus
        )

        raw_differential = attacker_total - defender_total

        # Apply base importance as a multiplier on the effects
        scaled_differential = raw_differential * definition.base_importance

        # Step 7: Determine outcome
        outcome = self._differential_to_outcome(raw_differential)

        # Step 8: Calculate boosts/penalties based on outcome and importance
        winner_boost, loser_penalty = self._calculate_effects(
            outcome,
            abs(scaled_differential),
            definition.base_importance
        )

        # Step 9: Generate narrative
        narrative = self._generate_narrative(
            definition,
            outcome,
            attacker,
            defender
        )

        return InteractionResult(
            interaction_type=definition.interaction_type,
            outcome=outcome,
            differential=raw_differential,
            winner_boost=winner_boost,
            loser_penalty=loser_penalty,
            narrative=narrative,
            modifiers_applied=modifiers_applied
        )

    def _differential_to_outcome(self, differential: float) -> InteractionOutcome:
        """Convert a raw differential to an outcome enum."""
        if differential >= 15:
            return InteractionOutcome.DOMINANT_WIN
        elif differential >= 8:
            return InteractionOutcome.WIN
        elif differential >= 2:
            return InteractionOutcome.SLIGHT_WIN
        elif differential >= -2:
            return InteractionOutcome.NEUTRAL
        elif differential >= -8:
            return InteractionOutcome.SLIGHT_LOSS
        elif differential >= -15:
            return InteractionOutcome.LOSS
        else:
            return InteractionOutcome.DOMINANT_LOSS

    def _calculate_effects(
        self,
        outcome: InteractionOutcome,
        scaled_diff: float,
        importance: float
    ) -> Tuple[float, float]:
        """
        Calculate winner boost and loser penalty based on outcome.

        Returns:
            Tuple of (winner_boost, loser_penalty)
        """
        base_effect = min(scaled_diff * 0.2, 15.0)  # Cap at 15 point effect

        effects = {
            InteractionOutcome.DOMINANT_WIN: (base_effect, base_effect * 0.5),
            InteractionOutcome.WIN: (base_effect * 0.7, base_effect * 0.3),
            InteractionOutcome.SLIGHT_WIN: (base_effect * 0.3, base_effect * 0.1),
            InteractionOutcome.NEUTRAL: (0.0, 0.0),
            InteractionOutcome.SLIGHT_LOSS: (0.0, base_effect * 0.3),
            InteractionOutcome.LOSS: (0.0, base_effect * 0.7),
            InteractionOutcome.DOMINANT_LOSS: (0.0, base_effect),
        }

        return effects.get(outcome, (0.0, 0.0))

    def _generate_narrative(
        self,
        definition: InteractionDefinition,
        outcome: InteractionOutcome,
        attacker: Any,
        defender: Any
    ) -> str:
        """Generate a human-readable narrative for the interaction."""
        template = definition.narrative_templates.get(outcome.value, "")

        if not template:
            return f"{outcome.value} in {definition.name}"

        # Get player names
        attacker_name = getattr(attacker, 'last_name', None) or \
                       getattr(attacker, 'name', 'Attacker')
        defender_name = getattr(defender, 'last_name', None) or \
                       getattr(defender, 'name', 'Defender')

        # Replace template placeholders
        narrative = template

        # Position-based replacements
        for pos in ["qb", "wr", "te", "rb", "ol", "dl", "lb", "cb", "db", "s", "bc"]:
            if f"{{{pos}}}" in narrative.lower():
                if pos in ["qb", "wr", "te", "rb", "ol", "bc"]:
                    narrative = narrative.replace(f"{{{pos}}}", attacker_name)
                else:
                    narrative = narrative.replace(f"{{{pos}}}", defender_name)

        # Generic replacements
        narrative = narrative.replace("{attacker}", attacker_name)
        narrative = narrative.replace("{defender}", defender_name)

        return narrative

    def _create_neutral_result(self, interaction_name: str) -> InteractionResult:
        """Create a neutral result for unknown interactions."""
        return InteractionResult(
            interaction_type=InteractionType.PRE_SNAP,
            outcome=InteractionOutcome.NEUTRAL,
            differential=0.0,
            winner_boost=0.0,
            loser_penalty=0.0,
            narrative=f"Unknown interaction: {interaction_name}",
            modifiers_applied={}
        )

    def get_all_interactions(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all available interactions."""
        return {
            name: {
                "name": defn.name,
                "type": defn.interaction_type.value,
                "attacker_attr": defn.attacker_attr,
                "defender_attr": defn.defender_attr,
                "importance": defn.base_importance,
                "positions_attacker": defn.positions_attacker,
                "positions_defender": defn.positions_defender
            }
            for name, defn in self.INTERACTION_CATALOG.items()
        }

    def get_interactions_for_situation(
        self,
        play_type: str,
        phase: str
    ) -> List[str]:
        """
        Get relevant interactions for a given play type and phase.

        Args:
            play_type: "PASS" or "RUN"
            phase: "PRE_SNAP", "SNAP", "POST_SNAP"

        Returns:
            List of interaction names applicable to the situation
        """
        relevant = []

        phase_map = {
            "PRE_SNAP": [InteractionType.PRE_SNAP],
            "SNAP": [InteractionType.LINE_OF_SCRIMMAGE, InteractionType.PASS_PROTECTION],
            "POST_SNAP": [
                InteractionType.ROUTE_VS_COVERAGE,
                InteractionType.RUN_GAME,
                InteractionType.BALL_CARRIER
            ]
        }

        target_types = phase_map.get(phase, [])

        for name, defn in self.INTERACTION_CATALOG.items():
            if defn.interaction_type in target_types:
                # Further filter by play type if needed
                if play_type == "PASS" and defn.interaction_type == InteractionType.RUN_GAME:
                    continue
                if play_type == "RUN" and defn.interaction_type == InteractionType.PASS_PROTECTION:
                    continue

                relevant.append(name)

        return relevant

    def batch_calculate_interactions(
        self,
        matchups: List[Tuple[str, Any, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> List[InteractionResult]:
        """
        Calculate multiple interactions at once.

        Args:
            matchups: List of (interaction_name, attacker, defender) tuples
            context: Shared context for all calculations

        Returns:
            List of InteractionResult objects
        """
        results = []
        for interaction_name, attacker, defender in matchups:
            result = self.calculate_interaction(
                interaction_name,
                attacker,
                defender,
                context
            )
            results.append(result)

        return results


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS FOR INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

def apply_interaction_to_play(
    engine: AttributeInteractionEngine,
    play_context: Dict[str, Any],
    key_matchups: List[Tuple[str, Any, Any]]
) -> Dict[str, Any]:
    """
    Apply attribute interactions to modify a play's outcome.

    Args:
        engine: AttributeInteractionEngine instance
        play_context: Current play state
        key_matchups: List of (interaction_name, attacker, defender) tuples

    Returns:
        Dictionary with aggregate modifiers to apply
    """
    results = engine.batch_calculate_interactions(key_matchups, play_context)

    aggregate = {
        "total_offense_boost": 0.0,
        "total_defense_boost": 0.0,
        "narratives": [],
        "dominant_events": [],
        "all_events": []
    }

    for result in results:
        if result.outcome in [InteractionOutcome.DOMINANT_WIN, InteractionOutcome.WIN,
                              InteractionOutcome.SLIGHT_WIN]:
            aggregate["total_offense_boost"] += result.winner_boost
        elif result.outcome in [InteractionOutcome.DOMINANT_LOSS, InteractionOutcome.LOSS,
                                InteractionOutcome.SLIGHT_LOSS]:
            aggregate["total_defense_boost"] += result.loser_penalty

        aggregate["narratives"].append(result.narrative)
        aggregate["all_events"].append(result.to_dict())

        if result.outcome in [InteractionOutcome.DOMINANT_WIN, InteractionOutcome.DOMINANT_LOSS]:
            aggregate["dominant_events"].append(result.to_dict())

    return aggregate
