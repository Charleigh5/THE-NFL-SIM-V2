"""
Player Archetype System
=======================
7 distinct player archetypes with unique abilities and development bonuses.

CITATION: ENHANCEMENT_REFERENCE.md - RPG Expansion - Player Archetypes

Archetypes:
1. The Field General (QB) - +Leadership, +Pre-snap Reads
2. The Sorcerer (QB) - +Improvisation, +Arm Talent
3. The Alpha Dog (WR/CB) - +Aggression, Demoralize ability
4. The Weapon (RB/WR) - +Versatility, Swiss Army knife
5. The Freak (Edge/LB) - +Physical traits, Fast development
6. The Technician (OL/DL) - +Consistency, -Mental errors
7. The Workhorse (RB) - +Durability, +Carry volume
"""

from dataclasses import dataclass
from enum import Enum


class PlayerArchetype(str, Enum):
    """7 core player archetypes."""
    FIELD_GENERAL = "FIELD_GENERAL"   # QB: Cerebral leader
    SORCERER = "SORCERER"              # QB: Magic arm, improviser
    ALPHA_DOG = "ALPHA_DOG"            # WR/CB: Dominant competitor
    WEAPON = "WEAPON"                  # RB/WR: Versatile threat
    FREAK = "FREAK"                    # EDGE/LB: Physical marvel
    TECHNICIAN = "TECHNICIAN"          # OL/DL: Precise craftsman
    WORKHORSE = "WORKHORSE"            # RB: Iron man


@dataclass
class ArchetypeDefinition:
    """Definition of an archetype with all its attributes."""
    name: str
    display_name: str
    description: str
    icon: str
    primary_positions: list[str]
    secondary_positions: list[str]
    stat_bonuses: dict[str, int]      # +/- to ratings
    xp_bonuses: dict[str, float]      # Multipliers for skill categories
    special_abilities: list[str]
    development_rate: float = 1.0     # Multiplier for XP gains
    consistency_modifier: float = 0.0  # Variance in performance
    durability_modifier: float = 0.0   # Injury resistance


# =============================================================================
# ARCHETYPE DEFINITIONS
# =============================================================================

ARCHETYPE_DEFINITIONS: dict[PlayerArchetype, ArchetypeDefinition] = {

    PlayerArchetype.FIELD_GENERAL: ArchetypeDefinition(
        name="FIELD_GENERAL",
        display_name="The Field General",
        description="A cerebral leader who controls the game from the pocket. Reads defenses before they move.",
        icon="🎖️",
        primary_positions=["QB"],
        secondary_positions=[],
        stat_bonuses={
            "awareness": 5,
            "play_recognition": 8,
            "leadership": 10,
            "poise": 5,
            "throw_accuracy_short": 3,
            "throw_accuracy_mid": 3,
        },
        xp_bonuses={
            "mental": 1.3,      # 30% faster mental skill development
            "accuracy": 1.15,
        },
        special_abilities=[
            "pre_snap_read",        # Reveal defensive play call pre-snap
            "protection_audible",   # Perfect protection adjustments
            "morale_boost",         # Team morale +5 in 4th quarter
        ],
        development_rate=1.1,
        consistency_modifier=-0.15,  # More consistent performance
    ),

    PlayerArchetype.SORCERER: ArchetypeDefinition(
        name="SORCERER",
        display_name="The Sorcerer",
        description="Magic arm, pure instinct. Throws dimes that shouldn't be possible. The ultimate improviser.",
        icon="🪄",
        primary_positions=["QB"],
        secondary_positions=[],
        stat_bonuses={
            "throw_power": 5,
            "throw_accuracy_deep": 5,
            "throw_on_run": 8,
            "agility": 5,
            "elusiveness": 5,
        },
        xp_bonuses={
            "physical": 1.2,
            "playmaking": 1.25,
        },
        special_abilities=[
            "no_look_pass",         # Occasional no-look throw for style points
            "pocket_escape",        # +20% escape rate under pressure
            "deep_ball_magician",   # +10yd on deep ball accuracy threshold
        ],
        development_rate=1.0,
        consistency_modifier=0.2,    # More variance (boom or bust)
    ),

    PlayerArchetype.ALPHA_DOG: ArchetypeDefinition(
        name="ALPHA_DOG",
        display_name="The Alpha Dog",
        description="Dominant competitor who wins every 50/50 battle. Gets in opponents' heads.",
        icon="🐺",
        primary_positions=["WR", "CB"],
        secondary_positions=["S"],
        stat_bonuses={
            "catching": 5,
            "aggressive_catch": 10,
            "press": 5,
            "man_coverage": 5,
            "confidence": 10,
        },
        xp_bonuses={
            "coverage": 1.2,
            "catching": 1.2,
        },
        special_abilities=[
            "demoralize",           # Lower opponent morale after big plays
            "contested_catch_king", # +15% win rate on 50/50 balls
            "alpha_swagger",        # Intimidate young players (awareness -3)
        ],
        development_rate=1.05,
    ),

    PlayerArchetype.WEAPON: ArchetypeDefinition(
        name="WEAPON",
        display_name="The Weapon",
        description="Swiss Army knife. Can line up anywhere and produce. Offensive coordinators dream.",
        icon="🗡️",
        primary_positions=["RB", "WR"],
        secondary_positions=["TE", "KR"],
        stat_bonuses={
            "catching": 5,
            "route_running": 5,
            "return_ability": 10,
            "versatility": 15,  # New stat
        },
        xp_bonuses={
            "receiving": 1.2,
            "rushing": 1.1,
        },
        special_abilities=[
            "flex_position",        # Can play multiple positions in game
            "mismatch_hunter",      # +5 ratings vs linebackers in coverage
            "trick_play_master",    # +25% chance of trick play success
        ],
        development_rate=1.15,
    ),

    PlayerArchetype.FREAK: ArchetypeDefinition(
        name="FREAK",
        display_name="The Freak",
        description="Physical specimen. Elite in every combine drill. Born, not made.",
        icon="💪",
        primary_positions=["EDGE", "LB"],
        secondary_positions=["DE", "CB", "S"],
        stat_bonuses={
            "speed": 5,
            "acceleration": 5,
            "strength": 5,
            "jumping": 8,
            "block_shedding": 5,
        },
        xp_bonuses={
            "physical": 0.5,       # Physicals HARDER to improve (already elite)
            "technique": 1.5,      # Technique improves much faster
        },
        special_abilities=[
            "combine_warrior",      # Always win combine drills
            "splash_play_threat",   # +15% chance for strip sack/pick 6
            "wear_down",            # Late-game bonus as opponents tire
        ],
        development_rate=1.25,     # Fastest overall development
    ),

    PlayerArchetype.TECHNICIAN: ArchetypeDefinition(
        name="TECHNICIAN",
        display_name="The Technician",
        description="Master of craft. Never loses on technique. Consistent excellence.",
        icon="🔧",
        primary_positions=["OL", "DL"],
        secondary_positions=["OT", "OG", "C", "DT", "DE"],
        stat_bonuses={
            "technique": 10,
            "pass_block": 5,
            "run_block": 5,
            "awareness": 5,
            "finesse_moves": 5,
            "power_moves": 5,
        },
        xp_bonuses={
            "technique": 1.3,
        },
        special_abilities=[
            "zero_false_starts",    # Immune to crowd noise false starts
            "perfect_set",          # First step always wins
            "ironclad_hands",       # Holding penalty chance -50%
        ],
        development_rate=1.0,
        consistency_modifier=-0.25,  # Very consistent
    ),

    PlayerArchetype.WORKHORSE: ArchetypeDefinition(
        name="WORKHORSE",
        display_name="The Workhorse",
        description="Iron man. 300 carry seasons without complaint. Gets better as game goes on.",
        icon="🐎",
        primary_positions=["RB"],
        secondary_positions=["FB"],
        stat_bonuses={
            "stamina": 10,
            "carrying": 5,
            "toughness": 8,
            "break_tackle": 5,
        },
        xp_bonuses={
            "durability": 1.5,
        },
        special_abilities=[
            "heavy_load",           # No fumble rate increase from carries
            "fourth_quarter_back",  # +3 all ratings in 4th quarter
            "iron_legs",            # Injury chance -40%
        ],
        development_rate=0.9,      # Slower development (physical style)
        durability_modifier=-0.40,  # 40% less injury risk
    ),
}


# =============================================================================
# ARCHETYPE SERVICE
# =============================================================================

class ArchetypeService:
    """Service for managing player archetypes."""

    def __init__(self):
        self.definitions = ARCHETYPE_DEFINITIONS

    def get_archetype(self, archetype: PlayerArchetype) -> ArchetypeDefinition:
        """Get the full definition for an archetype."""
        return self.definitions[archetype]

    def detect_archetype(
        self,
        position: str,
        ratings: dict[str, int],
        age: int,
    ) -> PlayerArchetype | None:
        """
        Detect which archetype best fits a player based on their ratings.

        Not all players have an archetype - must meet thresholds.

        Args:
            position: Player's position
            ratings: Current ratings
            age: Player's age

        Returns:
            Detected archetype or None if no strong match
        """
        # Find all archetypes valid for this position
        valid_archetypes = []
        for archetype, definition in self.definitions.items():
            if position in definition.primary_positions:
                valid_archetypes.append((archetype, 1.0))  # Primary match
            elif position in definition.secondary_positions:
                valid_archetypes.append((archetype, 0.7))  # Secondary match

        if not valid_archetypes:
            return None

        # Score each archetype based on rating profile
        best_archetype = None
        best_score = 0.0
        threshold = 150  # Minimum score to qualify

        for archetype, position_weight in valid_archetypes:
            definition = self.definitions[archetype]
            score = 0.0

            # Check for stat bonuses - player should already be good at these
            for stat, bonus in definition.stat_bonuses.items():
                if stat in ratings:
                    # Higher rating = better match
                    score += min(ratings[stat], 99) * 0.5

            score *= position_weight

            if score > best_score and score >= threshold:
                best_score = score
                best_archetype = archetype

        return best_archetype

    def apply_archetype_bonuses(
        self,
        base_ratings: dict[str, int],
        archetype: PlayerArchetype,
    ) -> dict[str, int]:
        """
        Apply archetype stat bonuses to base ratings.

        Args:
            base_ratings: Player's base ratings
            archetype: Player's archetype

        Returns:
            Modified ratings with bonuses applied
        """
        definition = self.definitions[archetype]
        modified = base_ratings.copy()

        for stat, bonus in definition.stat_bonuses.items():
            if stat in modified:
                modified[stat] = min(99, max(1, modified[stat] + bonus))
            else:
                # New stat - add with bonus as base
                modified[stat] = max(1, 50 + bonus)

        return modified

    def get_xp_multiplier(
        self,
        archetype: PlayerArchetype,
        skill_category: str,
    ) -> float:
        """
        Get XP multiplier for a skill category based on archetype.

        Args:
            archetype: Player's archetype
            skill_category: Category of skill being trained

        Returns:
            XP multiplier (0.5 - 1.5)
        """
        definition = self.definitions[archetype]
        return definition.xp_bonuses.get(skill_category, 1.0)

    def has_special_ability(
        self,
        archetype: PlayerArchetype,
        ability_name: str,
    ) -> bool:
        """Check if archetype has a specific special ability."""
        definition = self.definitions[archetype]
        return ability_name in definition.special_abilities

    def can_evolve_archetype(
        self,
        current_archetype: PlayerArchetype | None,
        position: str,
        ratings: dict[str, int],
        years_in_league: int,
    ) -> PlayerArchetype | None:
        """
        Check if a player can evolve their archetype over their career.

        Players under 26 with 3+ years can potentially evolve.

        Args:
            current_archetype: Current archetype (or None)
            position: Position
            ratings: Current ratings
            years_in_league: Experience

        Returns:
            New archetype if evolution is possible, else None
        """
        if years_in_league < 3:
            return None  # Too early to evolve

        # Try to detect if they now fit a different archetype better
        new_archetype = self.detect_archetype(position, ratings, 25)  # Assume prime age

        if new_archetype and new_archetype != current_archetype:
            # Evolution possible
            return new_archetype

        return None

    def get_all_archetypes_for_position(
        self,
        position: str,
    ) -> list[tuple[PlayerArchetype, ArchetypeDefinition]]:
        """Get all archetypes available for a position."""
        result = []
        for archetype, definition in self.definitions.items():
            if position in definition.primary_positions:
                result.append((archetype, definition))
            elif position in definition.secondary_positions:
                result.append((archetype, definition))
        return result
