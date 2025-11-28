import math

class ProgressionEngine:
    @staticmethod
    def calculate_xp_gain(stats: dict, position: str) -> int:
        """
        Calculate XP gained from a game based on stats and position.
        """
        xp = 0
        
        # General Playtime XP
        xp += 50 
        
        if position == "QB":
            xp += stats.get("pass_tds", 0) * 50
            xp += stats.get("pass_yards", 0) * 0.5
            xp -= stats.get("pass_ints", 0) * 20
        elif position == "RB":
            xp += stats.get("rush_tds", 0) * 40
            xp += stats.get("rush_yards", 0) * 0.8
        elif position == "DE" or position == "DT":
            xp += stats.get("sacks", 0) * 100
            xp += stats.get("tackles_for_loss", 0) * 30
            
        return int(max(0, xp))

    @staticmethod
    def check_level_up(current_xp: int, current_level: int) -> bool:
        """
        Check if XP threshold is met.
        Threshold = 1000 * Level * 1.2
        """
        threshold = 1000 * current_level * 1.2
        return current_xp >= threshold

    @staticmethod
    def apply_regression(age: int, attributes: dict) -> dict:
        """
        Apply age-based regression to physical stats.
        """
        if age < 29:
            return attributes
            
        regression_factor = (age - 28) * 0.5 # -0.5 per year after 28
        
        for attr in ["speed", "acceleration", "agility"]:
            if attr in attributes:
                attributes[attr] = max(10, attributes[attr] - regression_factor)
                
        return attributes
