from app.kernels.core.ecs_manager import Component

class OwnerMandateAI(Component):
    current_mandate: str = "Rebuild"
    patience: int = 50 # 0-100

    def evaluate_season(self, wins: int, playoff_result: str):
        if self.current_mandate == "Win Now":
            if wins < 10:
                self.patience -= 20
        elif self.current_mandate == "Rebuild":
            if wins > 4:
                self.patience += 10 # Progress shown

