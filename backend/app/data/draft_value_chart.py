from app.core.trade_config import trade_config


class DraftValueChart:
    """
    Implementation of the Fitzgerald-Spielberger draft value chart (2024).
    Used for valuing draft picks in trade scenarios.

    Source Methodology: OverTheCap (OTC) / Fitzgerald-Spielberger
    """

    # Key anchor points for the 2024 Fitzgerald-Spielberger chart
    # We interpolate between these points for full coverage
    _ANCHOR_VALUES = {
        1: 3000,
        2: 2649,
        3: 2443,
        4: 2297,
        5: 2184,
        6: 2091,
        7: 2011,
        8: 1941,
        9: 1878,
        10: 1821,
        11: 1769,
        12: 1721,
        16: 1595,
        20: 1492,
        24: 1403,
        32: 1244,
        # Round 2
        33: 1234,
        48: 1047,
        64: 895,
        # Round 3
        65: 885,
        80: 765,
        96: 668,
        # Round 4
        97: 661,
        112: 580,
        128: 510,
        # Round 5
        129: 506,
        144: 437,
        160: 380,
        # Round 6
        161: 377,
        176: 317,
        192: 268,
        # Round 7
        193: 264,
        208: 218,
        224: 177,
        256: 100,
    }

    # Cache for interpolated values
    _FULL_CHART: dict[int, int] = {}

    @classmethod
    def _initialize_chart(cls):
        """Interpolates values between anchor points to create full 1-256 chart."""
        if cls._FULL_CHART:
            return

        sorted_picks = sorted(cls._ANCHOR_VALUES.keys())

        for i in range(len(sorted_picks) - 1):
            start_pick = sorted_picks[i]
            end_pick = sorted_picks[i + 1]
            start_val = cls._ANCHOR_VALUES[start_pick]
            end_val = cls._ANCHOR_VALUES[end_pick]

            # Fill exact start point
            cls._FULL_CHART[start_pick] = start_val

            # Linear interpolation for points in between
            steps = end_pick - start_pick
            if steps > 0:
                val_step = (end_val - start_val) / steps
                for offset in range(1, steps):
                    pick_num = start_pick + offset
                    val = int(start_val + (val_step * offset))
                    cls._FULL_CHART[pick_num] = val

        # Ensure last point is set
        cls._FULL_CHART[256] = cls._ANCHOR_VALUES[256]

    @classmethod
    def get_pick_value(cls, overall_pick: int) -> int:
        """
        Get the base value of a draft pick for the current year.
        Applies Top-10 premium tax automatically.
        """
        if not cls._FULL_CHART:
            cls._initialize_chart()

        # Clamp to valid range
        overall_pick = max(1, min(256, overall_pick))
        base_value = cls._FULL_CHART.get(overall_pick, 10)

        # Apply Premium Tax for Top 10 Picks
        if overall_pick <= 10:
            return int(base_value * trade_config.TOP_10_PICK_PREMIUM)

        return base_value

    @classmethod
    def get_future_pick_value(
        cls, round_num: int, years_in_future: int, team_standing_rank: int = 16
    ) -> int:
        """
        Calculate value for a future draft pick.

        Rules:
        1. Base value estimated middle of round (pick 16 of round).
        2. Future Discount: Value drops ~1 round per year.
        3. Max 3 years out constraint.
        4. Team Standing modifier (if known/projected).
        """
        # Rule: Restrict trading > 3 years out
        if years_in_future > trade_config.MAX_FUTURE_PICK_YEARS:
            raise ValueError(
                f"Cannot value picks more than {trade_config.MAX_FUTURE_PICK_YEARS} years out."
            )

        if years_in_future < 0:
            years_in_future = 0

        # Effective round calculation (The "One Round Per Year" Rule)
        # e.g. A 2026 1st (1 year out) ~= 2025 2nd
        # We model this by decaying the value, not literally changing the round number for lookup,
        # but conceptually mapped to that value tier.

        # Methodology:
        # Year 0: 1st Round Value (~1000-3000)
        # Year 1: 2nd Round Value (~500-1200)
        # Year 2: 3rd Round Value (~250-800)
        # Rough decay factor valid approx: 0.4x to 0.5x per year for premium rounds

        # Using Fitzgerald-Spielberger Discount Rate:
        # A clearer analytic approach is discounting by fixed rate per year.
        # FS standard discount is often cited around 10-20% for financial reasons,
        # but in trade value ("Bird in hand"), the "One Round" heuristic is stronger.
        # Let's use the explicit "Round Devaluation" method as requested.

        effective_round = round_num + years_in_future
        if effective_round > 7:
            return 15  # Minimal value for distant late picks

        # Get base value for mid-round pick of that effective round
        # Est. Pick # = ((Round-1) * 32) + 16
        mid_round_pick = ((effective_round - 1) * 32) + 16
        value = cls.get_pick_value(mid_round_pick)

        return value

    @staticmethod
    def validate_trade_eligibility(pick_year: int, current_year: int = 2025) -> bool:
        """Validates if a pick is within the allowed trading window."""
        return (pick_year - current_year) <= trade_config.MAX_FUTURE_PICK_YEARS
