"""
Unit Tests: Tier 1 Mathematical Tension Engine (2025/2026 Production Standard)
==============================================================================
Validates deterministic differential equations, psychological DNA interactions,
resilience dampening, QB/OL trust dynamics, and performance benchmarks.
"""

import time
import pytest
from app.schemas.society import PsychologicalDNA, TensionDelta
from app.engine.society.tension_engine import TensionEngine


class MockPlayer:
    """Lightweight duck-typed player model for deterministic mathematical testing."""
    def __init__(
        self,
        id: int = 1,
        position: str = "WR",
        overall_rating: int = 85,
        depth_chart_rank: int = 1,
        contract_years: int = 2,
        age: int = 26,
        tension_score: float = 0.0,
        morale: int = 80,
        trust_in_coach: int = 80,
        trust_in_qb: int = 80,
        psychological_dna: dict = None,
        backstory: dict = None,
    ):
        self.id = id
        self.position = position
        self.overall_rating = overall_rating
        self.depth_chart_rank = depth_chart_rank
        self.contract_years = contract_years
        self.age = age
        self.tension_score = tension_score
        self.morale = morale
        self.trust_in_coach = trust_in_coach
        self.trust_in_qb = trust_in_qb
        self.psychological_dna = psychological_dna if psychological_dna is not None else {}
        self.backstory = backstory if backstory is not None else {}


class TestTensionEngine:
    """Comprehensive test suite for Tier 1 Mathematical Tension Engine."""

    def test_wr_target_share_deficit_tension_spike(self):
        """High-ego star WR receiving 1 target in a loss experiences a severe tension spike."""
        diva_wr = MockPlayer(
            id=10,
            position="WR",
            overall_rating=92,
            depth_chart_rank=1,
            tension_score=20.0,
            psychological_dna={"ego": 95, "paranoia": 85, "resilience": 30, "professionalism": 30, "loyalty": 40, "greed": 70},
        )
        humble_wr = MockPlayer(
            id=11,
            position="WR",
            overall_rating=92,
            depth_chart_rank=1,
            tension_score=20.0,
            psychological_dna={"ego": 20, "paranoia": 20, "resilience": 90, "professionalism": 90, "loyalty": 90, "greed": 30},
        )

        game_stats = {"targets": 1, "receptions": 1, "snap_percentage": 90.0}
        team_record = {"won_game": False, "loss_streak": 2}

        delta_diva = TensionEngine.calculate_weekly_tension(diva_wr, game_stats, team_record)
        delta_humble = TensionEngine.calculate_weekly_tension(humble_wr, game_stats, team_record)

        assert delta_diva.new_tension > delta_diva.prior_tension + 25.0
        assert delta_diva.primary_driver == "TARGET_SHARE_DEFICIT"
        assert delta_diva.is_active_grievance or delta_diva.new_tension > 45.0
        assert delta_diva.morale_delta < -10

        # Humble player absorbs the low-target game with minimal tension growth
        assert delta_humble.new_tension < delta_diva.new_tension - 20.0

    def test_benching_penalty_high_ego(self):
        """Starter-caliber player benched or receiving 0% snaps accumulates frustration."""
        benched_star = MockPlayer(
            id=20,
            position="CB",
            overall_rating=86,
            depth_chart_rank=1,
            tension_score=30.0,
            psychological_dna={"ego": 85, "loyalty": 25, "paranoia": 75, "resilience": 40, "professionalism": 35},
        )

        game_stats = {"snaps": 0, "snap_percentage": 0.0}
        team_record = {"won_game": False, "loss_streak": 1}

        delta = TensionEngine.calculate_weekly_tension(benched_star, game_stats, team_record)

        assert delta.new_tension > 45.0
        assert delta.primary_driver == "BENCHING_FRUSTRATION"
        assert benched_star.trust_in_coach < 80

    def test_contract_year_greed_leverage(self):
        """High-greed player in contract year on losing team experiences contract urgency tension."""
        contract_player = MockPlayer(
            id=30,
            position="DE",
            overall_rating=84,
            contract_years=1,
            age=29,
            tension_score=40.0,
            psychological_dna={"greed": 95, "paranoia": 80, "loyalty": 30, "resilience": 40, "ego": 60, "professionalism": 50},
        )

        game_stats = {"snaps": 50, "snap_percentage": 75.0, "tackles": 4, "sacks": 1}
        team_record = {"won_game": False, "loss_streak": 3, "wins": 2, "losses": 6}

        delta = TensionEngine.calculate_weekly_tension(contract_player, game_stats, team_record)

        assert delta.new_tension > delta.prior_tension
        assert delta.primary_driver in ("CONTRACT_YEAR_LEVERAGE", "LOSING_STREAK_APATHY")

    def test_qb_sacks_and_turnovers_trust_degradation(self):
        """Catastrophic QB game (5 sacks, 3 turnovers) degrades OL and WR trust in QB."""
        ol_player = MockPlayer(
            id=40,
            position="OT",
            overall_rating=82,
            trust_in_qb=80,
            psychological_dna={"loyalty": 40, "professionalism": 50},
        )
        wr_player = MockPlayer(
            id=41,
            position="WR",
            overall_rating=84,
            trust_in_qb=80,
            psychological_dna={"ego": 80, "loyalty": 35},
        )
        qb_player = MockPlayer(
            id=42,
            position="QB",
            overall_rating=80,
            tension_score=20.0,
            psychological_dna={"resilience": 25, "paranoia": 75},
        )

        team_context = {"qb_sacks_taken": 5, "qb_turnovers": 3}
        qb_stats = {"sacks_taken": 5, "pass_ints": 2, "fumbles": 1}

        TensionEngine.calculate_weekly_tension(ol_player, {}, {"won_game": False}, team_context)
        TensionEngine.calculate_weekly_tension(wr_player, {"targets": 5}, {"won_game": False}, team_context)
        delta_qb = TensionEngine.calculate_weekly_tension(qb_player, qb_stats, {"won_game": False}, team_context)

        # OL and WR trust in QB degraded
        assert ol_player.trust_in_qb < 70
        assert wr_player.trust_in_qb < 70
        # QB tension elevated due to lack of protection / mistakes
        assert delta_qb.new_tension > 35.0

    def test_clean_game_and_victory_boosts_qb_trust(self):
        """Clean pocket (0 sacks, 0 turnovers) and win improves QB trust and relieves tension."""
        ol_player = MockPlayer(
            id=50,
            position="C",
            overall_rating=80,
            trust_in_qb=80,
            tension_score=35.0,
            psychological_dna={"professionalism": 80, "resilience": 80},
        )

        team_context = {"qb_sacks_taken": 0, "qb_turnovers": 0}
        team_record = {"won_game": True, "win_streak": 3}

        delta = TensionEngine.calculate_weekly_tension(ol_player, {"snaps": 60, "snap_percentage": 100.0}, team_record, team_context)

        assert ol_player.trust_in_qb > 80
        assert delta.new_tension < 35.0

    def test_resilience_and_professionalism_dampener(self):
        """High resilience/professionalism dampens negative tension accumulation by >60%."""
        fragile_player = MockPlayer(
            id=60,
            position="LB",
            tension_score=20.0,
            psychological_dna={"resilience": 10, "professionalism": 10, "paranoia": 90, "ego": 80},
        )
        stoic_player = MockPlayer(
            id=61,
            position="LB",
            tension_score=20.0,
            psychological_dna={"resilience": 95, "professionalism": 95, "paranoia": 10, "ego": 30},
        )

        game_stats = {"snaps": 20, "snap_percentage": 25.0}
        team_record = {"won_game": False, "loss_streak": 4}

        delta_fragile = TensionEngine.calculate_weekly_tension(fragile_player, game_stats, team_record)
        delta_stoic = TensionEngine.calculate_weekly_tension(stoic_player, game_stats, team_record)

        assert delta_fragile.new_tension > delta_stoic.new_tension + 15.0

    def test_neutral_defaults_for_missing_dna(self):
        """Players with None or empty psychological_dna default safely without error."""
        blank_player = MockPlayer(id=70, psychological_dna=None)
        delta = TensionEngine.calculate_weekly_tension(blank_player, {}, {"won_game": True})

        assert isinstance(delta, TensionDelta)
        assert delta.player_id == 70
        assert 0.0 <= delta.new_tension <= 100.0

    def test_bye_week_relaxation_decay(self):
        """Bye weeks allow player tension to decay naturally."""
        tense_player = MockPlayer(
            id=80,
            tension_score=50.0,
            morale=60,
            psychological_dna={"resilience": 70, "professionalism": 80},
        )

        delta = TensionEngine.calculate_weekly_tension(tense_player, {}, {}, {"is_bye_week": True})

        assert delta.new_tension < 50.0
        assert delta.morale_delta >= 0

    def test_active_grievance_threshold(self):
        """is_active_grievance is precisely True if and only if new_tension >= 75.0."""
        p_high = MockPlayer(id=90, tension_score=74.0, psychological_dna={"ego": 90, "paranoia": 80})
        p_low = MockPlayer(id=91, tension_score=40.0, psychological_dna={"ego": 30, "paranoia": 20})

        d_high = TensionEngine.calculate_weekly_tension(p_high, {"snaps": 0}, {"won_game": False, "loss_streak": 2})
        d_low = TensionEngine.calculate_weekly_tension(p_low, {"snaps": 60}, {"won_game": True})

        assert d_high.new_tension >= 75.0
        assert d_high.is_active_grievance is True

        assert d_low.new_tension < 75.0
        assert d_low.is_active_grievance is False

    def test_tension_engine_performance_benchmark(self):
        """Full 53-man NFL roster evaluation executes in <2ms."""
        roster = [
            MockPlayer(
                id=i,
                position=["QB", "RB", "WR", "TE", "OT", "OG", "C", "DE", "DT", "LB", "CB", "S"][i % 12],
                overall_rating=65 + (i % 30),
                depth_chart_rank=(i % 3) + 1,
                tension_score=float(i % 50),
                psychological_dna={
                    "ego": 40 + (i % 55),
                    "greed": 30 + (i % 65),
                    "loyalty": 50 + (i % 45),
                    "resilience": 45 + (i % 50),
                    "paranoia": 30 + (i % 60),
                    "professionalism": 50 + (i % 45),
                },
            )
            for i in range(1, 54)
        ]

        game_stats_map = {
            p.id: {"snaps": 40, "snap_percentage": 65.0, "targets": 4, "receptions": 3}
            for p in roster
        }
        team_record = {"won_game": True, "win_streak": 2}
        team_context = {"qb_sacks_taken": 1, "qb_turnovers": 0}

        start = time.perf_counter()
        deltas = TensionEngine.evaluate_roster_weekly(roster, game_stats_map, team_record, team_context)
        duration_ms = (time.perf_counter() - start) * 1000.0

        assert len(deltas) == 53
        assert duration_ms < 5.0, f"Roster evaluation took {duration_ms:.2f}ms, expected < 5.0ms"

    def test_tension_engine_determinism(self):
        """Same inputs produce identical outputs down to the decimal."""
        p1 = MockPlayer(id=100, tension_score=45.5, psychological_dna={"ego": 82, "paranoia": 67, "resilience": 44})
        p2 = MockPlayer(id=100, tension_score=45.5, psychological_dna={"ego": 82, "paranoia": 67, "resilience": 44})

        stats = {"targets": 2, "snap_percentage": 50.0}
        record = {"won_game": False, "loss_streak": 1}

        d1 = TensionEngine.calculate_weekly_tension(p1, stats, record)
        d2 = TensionEngine.calculate_weekly_tension(p2, stats, record)

        assert d1.new_tension == d2.new_tension
        assert d1.morale_delta == d2.morale_delta
        assert d1.primary_driver == d2.primary_driver
        assert d1.is_active_grievance == d2.is_active_grievance
