"""
Trait System Service - Phase 1 Implementation

Manages player traits, their acquisition, activation, and gameplay effects.
Implements the top 5 priority traits as defined in the roadmap.
"""

from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.player import Player, Trait, PlayerTrait
import logging

logger = logging.getLogger(__name__)


class TraitDefinition:
    """Data class for trait metadata"""
    def __init__(
        self,
        name: str,
        description: str,
        position_requirements: List[str],
        acquisition_method: str,
        activation_triggers: List[str],
        effects: Dict[str, Any],
        tier: str = "COMMON"
    ):
        self.name = name
        self.description = description
        self.position_requirements = position_requirements
        self.acquisition_method = acquisition_method
        self.activation_triggers = activation_triggers
        self.effects = effects
        self.tier = tier

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "position_requirements": self.position_requirements,
            "acquisition_method": self.acquisition_method,
            "activation_triggers": self.activation_triggers,
            "effects": self.effects,
            "tier": self.tier
        }


# ============================================================================
# TRAIT CATALOG - TOP 5 PRIORITY TRAITS
# ============================================================================

TRAIT_CATALOG: Dict[str, TraitDefinition] = {
    # 1. QB Field General (Elite)
    "FIELD_GENERAL": TraitDefinition(
        name="Field General",
        description="Elite QB leadership that elevates offensive unit performance. Boosts awareness and reduces penalties for entire offense.",
        position_requirements=["QB"],
        acquisition_method="AUTO_UNLOCK",  # Unlocks at 90+ awareness, 3+ years experience
        activation_triggers=["ON_FIELD", "OFFENSE_ACTIVE"],
        effects={
            "team_awareness_boost": 5,  # +5 awareness to all offensive players
            "team_penalty_reduction": 0.15,  # -15% penalty rate for offense
            "audible_success_rate": 0.20,  # +20% audible effectiveness
            "pre_snap_adjustment_bonus": 1.0  # Better pre-snap reads
        },
        tier="ELITE"
    ),

    # 2. WR Possession Receiver (Gold)
    "POSSESSION_RECEIVER": TraitDefinition(
        name="Possession Receiver",
        description="Reliable hands in traffic. Increases catch rate in contested situations and reduces fumbles after contact.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",  # 100+ receptions in a season with <5% drop rate
        activation_triggers=["CONTESTED_CATCH", "TRAFFIC_SITUATION"],
        effects={
            "contested_catch_bonus": 15,  # +15 catching in traffic
            "drop_rate_reduction": 0.30,  # -30% drop rate
            "fumble_after_catch_reduction": 0.25,  # -25% fumble chance after catch
            "possession_awareness": 10  # +10 awareness in catch situations
        },
        tier="GOLD"
    ),

    # 3. RB Chip Block (Silver)
    "CHIP_BLOCK": TraitDefinition(
        name="Chip Block Specialist",
        description="Expert at delaying pass rushers with quick chip blocks before releasing into route. Improves pass protection and route timing.",
        position_requirements=["RB", "TE"],
        acquisition_method="COACHING_UNLOCK",  # Taught by coaching staff orprogression
        activation_triggers=["PASS_PLAY", "BLITZ_DETECTED"],
        effects={
            "chip_block_effectiveness": 0.40,  # 40% chance to significantly slow rusher
            "pass_pro_rating_boost": 10,  # +10 pass protection
            "release_timing_improvement": 0.15,  # +15% better route timing after chip
            "blitz_recognition": 5  # +5 awareness vs blitz
        },
        tier="SILVER"
    ),

    # 4. LB Green Dot (Elite)
    "GREEN_DOT": TraitDefinition(
        name="Green Dot (Defensive Captain)",
        description="Defensive playcaller and leader. Entire defense benefits from improved communication and alignment.",
        position_requirements=["LB"],
        acquisition_method="TEAM_DESIGNATION",  # Assigned by coaching staff, requires leadership
        activation_triggers=["ON_FIELD", "DEFENSE_ACTIVE"],
        effects={
            "team_play_recognition_boost": 5,  # +5 play recognition to all defenders
            "alignment_perfection_rate": 0.20,  # +20% reduced blown assignments
            "blitz_timing_coordination": 0.15,  # +15% blitz effectiveness
            "coverage_communication": 5  # +5 zone/man coverage for entire defense
        },
        tier="ELITE"
    ),

    # 5. DB Pick Artist (Gold)
    "PICK_ARTIST": TraitDefinition(
        name="Pick Artist",
        description="Ball hawk with elite hands and instincts. Dramatically increased interception rate and catch radius on balls in the air.",
        position_requirements=["CB", "S"],
        acquisition_method="STAT_THRESHOLD",  # 5+ INTs in a season
        activation_triggers=["BALL_IN_AIR", "IN_COVERAGE"],
        effects={
            "interception_rate_multiplier": 1.5,  # +50% INT rate
            "catch_radius_in_coverage": 1.3,  # +30% catch radius for INTs
            "ball_tracking_boost": 15,  # +15 ball tracking
            "break_on_ball_speed": 0.20  # +20% faster reaction to thrown ball
        },
        tier="GOLD"
    ),

    # --- EXPANDED CATALOG ---

    # QB Traits
    "GUNSLINGER": TraitDefinition(
        name="Gunslinger",
        description="Faster release and increased throw power, but slightly higher interception risk.",
        position_requirements=["QB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_PLAY"],
        effects={
            "throw_power_boost": 5,
            "release_time_reduction": 0.1,
            "interception_chance_increase": 0.05
        },
        tier="GOLD"
    ),
    "ESCAPE_ARTIST": TraitDefinition(
        name="Escape Artist",
        description="Elite agility and speed when scrambling behind the line of scrimmage.",
        position_requirements=["QB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["SCRAMBLE"],
        effects={
            "scramble_speed_boost": 10,
            "agility_boost": 10,
            "break_sack_chance": 0.15
        },
        tier="GOLD"
    ),

    # RB Traits
    "BRUISER": TraitDefinition(
        name="Bruiser",
        description="Power runner who excels at trucking and stiff arms.",
        position_requirements=["RB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["RUN_PLAY", "CONTACT"],
        effects={
            "trucking_boost": 10,
            "stiff_arm_boost": 10,
            "fall_forward_chance": 0.25
        },
        tier="GOLD"
    ),
    "SATELLITE": TraitDefinition(
        name="Satellite",
        description="Elite receiving back with receiver-like route running skills.",
        position_requirements=["RB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_PLAY", "ROUTE_RUNNING"],
        effects={
            "route_running_boost": 10,
            "catching_boost": 5,
            "mismatch_bonus_vs_lb": 0.15
        },
        tier="SILVER"
    ),

    # WR/TE Traits
    "DEEP_THREAT": TraitDefinition(
        name="Deep Threat",
        description="Specializes in deep routes and beating coverage over the top.",
        position_requirements=["WR"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["DEEP_ROUTE"],
        effects={
            "speed_bonus_deep": 5,
            "deep_tracking_boost": 10,
            "separation_bonus_deep": 0.10
        },
        tier="GOLD"
    ),
    "ROUTE_TECHNICIAN": TraitDefinition(
        name="Route Technician",
        description="Elite footwork creates separation on sharp cuts.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["CUT_MOVE"],
        effects={
            "route_running_boost": 10,
            "separation_bonus_cut": 0.15,
            "release_boost": 5
        },
        tier="GOLD"
    ),
    "YAC_MONSTER": TraitDefinition(
        name="YAC Monster",
        description="Dangerous with the ball in hands, hard to tackle.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["AFTER_CATCH"],
        effects={
            "break_tackle_boost": 10,
            "elusiveness_boost": 10,
            "juke_move_boost": 5
        },
        tier="SILVER"
    ),
    "RED_ZONE_THREAT": TraitDefinition(
        name="Red Zone Threat",
        description="Dominant inside the 20 yard line.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["RED_ZONE"],
        effects={
            "catching_boost_rz": 10,
            "contested_catch_bonus_rz": 10,
            "endzone_awareness": 10
        },
        tier="GOLD"
    ),

    # OL Traits
    "ANCHOR": TraitDefinition(
        name="Anchor",
        description="Stout pass protector who rarely gives ground to bull rushes.",
        position_requirements=["OT", "OG", "C"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_BLOCK", "VS_BULL_RUSH"],
        effects={
            "strength_boost_block": 10,
            "balance_boost": 10,
            "pancake_resistance": 0.50
        },
        tier="GOLD"
    ),
    "PULL_SPECIALIST": TraitDefinition(
        name="Pull Specialist",
        description="Agile lineman who excels at pulling and blocking in space.",
        position_requirements=["OG", "C", "OT"],
        acquisition_method="COACHING_UNLOCK",
        activation_triggers=["PULL_BLOCK", "RUN_PLAY"],
        effects={
            "speed_boost_pull": 10,
            "blocking_in_space_boost": 10,
            "awareness_boost_pull": 5
        },
        tier="SILVER"
    ),

    # DL Traits
    "EDGE_RUSHER": TraitDefinition(
        name="Edge Threat",
        description="Explosive first step off the edge.",
        position_requirements=["DE", "LB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_RUSH", "EDGE_RUSH"],
        effects={
            "acceleration_boost_rush": 10,
            "finesse_move_boost": 5,
            "qb_pressure_chance": 0.15
        },
        tier="GOLD"
    ),
    "RUN_STUFFER": TraitDefinition(
        name="Run Stuffer",
        description="Impossible to move in the run game, sheds blocks easily.",
        position_requirements=["DT", "DE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["RUN_DEFENSE"],
        effects={
            "block_shedding_boost_run": 10,
            "strength_boost_run": 5,
            "tackle_bonus_run": 5
        },
        tier="GOLD"
    ),

    # LB Traits
    "COVERAGE_LB": TraitDefinition(
        name="Coverage Linebacker",
        description="Linebacker with safety-like coverage skills.",
        position_requirements=["LB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["COVERAGE"],
        effects={
            "zone_coverage_boost": 10,
            "man_coverage_boost": 5,
            "reaction_time_reduction": 0.1
        },
        tier="GOLD"
    ),
    "ENFORCER": TraitDefinition(
        name="Enforcer",
        description="Heavy hitter who causes more fumbles and fatigue.",
        position_requirements=["LB", "S"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["TACKLE", "HIT_STICK"],
        effects={
            "hit_power_boost": 10,
            "forced_fumble_chance": 0.15,
            "fatigue_damage_boost": 0.20
        },
        tier="SILVER"
    ),

    # DB Traits
    "SHUTDOWN_CORNER": TraitDefinition(
        name="Shutdown Corner",
        description="Elite man coverage specialist who erases receivers.",
        position_requirements=["CB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["MAN_COVERAGE"],
        effects={
            "man_coverage_boost": 10,
            "press_coverage_boost": 10,
            "receiver_separation_reduction": 0.20
        },
        tier="ELITE"
    ),
    "ZONE_HAWK": TraitDefinition(
        name="Zone Hawk",
        description="Elite zone coverage instincts and break-on-ball speed.",
        position_requirements=["CB", "S"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["ZONE_COVERAGE"],
        effects={
            "zone_coverage_boost": 10,
            "reaction_time_zone": 0.15,
            "interception_chance_zone": 0.10
        },
        tier="GOLD"
    ),

    # Special Teams
    "CLUTCH_KICKER": TraitDefinition(
        name="Clutch Kicker",
        description="Immune to pressure in critical game-winning situations.",
        position_requirements=["K"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["CLUTCH_MOMENT", "FIELD_GOAL"],
        effects={
            "accuracy_boost_clutch": 15,
            "ice_kicker_immunity": 1.0,
            "kick_power_boost_clutch": 5
        },
        tier="SILVER"
    ),
    "COFFIN_CORNER": TraitDefinition(
        name="Coffin Corner",
        description="Elite precision punting inside the 20.",
        position_requirements=["P"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PUNT_INSIDE_50"],
        effects={
            "accuracy_boost_punt": 15,
            "backspin_chance": 0.30,
            "touchback_chance_reduction": 0.20
        },
        tier="SILVER"
    ),

    # General
    "IRON_MAN": TraitDefinition(
        name="Iron Man",
        description="Superior conditioning and durability.",
        position_requirements=["ALL"],
        acquisition_method="PROGRESSION",
        activation_triggers=["ALWAYS"],
        effects={
            "fatigue_recovery_boost": 0.20,
            "injury_resistance": 0.15,
            "stamina_drain_reduction": 0.10
        },
        tier="SILVER"
    ),
    "MENTOR": TraitDefinition(
        name="Mentor",
        description="Veteran presence that accelerates development of younger players.",
        position_requirements=["ALL"],
        acquisition_method="PROGRESSION",
        activation_triggers=["WEEKLY_TRAINING"],
        effects={
            "xp_boost_position_group": 0.10,
            "regression_delay": 1.0
        },
        tier="SILVER"
    ),
}


class TraitService:
    """Service for managing player traits"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def initialize_trait_catalog(self) -> None:
        """
        Initialize all traits in the database.
        Should be run once during setup or migrations.
        """
        for trait_key, trait_def in TRAIT_CATALOG.items():
            # Check if trait exists
            stmt = select(Trait).filter(Trait.name == trait_def.name)
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()

            if not existing:
                # Create new trait
                trait = Trait(
                    name=trait_def.name,
                    description=trait_def.description
                )
                self.db.add(trait)
                logger.info(f"Initialized trait: {trait_def.name}")

        await self.db.commit()

    async def grant_trait_to_player(
        self,
        player_id: int,
        trait_name: str
    ) -> bool:
        """
        Grant a trait to a player.

        Args:
            player_id: Player ID
            trait_name: Name of trait to grant

        Returns:
            True if granted successfully, False if player already has trait
        """
        # Get trait
        stmt = select(Trait).filter(Trait.name == trait_name)
        result = await self.db.execute(stmt)
        trait = result.scalar_one_or_none()

        if not trait:
            logger.error(f"Trait not found: {trait_name}")
            return False

        # Check if player already has trait
        stmt = select(PlayerTrait).filter(
            PlayerTrait.player_id == player_id,
            PlayerTrait.trait_id == trait.id
        )
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            logger.warning(f"Player {player_id} already has trait {trait_name}")
            return False

        # Grant trait
        player_trait = PlayerTrait(
            player_id=player_id,
            trait_id=trait.id
        )
        self.db.add(player_trait)
        await self.db.commit()

        logger.info(f"Granted trait '{trait_name}' to player {player_id}")
        return True

    async def remove_trait_from_player(
        self,
        player_id: int,
        trait_name: str
    ) -> bool:
        """Remove a trait from a player"""
        # Get trait
        stmt = select(Trait).filter(Trait.name == trait_name)
        result = await self.db.execute(stmt)
        trait = result.scalar_one_or_none()

        if not trait:
            return False

        # Delete association
        stmt = select(PlayerTrait).filter(
            PlayerTrait.player_id == player_id,
            PlayerTrait.trait_id == trait.id
        )
        result = await self.db.execute(stmt)
        player_trait = result.scalar_one_or_none()

        if player_trait:
            await self.db.delete(player_trait)
            await self.db.commit()
            logger.info(f"Removed trait '{trait_name}' from player {player_id}")
            return True

        return False

    async def get_player_traits(self, player_id: int) -> List[TraitDefinition]:
        """Get all traits for a player with full metadata"""
        stmt = (
            select(Trait)
            .join(PlayerTrait, Trait.id == PlayerTrait.trait_id)
            .filter(PlayerTrait.player_id == player_id)
        )
        result = await self.db.execute(stmt)
        traits = result.scalars().all()

        # Map to TraitDefinitions
        trait_defs = []
        for trait in traits:
            # Find matching definition in catalog
            for trait_def in TRAIT_CATALOG.values():
                if trait_def.name == trait.name:
                    trait_defs.append(trait_def)
                    break

        return trait_defs

    def check_trait_activation(
        self,
        trait_def: TraitDefinition,
        current_context: Dict[str, Any]
    ) -> bool:
        """
        Check if a trait should be activated in the current game context.

        Args:
            trait_def: Trait definition
            current_context: Current game state (e.g., {"situation": "PASS_PLAY", "down": 3})

        Returns:
            True if trait should activate
        """
        for trigger in trait_def.activation_triggers:
            if trigger in current_context.get("triggers", []):
                return True

        return False

    def apply_trait_effects(
        self,
        player: Player,
        trait_def: TraitDefinition,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply trait effects to a player or game situation.

        Args:
            player: Player object
            trait_def: Trait definition
            context: Current game context

        Returns:
            Dictionary of applied modifiers
        """
        applied_effects = {}

        # Apply attribute bonuses
        if not hasattr(player, "trait_modifiers"):
            player.trait_modifiers = {}

        for effect_key, effect_value in trait_def.effects.items():
            # Map effect to player attribute or context modifier
            if "_boost" in effect_key or "_bonus" in effect_key:
                # Add to player's active modifiers
                if not hasattr(player, "active_modifiers"):
                    player.active_modifiers = {}

                # Extract attribute name (e.g., "team_awareness_boost" -> apply to team)
                # For now, store in trait_modifiers for game logic to consume
                player.trait_modifiers[effect_key] = effect_value
                applied_effects[effect_key] = effect_value

        return applied_effects

    async def check_trait_eligibility(
        self,
        player: Player,
        trait_name: str
    ) -> tuple[bool, str]:
        """
        Check if a player is eligible for a trait.

        Returns:
            (is_eligible, reason)
        """
        trait_def = None
        for trait_def_candidate in TRAIT_CATALOG.values():
            if trait_def_candidate.name == trait_name:
                trait_def = trait_def_candidate
                break

        if not trait_def:
            return False, "Trait not found"

        # Check position requirements
        if player.position not in trait_def.position_requirements:
            return False, f"Position {player.position} not eligible (requires {trait_def.position_requirements})"

        # Check acquisition method requirements
        method = trait_def.acquisition_method

        if method == "AUTO_UNLOCK":
            # Field General: 90+ awareness, 3+ years
            if trait_name == "Field General":
                if player.awareness < 90:
                    return False, "Requires 90+ awareness"
                if player.experience < 3:
                    return False, "Requires 3+ years experience"

        elif method == "STAT_THRESHOLD":
            # Would need to check season stats (not implemented here)
            pass

        return True, "Eligible"
