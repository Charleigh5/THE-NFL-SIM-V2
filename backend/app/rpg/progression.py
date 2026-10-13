class ProgressionEngine:
    """
    RPG Progression Engine for player XP calculation and leveling.

    XP Formulas follow industry best practices from Madden/2K:
    - Position-specific XP multipliers
    - Performance-based rewards (positive actions add XP)
    - Penalty-based deductions (negative actions subtract XP)
    - Specialists (K/P) have lower base XP but high multipliers
    """

    @staticmethod
    def calculate_xp_gain(stats: dict, position: str) -> int:
        """
        Calculate XP gained from a game based on stats and position.

        Args:
            stats: Dictionary of game statistics
            position: Player's position (QB, RB, WR, etc.)

        Returns:
            Integer XP gained (minimum 0)
        """
        xp = 0

        # General Playtime XP - base reward for participating
        base_xp = 50 if position not in ["K", "P"] else 20
        xp += base_xp

        if position == "QB":
            # QB: High value on TDs and yards, penalty for INTs
            xp += stats.get("pass_tds", 0) * 50
            xp += stats.get("pass_yards", 0) * 0.5
            xp -= stats.get("pass_ints", 0) * 20
            # Bonus for rushing production
            xp += stats.get("rush_yards", 0) * 0.3
            xp += stats.get("rush_tds", 0) * 30

        elif position == "RB":
            # RB: Rushing and receiving production
            xp += stats.get("rush_tds", 0) * 40
            xp += stats.get("rush_yards", 0) * 0.8
            # Bonus for receiving (dual-threat backs)
            xp += stats.get("receptions", 0) * 3
            xp += stats.get("rec_yards", 0) * 0.4
            xp += stats.get("rec_tds", 0) * 30
            # Fumble penalty
            xp -= stats.get("fumbles", 0) * 25

        elif position in ["WR", "TE"]:
            # WR/TE: Reception-based XP
            xp += stats.get("rec_yards", 0) * 0.8
            xp += stats.get("rec_tds", 0) * 40
            xp += stats.get("receptions", 0) * 5
            # Drops hurt development
            xp -= stats.get("drops", 0) * 10

        elif position == "LB":
            # LB: Versatile defender - tackles, sacks, and coverage
            xp += stats.get("sacks", 0) * 100
            xp += stats.get("tackles_for_loss", 0) * 30
            xp += stats.get("tackles", 0) * 2
            xp += stats.get("interceptions", 0) * 40
            xp += stats.get("passes_defended", 0) * 8
            xp += stats.get("forced_fumbles", 0) * 25

        elif position in ["DE", "DT"]:
            # DL: Sacks and disruption
            xp += stats.get("sacks", 0) * 100
            xp += stats.get("tackles_for_loss", 0) * 30
            xp += stats.get("tackles", 0) * 1
            xp += stats.get("qb_hits", 0) * 15
            xp += stats.get("forced_fumbles", 0) * 25

        elif position in ["CB", "S"]:
            # DB: Coverage stats and opportunistic plays
            xp += stats.get("interceptions", 0) * 50
            xp += stats.get("passes_defended", 0) * 10
            xp += stats.get("tackles", 0) * 2
            xp += stats.get("forced_fumbles", 0) * 25
            # Penalty for big plays allowed
            xp -= stats.get("tds_allowed", 0) * 15

        elif position in ["OT", "OG", "C"]:
            # OL: Run blocking and pass protection
            xp += stats.get("pancakes", 0) * 10
            xp += stats.get("knockdowns", 0) * 5
            # Penalties for negative plays
            xp -= stats.get("sacks_allowed", 0) * 10
            xp -= stats.get("qb_hits_allowed", 0) * 5
            xp -= stats.get("penalties", 0) * 8

        elif position == "K":
            # K: Field goal production (lower base XP)
            xp += stats.get("fg_made", 0) * 20
            xp += stats.get("fg_long", 0) * 0.5
            xp += stats.get("xp_made", 0) * 2
            # Penalty for misses
            xp -= stats.get("fg_missed", 0) * 15
            xp -= stats.get("xp_missed", 0) * 10

        elif position == "P":
            # P: Punting production (lower base XP)
            xp += stats.get("punts_inside_20", 0) * 10
            xp += stats.get("avg_punt_yards", 0) * 0.5
            # Penalty for touchbacks
            xp -= stats.get("touchbacks", 0) * 5

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

        regression_factor = (age - 28) * 0.5  # -0.5 per year after 28

        for attr in ["speed", "acceleration", "agility"]:
            if attr in attributes:
                attributes[attr] = max(10, attributes[attr] - regression_factor)

        return attributes
