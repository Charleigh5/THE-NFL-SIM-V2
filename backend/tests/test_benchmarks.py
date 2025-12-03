"""
Performance benchmarks for the NFL SIM Engine.

These tests use pytest-benchmark to measure and track performance
of critical simulation components over time.

Run with: pytest backend/tests/test_benchmarks.py -v --benchmark-only
"""
import pytest
from unittest.mock import Mock, MagicMock
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_caller import PlayCaller
from app.engine.probability_engine import ProbabilityEngine
from app.models.player import Player
from app.models.team import Team


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

    def test_pass_play_resolution(self, benchmark, mock_db, sample_players, sample_teams):
        """Benchmark pass play resolution time."""
        from app.schemas.play import PlayCommand

        resolver = PlayResolver(mock_db)
        team1, team2 = sample_teams

        play_command = PlayCommand(
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
            play_command=play_command,
            offense_team=team1,
            defense_team=team2,
            down=1,
            distance=10,
            field_position=25
        )

        assert result is not None

    def test_run_play_resolution(self, benchmark, mock_db, sample_players, sample_teams):
        """Benchmark run play resolution time."""
        from app.schemas.play import PlayCommand

        resolver = PlayResolver(mock_db)
        team1, team2 = sample_teams

        play_command = PlayCommand(
            play_type="run",
            formation="i_form",
            play_direction="middle",
            gap="a",
            offense_players=[sample_players["RB"]],
            defense_players=[]
        )

        result = benchmark(
            resolver.resolve_play,
            play_command=play_command,
            offense_team=team1,
            defense_team=team2,
            down=1,
            distance=10,
            field_position=25
        )

        assert result is not None


class TestProbabilityEngineBenchmarks:
    """Benchmark probability engine performance."""

    def test_attribute_comparison(self, benchmark):
        """Benchmark attribute comparison calculations."""
        engine = ProbabilityEngine()

        result = benchmark(
            engine.compare_attributes,
            offense_rating=85,
            defense_rating=75,
            variance=0.15
        )

        assert 0.0 <= result <= 1.0

    def test_tiered_outcome_resolution(self, benchmark):
        """Benchmark tiered outcome resolution."""
        engine = ProbabilityEngine()

        result = benchmark(
            engine.resolve_tiered_outcome,
            base_probability=0.65,
            critical_threshold=0.10
        )

        assert result in ["critical_success", "success", "failure", "critical_failure"]


class TestPlayCallerBenchmarks:
    """Benchmark play-calling AI performance."""

    def test_play_selection(self, benchmark, mock_db, sample_teams):
        """Benchmark AI play selection time."""
        caller = PlayCaller(mock_db)
        team1, team2 = sample_teams

        result = benchmark(
            caller.select_play,
            offense_team=team1,
            defense_team=team2,
            down=2,
            distance=7,
            field_position=35,
            time_remaining=450,
            score_differential=0
        )

        assert result is not None
        assert hasattr(result, "play_type")


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
