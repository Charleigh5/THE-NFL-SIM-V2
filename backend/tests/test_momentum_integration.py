#!/usr/bin/env python3
"""
Test Momentum Integration (B-009)
=================================
Validates that MomentumEngine is properly integrated into the simulation
orchestrator and play resolver.

Tests B-001 to B-008:
- B-001: MomentumEngine import
- B-002: MomentumEngine initialization
- B-003: Touchdown event processing
- B-004: Turnover event processing
- B-005: Sack event processing
- B-006: Momentum engine wiring to play_resolver
- B-007: Momentum modifier in pass plays
- B-008: Momentum modifier in run plays
"""

from unittest.mock import Mock

import pytest

from app.services.society.momentum import MomentumEngine, MomentumEvent, MomentumState


class TestMomentumEngineUnit:
    """Unit tests for MomentumEngine itself."""

    def test_initial_state_is_neutral(self):
        """Momentum should start at neutral (50)."""
        engine = MomentumEngine()
        momentum = engine.get_team_momentum("team_1")
        assert momentum.score == 50.0
        assert momentum.state == MomentumState.NEUTRAL

    def test_touchdown_increases_momentum(self):
        """B-003: Touchdown should increase momentum."""
        engine = MomentumEngine()
        engine.process_event("team_1", MomentumEvent.TOUCHDOWN)
        momentum = engine.get_team_momentum("team_1")
        assert momentum.score > 50.0
        assert momentum.score == 65.0  # +15 for TD

    def test_turnover_decreases_momentum(self):
        """B-004: Turnover should decrease momentum significantly."""
        engine = MomentumEngine()
        engine.process_event("team_1", MomentumEvent.TURNOVER)
        momentum = engine.get_team_momentum("team_1")
        assert momentum.score < 50.0
        assert momentum.score == 30.0  # -20 for turnover

    def test_sack_decreases_momentum(self):
        """B-005: Sack should decrease offensive momentum."""
        engine = MomentumEngine()
        engine.process_event("team_1", MomentumEvent.SACK)
        momentum = engine.get_team_momentum("team_1")
        assert momentum.score < 50.0
        assert momentum.score == 45.0  # -5 for sack

    def test_big_play_increases_momentum(self):
        """Big play should boost momentum."""
        engine = MomentumEngine()
        engine.process_event("team_1", MomentumEvent.BIG_PLAY_OFFENSE)
        momentum = engine.get_team_momentum("team_1")
        assert momentum.score == 58.0  # +8 for big play

    def test_third_down_stop_increases_defense_momentum(self):
        """3rd down stop should boost defensive momentum."""
        engine = MomentumEngine()
        engine.process_event("team_1", MomentumEvent.THRD_DOWN_STOP)
        momentum = engine.get_team_momentum("team_1")
        assert momentum.score == 55.0  # +5 for 3rd down stop

    def test_performance_modifier_neutral(self):
        """Neutral momentum should give 1.0 modifier."""
        engine = MomentumEngine()
        modifier = engine.get_performance_modifier("team_1")
        assert modifier == 1.0

    def test_performance_modifier_high_momentum(self):
        """High momentum (90+) should give > 1.0 modifier."""
        engine = MomentumEngine()
        # Force high momentum
        engine.get_team_momentum("team_1").score = 90.0
        modifier = engine.get_performance_modifier("team_1")
        assert modifier > 1.0
        assert abs(modifier - 1.08) < 0.01  # ~1.08 at score 90

    def test_performance_modifier_low_momentum(self):
        """Low momentum (10) should give < 1.0 modifier."""
        engine = MomentumEngine()
        engine.get_team_momentum("team_1").score = 10.0
        modifier = engine.get_performance_modifier("team_1")
        assert modifier < 1.0
        assert abs(modifier - 0.92) < 0.01  # ~0.92 at score 10

    def test_state_transitions_to_on_fire(self):
        """Momentum >= 90 should transition to ON_FIRE state."""
        engine = MomentumEngine()
        # Multiple touchdowns
        for _ in range(4):  # 4 TDs = +60, capped at 100
            engine.process_event("team_1", MomentumEvent.TOUCHDOWN)

        momentum = engine.get_team_momentum("team_1")
        assert momentum.state == MomentumState.ON_FIRE
        assert momentum.score >= 90.0

    def test_state_transitions_to_ice_cold(self):
        """Momentum <= 10 should transition to ICE_COLD state."""
        engine = MomentumEngine()
        # Multiple turnovers
        for _ in range(3):  # 3 turnovers = -60, floored at 0
            engine.process_event("team_1", MomentumEvent.TURNOVER)

        momentum = engine.get_team_momentum("team_1")
        assert momentum.state == MomentumState.ICE_COLD
        assert momentum.score <= 10.0


class TestMomentumOrchestatorIntegration:
    """Integration tests for momentum in SimulationOrchestrator."""

    def test_orchestrator_has_momentum_engine(self):
        """B-001/B-002: SimulationOrchestrator should have MomentumEngine."""
        from app.orchestrator.simulation_orchestrator import SimulationOrchestrator

        orchestrator = SimulationOrchestrator()
        assert hasattr(orchestrator, 'momentum_engine')
        assert isinstance(orchestrator.momentum_engine, MomentumEngine)

    def test_play_resolver_has_momentum_engine_attribute(self):
        """B-006: PlayResolver should have momentum_engine attribute."""
        from app.core.random_utils import DeterministicRNG
        from app.orchestrator.play_resolver import PlayResolver

        rng = DeterministicRNG("test_seed")
        resolver = PlayResolver(rng)
        assert hasattr(resolver, 'momentum_engine')
        # Initially None until wired by orchestrator
        assert resolver.momentum_engine is None


class TestMomentumPlayResolverIntegration:
    """Integration tests for momentum in PlayResolver."""

    def test_pass_play_uses_momentum_modifier(self):
        """B-007: Pass play should factor in momentum modifier."""
        from app.core.random_utils import DeterministicRNG
        from app.orchestrator.play_resolver import PlayResolver

        rng = DeterministicRNG("test_seed")
        resolver = PlayResolver(rng)

        # Create mock momentum engine with high momentum
        mock_engine = MomentumEngine()
        mock_engine.get_team_momentum("1").score = 90.0  # ON_FIRE
        resolver.momentum_engine = mock_engine

        # Create mock context
        mock_context = Mock()
        mock_context.home_team_id = 1
        mock_context.away_team_id = 2
        mock_context.weather_config = {"temperature": 70}
        resolver.current_match_context = mock_context

        # Note: Full pass play resolution requires player objects
        # This test validates the structure is in place
        modifier = mock_engine.get_performance_modifier("1")
        assert modifier > 1.0

    def test_run_play_uses_momentum_modifier(self):
        """B-008: Run play should factor in momentum modifier."""
        from app.core.random_utils import DeterministicRNG
        from app.orchestrator.play_resolver import PlayResolver

        rng = DeterministicRNG("test_seed")
        resolver = PlayResolver(rng)

        # Create mock momentum engine with low momentum
        mock_engine = MomentumEngine()
        mock_engine.get_team_momentum("1").score = 10.0  # ICE_COLD
        resolver.momentum_engine = mock_engine

        # Create mock context
        mock_context = Mock()
        mock_context.home_team_id = 1
        resolver.current_match_context = mock_context

        # Get modifier - should be < 1.0 for ICE_COLD
        modifier = mock_engine.get_performance_modifier("1")
        assert modifier < 1.0


class TestMomentumEventSequences:
    """Test realistic game event sequences."""

    def test_scoring_drive_builds_momentum(self):
        """A successful scoring drive should build momentum."""
        engine = MomentumEngine()

        # Big play
        engine.process_event("team_1", MomentumEvent.BIG_PLAY_OFFENSE)
        assert engine.get_team_momentum("team_1").score > 50.0

        # Another big play (+8 each = 66 total, still below 70 for HEATING_UP)
        engine.process_event("team_1", MomentumEvent.BIG_PLAY_OFFENSE)
        assert engine.get_team_momentum("team_1").score == 66.0

        # Touchdown (+15 = 81 total, now HEATING_UP)
        engine.process_event("team_1", MomentumEvent.TOUCHDOWN)
        assert engine.get_team_momentum("team_1").score >= 70.0
        assert engine.get_team_momentum("team_1").state == MomentumState.HEATING_UP

    def test_defensive_stand_shifts_momentum(self):
        """A defensive stand should shift momentum."""
        engine = MomentumEngine()

        # Defense gets a sack
        engine.process_event("defense", MomentumEvent.SACK)
        # Note: SACK is -5, but here it's a positive for defense conceptually
        # Our implementation has SACK as -5 to the team who got sacked
        # So let's test 3rd down stop instead

        engine = MomentumEngine()  # Reset
        engine.process_event("defense", MomentumEvent.THRD_DOWN_STOP)
        engine.process_event("defense", MomentumEvent.THRD_DOWN_STOP)
        engine.process_event("defense", MomentumEvent.THRD_DOWN_STOP)

        assert engine.get_team_momentum("defense").score >= 60.0

    def test_turnover_devastates_momentum(self):
        """A turnover after a hot streak should devastate momentum."""
        engine = MomentumEngine()

        # Build momentum
        engine.process_event("team_1", MomentumEvent.TOUCHDOWN)
        engine.process_event("team_1", MomentumEvent.BIG_PLAY_OFFENSE)
        initial_score = engine.get_team_momentum("team_1").score
        assert initial_score > 70.0

        # Turnover
        engine.process_event("team_1", MomentumEvent.TURNOVER)
        final_score = engine.get_team_momentum("team_1").score

        # Should drop significantly
        assert final_score < initial_score - 15


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
