"""
TraitEvolutionService - The Law of Interconnectivity

This service implements dynamic trait acquisition and loss based on in-game events.
It subscribes to EventBus and checks if any events trigger trait changes.

Examples:
- 3+ injuries in a season -> "Injury Prone" trait
- 5+ sacks in a game -> Defender earns "Dominant Pass Rusher" badge
- Loss of 3+ fumbles -> "Butterfingers" trait
- QB throws 4+ TDs in a game -> "Gunslinger" trait boost
"""

from sqlalchemy.orm import Session

from app.engine.event_bus import EventBus, EventType
from app.models.rpg_event import RPGEvent
from app.models.trait import PlayerTrait, Trait, TraitSource, TraitTier

# Trait Trigger Definitions
# Format: { trigger_key: { threshold, trait_name, tier, is_positive } }
TRAIT_TRIGGERS = {
    "injuries_in_season": {
        "threshold": 3,
        "trait_name": "Injury Prone",
        "tier": TraitTier.BRONZE,
        "is_positive": False,
        "description": "This player has a history of injuries.",
    },
    "sacks_in_game": {
        "threshold": 3,
        "trait_name": "Dominant Pass Rusher",
        "tier": TraitTier.SILVER,
        "is_positive": True,
        "description": "An elite pass rusher who can take over games.",
    },
    "fumbles_in_season": {
        "threshold": 3,
        "trait_name": "Butterfingers",
        "tier": TraitTier.BRONZE,
        "is_positive": False,
        "description": "Has a tendency to fumble in critical moments.",
    },
    "tds_in_game": {
        "threshold": 4,
        "trait_name": "Gunslinger",
        "tier": TraitTier.GOLD,
        "is_positive": True,
        "description": "A fearless QB who can light up the scoreboard.",
    },
    "dropped_passes_in_game": {
        "threshold": 3,
        "trait_name": "Stone Hands",
        "tier": TraitTier.BRONZE,
        "is_positive": False,
        "description": "Has trouble catching the ball under pressure.",
    },
    "spectacular_catches_in_season": {
        "threshold": 5,
        "trait_name": "Highlight Reel",
        "tier": TraitTier.SILVER,
        "is_positive": True,
        "description": "Makes acrobatic catches that define games.",
    },
}


class TraitEvolutionService:
    """
    Monitors player performance and dynamically awards or removes traits.
    """

    def __init__(self):
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        """Subscribe to relevant gameplay events."""
        # We'll process events after each game, not on every play
        # This is handled by the orchestrator calling check_trait_triggers
        pass

    def check_trait_triggers(
        self,
        db: Session,
        player_id: int,
        season_id: int,
        week: int | None = None,
        game_id: str | None = None,
    ) -> list[dict]:
        """
        Check if a player has triggered any new traits based on their RPG event history.

        Args:
            db: Database session
            player_id: The player to check
            season_id: Current season
            week: Optional week filter (for game-specific triggers)
            game_id: Optional game filter (for game-specific triggers)

        Returns:
            List of triggered traits: [{"trait_name": str, "action": "EARNED" | "LOST"}]
        """
        triggered = []

        # Build query for this player's events
        query = db.query(RPGEvent).filter(
            RPGEvent.player_id == player_id, RPGEvent.season_id == season_id
        )

        if game_id:
            query = query.filter(RPGEvent.game_id == game_id)

        events = query.all()

        # Count events by type
        event_counts = {}
        for event in events:
            event_type = event.event_type
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        # Check each trigger
        if game_id:
            # Game-specific triggers
            triggered.extend(self._check_game_triggers(db, player_id, event_counts))
        else:
            # Season-wide triggers
            triggered.extend(self._check_season_triggers(db, player_id, event_counts))

        return triggered

    def _check_game_triggers(
        self, db: Session, player_id: int, counts: dict[str, int]
    ) -> list[dict]:
        """Check game-specific trait triggers."""
        triggered = []

        # Sacks in game
        sack_count = counts.get(EventType.SACK_EVENT, 0)
        if sack_count >= TRAIT_TRIGGERS["sacks_in_game"]["threshold"]:
            result = self._award_trait(db, player_id, "sacks_in_game")
            if result:
                triggered.append(result)

        # TDs in game
        td_count = counts.get(EventType.TOUCHDOWN_EVENT, 0)
        if td_count >= TRAIT_TRIGGERS["tds_in_game"]["threshold"]:
            result = self._award_trait(db, player_id, "tds_in_game")
            if result:
                triggered.append(result)

        # Dropped passes in game
        drop_count = counts.get(EventType.DROPPED_PASS, 0)
        if drop_count >= TRAIT_TRIGGERS["dropped_passes_in_game"]["threshold"]:
            result = self._award_trait(db, player_id, "dropped_passes_in_game")
            if result:
                triggered.append(result)

        return triggered

    def _check_season_triggers(
        self, db: Session, player_id: int, counts: dict[str, int]
    ) -> list[dict]:
        """Check season-wide trait triggers."""
        triggered = []

        # Injuries in season
        injury_count = counts.get(EventType.PLAYER_INJURED, 0)
        if injury_count >= TRAIT_TRIGGERS["injuries_in_season"]["threshold"]:
            result = self._award_trait(db, player_id, "injuries_in_season")
            if result:
                triggered.append(result)

        # Fumbles in season
        fumble_count = counts.get(EventType.CRITICAL_FUMBLE, 0) + counts.get(
            EventType.TURNOVER_EVENT, 0
        )
        if fumble_count >= TRAIT_TRIGGERS["fumbles_in_season"]["threshold"]:
            result = self._award_trait(db, player_id, "fumbles_in_season")
            if result:
                triggered.append(result)

        # Spectacular catches in season
        catch_count = counts.get(EventType.SPECTACULAR_CATCH, 0)
        if catch_count >= TRAIT_TRIGGERS["spectacular_catches_in_season"]["threshold"]:
            result = self._award_trait(db, player_id, "spectacular_catches_in_season")
            if result:
                triggered.append(result)

        return triggered

    def _award_trait(self, db: Session, player_id: int, trigger_key: str) -> dict | None:
        """
        Award a trait to a player if they don't already have it.

        Returns:
            Dict with trait info if awarded, None if already had trait
        """
        trigger = TRAIT_TRIGGERS[trigger_key]
        trait_name = trigger["trait_name"]

        # Check if trait exists in DB, create if not
        trait = db.query(Trait).filter(Trait.name == trait_name).first()
        if not trait:
            trait = Trait(
                name=trait_name,
                description=trigger["description"],
                tier=trigger["tier"],
                is_badge=True,
            )
            db.add(trait)
            db.flush()

        # Check if player already has this trait
        existing = (
            db.query(PlayerTrait)
            .filter(PlayerTrait.player_id == player_id, PlayerTrait.trait_id == trait.id)
            .first()
        )

        if existing:
            return None  # Already has trait

        # Award the trait
        player_trait = PlayerTrait(
            player_id=player_id, trait_id=trait.id, source=TraitSource.DEVELOPMENT
        )
        db.add(player_trait)

        # Publish event
        EventBus.publish(
            EventType.BADGE_EARNED,
            {
                "player_id": player_id,
                "badge_name": trait_name,
                "tier": trigger["tier"].value,
                "is_positive": trigger["is_positive"],
            },
        )

        db.commit()

        return {"trait_name": trait_name, "action": "EARNED", "tier": trigger["tier"].value}

    def remove_trait(self, db: Session, player_id: int, trait_name: str) -> dict | None:
        """
        Remove a trait from a player.
        Useful for traits that can be "un-earned" (e.g., player improves ball security).
        """
        trait = db.query(Trait).filter(Trait.name == trait_name).first()
        if not trait:
            return None

        player_trait = (
            db.query(PlayerTrait)
            .filter(PlayerTrait.player_id == player_id, PlayerTrait.trait_id == trait.id)
            .first()
        )

        if not player_trait:
            return None

        db.delete(player_trait)

        EventBus.publish(EventType.BADGE_LOST, {"player_id": player_id, "badge_name": trait_name})

        db.commit()

        return {"trait_name": trait_name, "action": "LOST"}


trait_evolution_service = TraitEvolutionService()
