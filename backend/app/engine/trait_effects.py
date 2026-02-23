from typing import Any

from app.models.player import Player


class TraitEffectResolver:
    """
    Resolves complex trait effects that go beyond simple attribute modifiers.
    Handles team-wide buffs, opponent debuffs, and situational logic.
    """

    @staticmethod
    def resolve_team_wide_traits(
        offense: list[Player], defense: list[Player], context: dict[str, Any]
    ) -> dict[str, float]:
        """
        Scan for traits that affect the entire unit (e.g. Field General).
        Returns a dictionary of aggregated modifiers.
        """
        modifiers = {
            "offense_awareness_boost": 0.0,
            "defense_reaction_boost": 0.0,
            "penalty_chance_multiplier": 1.0,
        }

        # Check Offense
        for player in offense:
            # We assume active traits are already loaded or we check defining traits
            # For now, let's assume we check the catalog for known traits if checking directly
            # Or better, we check if the player has the trait assigned.

            # Since we don't have the full PlayerTrait objects here easily without DB query
            # We will rely on what's passed in the player object (conceptually)
            # Or we iterate specific positions known to have leaders.

            # QB Field General Check
            if player.position == "QB":
                # How do we know if he has Field General?
                # In a real run, this data should be pre-loaded.
                # Let's assume player.traits is a list of trait names or definitions.
                pass

        return modifiers

    @staticmethod
    def apply_field_general_boost(offense: list[Player], qb: Player) -> dict[str, float]:
        """
        Apply Field General boost if QB has it.
        """
        results = {}
        # In a real implementation, we'd check `qb.has_trait("Field General")`
        # But for now, we'll assume the caller determines eligibility or we check a property

        # Effect: Boost all offensive players' awareness
        for player in offense:
            if player.id != qb.id:
                # Boost awareness (in-memory only for this play)
                current = getattr(player, "awareness", 50)
                player.awareness_boosted = current + 5

        results["team_awareness_boost"] = 5.0
        results["penalty_chance_multiplier"] = 0.85
        return results

    @staticmethod
    def apply_green_dot_effects(defense: list[Player]) -> dict[str, float]:
        """
        Apply Green Dot (Defensive Captain) boost.
        Boosts Play Recognition for all defenders.
        """
        results = {}
        # Locate the captain (usually MLB/LB with the trait)
        captain = next(
            (p for p in defense if "Green Dot" in (getattr(p, "active_traits", []) or [])), None
        )

        if captain:
            for player in defense:
                if player.id != captain.id:
                    current_pr = getattr(player, "play_recognition", 50)
                    player.play_recognition_boosted = current_pr + 5

            results["team_play_recognition_boost"] = 5.0
            results["blown_coverage_reduction"] = 0.20

        return results

    @staticmethod
    def apply_pick_artist_effects(defender: Player, ball_in_air: bool = False) -> dict[str, float]:
        """
        Apply Pick Artist effects during interception opportunities.
        """
        results = {}
        if "Pick Artist" in (getattr(defender, "active_traits", []) or []):
            if ball_in_air:
                results["interception_chance_multiplier"] = 1.50
                results["catch_radius_boost"] = 0.30
                # Reduce drop chance for INTs
                results["int_drop_chance_reduction"] = 0.50
        return results

    @staticmethod
    def apply_chip_block_effects(rb: Player, is_blocking: bool = False) -> dict[str, float]:
        """
        Apply Chip Block Specialist effects for RBs in pass protection.
        """
        results = {}
        if "Chip Block Specialist" in (getattr(rb, "active_traits", []) or []) and is_blocking:
            results["pass_pro_rating_boost"] = 10.0  # Aligned with attribute_interaction.py
            results["edge_rusher_slow_effect"] = 0.15  # 15% slower edge rush acceleration
        return results

    @staticmethod
    def apply_possession_receiver_effects(
        receiver: Player, down: int, yards_to_go: int
    ) -> dict[str, float]:
        """
        Apply Possession Receiver effects on 3rd/4th down or critical situations.
        """
        results = {}
        is_critical_down = down >= 3

        if (
            "Possession Receiver" in (getattr(receiver, "active_traits", []) or [])
            and is_critical_down
        ):
            results["catch_in_traffic_boost"] = 15.0
            results["drop_chance_reduction"] = 0.30
            results["contest_catch_win_rate"] = 0.25

        return results

    @staticmethod
    def cleanup_boosts(players: list[Player]):
        """Remove temporary boosts."""
        for player in players:
            if hasattr(player, "awareness_boosted"):
                delattr(player, "awareness_boosted")
            if hasattr(player, "play_recognition_boosted"):
                delattr(player, "play_recognition_boosted")
