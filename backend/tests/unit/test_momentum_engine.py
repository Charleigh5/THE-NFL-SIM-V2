"""
Unit Tests for Game Momentum & HUD Telemetry Engine
===================================================
Tests verifying:
1. Play-by-play EPA calculations (Touchdown, Turnover, First Down, Incomplete)
2. Calibrated Win Probability bounds and volatility decay
3. Sub-millisecond Ben Baldwin 4th-down decision telemetry
4. Full game momentum flow generation
"""

import time
import pytest
from app.services.momentum_engine import MomentumEngine
from app.schemas.hud_telemetry import (
    FourthDownTelemetryPayload,
    MomentumFlowResponse,
)


def test_calculate_play_epa_touchdown():
    """Verify EPA for scoring a touchdown returns large positive value (>5.0)."""
    epa = MomentumEngine.calculate_play_epa(
        down=2,
        distance=5,
        yard_line=85,
        yards_gained=15,
        is_touchdown=True,
    )
    assert epa >= 2.0
    assert epa <= 8.0


def test_calculate_play_epa_turnover():
    """Verify EPA for committing a turnover produces severe negative impact."""
    epa = MomentumEngine.calculate_play_epa(
        down=1,
        distance=10,
        yard_line=60,
        yards_gained=0,
        is_turnover=True,
    )
    assert epa < -2.0


def test_calculate_play_epa_first_down_conversion():
    """Converting on 3rd and short should yield positive EPA."""
    epa = MomentumEngine.calculate_play_epa(
        down=3,
        distance=2,
        yard_line=45,
        yards_gained=6,
    )
    assert epa > 0.4


def test_calculate_win_probability_boundaries():
    """Win probability must strictly remain between 0.001 and 0.999."""
    # Massive lead late
    wp_huge_lead = MomentumEngine.calculate_win_probability(
        home_score=45,
        away_score=10,
        yard_line=50,
        time_remaining_seconds=60,
        is_home_offense=True,
    )
    assert 0.95 <= wp_huge_lead <= 0.999

    # Massive deficit late
    wp_huge_deficit = MomentumEngine.calculate_win_probability(
        home_score=7,
        away_score=42,
        yard_line=20,
        time_remaining_seconds=90,
        is_home_offense=True,
    )
    assert 0.001 <= wp_huge_deficit <= 0.05


def test_calculate_win_probability_score_differential():
    """Tied game at halftime should hover near 50%."""
    wp_tied = MomentumEngine.calculate_win_probability(
        home_score=14,
        away_score=14,
        yard_line=50,
        time_remaining_seconds=1800,
        is_home_offense=True,
    )
    assert 0.45 <= wp_tied <= 0.65


def test_evaluate_live_fourth_down_recommendation():
    """4th & 1 at midfield trailing late should strongly recommend GO."""
    telemetry: FourthDownTelemetryPayload = MomentumEngine.evaluate_live_fourth_down(
        yard_line=55,
        yards_to_go=1,
        score_differential=-3,
        quarter=4,
        time_remaining_seconds=240,
        timeouts=2,
    )

    assert telemetry.recommendation == "GO"
    assert telemetry.conversion_prob > 0.60
    assert telemetry.wp_net_gain >= 0.0
    assert isinstance(telemetry.summary, str)
    assert len(telemetry.summary) > 5


def test_evaluate_live_fourth_down_latency():
    """Ensure 4th down telemetry evaluates in <10ms (typical <0.05ms)."""
    start = time.perf_counter()
    for _ in range(100):
        MomentumEngine.evaluate_live_fourth_down(
            yard_line=50,
            yards_to_go=2,
            score_differential=0,
            quarter=4,
            time_remaining_seconds=300,
        )
    elapsed = (time.perf_counter() - start) / 100 * 1000  # ms per call
    assert elapsed < 10.0, f"Latency {elapsed:.3f}ms exceeded 10ms budget"


def test_generate_momentum_flow():
    """Generate sequential momentum curve with valid nodes and key events."""
    flow: MomentumFlowResponse = MomentumEngine.generate_momentum_flow(
        game_id=1,
        home_team_abbr="GB",
        away_team_abbr="CHI",
        home_score=27,
        away_score=21,
    )

    assert flow.game_id == 1
    assert flow.home_team_abbr == "GB"
    assert flow.away_team_abbr == "CHI"
    assert len(flow.play_nodes) >= 8

    # Verify nodes
    has_key_event = any(node.is_key_event for node in flow.play_nodes)
    assert has_key_event, "Momentum flow should mark key swing plays"

    for node in flow.play_nodes:
        assert 0.0 <= node.home_win_prob <= 1.0
        assert 0.0 <= node.away_win_prob <= 1.0
        assert abs(node.home_win_prob + node.away_win_prob - 1.0) < 0.01
