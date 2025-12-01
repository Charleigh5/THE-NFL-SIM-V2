import pytest
import asyncio
from unittest.mock import MagicMock, patch
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.match_context import MatchContext
from app.orchestrator.kernels.cortex_kernel import CortexKernel, GameSituation
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand, PuntCommand

def test_orchestrator_uses_cortex():
    orch = SimulationOrchestrator()

    # Mock MatchContext and Cortex
    orch.match_context = MagicMock(spec=MatchContext)
    orch.match_context.cortex = MagicMock(spec=CortexKernel)
    orch.match_context.weather_config = {"temperature": 70}

    # Setup Game State
    orch.down = 3
    orch.distance = 15
    orch.yard_line = 20
    orch.possession = "home"
    orch.current_quarter = 1
    orch.time_left = "15:00"

    # Mock Cortex Decision
    orch.match_context.cortex.call_play.return_value = "PASS_DEEP"

    # Mock PlayResolver to avoid actual execution
    orch.play_resolver = MagicMock()
    orch.play_resolver.resolve_play.return_value = MagicMock(yards_gained=0, is_touchdown=False, is_turnover=False, time_elapsed=5)

    # Execute Play (async)
    asyncio.run(orch._execute_single_play())

    # Verify Cortex was called
    orch.match_context.cortex.call_play.assert_called_once()

    # Verify arguments passed to Cortex
    call_args = orch.match_context.cortex.call_play.call_args
    situation = call_args[0][0]
    assert isinstance(situation, GameSituation)
    assert situation.down == 3
    assert situation.distance == 15

    # Verify PlayResolver was called with a PassPlayCommand
    orch.play_resolver.resolve_play.assert_called_once()
    command = orch.play_resolver.resolve_play.call_args[0][0]
    assert isinstance(command, PassPlayCommand)
    assert command.depth == "deep"

def test_orchestrator_cortex_punt():
    orch = SimulationOrchestrator()
    orch.match_context = MagicMock(spec=MatchContext)
    orch.match_context.cortex = MagicMock(spec=CortexKernel)
    orch.match_context.weather_config = {"temperature": 70}

    # Mock Cortex Decision -> PUNT
    orch.match_context.cortex.call_play.return_value = "PUNT"

    orch.play_resolver = MagicMock()
    orch.play_resolver.resolve_play.return_value = MagicMock(yards_gained=0, is_touchdown=False, is_turnover=False, time_elapsed=5)

    asyncio.run(orch._execute_single_play())

    command = orch.play_resolver.resolve_play.call_args[0][0]
    assert isinstance(command, PuntCommand)
