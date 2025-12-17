"""
Test XP Formulas - Unit Tests for ProgressionEngine
=====================================================

Tests follow industry best practices:
- AAA Pattern (Arrange, Act, Assert)
- Parameterized tests for multiple scenarios
- Descriptive test names
- Edge case coverage
"""
import pytest
from app.rpg.progression import ProgressionEngine


# =============================================================================
# FIXTURE: Common stats dictionaries for testing
# =============================================================================

@pytest.fixture
def empty_stats():
    """Returns an empty stats dictionary."""
    return {}


@pytest.fixture
def elite_qb_stats():
    """Returns stats for an elite QB performance."""
    return {
        "pass_tds": 4,
        "pass_yards": 350,
        "pass_ints": 0,
        "rush_yards": 25,
        "rush_tds": 0
    }


@pytest.fixture
def poor_qb_stats():
    """Returns stats for a poor QB performance with multiple INTs."""
    return {
        "pass_tds": 0,
        "pass_yards": 150,
        "pass_ints": 3,
    }


# =============================================================================
# QB XP TESTS
# =============================================================================

class TestQBProgression:
    """Tests for QB XP calculation."""

    def test_qb_elite_performance_xp(self, elite_qb_stats):
        """Elite QB performance should generate high XP."""
        # Arrange - provided by fixture
        # Act
        xp = ProgressionEngine.calculate_xp_gain(elite_qb_stats, "QB")
        # Assert
        # 50 + (4*50) + (350*0.5) + (25*0.3) = 50 + 200 + 175 + 7.5 = 432
        assert xp == 432

    def test_qb_turnover_penalty(self, poor_qb_stats):
        """INTs should reduce XP earned."""
        xp = ProgressionEngine.calculate_xp_gain(poor_qb_stats, "QB")
        # 50 + (0) + (150*0.5) - (3*20) = 50 + 75 - 60 = 65
        assert xp == 65

    def test_qb_minimal_stats_gets_base_xp(self, empty_stats):
        """QB with no stats still gets base playtime XP."""
        xp = ProgressionEngine.calculate_xp_gain(empty_stats, "QB")
        assert xp == 50


# =============================================================================
# RB XP TESTS
# =============================================================================

class TestRBProgression:
    """Tests for RB XP calculation."""

    @pytest.mark.parametrize("rush_yards,rush_tds,expected_xp", [
        (100, 1, 50 + 80 + 40),           # 100 yards, 1 TD = 170 XP
        (0, 0, 50),                        # No production = base XP
        (200, 2, 50 + 160 + 80),          # 200 yards, 2 TDs = 290 XP
    ])
    def test_rb_rushing_xp(self, rush_yards, rush_tds, expected_xp):
        """RB rushing production should generate proportional XP."""
        stats = {"rush_yards": rush_yards, "rush_tds": rush_tds}
        xp = ProgressionEngine.calculate_xp_gain(stats, "RB")
        assert xp == expected_xp

    def test_rb_receiving_bonus(self):
        """Dual-threat RB with receiving should get bonus XP."""
        stats = {
            "rush_yards": 50,
            "rush_tds": 0,
            "receptions": 5,
            "rec_yards": 40,
            "rec_tds": 1
        }
        xp = ProgressionEngine.calculate_xp_gain(stats, "RB")
        # 50 + (50*0.8) + (5*3) + (40*0.4) + (1*30) = 50 + 40 + 15 + 16 + 30 = 151
        assert xp == 151

    def test_rb_fumble_penalty(self):
        """Fumbles should reduce RB XP."""
        stats = {"rush_yards": 100, "fumbles": 2}
        xp = ProgressionEngine.calculate_xp_gain(stats, "RB")
        # 50 + (100*0.8) - (2*25) = 50 + 80 - 50 = 80
        assert xp == 80


# =============================================================================
# WR/TE XP TESTS
# =============================================================================

class TestWRTEProgression:
    """Tests for WR and TE XP calculation."""

    @pytest.mark.parametrize("position", ["WR", "TE"])
    def test_wr_te_reception_xp(self, position):
        """Both WR and TE should use reception-based XP."""
        stats = {"receptions": 5, "rec_yards": 80, "rec_tds": 1}
        xp = ProgressionEngine.calculate_xp_gain(stats, position)
        # 50 + (80*0.8) + (1*40) + (5*5) = 50 + 64 + 40 + 25 = 179
        assert xp == 179

    def test_wr_drop_penalty(self):
        """Drops should reduce WR XP."""
        stats = {"receptions": 3, "rec_yards": 40, "drops": 2}
        xp = ProgressionEngine.calculate_xp_gain(stats, "WR")
        # 50 + (40*0.8) + (3*5) - (2*10) = 50 + 32 + 15 - 20 = 77
        assert xp == 77


# =============================================================================
# DEFENSIVE XP TESTS (LB, DE, DT, CB, S)
# =============================================================================

class TestDefensiveProgression:
    """Tests for defensive position XP calculation."""

    def test_lb_versatile_stats(self):
        """LB should get XP from tackles, sacks, and coverage."""
        stats = {
            "sacks": 1,
            "tackles_for_loss": 2,
            "tackles": 8,
            "interceptions": 1,
            "passes_defended": 2,
            "forced_fumbles": 1
        }
        xp = ProgressionEngine.calculate_xp_gain(stats, "LB")
        # 50 + (1*100) + (2*30) + (8*2) + (1*40) + (2*8) + (1*25)
        # = 50 + 100 + 60 + 16 + 40 + 16 + 25 = 307
        assert xp == 307

    @pytest.mark.parametrize("position", ["DE", "DT"])
    def test_dl_sack_xp(self, position):
        """DL should be rewarded heavily for sacks and TFLs."""
        stats = {"sacks": 2, "tackles_for_loss": 1, "qb_hits": 3}
        xp = ProgressionEngine.calculate_xp_gain(stats, position)
        # 50 + (2*100) + (1*30) + (3*15) = 50 + 200 + 30 + 45 = 325
        assert xp == 325

    @pytest.mark.parametrize("position", ["CB", "S"])
    def test_db_coverage_xp(self, position):
        """DB should be rewarded for coverage stats."""
        stats = {"interceptions": 1, "passes_defended": 3, "tackles": 5}
        xp = ProgressionEngine.calculate_xp_gain(stats, position)
        # 50 + (1*50) + (3*10) + (5*2) = 50 + 50 + 30 + 10 = 140
        assert xp == 140

    def test_cb_td_allowed_penalty(self):
        """CB should lose XP for TDs allowed."""
        stats = {"tackles": 2, "tds_allowed": 2}
        xp = ProgressionEngine.calculate_xp_gain(stats, "CB")
        # 50 + (2*2) - (2*15) = 50 + 4 - 30 = 24
        assert xp == 24


# =============================================================================
# OL XP TESTS
# =============================================================================

class TestOLProgression:
    """Tests for OL (OT, OG, C) XP calculation."""

    @pytest.mark.parametrize("position", ["OT", "OG", "C"])
    def test_ol_blocking_xp(self, position):
        """All OL positions should use blocking-based XP."""
        stats = {"pancakes": 3, "knockdowns": 4}
        xp = ProgressionEngine.calculate_xp_gain(stats, position)
        # 50 + (3*10) + (4*5) = 50 + 30 + 20 = 100
        assert xp == 100

    def test_ol_sack_allowed_penalty(self):
        """OL should lose XP for sacks allowed."""
        stats = {"pancakes": 1, "sacks_allowed": 2, "penalties": 1}
        xp = ProgressionEngine.calculate_xp_gain(stats, "OT")
        # 50 + (1*10) - (2*10) - (1*8) = 50 + 10 - 20 - 8 = 32
        assert xp == 32


# =============================================================================
# SPECIAL TEAMS XP TESTS (K, P)
# =============================================================================

class TestSpecialTeamsProgression:
    """Tests for K and P XP calculation with lower base XP."""

    def test_kicker_base_xp_is_lower(self, empty_stats):
        """Kicker base XP should be 20, not 50."""
        xp = ProgressionEngine.calculate_xp_gain(empty_stats, "K")
        assert xp == 20

    def test_kicker_field_goal_xp(self):
        """Kicker should get XP for made FGs."""
        stats = {"fg_made": 3, "fg_long": 52, "xp_made": 4}
        xp = ProgressionEngine.calculate_xp_gain(stats, "K")
        # 20 + (3*20) + (52*0.5) + (4*2) = 20 + 60 + 26 + 8 = 114
        assert xp == 114

    def test_kicker_miss_penalty(self):
        """Kicker should lose XP for misses."""
        stats = {"fg_made": 1, "fg_missed": 2, "xp_missed": 1}
        xp = ProgressionEngine.calculate_xp_gain(stats, "K")
        # 20 + (1*20) - (2*15) - (1*10) = 20 + 20 - 30 - 10 = 0
        assert xp == 0  # Clamped to 0

    def test_punter_base_xp_is_lower(self, empty_stats):
        """Punter base XP should be 20, not 50."""
        xp = ProgressionEngine.calculate_xp_gain(empty_stats, "P")
        assert xp == 20

    def test_punter_inside_20_xp(self):
        """Punter should get XP for punts inside 20."""
        stats = {"punts_inside_20": 3, "avg_punt_yards": 45}
        xp = ProgressionEngine.calculate_xp_gain(stats, "P")
        # 20 + (3*10) + (45*0.5) = 20 + 30 + 22.5 = 72 (truncated to int)
        assert xp == 72


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestXPEdgeCases:
    """Edge case and boundary tests."""

    def test_xp_never_negative(self):
        """XP should never be negative even with heavy penalties."""
        stats = {"pass_ints": 10}  # Heavy INT game
        xp = ProgressionEngine.calculate_xp_gain(stats, "QB")
        # 50 - (10*20) = 50 - 200 = -150 -> clamped to 0
        assert xp == 0

    def test_unknown_position_gets_base_xp(self, empty_stats):
        """Unknown position should still get base XP."""
        xp = ProgressionEngine.calculate_xp_gain(empty_stats, "UNKNOWN")
        assert xp == 50

    def test_xp_is_integer(self):
        """XP should always be an integer."""
        stats = {"pass_yards": 333}  # Would give fractional XP
        xp = ProgressionEngine.calculate_xp_gain(stats, "QB")
        assert isinstance(xp, int)
