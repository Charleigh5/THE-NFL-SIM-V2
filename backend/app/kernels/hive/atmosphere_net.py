from app.kernels.core.ecs_manager import Component
import enum

class CrowdSentiment(str, enum.Enum):
    EUPHORIC = "Euphoric"
    ANXIOUS = "Anxious"
    HOSTILE = "Hostile"
    SILENT = "Silent"

class CrowdSentimentMachine(Component):
    sentiment: CrowdSentiment = CrowdSentiment.ANXIOUS
    decibels: float = 85.0
    momentum: float = 50.0 # 0-100 (Home Team advantage)

    def update_sentiment(self, home_score: int, away_score: int, big_play: bool):
        diff = home_score - away_score
        
        if big_play:
            self.momentum += 10
            self.decibels += 15
            
        if diff > 14:
            self.sentiment = CrowdSentiment.EUPHORIC
            self.decibels = max(self.decibels, 100)
        elif diff < -14:
            self.sentiment = CrowdSentiment.SILENT
            self.decibels = 70
        elif diff < 0:
            self.sentiment = CrowdSentiment.ANXIOUS
            self.decibels = 90
            
        # Decay
        self.decibels = max(70, self.decibels - 0.5)

class MomentumPressureValve(Component):
    def check_cognitive_penalty(self, decibels: float) -> bool:
        # >105dB disables hot routes / increases confusion
        return decibels > 105

