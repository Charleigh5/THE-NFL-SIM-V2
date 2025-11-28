from app.kernels.core.ecs_manager import Component
from enum import Enum
from pydantic import Field

class CrowdSentiment(Enum):
    EUPHORIC = "Euphoric"
    ANXIOUS = "Anxious"
    HOSTILE = "Hostile"
    DEAD = "Dead"

class CrowdNet(Component):
    # Directive 3: Crowd Sentiment State Machine
    sentiment: CrowdSentiment = CrowdSentiment.ANXIOUS
    decibel_level: float = 85.0 # Base level
    momentum_meter: float = 50.0 # 0-100 (50 is neutral)

    def update_sentiment(self, home_score: int, away_score: int, big_play: bool):
        score_diff = home_score - away_score
        
        if big_play:
            self.decibel_level = min(120.0, self.decibel_level + 15.0)
            self.momentum_meter += 10.0
        else:
            # Decay
            self.decibel_level = max(70.0, self.decibel_level - 1.0)

        # State Machine Logic
        if self.decibel_level > 105.0:
            self.sentiment = CrowdSentiment.HOSTILE if score_diff < 0 else CrowdSentiment.EUPHORIC
        elif score_diff < -14:
            self.sentiment = CrowdSentiment.DEAD
        else:
            self.sentiment = CrowdSentiment.ANXIOUS

    def get_communication_jamming(self) -> float:
        """
        Directive 4: Communication Jamming.
        Returns % chance of audibles failing.
        """
        if self.decibel_level > 105.0:
            return (self.decibel_level - 105.0) * 2.0 # 110dB = 10% fail, 115dB = 20% fail
        return 0.0

    def get_momentum_drain(self) -> float:
        """
        Directive 10: Momentum Draining.
        Hostile crowds drain away team stamina/composure.
        """
        if self.sentiment == CrowdSentiment.HOSTILE:
            return 0.05 # 5% drain per play
        return 0.0
