#!/usr/bin/env python3
"""
NFL Sim Engine: Orchestrator Test Suite
========================================
Comprehensive tests for the orchestration workflow using simulation.

Context7 Best Practices Applied:
- pytest-asyncio for async test support
- Factory fixtures with cleanup
- Monkeypatch for mocking
- Comprehensive edge case testing

Run tests:
    pytest test_orchestrator.py -v
    pytest test_orchestrator.py -v --tb=short  # Shorter traceback
    pytest test_orchestrator.py::TestSimulation -v  # Run only simulation tests
"""

import asyncio

import pytest

# Import from master_orchestrator
from master_orchestrator import (
    AgentTask,
    DependencyGraph,
    MasterOrchestrator,
    Phase,
    PhaseOrchestrator,
    PhaseStatus,
    SimulatedAgentExecutor,
    TaskStatus,
    create_nfl_sim_phases,
)

# ============================================================================
# FIXTURES (Context7 Pattern: Factory with Cleanup)
# ============================================================================

@pytest.fixture
def make_task():
    """Factory fixture for creating test tasks."""
    created_tasks = []

    def _make_task(
        id: str = "test_task",
        name: str = "Test Task",
        dependencies: list[str] | None = None,
        outputs: list[str] | None = None,
        **kwargs
    ) -> AgentTask:
        task = AgentTask(
            id=id,
            name=name,
            script_path=f"scripts/{id}.py",
            dependencies=dependencies or [],
            outputs=outputs or [f"{id}_output"],
            **kwargs
        )
        created_tasks.append(task)
        return task

    yield _make_task
    created_tasks.clear()


@pytest.fixture
def make_phase(make_task):
    """Factory fixture for creating test phases."""
    created_phases = []

    def _make_phase(
        id: str = "test_phase",
        name: str = "Test Phase",
        tasks: list[AgentTask] | None = None,
        phase_dependencies: list[str] | None = None,
        **kwargs
    ) -> Phase:
        if tasks is None:
            tasks = [make_task(id=f"{id}_task_1")]

        phase = Phase(
            id=id,
            name=name,
            tasks=tasks,
            phase_dependencies=phase_dependencies or [],
            **kwargs
        )
        created_phases.append(phase)
        return phase

    yield _make_phase
    created_phases.clear()


@pytest.fixture
def simple_executor():
    """Create a simple simulated executor with instant completion."""
    return SimulatedAgentExecutor(base_delay=0.01)


@pytest.fixture
def nfl_phases():
    """Get the full NFL Sim Engine phase configuration."""
    return create_nfl_sim_phases()


# ============================================================================
# UNIT TESTS: AgentTask
# ============================================================================

class TestAgentTask:
    """Tests for the AgentTask dataclass."""

    def test_task_creation(self, make_task):
        """Test basic task creation."""
        task = make_task(id="my_task", name="My Task")

        assert task.id == "my_task"
        assert task.name == "My Task"
        assert task.status == TaskStatus.PENDING
        assert task.duration is None

    def test_task_duration_calculation(self, make_task):
        """Test duration calculation when times are set."""
        task = make_task()
        task.start_time = 100.0
        task.end_time = 105.5

        assert task.duration == 5.5

    def test_task_with_dependencies(self, make_task):
        """Test task with dependencies."""
        task = make_task(
            id="dependent_task",
            dependencies=["dep_1", "dep_2"],
            outputs=["output_1", "output_2"]
        )

        assert len(task.dependencies) == 2
        assert "dep_1" in task.dependencies
        assert len(task.outputs) == 2


# ============================================================================
# UNIT TESTS: Phase
# ============================================================================

class TestPhase:
    """Tests for the Phase dataclass."""

    def test_phase_creation(self, make_phase, make_task):
        """Test basic phase creation."""
        tasks = [
            make_task(id="t1", outputs=["out1"]),
            make_task(id="t2", outputs=["out2", "out3"])
        ]
        phase = make_phase(id="my_phase", tasks=tasks)

        assert phase.id == "my_phase"
        assert len(phase.tasks) == 2
        assert phase.status == PhaseStatus.PENDING

    def test_phase_outputs_collection(self, make_phase, make_task):
        """Test that phase collects outputs from all tasks."""
        tasks = [
            make_task(id="t1", outputs=["a", "b"]),
            make_task(id="t2", outputs=["c"])
        ]
        phase = make_phase(tasks=tasks)

        outputs = phase.outputs
        assert len(outputs) == 3
        assert "a" in outputs
        assert "b" in outputs
        assert "c" in outputs


# ============================================================================
# UNIT TESTS: DependencyGraph
# ============================================================================

class TestDependencyGraph:
    """Tests for dependency graph management."""

    def test_initial_phases(self, make_phase):
        """Test getting phases with no dependencies."""
        phase1 = make_phase(id="p1", phase_dependencies=[])
        phase2 = make_phase(id="p2", phase_dependencies=["p1"])

        graph = DependencyGraph([phase1, phase2])
        initial = graph.get_initial_phases()

        assert len(initial) == 1
        assert initial[0].id == "p1"

    def test_mark_output_complete(self, make_phase, make_task):
        """Test marking outputs and finding ready tasks."""
        task1 = make_task(id="t1", dependencies=[], outputs=["x"])
        task2 = make_task(id="t2", dependencies=["x"], outputs=["y"])

        phase = make_phase(
            id="p1",
            tasks=[task1, task2],
            phase_dependencies=[]
        )
        phase.status = PhaseStatus.RUNNING
        task1.status = TaskStatus.COMPLETED

        graph = DependencyGraph([phase])
        ready = graph.mark_output_complete("x")

        assert len(ready) == 1
        assert ready[0].id == "t2"

    def test_phase_dependency_chain(self, make_phase):
        """Test phase dependencies trigger correctly."""
        phase1 = make_phase(id="p1", phase_dependencies=[])
        phase2 = make_phase(id="p2", phase_dependencies=["p1"])
        phase3 = make_phase(id="p3", phase_dependencies=["p1", "p2"])

        graph = DependencyGraph([phase1, phase2, phase3])

        # Initially only p1 is ready
        assert len(graph.get_initial_phases()) == 1

        # Complete p1
        ready = graph.mark_phase_complete("p1")
        assert len(ready) == 1
        assert ready[0].id == "p2"

        # Complete p2
        ready = graph.mark_phase_complete("p2")
        assert len(ready) == 1
        assert ready[0].id == "p3"


# ============================================================================
# UNIT TESTS: SimulatedAgentExecutor
# ============================================================================

class TestSimulatedAgentExecutor:
    """Tests for the simulation executor."""

    @pytest.mark.asyncio
    async def test_successful_execution(self, make_task):
        """Test successful simulated execution."""
        executor = SimulatedAgentExecutor(base_delay=0.01)
        task = make_task(outputs=["out1", "out2"])

        result = await executor.execute(task)

        assert result.success is True
        assert result.outputs == ["out1", "out2"]
        assert result.error is None

    @pytest.mark.asyncio
    async def test_simulated_failure(self, make_task):
        """Test simulated failure."""
        task = make_task(id="fail_me")
        executor = SimulatedAgentExecutor(
            base_delay=0.01,
            simulated_failures={"fail_me"}
        )

        result = await executor.execute(task)

        assert result.success is False
        assert result.error is not None and "Simulated failure" in result.error
        assert result.outputs == []

    @pytest.mark.asyncio
    async def test_custom_durations(self, make_task):
        """Test custom task durations."""
        task = make_task(id="slow_task")
        executor = SimulatedAgentExecutor(
            simulated_durations={"slow_task": 0.1},
            base_delay=0.01
        )

        result = await executor.execute(task)

        # Should take at least 0.1 seconds
        assert result.duration >= 0.09

    @pytest.mark.asyncio
    async def test_execution_logging(self, make_task):
        """Test that execution is logged."""
        executor = SimulatedAgentExecutor(base_delay=0.01)
        task = make_task(id="logged_task", name="Logged Task")

        await executor.execute(task)

        assert len(executor.execution_log) == 1
        assert executor.execution_log[0]["task_id"] == "logged_task"
        assert executor.execution_log[0]["task_name"] == "Logged Task"


# ============================================================================
# INTEGRATION TESTS: PhaseOrchestrator
# ============================================================================

class TestPhaseOrchestrator:
    """Integration tests for phase-level orchestration."""

    @pytest.mark.asyncio
    async def test_single_task_phase(self, make_phase, make_task, simple_executor):
        """Test phase with single task."""
        task = make_task(id="solo", outputs=["solo_out"])
        phase = make_phase(tasks=[task])

        orchestrator = PhaseOrchestrator(
            phase=phase,
            executor=simple_executor
        )

        success = await orchestrator.run()

        assert success is True
        assert phase.status == PhaseStatus.COMPLETED
        assert task.status == TaskStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_parallel_tasks(self, make_phase, make_task, simple_executor):
        """Test multiple independent tasks run in parallel."""
        tasks = [
            make_task(id="t1", dependencies=[], outputs=["out1"]),
            make_task(id="t2", dependencies=[], outputs=["out2"]),
            make_task(id="t3", dependencies=[], outputs=["out3"]),
        ]
        phase = make_phase(tasks=tasks)

        orchestrator = PhaseOrchestrator(
            phase=phase,
            executor=simple_executor,
            max_parallel=3
        )

        success = await orchestrator.run()

        assert success is True
        assert all(t.status == TaskStatus.COMPLETED for t in tasks)

    @pytest.mark.asyncio
    async def test_task_dependency_ordering(self, make_phase, make_task, simple_executor):
        """Test that tasks respect dependency order."""
        execution_order = []

        def track_completion(task, result):
            execution_order.append(task.id)

        tasks = [
            make_task(id="first", dependencies=[], outputs=["first_out"]),
            make_task(id="second", dependencies=["first_out"], outputs=["second_out"]),
            make_task(id="third", dependencies=["second_out"], outputs=["third_out"]),
        ]
        phase = make_phase(tasks=tasks)

        orchestrator = PhaseOrchestrator(
            phase=phase,
            executor=simple_executor,
            on_task_complete=track_completion
        )

        await orchestrator.run()

        # Verify order
        assert execution_order.index("first") < execution_order.index("second")
        assert execution_order.index("second") < execution_order.index("third")

    @pytest.mark.asyncio
    async def test_phase_with_failure(self, make_phase, make_task):
        """Test phase handles task failure."""
        task = make_task(id="will_fail")
        phase = make_phase(tasks=[task])

        executor = SimulatedAgentExecutor(
            base_delay=0.01,
            simulated_failures={"will_fail"}
        )

        orchestrator = PhaseOrchestrator(phase=phase, executor=executor)
        success = await orchestrator.run()

        assert success is False
        assert phase.status == PhaseStatus.FAILED
        assert task.status == TaskStatus.FAILED


# ============================================================================
# INTEGRATION TESTS: MasterOrchestrator
# ============================================================================

class TestMasterOrchestrator:
    """Integration tests for master orchestration."""

    @pytest.mark.asyncio
    async def test_single_phase_execution(self, make_phase, make_task, simple_executor):
        """Test orchestration of a single phase."""
        task = make_task()
        phase = make_phase(tasks=[task], phase_dependencies=[])

        orchestrator = MasterOrchestrator(
            phases=[phase],
            executor=simple_executor
        )

        results = await orchestrator.run()

        assert results[phase.id] is True

    @pytest.mark.asyncio
    async def test_phase_chain_execution(self, make_phase, make_task, simple_executor):
        """Test phases execute in dependency order."""
        phase1 = make_phase(id="p1", name="Phase 1", phase_dependencies=[])
        phase2 = make_phase(id="p2", name="Phase 2", phase_dependencies=["p1"])
        phase3 = make_phase(id="p3", name="Phase 3", phase_dependencies=["p2"])

        orchestrator = MasterOrchestrator(
            phases=[phase1, phase2, phase3],
            executor=simple_executor,
            max_parallel_phases=1  # Force sequential
        )

        results = await orchestrator.run()

        assert all(success for success in results.values())
        # Verify order via end times
        assert phase1.end_time <= phase2.start_time
        assert phase2.end_time <= phase3.start_time

    @pytest.mark.asyncio
    async def test_parallel_phase_execution(self, make_phase, make_task, simple_executor):
        """Test independent phases run in parallel."""
        # Two phases with no dependencies
        phase1 = make_phase(id="p1", name="Phase 1", phase_dependencies=[])
        phase2 = make_phase(id="p2", name="Phase 2", phase_dependencies=[])

        orchestrator = MasterOrchestrator(
            phases=[phase1, phase2],
            executor=simple_executor,
            max_parallel_phases=2
        )

        results = await orchestrator.run()

        assert all(success for success in results.values())
        # Both should start around the same time
        assert abs(phase1.start_time - phase2.start_time) < 0.1


# ============================================================================
# SIMULATION TESTS: Full NFL Sim Workflow
# ============================================================================

class TestSimulation:
    """Full simulation tests of the NFL Sim Engine orchestration."""

    @pytest.mark.asyncio
    async def test_full_simulation_completes(self, nfl_phases):
        """Test that full 12-phase simulation completes successfully."""
        executor = SimulatedAgentExecutor(base_delay=0.01)

        orchestrator = MasterOrchestrator(
            phases=nfl_phases,
            executor=executor,
            max_parallel_phases=4,
            max_parallel_tasks_per_phase=3
        )

        results = await orchestrator.run()

        # All 12 phases should complete
        assert len(results) == 12
        assert all(success for success in results.values())

    @pytest.mark.asyncio
    async def test_phase_dependencies_respected(self, nfl_phases):
        """Verify phase dependencies are respected in full simulation."""
        executor = SimulatedAgentExecutor(base_delay=0.01)

        orchestrator = MasterOrchestrator(
            phases=nfl_phases,
            executor=executor,
            max_parallel_phases=4
        )

        await orchestrator.run()

        # Get phase by id helper
        phases_by_id = {p.id: p for p in nfl_phases}

        # Phase 2 depends on Phase 1
        assert phases_by_id["phase_1"].end_time <= phases_by_id["phase_2"].start_time

        # Phase 3 depends on Phase 2
        assert phases_by_id["phase_2"].end_time <= phases_by_id["phase_3"].start_time

        # Phase 11 depends on Phases 3, 4, and 7
        p11_start = phases_by_id["phase_11"].start_time
        assert phases_by_id["phase_3"].end_time <= p11_start
        assert phases_by_id["phase_4"].end_time <= p11_start
        assert phases_by_id["phase_7"].end_time <= p11_start

    @pytest.mark.asyncio
    async def test_single_phase_failure_doesnt_block_independents(self, nfl_phases):
        """Test that failing Phase 5 doesn't block Phase 3 (which doesn't depend on it)."""
        executor = SimulatedAgentExecutor(
            base_delay=0.01,
            simulated_failures={"agent_5_1"}  # Fail salary cap engine
        )

        orchestrator = MasterOrchestrator(
            phases=nfl_phases,
            executor=executor,
            max_parallel_phases=4
        )

        results = await orchestrator.run()

        # Phase 5 should fail
        assert results["phase_5"] is False

        # Phase 3 (Position Physics) should still complete
        # (it depends on Phase 2, not Phase 5)
        assert results["phase_3"] is True

    @pytest.mark.asyncio
    async def test_execution_log_completeness(self, nfl_phases):
        """Verify all tasks are logged in execution order."""
        executor = SimulatedAgentExecutor(base_delay=0.01)

        orchestrator = MasterOrchestrator(
            phases=nfl_phases,
            executor=executor,
            max_parallel_phases=4
        )

        await orchestrator.run()

        # Count total tasks
        total_tasks = sum(len(p.tasks) for p in nfl_phases)

        # All should be logged
        assert len(executor.execution_log) == total_tasks

        # Each task should appear exactly once
        logged_ids = [entry["task_id"] for entry in executor.execution_log]
        assert len(set(logged_ids)) == total_tasks


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error scenarios."""

    @pytest.mark.asyncio
    async def test_empty_phase_list(self, simple_executor):
        """Test orchestration with no phases."""
        orchestrator = MasterOrchestrator(
            phases=[],
            executor=simple_executor
        )

        results = await orchestrator.run()

        assert results == {}

    @pytest.mark.asyncio
    async def test_phase_with_no_tasks(self, make_phase, simple_executor):
        """Test phase with empty task list."""
        phase = make_phase(id="empty", tasks=[])

        orchestrator = MasterOrchestrator(
            phases=[phase],
            executor=simple_executor
        )

        results = await orchestrator.run()

        assert results["empty"] is True

    @pytest.mark.asyncio
    async def test_circular_task_dependencies_detected(self, make_phase, make_task):
        """Test that circular dependencies are handled gracefully."""
        # Create tasks with circular dependency
        task1 = make_task(id="t1", dependencies=["t2_out"], outputs=["t1_out"])
        task2 = make_task(id="t2", dependencies=["t1_out"], outputs=["t2_out"])

        phase = make_phase(tasks=[task1, task2])
        executor = SimulatedAgentExecutor(base_delay=0.01)

        orchestrator = PhaseOrchestrator(
            phase=phase,
            executor=executor
        )

        # Should complete (with tasks stuck in PENDING)
        success = await asyncio.wait_for(orchestrator.run(), timeout=1.0)

        # Neither task should complete due to deadlock
        assert success is False


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Performance and stress tests."""

    @pytest.mark.asyncio
    async def test_high_parallelism(self, make_phase, make_task):
        """Test with many parallel tasks."""
        tasks = [
            make_task(id=f"t{i}", dependencies=[], outputs=[f"out{i}"])
            for i in range(20)
        ]
        phase = make_phase(tasks=tasks)

        executor = SimulatedAgentExecutor(base_delay=0.01)
        orchestrator = PhaseOrchestrator(
            phase=phase,
            executor=executor,
            max_parallel=10  # Allow 10 parallel
        )

        success = await orchestrator.run()

        assert success is True
        assert all(t.status == TaskStatus.COMPLETED for t in tasks)

    @pytest.mark.asyncio
    async def test_deep_dependency_chain(self, make_phase, make_task):
        """Test with deep dependency chain."""
        tasks = []
        for i in range(10):
            deps = [f"out{i-1}"] if i > 0 else []
            tasks.append(make_task(
                id=f"t{i}",
                dependencies=deps,
                outputs=[f"out{i}"]
            ))

        phase = make_phase(tasks=tasks)
        executor = SimulatedAgentExecutor(base_delay=0.01)

        orchestrator = PhaseOrchestrator(
            phase=phase,
            executor=executor
        )

        success = await orchestrator.run()

        assert success is True


# ============================================================================
# RUN CONFIGURATION
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
