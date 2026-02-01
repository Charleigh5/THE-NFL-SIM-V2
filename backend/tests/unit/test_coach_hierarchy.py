from app.models.coach import CoachTier
from app.services.training.coach_expertise import (
    CoachArchetype,
    calculate_development_bonus,
    calculate_tier_from_ratings,
    get_archetype_bonus,
    get_position_development_summary,
    get_scheme_bonus,
    get_tier_multiplier,
)


class TestCoachTierSystem:
    """Tests for the coaching tier system."""

    def test_tier_calculation_legend(self):
        """Legend tier requires 270+ combined rating."""
        tier = calculate_tier_from_ratings(95, 90, 90)  # 275
        assert tier == CoachTier.LEGEND

    def test_tier_calculation_elite(self):
        """Elite tier: 230-269."""
        tier = calculate_tier_from_ratings(85, 80, 80)  # 245
        assert tier == CoachTier.ELITE

    def test_tier_calculation_veteran(self):
        """Veteran tier: 180-229."""
        tier = calculate_tier_from_ratings(70, 70, 70)  # 210
        assert tier == CoachTier.VETERAN

    def test_tier_calculation_developing(self):
        """Developing tier: 140-179."""
        tier = calculate_tier_from_ratings(55, 55, 55)  # 165
        assert tier == CoachTier.DEVELOPING

    def test_tier_calculation_rookie(self):
        """Rookie tier: <140."""
        tier = calculate_tier_from_ratings(40, 40, 40)  # 120
        assert tier == CoachTier.ROOKIE

    def test_tier_multipliers(self):
        """Verify tier multiplier values."""
        assert get_tier_multiplier(CoachTier.LEGEND) == 1.50
        assert get_tier_multiplier(CoachTier.ELITE) == 1.30
        assert get_tier_multiplier(CoachTier.VETERAN) == 1.10
        assert get_tier_multiplier(CoachTier.DEVELOPING) == 1.00
        assert get_tier_multiplier(CoachTier.ROOKIE) == 0.90


class TestSchemeExpertise:
    """Tests for scheme-based development bonuses."""

    def test_west_coast_qb_bonus(self):
        """West Coast offense gives 15% QB bonus."""
        bonus = get_scheme_bonus("West Coast", "QB")
        assert bonus == 0.15

    def test_west_coast_wr_bonus(self):
        """West Coast offense gives 15% WR bonus."""
        bonus = get_scheme_bonus("West Coast", "WR")
        assert bonus == 0.15

    def test_power_run_rb_bonus(self):
        """Power Run gives 18% RB bonus."""
        bonus = get_scheme_bonus("Power Run", "RB")
        assert bonus == 0.18

    def test_four_three_de_bonus(self):
        """4-3 defense gives 15% DE bonus."""
        bonus = get_scheme_bonus("4-3", "DE")
        assert bonus == 0.15

    def test_no_scheme_match(self):
        """No bonus for non-matching positions."""
        bonus = get_scheme_bonus("West Coast", "CB")
        assert bonus == 0.0

    def test_unknown_scheme(self):
        """Unknown scheme returns 0."""
        bonus = get_scheme_bonus("Unknown Scheme", "QB")
        assert bonus == 0.0


class TestArchetypes:
    """Tests for coach archetype bonuses."""

    def test_qb_guru_qb_bonus(self):
        """QB Guru gives 25% QB bonus."""
        bonus = get_archetype_bonus(CoachArchetype.QB_GURU, "QB")
        assert bonus == 0.25

    def test_qb_guru_wr_secondary(self):
        """QB Guru gives secondary WR bonus."""
        bonus = get_archetype_bonus(CoachArchetype.QB_GURU, "WR")
        assert bonus == 0.10

    def test_ol_master_bonus(self):
        """OL Master gives 25% OL bonus."""
        bonus = get_archetype_bonus(CoachArchetype.OL_MASTER, "OL")
        assert bonus == 0.25

    def test_generalist_no_bonus(self):
        """Generalist has no specific bonuses."""
        bonus = get_archetype_bonus(CoachArchetype.GENERALIST, "QB")
        assert bonus == 0.0


class TestDevelopmentCalculation:
    """Tests for combined development bonus calculation."""

    def test_legend_qb_guru_west_coast_qb(self):
        """
        Legend QB Guru with West Coast = massive QB development.
        1.50 * (1.0 + 0.15 + 0.25) = 1.50 * 1.40 = 2.10 -> capped at 2.0
        """
        bonus = calculate_development_bonus(
            coach_tier=CoachTier.LEGEND,
            offensive_scheme="West Coast",
            defensive_scheme=None,
            archetype=CoachArchetype.QB_GURU,
            player_position="QB"
        )
        assert bonus == 2.0  # Capped

    def test_rookie_generalist(self):
        """Rookie generalist with no scheme = below baseline."""
        bonus = calculate_development_bonus(
            coach_tier=CoachTier.ROOKIE,
            offensive_scheme=None,
            defensive_scheme=None,
            archetype=CoachArchetype.GENERALIST,
            player_position="QB"
        )
        assert bonus == 0.90

    def test_elite_with_scheme_match(self):
        """Elite coach with scheme match gets combined bonus."""
        bonus = calculate_development_bonus(
            coach_tier=CoachTier.ELITE,
            offensive_scheme="Power Run",
            defensive_scheme=None,
            archetype=CoachArchetype.RUN_GAME_SPECIALIST,
            player_position="RB"
        )
        # 1.30 * (1.0 + 0.18 + 0.25) = 1.30 * 1.43 = 1.859
        assert 1.85 < bonus < 1.90

    def test_position_summary(self):
        """Get all position bonuses for a coach."""
        summary = get_position_development_summary(
            coach_tier=CoachTier.ELITE,
            offensive_scheme="West Coast",
            defensive_scheme="4-3",
            archetype=CoachArchetype.QB_GURU
        )

        # QB should have high bonus
        assert summary["QB"] > 1.5
        # DE should have scheme bonus
        assert summary["DE"] > 1.3
        # Non-matching position should be baseline elite
        assert summary["K"] == 1.30
