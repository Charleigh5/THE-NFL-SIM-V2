import random

class NarrativeEngine:
    EVENTS = [
        {
            "id": "locker_room_drama",
            "title": "Locker Room Drama",
            "description": "Two star players are feuding over targets.",
            "choices": [
                {"text": "Side with Player A", "effect": {"morale_a": 10, "morale_b": -20}},
                {"text": "Side with Player B", "effect": {"morale_a": -20, "morale_b": 10}},
                {"text": "Fine both", "effect": {"morale_team": -5, "discipline": 10}}
            ]
        },
        {
            "id": "media_circus",
            "title": "Media Circus",
            "description": "The local media is questioning your playcalling.",
            "choices": [
                {"text": "Defend strategy", "effect": {"fan_support": -5, "owner_trust": 5}},
                {"text": "Admit mistakes", "effect": {"fan_support": 5, "owner_trust": -5}}
            ]
        }
    ]
    
    @staticmethod
    def generate_weekly_event(team_morale: int, win_streak: int) -> dict:
        """
        Generate a random narrative event based on context.
        """
        if team_morale < 30:
            return NarrativeEngine.EVENTS[0] # Drama likely
        
        if random.random() < 0.1:
            return random.choice(NarrativeEngine.EVENTS)
            
        return None
