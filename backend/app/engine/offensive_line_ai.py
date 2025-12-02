from typing import Dict, List, Any
from app.engine.event_bus import EventBus, EventType

class OffensiveLineAI:
    def __init__(self):
        self.active_debuffs: Dict[str, Dict[str, Any]] = {} # player_id -> {value: int, duration: int}
        EventBus.subscribe(EventType.SACK_EVENT, self.handle_sack_event)

    def handle_sack_event(self, payload: Dict[str, Any]):
        """
        Handle SACK_EVENT by applying intimidation debuffs to beaten linemen.
        """
        beaten_linemen_ids = payload.get("beaten_linemen_ids", [])
        intimidation_factor = payload.get("intimidation_factor", 1.0) # From defender trait

        for player_id in beaten_linemen_ids:
            # Apply debuff
            # Base debuff is -5, scaled by intimidation
            debuff_value = -5 * intimidation_factor
            duration = 3 # Lasts for 3 plays

            # Store or update debuff
            self.active_debuffs[player_id] = {
                "pass_block_modifier": debuff_value,
                "duration": duration
            }
            print(f"DEBUG: Applied intimidation debuff to OL {player_id}: {debuff_value} for {duration} plays")

    def get_player_modifier(self, player_id: str) -> int:
        """
        Get the current pass_block modifier for a player.
        """
        if player_id in self.active_debuffs:
            return self.active_debuffs[player_id]["pass_block_modifier"]
        return 0

    def decrement_debuffs(self):
        """
        Call this after every play to reduce the duration of active debuffs.
        """
        to_remove = []
        for player_id, debuff in self.active_debuffs.items():
            debuff["duration"] -= 1
            if debuff["duration"] <= 0:
                to_remove.append(player_id)

        for player_id in to_remove:
            del self.active_debuffs[player_id]
