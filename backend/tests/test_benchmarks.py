"""
Performance benchmarks for the NFL SIM Engine.

These tests use pytest-benchmark to measure and track performance
of critical simulation components over time.

Run with: pytest backend/tests/test_benchmarks.py -v --benchmark-only
"""
import random
from unittest.mock import Mock

import pytest

from app.engine.probability_engine import ProbabilityEngine
from app.models.player import Player
from app.models.team import Team
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_resolver import PlayResolver


@pytest.fixture
def rng():
    """Provide a seeded RNG for deterministic benchmarks."""
    return random.Random(42)


@pytest.fixture
def mock_db():
    """Provide a mock database session."""
    return Mock()


@pytest.fixture
def sample_players():
    """Create sample player objects for testing."""
    qb = Mock(spec=Player)
    qb.id = 1
    qb.position = "QB"
    qb.throw_accuracy_short = 85
    qb.throw_accuracy_medium = 80
    qb.throw_accuracy_deep = 75
    qb.throw_power = 90
    qb.speed = 70
    qb.agility = 75
    qb.awareness = 88

    rb = Mock(spec=Player)
    rb.id = 2
    rb.position = "RB"
    rb.speed = 92
    rb.agility = 90
    rb.carrying = 85
    rb.trucking = 80
    rb.elusiveness = 88

    wr = Mock(spec=Player)
    wr.id = 3
    wr.position = "WR"
    wr.speed = 95
    wr.catch_rating = 88
    wr.route_running = 85
    wr.spectacular_catch = 80

    return {"QB": qb, "RB": rb, "WR": wr}


@pytest.fixture
def sample_teams(sample_players):
    """Create sample team objects."""
    team1 = Mock(spec=Team)
    team1.id = 1
    team1.name = "Test Team 1"

    team2 = Mock(spec=Team)
    team2.id = 2
    team2.name = "Test Team 2"

    return team1, team2


class TestPlayResolutionBenchmarks:
    """Benchmark play resolution performance."""

    def test_pass_play_resolution(self, benchmark, rng, sample_players, sample_teams):
        """Benchmark pass play resolution time."""
        from app.orchestrator.play_commands import PassPlayCommand

        resolver = PlayResolver(rng=rng)
        team1, team2 = sample_teams

        play_command = PassPlayCommand(
            play_type="pass",
            formation="shotgun",
            route_concept="slant",
            target_position="WR",
            offense_players=[sample_players["QB"], sample_players["WR"]],
            defense_players=[]
        )

        # Benchmark the resolution
        result = benchmark(
            resolver.resolve_play,
            command=play_command
        )

        assert result is not None

    def test_run_play_resolution(self, benchmark, rng, sample_players, sample_teams):
        """Benchmark run play resolution time."""
        from app.orchestrator.play_commands import RunPlayCommand

        resolver = PlayResolver(rng=rng)
        team1, team2 = sample_teams

        play_command = RunPlayCommand(
            play_type="run",
            formation="i_form",
            run_direction="middle",
            gap="a",
            offense_players=[sample_players["RB"]],
            defense_players=[]
        )

        result = benchmark(
            resolver.resolve_play,
            command=play_command
        )

        assert result is not None


class TestProbabilityEngineBenchmarks:
    """Benchmark probability engine performance."""

    def test_attribute_comparison(self, benchmark):
        """Benchmark attribute comparison calculations."""
        engine = ProbabilityEngine()

        result = benchmark(
            engine.compare_attributes,
            attacker_val=85,
            defender_val=75,
            scale=0.01,
            max_mod=0.3
        )

        assert -0.3 <= result <= 0.3

    def test_tiered_outcome_resolution(self, benchmark, rng):
        """Benchmark tiered outcome resolution."""
        engine = ProbabilityEngine()

        result = benchmark(
            engine.resolve_tiered_outcome,
            rng=rng,
            probability=0.65,
            critical_threshold=0.10
        )

        # OutcomeType is an Enum
        from app.engine.probability_engine import OutcomeType
        assert result in [OutcomeType.CRITICAL_SUCCESS, OutcomeType.SUCCESS, OutcomeType.FAILURE, OutcomeType.CRITICAL_FAILURE]


class TestPlayCallerBenchmarks:
    """Benchmark play-calling AI performance."""

    def test_play_selection(self, benchmark, rng, sample_teams):
        """Benchmark AI play selection time."""
        caller = PlayCaller(rng=rng, aggression=0.5)
        team1, team2 = sample_teams

        context = PlayCallingContext(
            down=2,
            distance=7,
            distance_to_goal=35,
            time_left_seconds=450,
            score_diff=0,
            possession="home",
            offense_players=[],
            defense_players=[]
        )

        result = benchmark(
            caller.select_play,
            context
        )

        assert result is not None


class TestSeasonSimulationBenchmarks:
    """Benchmark full season simulation performance."""

    @pytest.mark.slow
    def test_single_game_simulation(self, benchmark, mock_db, sample_teams):
        """Benchmark a complete game simulation."""
        from app.orchestrator.game_orchestrator import GameOrchestrator

        orchestrator = GameOrchestrator(mock_db)
        team1, team2 = sample_teams

        # Mock necessary methods to avoid database operations
        orchestrator._initialize_game = Mock(return_value=Mock(id=1))
        orchestrator._finalize_game = Mock()

        result = benchmark(
            orchestrator.simulate_game,
            home_team=team1,
            away_team=team2,
            season_id=1,
            week=1
        )

        # This test might need adjustment based on actual GameOrchestrator implementation
        assert result is not None


# Performance thresholds (these can be adjusted based on requirements)
PERFORMANCE_THRESHOLDS = {
    "play_resolution_max_ms": 50,  # Max 50ms per play
    "probability_calc_max_ms": 5,   # Max 5ms per probability calculation
    "play_selection_max_ms": 25,    # Max 25ms for AI play selection
    "game_simulation_max_s": 10,    # Max 10 seconds per game
}


def test_performance_thresholds():
    """Document performance requirements for the simulation engine."""
    # This is a documentation test that always passes
    # It serves to record our performance goals
    print("\nPerformance Thresholds:")
    for metric, threshold in PERFORMANCE_THRESHOLDS.items():
        print(f"  - {metric}: {threshold}")
    assert True
