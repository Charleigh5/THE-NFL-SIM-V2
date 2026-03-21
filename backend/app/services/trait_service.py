from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.logging_config import ErrorCategory, get_logger, log_error
from app.models.player import Player
from app.models.trait import PlayerTrait, Trait, TraitSource

logger = get_logger(__name__)


# ============================================================================
# TRAIT DEFINITION DATACLASS
# ============================================================================

# ============================================================================
# TRAIT RARITY TIERS
# ============================================================================
# Controls how rare traits are in the league based on real-world distributions

class TraitRarity:
    """Rarity tiers for trait distribution."""
    LEGENDARY = "LEGENDARY"  # 1-5 players league-wide (e.g., Ragknow, Rocket Arm)
    RARE = "RARE"            # 5-15 players league-wide (e.g., Elite Speed)
    UNCOMMON = "UNCOMMON"    # ~50-100 players (e.g., most Gold-tier traits)
    COMMON = "COMMON"        # No cap (e.g., most Silver/Common traits)


# Soft caps for legendary traits (approximate league-wide limits)
LEGENDARY_TRAIT_CAPS = {
    "ragknow": 3,           # ~3 players with legendary toughness
    "rocket_arm": 5,        # ~5 QBs with truly elite arm strength
    "elite_speed": 10,      # ~10 players with 4.3 speed or better
    "generational": 2,      # ~2 truly generational talents at a time
}


@dataclass
class TraitDefinition:
    """
    Defines a trait's properties, requirements, and effects.
    Used for the in-memory catalog and eligibility checking.
    """
    name: str
    description: str
    position_requirements: list[str]
    acquisition_method: str  # AUTO_UNLOCK, STAT_THRESHOLD, COACHING_UNLOCK, TEAM_DESIGNATION, PROGRESSION, RPG_UNLOCK
    activation_triggers: list[str]  # ON_FIELD, PASS_PLAY, RUN_PLAY, CONTESTED_CATCH, INJURY_ACTIVE, etc.
    effects: dict[str, float]
    tier: str  # COMMON, SILVER, GOLD, ELITE

    # Optional eligibility requirements
    min_awareness: int | None = None
    min_experience: int | None = None
    min_stat_threshold: dict[str, int] | None = None

    # Rarity system
    rarity_tier: str = TraitRarity.COMMON  # LEGENDARY, RARE, UNCOMMON, COMMON
    max_league_count: int | None = None  # Soft cap on total players with this trait

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "name": self.name,
            "description": self.description,
            "position_requirements": self.position_requirements,
            "acquisition_method": self.acquisition_method,
            "activation_triggers": self.activation_triggers,
            "effects": self.effects,
            "tier": self.tier,
        }


# ============================================================================
# TRAIT CATALOG - 25 TRAITS
# ============================================================================

TRAIT_CATALOG: dict[str, TraitDefinition] = {
    # -------------------------------------------------------------------------
    # QB TRAITS (3)
    # -------------------------------------------------------------------------
    "field_general": TraitDefinition(
        name="Field General",
        description="Elite QB leadership that elevates the entire offense. +5 awareness to all offensive players, -15% penalty rate.",
        position_requirements=["QB"],
        acquisition_method="AUTO_UNLOCK",
        activation_triggers=["ON_FIELD"],
        effects={
            "team_awareness_boost": 5,
            "team_penalty_reduction": 0.15,
            "audible_effectiveness": 0.20,
            "pre_snap_adjustment_bonus": 1.0,
        },
        tier="ELITE",
        min_awareness=90,
        min_experience=3,
    ),
    "gunslinger": TraitDefinition(
        name="Gunslinger",
        description="Faster release and increased throw power, but slightly higher interception risk.",
        position_requirements=["QB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_PLAY"],
        effects={
            "throw_power_boost": 5,
            "release_time_reduction": 0.10,
            "interception_risk_increase": 0.05,
        },
        tier="GOLD",
    ),
    "escape_artist": TraitDefinition(
        name="Escape Artist",
        description="Elite agility and speed when scrambling behind the line of scrimmage.",
        position_requirements=["QB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["SCRAMBLE"],
        effects={
            "scramble_speed_boost": 10,
            "agility_boost": 10,
            "sack_break_chance": 0.15,
        },
        tier="GOLD",
    ),

    # -------------------------------------------------------------------------
    # RB TRAITS (3)
    # -------------------------------------------------------------------------
    "chip_block_specialist": TraitDefinition(
        name="Chip Block Specialist",
        description="Dual-threat backs become better pass protectors with improved chip blocking.",
        position_requirements=["RB"],
        acquisition_method="COACHING_UNLOCK",
        activation_triggers=["PASS_PLAY", "BLITZ_DETECTED"],
        effects={
            "chip_block_success_rate": 0.40,
            "pass_protection_boost": 10,
            "route_timing_after_chip": 0.15,
            "blitz_awareness_boost": 5,
        },
        tier="SILVER",
    ),
    "bruiser": TraitDefinition(
        name="Bruiser",
        description="Power runner who excels at trucking and stiff arms.",
        position_requirements=["RB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["RUN_PLAY", "CONTACT"],
        effects={
            "trucking_boost": 10,
            "stiff_arm_boost": 10,
            "fall_forward_chance": 0.25,
        },
        tier="GOLD",
    ),
    "satellite": TraitDefinition(
        name="Satellite",
        description="Elite receiving back with receiver-like route running skills.",
        position_requirements=["RB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_PLAY", "ROUTE_RUNNING"],
        effects={
            "route_running_boost": 10,
            "catching_boost": 5,
            "mismatch_bonus_vs_lb": 0.15,
        },
        tier="SILVER",
    ),

    # -------------------------------------------------------------------------
    # WR/TE TRAITS (5)
    # -------------------------------------------------------------------------
    "possession_receiver": TraitDefinition(
        name="Possession Receiver",
        description="Reliable third-down target, clutch performer in traffic.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["CONTESTED_CATCH", "TRAFFIC"],
        effects={
            "catching_in_traffic_boost": 15,
            "drop_rate_reduction": 0.30,
            "fumble_after_catch_reduction": 0.25,
            "catch_awareness_boost": 10,
        },
        tier="GOLD",
        min_stat_threshold={"receptions": 100, "drop_rate_max": 0.05},
    ),
    "deep_threat": TraitDefinition(
        name="Deep Threat",
        description="Specializes in deep routes and beating coverage over the top.",
        position_requirements=["WR"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["DEEP_ROUTE"],
        effects={
            "deep_route_speed_boost": 5,
            "deep_ball_tracking_boost": 10,
            "deep_route_separation_bonus": 0.10,
        },
        tier="GOLD",
    ),
    "route_technician": TraitDefinition(
        name="Route Technician",
        description="Elite footwork creates separation on sharp cuts.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["CUT_MOVE"],
        effects={
            "route_running_boost": 10,
            "cut_separation_bonus": 0.15,
            "release_boost": 5,
        },
        tier="GOLD",
    ),
    "yac_monster": TraitDefinition(
        name="YAC Monster",
        description="Dangerous with the ball in hands, hard to tackle after catch.",
        position_requirements=["WR", "TE", "RB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["AFTER_CATCH"],
        effects={
            "break_tackle_boost": 10,
            "elusiveness_boost": 10,
            "juke_move_boost": 5,
        },
        tier="SILVER",
    ),
    "red_zone_threat": TraitDefinition(
        name="Red Zone Threat",
        description="Dominant inside the 20 yard line.",
        position_requirements=["WR", "TE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["RED_ZONE"],
        effects={
            "red_zone_catching_boost": 10,
            "red_zone_contested_catch_boost": 10,
            "endzone_awareness_boost": 10,
        },
        tier="GOLD",
    ),

    # -------------------------------------------------------------------------
    # OL TRAITS (2)
    # -------------------------------------------------------------------------
    "anchor": TraitDefinition(
        name="Anchor",
        description="Stout pass protector who rarely gives ground to bull rushes.",
        position_requirements=["OT", "OG", "C"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_BLOCK", "VS_BULL_RUSH"],
        effects={
            "strength_blocking_boost": 10,
            "balance_boost": 10,
            "pancake_resistance": 0.50,
        },
        tier="GOLD",
    ),
    "pull_specialist": TraitDefinition(
        name="Pull Specialist",
        description="Agile lineman who excels at pulling and blocking in space.",
        position_requirements=["OG", "C"],
        acquisition_method="COACHING_UNLOCK",
        activation_triggers=["PULL_BLOCK", "RUN_PLAY"],
        effects={
            "pull_speed_boost": 10,
            "blocking_in_space_boost": 10,
            "pull_awareness_boost": 5,
        },
        tier="SILVER",
    ),

    # -------------------------------------------------------------------------
    # DL TRAITS (2)
    # -------------------------------------------------------------------------
    "edge_threat": TraitDefinition(
        name="Edge Threat",
        description="Explosive first step off the edge.",
        position_requirements=["DE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PASS_RUSH", "EDGE_RUSH"],
        effects={
            "acceleration_boost": 10,
            "finesse_move_boost": 5,
            "pressure_chance_boost": 0.15,
        },
        tier="GOLD",
    ),
    "run_stuffer": TraitDefinition(
        name="Run Stuffer",
        description="Impossible to move in the run game, sheds blocks easily.",
        position_requirements=["DT", "DE"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["RUN_DEFENSE"],
        effects={
            "block_shedding_vs_run_boost": 10,
            "run_strength_boost": 5,
            "run_tackle_bonus": 5,
        },
        tier="GOLD",
    ),

    # -------------------------------------------------------------------------
    # LB TRAITS (3)
    # -------------------------------------------------------------------------
    "green_dot": TraitDefinition(
        name="Green Dot (Defensive Captain)",
        description="Defensive quarterback that coordinates the entire unit. +5 play recognition to all defenders.",
        position_requirements=["LB"],
        acquisition_method="TEAM_DESIGNATION",
        activation_triggers=["ON_FIELD"],
        effects={
            "team_play_recognition_boost": 5,
            "blown_assignment_reduction": 0.20,
            "blitz_effectiveness_boost": 0.15,
            "team_coverage_boost": 5,
        },
        tier="ELITE",
    ),
    "coverage_linebacker": TraitDefinition(
        name="Coverage Linebacker",
        description="Linebacker with safety-like coverage skills.",
        position_requirements=["LB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["COVERAGE"],
        effects={
            "zone_coverage_boost": 10,
            "man_coverage_boost": 5,
            "reaction_time_reduction": 0.10,
        },
        tier="GOLD",
    ),
    "enforcer": TraitDefinition(
        name="Enforcer",
        description="Heavy hitter who causes more fumbles and fatigue.",
        position_requirements=["LB", "S"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["TACKLE", "HIT_STICK"],
        effects={
            "hit_power_boost": 10,
            "forced_fumble_chance_boost": 0.15,
            "fatigue_damage_to_carrier": 0.20,
        },
        tier="SILVER",
    ),

    # -------------------------------------------------------------------------
    # DB TRAITS (3)
    # -------------------------------------------------------------------------
    "pick_artist": TraitDefinition(
        name="Pick Artist",
        description="Game-changing ball hawk who creates turnovers.",
        position_requirements=["CB", "S"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["BALL_IN_AIR", "IN_COVERAGE"],
        effects={
            "interception_rate_multiplier": 1.50,
            "interception_catch_radius_boost": 0.30,
            "ball_tracking_boost": 15,
            "ball_reaction_speed_boost": 0.20,
        },
        tier="GOLD",
        min_stat_threshold={"interceptions": 5},
    ),
    "shutdown_corner": TraitDefinition(
        name="Shutdown Corner",
        description="Elite man coverage specialist who erases receivers.",
        position_requirements=["CB"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["MAN_COVERAGE"],
        effects={
            "man_coverage_boost": 10,
            "press_coverage_boost": 10,
            "receiver_separation_reduction": 0.20,
        },
        tier="ELITE",
    ),
    "zone_hawk": TraitDefinition(
        name="Zone Hawk",
        description="Elite zone coverage instincts and break-on-ball speed.",
        position_requirements=["CB", "S"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["ZONE_COVERAGE"],
        effects={
            "zone_coverage_boost": 10,
            "zone_reaction_time_reduction": 0.15,
            "zone_interception_chance_boost": 0.10,
        },
        tier="GOLD",
    ),

    # -------------------------------------------------------------------------
    # SPECIAL TEAMS TRAITS (2)
    # -------------------------------------------------------------------------
    "clutch_kicker": TraitDefinition(
        name="Clutch Kicker",
        description="Immune to pressure in critical game-winning situations.",
        position_requirements=["K"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["CLUTCH_MOMENT", "FIELD_GOAL"],
        effects={
            "clutch_accuracy_boost": 15,
            "ice_the_kicker_immunity": 1.0,
            "clutch_kick_power_boost": 5,
        },
        tier="SILVER",
    ),
    "coffin_corner": TraitDefinition(
        name="Coffin Corner",
        description="Elite precision punting inside the 20.",
        position_requirements=["P"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["PUNT_INSIDE_50"],
        effects={
            "punt_accuracy_boost": 15,
            "backspin_chance": 0.30,
            "touchback_reduction": 0.20,
        },
        tier="SILVER",
    ),

    # -------------------------------------------------------------------------
    # GENERAL TRAITS (2)
    # -------------------------------------------------------------------------
    "iron_man": TraitDefinition(
        name="Iron Man",
        description="Superior conditioning and durability.",
        position_requirements=["ALL"],
        acquisition_method="PROGRESSION",
        activation_triggers=["ALWAYS"],
        effects={
            "fatigue_recovery_boost": 0.20,
            "injury_resistance_boost": 0.15,
            "stamina_drain_reduction": 0.10,
        },
        tier="SILVER",
    ),
    "mentor": TraitDefinition(
        name="Mentor",
        description="Veteran presence that accelerates development of younger players.",
        position_requirements=["ALL"],
        acquisition_method="PROGRESSION",
        activation_triggers=["WEEKLY_TRAINING"],
        effects={
            "position_group_xp_boost": 0.10,
            "regression_delay": 1.0,
        },
        tier="SILVER",
        min_experience=8,
    ),

    # -------------------------------------------------------------------------
    # LEGENDARY TRAITS (Rare, League-Wide Soft Caps)
    # -------------------------------------------------------------------------
    "ragknow": TraitDefinition(
        name="Ragknow",
        description="Legendary toughness that allows the player to ignore injury penalties and play through Minor/Moderate injuries (severity 1-7) without performance loss. Named after the legendary warriors who fought through any wound.",
        position_requirements=["ALL"],
        acquisition_method="RPG_UNLOCK",  # Rare trait from RPG events or draft
        activation_triggers=["INJURY_ACTIVE", "ALWAYS"],
        effects={
            "ignore_injury_penalties": 1.0,       # Boolean flag (1.0 = true)
            "max_playable_severity": 7,           # Can play through severity 1-7
            "block_injury_degradation": 1.0,      # No permanent attribute loss while injured
            "recovery_time_multiplier": 0.90,     # 10% faster recovery
        },
        tier="ELITE",
        min_experience=5,  # Must be veteran to unlock through progression
        rarity_tier=TraitRarity.LEGENDARY,
        max_league_count=3,  # Only ~3 players in the entire league
    ),
    "rocket_arm": TraitDefinition(
        name="Rocket Arm",
        description="Truly elite arm strength that allows throws other QBs simply cannot make. Off-platform power, deep ball velocity, and tight-window velocity are all enhanced.",
        position_requirements=["QB"],
        acquisition_method="STAT_THRESHOLD",  # Born with it or develop through extreme training
        activation_triggers=["PASS_PLAY", "DEEP_ROUTE"],
        effects={
            "throw_power_boost": 8,
            "deep_throw_accuracy_boost": 5,
            "off_platform_throw_boost": 0.20,
            "tight_window_velocity_boost": 0.15,
        },
        tier="ELITE",
        min_stat_threshold={"throw_power": 95},
        rarity_tier=TraitRarity.LEGENDARY,
        max_league_count=5,  # Only ~5 QBs with truly elite arms
    ),
    "elite_speed": TraitDefinition(
        name="Elite Speed",
        description="4.3 forty or better. This player is in the 99th percentile of human speed and can change games with pure athleticism.",
        position_requirements=["WR", "CB", "RB", "S"],
        acquisition_method="STAT_THRESHOLD",  # Born with it
        activation_triggers=["ALWAYS"],
        effects={
            "speed_boost": 3,  # Additional boost on top of base speed
            "breakaway_chance_boost": 0.15,
            "closing_speed_boost": 0.20,
        },
        tier="ELITE",
        min_stat_threshold={"speed": 96},
        rarity_tier=TraitRarity.RARE,
        max_league_count=10,  # ~10 players with 4.3 speed
    ),
    "generational": TraitDefinition(
        name="Generational Talent",
        description="A once-in-a-generation player who redefines their position. Everything they do is at an elite level.",
        position_requirements=["ALL"],
        acquisition_method="DRAFT",  # Only acquired at draft time
        activation_triggers=["ALWAYS"],
        effects={
            "all_ratings_boost": 3,
            "development_speed_boost": 0.25,
            "clutch_performance_boost": 0.15,
            "highlight_play_chance": 0.10,
        },
        tier="ELITE",
        rarity_tier=TraitRarity.LEGENDARY,
        max_league_count=2,  # Only ~2 truly generational talents at a time
    ),

    # -------------------------------------------------------------------------
    # RARE TRAITS (5-15 players league-wide)
    # -------------------------------------------------------------------------
    "football_iq": TraitDefinition(
        name="Football IQ",
        description="Elite mental processing that allows the player to read plays before they develop and make adjustments on the fly.",
        position_requirements=["QB", "LB", "S", "C"],
        acquisition_method="PROGRESSION",
        activation_triggers=["ALWAYS"],
        effects={
            "play_recognition_boost": 10,
            "pre_snap_adjustment_boost": 0.20,
            "audible_success_boost": 0.15,
            "blown_assignment_reduction": 0.25,
        },
        tier="GOLD",
        min_awareness=92,
        min_experience=4,
        rarity_tier=TraitRarity.RARE,
        max_league_count=15,
    ),
    "freak_athlete": TraitDefinition(
        name="Freak Athlete",
        description="Combine numbers that defy belief. This player is built differently and can do things others physically cannot.",
        position_requirements=["ALL"],
        acquisition_method="STAT_THRESHOLD",
        activation_triggers=["ALWAYS"],
        effects={
            "agility_boost": 4,
            "acceleration_boost": 4,
            "jumping_boost": 5,
            "change_of_direction_boost": 0.15,
        },
        tier="GOLD",
        min_stat_threshold={"agility": 94, "acceleration": 94},
        rarity_tier=TraitRarity.RARE,
        max_league_count=12,
    ),

    # -------------------------------------------------------------------------
    # TRUE-TO-LIFE TRAITS (Phase 11)
    # -------------------------------------------------------------------------
    "the_closer": TraitDefinition(
        name="The Closer",
        description="Ice in the veins. Ignores pressure penalties and fatigue effects in crunch time (4th quarter <5 min remaining, score within 8 points, or Overtime).",
        position_requirements=["ALL"],
        acquisition_method="PROGRESSION",
        activation_triggers=["CRUNCH_TIME"],
        effects={
            "pressure_immunity": 1.0,      # Boolean: Nullifies pressure penalties
            "fatigue_override": 1.0,       # Boolean: Ignores fatigue penalties
            "awareness_boost": 15,         # Situational awareness for clock/bounds
            "fumble_chance_reduction": 0.20,  # 20% less fumbles under pressure
        },
        tier="ELITE",
        min_experience=4,
        rarity_tier=TraitRarity.RARE,
        max_league_count=15,
    ),
}



# ============================================================================
# TRAIT SERVICE CLASS
# ============================================================================

class TraitService:
    """
    Service for managing Player Traits (X-Factors, Passive Boosts).
    Supports both database-backed traits and in-memory catalog lookups.
    """

    def __init__(self, db: Session = None):
        """Initialize with optional database session for async operations."""
        self.db = db

    # -------------------------------------------------------------------------
    # CATALOG METHODS (In-Memory)
    # -------------------------------------------------------------------------

    @staticmethod
    def get_catalog() -> dict[str, TraitDefinition]:
        """Return the full trait catalog."""
        return TRAIT_CATALOG

    @staticmethod
    def get_trait_definition(trait_key: str) -> TraitDefinition | None:
        """Get a specific trait definition by key."""
        return TRAIT_CATALOG.get(trait_key)

    @staticmethod
    def get_trait_by_name(name: str) -> TraitDefinition | None:
        """Get a trait definition by its display name."""
        for trait_def in TRAIT_CATALOG.values():
            if trait_def.name == name:
                return trait_def
        return None

    # -------------------------------------------------------------------------
    # DATABASE METHODS (Persistence)
    # -------------------------------------------------------------------------

    @staticmethod
    def get_all_traits(db: Session) -> list[Trait]:
        """List all available traits in the system."""
        return db.scalars(select(Trait)).all()

    @staticmethod
    def get_player_traits(db: Session, player_id: int) -> list[TraitDefinition]:
        """
        Get all traits assigned to a specific player.
        Returns TraitDefinition objects from the catalog for full effect data.
        """
        # Query trait names from DB
        db_traits = db.scalars(
            select(Trait)
            .join(PlayerTrait, Trait.id == PlayerTrait.trait_id)
            .where(PlayerTrait.player_id == player_id)
        ).all()

        # Map DB traits to catalog definitions for full data
        trait_defs = []
        for db_trait in db_traits:
            # Try to find matching catalog trait
            catalog_def = TraitService.get_trait_by_name(db_trait.name)
            if catalog_def:
                trait_defs.append(catalog_def)
            else:
                # Fallback: create minimal TraitDefinition from DB data
                trait_defs.append(TraitDefinition(
                    name=db_trait.name,
                    description=db_trait.description or "",
                    position_requirements=[],
                    acquisition_method="UNKNOWN",
                    activation_triggers=["ON_FIELD"],
                    effects={},
                    tier="COMMON",
                ))

        return trait_defs

    @staticmethod
    def assign_trait(
        db: Session,
        player_id: int,
        trait_id: int,
        source: TraitSource = TraitSource.DEVELOPMENT
    ) -> PlayerTrait | None:
        """Assign a trait to a player with APF 2K8-style tier caps."""
        from app.models.trait import TraitTier  # Local import to avoid circular

        # Tier caps: limits per player (APF 2K8 balance)
        TIER_CAPS = {
            TraitTier.GOLD: 1,
            TraitTier.SILVER: 2,
            TraitTier.BRONZE: 3,
            TraitTier.COMMON: None,  # No limit
        }

        try:
            # Check if already assigned
            existing = db.scalar(
                select(PlayerTrait)
                .where(PlayerTrait.player_id == player_id, PlayerTrait.trait_id == trait_id)
            )
            if existing:
                logger.info("trait_already_assigned", player_id=player_id, trait_id=trait_id)
                return existing

            # Validate Player and Trait existence
            player = db.get(Player, player_id)
            trait = db.get(Trait, trait_id)

            if not player or not trait:
                raise ValueError("Player or Trait not found")

            # Validate tier cap
            trait_tier = getattr(trait, 'tier', TraitTier.COMMON)
            cap = TIER_CAPS.get(trait_tier)
            if cap is not None:
                # Count existing traits of this tier
                existing_count = db.scalar(
                    select(func.count(PlayerTrait.trait_id))
                    .join(Trait, Trait.id == PlayerTrait.trait_id)
                    .where(PlayerTrait.player_id == player_id)
                    .where(Trait.tier == trait_tier)
                )
                if existing_count >= cap:
                    raise ValueError(
                        f"Player already has {existing_count} {trait_tier.value} traits "
                        f"(max {cap}). Cannot assign '{trait.name}'."
                    )

            new_assignment = PlayerTrait(
                player_id=player_id,
                trait_id=trait_id,
                source=source
            )
            db.add(new_assignment)
            db.commit()
            db.refresh(new_assignment)

            logger.info(
                "trait_assigned",
                player_id=player_id,
                trait_id=trait_id,
                source=source,
                trait_name=trait.name,
                tier=str(trait_tier)
            )
            return new_assignment

        except Exception as e:
            db.rollback()
            log_error(logger, ErrorCategory.TRAIT_ERROR, "Failed to assign trait", exc_info=e, player_id=player_id)
            raise

    # -------------------------------------------------------------------------
    # ASYNC INSTANCE METHOD WRAPPERS (for services that pass db in constructor)
    # -------------------------------------------------------------------------

    async def get_player_traits_async(self, player_id: int) -> list[TraitDefinition]:
        """
        Async instance method wrapper for get_player_traits.
        Uses self.db passed in constructor.
        """
        if self.db is None:
            raise ValueError("TraitService requires db session for this operation")

        # For async sessions, we need to use await
        from sqlalchemy import select as sa_select
        from sqlalchemy.ext.asyncio import AsyncSession

        if isinstance(self.db, AsyncSession):
            result = await self.db.execute(
                sa_select(Trait)
                .join(PlayerTrait, Trait.id == PlayerTrait.trait_id)
                .where(PlayerTrait.player_id == player_id)
            )
            db_traits = result.scalars().all()
        else:
            # Sync session fallback
            db_traits = self.db.scalars(
                sa_select(Trait)
                .join(PlayerTrait, Trait.id == PlayerTrait.trait_id)
                .where(PlayerTrait.player_id == player_id)
            ).all()

        # Map DB traits to catalog definitions for full data
        trait_defs = []
        for db_trait in db_traits:
            catalog_def = self.get_trait_by_name(db_trait.name)
            if catalog_def:
                trait_defs.append(catalog_def)
            else:
                trait_defs.append(TraitDefinition(
                    name=db_trait.name,
                    description=db_trait.description or "",
                    position_requirements=[],
                    acquisition_method="UNKNOWN",
                    activation_triggers=["ON_FIELD"],
                    effects={},
                    tier="COMMON",
                ))

        return trait_defs

    # -------------------------------------------------------------------------
    # ELIGIBILITY & ACTIVATION METHODS
    # -------------------------------------------------------------------------

    async def check_trait_eligibility(
        self,
        player: Player,
        trait_name: str
    ) -> tuple[bool, str]:
        """
        Check if a player is eligible for a specific trait.
        Returns (is_eligible, reason_string).
        """
        trait_def = self.get_trait_by_name(trait_name)

        if not trait_def:
            return False, f"Unknown trait: {trait_name}"

        # Check position requirements
        if "ALL" not in trait_def.position_requirements:
            if player.position not in trait_def.position_requirements:
                return False, f"Position {player.position} not eligible for {trait_name}"

        # Check awareness requirement
        if trait_def.min_awareness:
            player_awareness = getattr(player, "awareness", 0)
            if player_awareness < trait_def.min_awareness:
                return False, f"Requires {trait_def.min_awareness}+ awareness (player has {player_awareness})"

        # Check experience requirement
        if trait_def.min_experience:
            player_experience = getattr(player, "experience", 0) or getattr(player, "years_pro", 0)
            if player_experience < trait_def.min_experience:
                return False, f"Requires {trait_def.min_experience}+ years experience (player has {player_experience})"

        # Check stat thresholds
        if trait_def.min_stat_threshold:
            for stat_name, min_value in trait_def.min_stat_threshold.items():
                player_stat = getattr(player, stat_name, 0)
                if player_stat < min_value:
                    return False, f"Requires {min_value}+ {stat_name} (player has {player_stat})"

        return True, "Eligible"

    @staticmethod
    def check_crunch_time(context: dict[str, Any]) -> bool:
        """
        Determine if the game is in "Crunch Time" for The Closer trait activation.

        Crunch Time conditions (ANY of the following):
        - 4th Quarter with less than 5 minutes remaining AND score within 8 points
        - Overtime period

        Args:
            context: Game context with keys:
                - quarter: int (1-4, 5+ for OT)
                - time_remaining: float (seconds remaining in quarter)
                - score_differential: int (absolute difference in score)

        Returns:
            True if crunch time conditions are met
        """
        quarter = context.get("quarter", 1)
        time_remaining = context.get("time_remaining", 900)  # Default 15 min
        score_diff = abs(context.get("score_differential", 0))

        # Overtime is always crunch time
        if quarter >= 5:
            return True

        # 4th quarter with < 5 min AND close game (within 8 points)
        if quarter == 4 and time_remaining <= 300 and score_diff <= 8:
            return True

        return False

    @staticmethod
    def check_trait_activation(
        trait_def: TraitDefinition,
        context: dict[str, Any]
    ) -> bool:
        """
        Check if a trait is active given the game context.
        Context should contain keys like 'triggers': ['PASS_PLAY', 'RED_ZONE'], etc.
        """
        if not trait_def or not trait_def.activation_triggers:
            return False

        # Always-active traits
        if "ALWAYS" in trait_def.activation_triggers or "ON_FIELD" in trait_def.activation_triggers:
            return True

        # Special case: CRUNCH_TIME trigger (The Closer)
        if "CRUNCH_TIME" in trait_def.activation_triggers:
            if TraitService.check_crunch_time(context):
                return True

        # Check if any context triggers match trait triggers
        context_triggers = context.get("triggers", [])
        for trigger in trait_def.activation_triggers:
            if trigger in context_triggers:
                return True

        return False

    @staticmethod
    def apply_trait_effects(
        player: Player,
        trait_def: TraitDefinition,
        context: dict[str, Any] = None
    ) -> dict[str, float]:
        """
        Apply trait effects to a player's attributes.
        Returns the effects that were applied.
        """
        if not trait_def:
            return {}

        # Initialize player modifiers if needed
        if not hasattr(player, "active_modifiers"):
            player.active_modifiers = {}
        if not hasattr(player, "active_traits"):
            player.active_traits = []

        # Track active trait
        if trait_def.name not in player.active_traits:
            player.active_traits.append(trait_def.name)

        # Apply each effect
        for effect_key, effect_value in trait_def.effects.items():
            # Accumulate effects (don't overwrite)
            current = player.active_modifiers.get(effect_key, 0)
            player.active_modifiers[effect_key] = current + effect_value

        return trait_def.effects
