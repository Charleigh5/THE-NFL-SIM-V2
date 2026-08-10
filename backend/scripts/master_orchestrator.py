#!/usr/bin/env python3
"""
NFL Sim Engine: Master Orchestrator
====================================
Dependency-driven multi-phase agent orchestration with automatic handoffs.

Context7 Best Practices Applied:
- pytest-asyncio for async testing patterns
- Factory fixtures with cleanup
- Monkeypatch for simulation testing
- Typed dataclasses for configuration

Usage:
    # Simulation mode (dry run with mocked agents)
    python master_orchestrator.py --simulate

    # Real execution
    python master_orchestrator.py --execute

    # Run tests first
    pytest test_orchestrator.py -v
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS & DATA CLASSES
# ============================================================================

class TaskStatus(str, Enum):
    """Status of individual tasks within a phase."""
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class PhaseStatus(str, Enum):
    """Status of entire phases."""
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class AgentTask:
    """Represents a single agent task within a phase."""
    id: str
    name: str
    script_path: str
    dependencies: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    start_time: float | None = None
    end_time: float | None = None
    error_message: str | None = None

    @property
    def duration(self) -> float | None:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class Phase:
    """Represents a development phase containing multiple agent tasks."""
    id: str
    name: str
    tasks: list[AgentTask] = field(default_factory=list)
    phase_dependencies: list[str] = field(default_factory=list)
    status: PhaseStatus = PhaseStatus.PENDING
    start_time: float | None = None
    end_time: float | None = None

    @property
    def outputs(self) -> list[str]:
        """Collect all outputs from all tasks in this phase."""
        all_outputs = []
        for task in self.tasks:
            all_outputs.extend(task.outputs)
        return all_outputs

    @property
    def duration(self) -> float | None:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class ExecutionResult:
    """Result of executing an agent task."""
    task_id: str
    success: bool
    outputs: list[str]
    duration: float
    error: str | None = None
    logs: str = ""


# ============================================================================
# PROTOCOLS (For dependency injection & testing)
# ============================================================================

class AgentExecutor(Protocol):
    """Protocol for executing agent tasks (allows mocking for simulation)."""

    async def execute(self, task: AgentTask) -> ExecutionResult:
        """Execute a task and return the result."""
        ...


class CompletionNotifier(Protocol):
    """Protocol for notifying when outputs are complete."""

    def mark_complete(self, output_id: str) -> None:
        """Mark an output as complete."""
        ...

    def is_complete(self, output_id: str) -> bool:
        """Check if an output is complete."""
        ...


# ============================================================================
# DEPENDENCY GRAPH
# ============================================================================

class DependencyGraph:
    """
    Manages task and phase dependencies using a directed acyclic graph.
    Determines when tasks/phases are ready to execute.
    """

    def __init__(self, phases: list[Phase]):
        self.phases: dict[str, Phase] = {p.id: p for p in phases}
        self.completed_outputs: set[str] = set()
        self.completed_phases: set[str] = set()

    def mark_output_complete(self, output_id: str) -> list[AgentTask]:
        """
        Mark an output as complete and return newly ready tasks.

        Args:
            output_id: The identifier of the completed output

        Returns:
            List of tasks that are now ready to execute
        """
        self.completed_outputs.add(output_id)
        logger.debug(f"Output completed: {output_id}")
        return self._get_newly_ready_tasks()

    def mark_phase_complete(self, phase_id: str) -> list[Phase]:
        """
        Mark a phase as complete and return newly ready phases.

        Args:
            phase_id: The identifier of the completed phase

        Returns:
            List of phases that are now ready to execute
        """
        self.completed_phases.add(phase_id)
        phase = self.phases[phase_id]
        phase.status = PhaseStatus.COMPLETED
        phase.end_time = time.time()

        # Mark phase completion as an output
        self.completed_outputs.add(f"{phase_id}_complete")

        logger.info(f"✅ Phase completed: {phase.name}")
        return self._get_newly_ready_phases()

    def _get_newly_ready_tasks(self) -> list[AgentTask]:
        """Find tasks whose dependencies are now satisfied."""
        ready_tasks = []

        for phase in self.phases.values():
            if phase.status != PhaseStatus.RUNNING:
                continue

            for task in phase.tasks:
                if task.status != TaskStatus.PENDING:
                    continue

                if all(dep in self.completed_outputs for dep in task.dependencies):
                    task.status = TaskStatus.READY
                    ready_tasks.append(task)

        return ready_tasks

    def _get_newly_ready_phases(self) -> list[Phase]:
        """Find phases whose phase-level dependencies are now satisfied."""
        ready_phases = []

        for phase in self.phases.values():
            if phase.status != PhaseStatus.PENDING:
                continue

            phase_deps_satisfied = all(
                f"{dep}_complete" in self.completed_outputs
                for dep in phase.phase_dependencies
            )

            if phase_deps_satisfied:
                phase.status = PhaseStatus.READY
                ready_phases.append(phase)

        return ready_phases

    def get_initial_phases(self) -> list[Phase]:
        """Get phases with no dependencies (can start immediately)."""
        return [p for p in self.phases.values() if not p.phase_dependencies]


# ============================================================================
# AGENT EXECUTORS
# ============================================================================

class RealAgentExecutor:
    """Executes agent tasks by running actual Python scripts."""

    def __init__(self, work_dir: Path, marker_dir: Path):
        self.work_dir = work_dir
        self.marker_dir = marker_dir
        self.marker_dir.mkdir(exist_ok=True)

    async def execute(self, task: AgentTask) -> ExecutionResult:
        """Execute a task by running its script."""
        start_time = time.time()

        try:
            process = await asyncio.create_subprocess_exec(
                "python", task.script_path,
                cwd=str(self.work_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                # Write completion markers
                for output in task.outputs:
                    marker_path = self.marker_dir / f"{output}.done"
                    marker_path.write_text(json.dumps({
                        "task_id": task.id,
                        "output": output,
                        "timestamp": time.time()
                    }))

                return ExecutionResult(
                    task_id=task.id,
                    success=True,
                    outputs=task.outputs,
                    duration=time.time() - start_time,
                    logs=stdout.decode()
                )
            else:
                return ExecutionResult(
                    task_id=task.id,
                    success=False,
                    outputs=[],
                    duration=time.time() - start_time,
                    error=stderr.decode(),
                    logs=stdout.decode()
                )

        except Exception as e:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                outputs=[],
                duration=time.time() - start_time,
                error=str(e)
            )


class SimulatedAgentExecutor:
    """
    Simulates agent execution for testing the orchestration flow.
    Does not run actual scripts - instead simulates timing and success/failure.
    """

    def __init__(
        self,
        simulated_durations: dict[str, float] | None = None,
        simulated_failures: set[str] | None = None,
        base_delay: float = 0.1
    ):
        self.simulated_durations = simulated_durations or {}
        self.simulated_failures = simulated_failures or set()
        self.base_delay = base_delay
        self.execution_log: list[dict[str, Any]] = []

    async def execute(self, task: AgentTask) -> ExecutionResult:
        """Simulate task execution with configurable delays and failures."""
        start_time = time.time()

        # Get simulated duration or use base delay
        duration = self.simulated_durations.get(task.id, self.base_delay)
        await asyncio.sleep(duration)

        # Log the execution for verification
        self.execution_log.append({
            "task_id": task.id,
            "task_name": task.name,
            "timestamp": start_time,
            "simulated_duration": duration
        })

        # Check if this task should fail
        if task.id in self.simulated_failures:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                outputs=[],
                duration=time.time() - start_time,
                error=f"Simulated failure for {task.id}"
            )

        logger.info(f"  📦 [SIM] {task.name} produced: {task.outputs}")

        return ExecutionResult(
            task_id=task.id,
            success=True,
            outputs=task.outputs,
            duration=time.time() - start_time,
            logs=f"[SIMULATED] Task {task.id} completed successfully"
        )


# ============================================================================
# PHASE ORCHESTRATOR
# ============================================================================

class PhaseOrchestrator:
    """
    Orchestrates execution of tasks within a single phase.
    Runs agents in parallel when dependencies allow.
    """

    def __init__(
        self,
        phase: Phase,
        executor: AgentExecutor,
        max_parallel: int = 3,
        on_task_complete: Callable[[AgentTask, ExecutionResult], None] | None = None
    ):
        self.phase = phase
        self.executor = executor
        self.max_parallel = max_parallel
        self.on_task_complete = on_task_complete
        self.running_tasks: set[str] = set()
        self.completed_outputs: set[str] = set()

    async def run(self) -> bool:
        """
        Execute all tasks in the phase, respecting dependencies.

        Returns:
            True if all tasks completed successfully, False otherwise.
        """
        self.phase.status = PhaseStatus.RUNNING
        self.phase.start_time = time.time()

        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 STARTING PHASE: {self.phase.name}")
        logger.info(f"{'='*60}")
        logger.info(f"   Tasks: {len(self.phase.tasks)}")

        # Track tasks by status
        pending_tasks = {t.id: t for t in self.phase.tasks}
        active_futures: dict[asyncio.Task, str] = {}  # Map future -> task_id

        while pending_tasks or active_futures:
            # Find ready tasks (pending with satisfied dependencies)
            ready_tasks = [
                t for t in pending_tasks.values()
                if t.status in [TaskStatus.PENDING, TaskStatus.READY]
                and all(dep in self.completed_outputs for dep in t.dependencies)
            ]

            # Start ready tasks up to max_parallel limit
            while ready_tasks and len(active_futures) < self.max_parallel:
                task = ready_tasks.pop(0)
                task.status = TaskStatus.RUNNING
                task.start_time = time.time()
                self.running_tasks.add(task.id)
                logger.info(f"   ▶️  Starting: {task.name}")

                future = asyncio.create_task(self._execute_task(task))
                active_futures[future] = task.id

            # If we have active tasks, wait for at least one to complete
            if active_futures:
                done, _ = await asyncio.wait(
                    active_futures.keys(),
                    return_when=asyncio.FIRST_COMPLETED
                )

                # Process completed tasks
                for future in done:
                    task_id = active_futures.pop(future)
                    task, result = future.result()
                    self._handle_task_result(task, result)

                    # Remove from pending
                    if task_id in pending_tasks:
                        del pending_tasks[task_id]
            elif not ready_tasks:
                # No active tasks and nothing ready - deadlock or done
                break

        # Check if all tasks succeeded
        all_success = all(t.status == TaskStatus.COMPLETED for t in self.phase.tasks)

        self.phase.end_time = time.time()
        self.phase.status = PhaseStatus.COMPLETED if all_success else PhaseStatus.FAILED

        return all_success

    async def _execute_task(self, task: AgentTask) -> tuple[AgentTask, ExecutionResult]:
        """Execute a single task and return it with its result."""
        result = await self.executor.execute(task)
        return task, result

    def _handle_task_result(self, task: AgentTask, result: ExecutionResult) -> None:
        """Handle the result of a completed task."""
        self.running_tasks.discard(task.id)
        task.end_time = time.time()

        if result.success:
            task.status = TaskStatus.COMPLETED
            self.completed_outputs.update(result.outputs)
            logger.info(f"   ✅ Completed: {task.name} ({result.duration:.2f}s)")
        else:
            task.status = TaskStatus.FAILED
            task.error_message = result.error
            logger.error(f"   ❌ Failed: {task.name} - {result.error}")

        if self.on_task_complete:
            self.on_task_complete(task, result)


# ============================================================================
# MASTER ORCHESTRATOR
# ============================================================================

class MasterOrchestrator:
    """
    Top-level orchestrator that coordinates all phases.
    Triggers phases when their dependencies are satisfied.
    """

    def __init__(
        self,
        phases: list[Phase],
        executor: AgentExecutor,
        max_parallel_phases: int = 4,
        max_parallel_tasks_per_phase: int = 3
    ):
        self.graph = DependencyGraph(phases)
        self.executor = executor
        self.max_parallel_phases = max_parallel_phases
        self.max_parallel_tasks = max_parallel_tasks_per_phase
        self.running_phases: dict[str, asyncio.Task] = {}
        self.results: dict[str, bool] = {}

    async def run(self) -> dict[str, bool]:
        """
        Execute all phases in dependency order.

        Returns:
            Dictionary mapping phase_id to success status.
        """
        logger.info("="*60)
        logger.info("NFL SIM ENGINE: MASTER ORCHESTRATOR")
        logger.info("="*60)
        logger.info(f"Total phases: {len(self.graph.phases)}")
        logger.info(f"Max parallel phases: {self.max_parallel_phases}")
        logger.info("")

        # Start initial phases (no dependencies)
        initial_phases = self.graph.get_initial_phases()
        for phase in initial_phases:
            if len(self.running_phases) < self.max_parallel_phases:
                self._start_phase(phase)

        # Main loop
        while self.running_phases or any(
            p.status == PhaseStatus.PENDING for p in self.graph.phases.values()
        ):
            # Wait for any phase to complete
            if self.running_phases:
                done, _ = await asyncio.wait(
                    self.running_phases.values(),
                    return_when=asyncio.FIRST_COMPLETED
                )

                for future in done:
                    phase_id = await future
                    del self.running_phases[phase_id]

                    # Get newly ready phases
                    ready_phases = self.graph.mark_phase_complete(phase_id)
                    for phase in ready_phases:
                        if len(self.running_phases) < self.max_parallel_phases:
                            self._start_phase(phase)
            else:
                await asyncio.sleep(0.01)

        self._print_summary()
        return self.results

    def _start_phase(self, phase: Phase) -> None:
        """Start execution of a phase."""
        async def run_phase() -> str:
            orchestrator = PhaseOrchestrator(
                phase=phase,
                executor=self.executor,
                max_parallel=self.max_parallel_tasks
            )
            success = await orchestrator.run()
            self.results[phase.id] = success
            return phase.id

        self.running_phases[phase.id] = asyncio.create_task(run_phase())

    def _print_summary(self) -> None:
        """Print execution summary."""
        logger.info("")
        logger.info("="*60)
        logger.info("ORCHESTRATION COMPLETE")
        logger.info("="*60)

        total_duration = 0.0
        for phase in self.graph.phases.values():
            icon = "✅" if phase.status == PhaseStatus.COMPLETED else "❌"
            duration_str = f"({phase.duration:.2f}s)" if phase.duration else ""
            logger.info(f"{icon} {phase.name} {duration_str}")
            if phase.duration is not None and phase.end_time is not None:
                start_times = [p.start_time for p in self.graph.phases.values() if p.start_time is not None]
                if start_times:
                    total_duration = max(total_duration, phase.end_time - min(start_times))

        success_count = sum(1 for p in self.graph.phases.values()
                          if p.status == PhaseStatus.COMPLETED)
        logger.info("")
        logger.info(f"Phases completed: {success_count}/{len(self.graph.phases)}")
        logger.info(f"Total time: {total_duration:.2f}s")


# ============================================================================
# PHASE DEFINITIONS (NFL Sim Engine Specific)
# ============================================================================

def create_nfl_sim_phases() -> list[Phase]:
    """Create all 12 phases for the NFL Sim Engine enhancement."""

    phases = [
        # Phase 1: CORTEX Foundation
        Phase(
            id="phase_1",
            name="CORTEX Foundation",
            phase_dependencies=[],
            tasks=[
                AgentTask(
                    id="agent_1_1",
                    name="60Hz Tick Engine",
                    script_path="scripts/agents/phase1/tick_engine.py",
                    dependencies=[],
                    outputs=["tick_engine", "tick_engine_tests"]
                ),
                AgentTask(
                    id="agent_1_2",
                    name="Deterministic RNG",
                    script_path="scripts/agents/phase1/deterministic_rng.py",
                    dependencies=[],
                    outputs=["rng_core", "rng_api", "rng_migration"]
                ),
                AgentTask(
                    id="agent_1_3",
                    name="Event Bus Enhancement",
                    script_path="scripts/agents/phase1/event_bus.py",
                    dependencies=[],
                    outputs=["event_bus", "event_bus_tests"]
                ),
            ]
        ),

        # Phase 2: GENESIS Biological
        Phase(
            id="phase_2",
            name="GENESIS Biological",
            phase_dependencies=["phase_1"],
            tasks=[
                AgentTask(
                    id="agent_2_1",
                    name="Biometric Extensions",
                    script_path="scripts/agents/phase2/biometrics.py",
                    dependencies=[],
                    outputs=["player_biometrics", "biometrics_migration"]
                ),
                AgentTask(
                    id="agent_2_2",
                    name="S2 Cognition System",
                    script_path="scripts/agents/phase2/cognition.py",
                    dependencies=["player_biometrics"],
                    outputs=["cognition_engine", "cognition_tests"]
                ),
                AgentTask(
                    id="agent_2_3",
                    name="4-Compartment Fatigue",
                    script_path="scripts/agents/phase2/fatigue.py",
                    dependencies=["player_biometrics"],
                    outputs=["fatigue_model", "fatigue_tests"]
                ),
                AgentTask(
                    id="agent_2_4",
                    name="Enhanced Injury System",
                    script_path="scripts/agents/phase2/injury.py",
                    dependencies=["player_biometrics", "fatigue_model"],
                    outputs=["injury_system_v2", "injury_tests"]
                ),
            ]
        ),

        # Phase 3: Position Physics
        Phase(
            id="phase_3",
            name="Position Physics",
            phase_dependencies=["phase_2"],
            tasks=[
                AgentTask(
                    id="agent_3_1",
                    name="QB Physics",
                    script_path="scripts/agents/phase3/qb_physics.py",
                    dependencies=[],
                    outputs=["qb_physics", "qb_tests"]
                ),
                AgentTask(
                    id="agent_3_2",
                    name="RB Physics",
                    script_path="scripts/agents/phase3/rb_physics.py",
                    dependencies=[],
                    outputs=["rb_physics", "rb_tests"]
                ),
                AgentTask(
                    id="agent_3_3",
                    name="WR Physics",
                    script_path="scripts/agents/phase3/wr_physics.py",
                    dependencies=[],
                    outputs=["wr_physics", "wr_tests"]
                ),
                AgentTask(
                    id="agent_3_4",
                    name="CB Physics",
                    script_path="scripts/agents/phase3/cb_physics.py",
                    dependencies=[],
                    outputs=["cb_physics", "cb_tests"]
                ),
                AgentTask(
                    id="agent_3_5",
                    name="DL/Edge Physics",
                    script_path="scripts/agents/phase3/dl_physics.py",
                    dependencies=[],
                    outputs=["dl_physics", "dl_tests"]
                ),
                AgentTask(
                    id="agent_3_6",
                    name="OL Physics",
                    script_path="scripts/agents/phase3/ol_physics.py",
                    dependencies=["dl_physics"],  # OL depends on DL for matchup testing
                    outputs=["ol_physics", "ol_tests"]
                ),
            ]
        ),

        # Phase 4: HIVE Environment
        Phase(
            id="phase_4",
            name="HIVE Environment",
            phase_dependencies=["phase_1", "phase_3"],
            tasks=[
                AgentTask(
                    id="agent_4_1",
                    name="Turf Degradation Grid",
                    script_path="scripts/agents/phase4/turf_grid.py",
                    dependencies=[],
                    outputs=["turf_grid", "turf_tests"]
                ),
                AgentTask(
                    id="agent_4_2",
                    name="Equipment Physics",
                    script_path="scripts/agents/phase4/equipment.py",
                    dependencies=["turf_grid"],
                    outputs=["equipment", "equipment_tests"]
                ),
                AgentTask(
                    id="agent_4_3",
                    name="Weather Integration",
                    script_path="scripts/agents/phase4/weather.py",
                    dependencies=["turf_grid", "equipment"],
                    outputs=["weather_v2", "weather_tests"]
                ),
            ]
        ),

        # Phase 5: EMPIRE Economics
        Phase(
            id="phase_5",
            name="EMPIRE Economics",
            phase_dependencies=["phase_1"],
            tasks=[
                AgentTask(
                    id="agent_5_1",
                    name="Salary Cap Engine",
                    script_path="scripts/agents/phase5/salary_cap.py",
                    dependencies=[],
                    outputs=["cap_engine", "cap_tests"]
                ),
                AgentTask(
                    id="agent_5_2",
                    name="CPU GM AI",
                    script_path="scripts/agents/phase5/gm_ai.py",
                    dependencies=["cap_engine"],
                    outputs=["gm_ai", "gm_tests"]
                ),
            ]
        ),

        # Phase 6: SOCIETY Locker Room
        Phase(
            id="phase_6",
            name="SOCIETY Locker Room",
            phase_dependencies=["phase_2", "phase_5"],
            tasks=[
                AgentTask(
                    id="agent_6_1",
                    name="Social Graph",
                    script_path="scripts/agents/phase6/social_graph.py",
                    dependencies=[],
                    outputs=["social_graph", "social_tests"]
                ),
                AgentTask(
                    id="agent_6_2",
                    name="Nemesis System",
                    script_path="scripts/agents/phase6/nemesis.py",
                    dependencies=["social_graph"],
                    outputs=["nemesis", "nemesis_tests"]
                ),
                AgentTask(
                    id="agent_6_3",
                    name="Momentum Engine",
                    script_path="scripts/agents/phase6/momentum.py",
                    dependencies=["social_graph"],
                    outputs=["momentum", "momentum_tests"]
                ),
            ]
        ),

        # Phase 7: Training System
        Phase(
            id="phase_7",
            name="Training System",
            phase_dependencies=["phase_2", "phase_3"],
            tasks=[
                AgentTask(
                    id="agent_7_1",
                    name="Position Training Programs",
                    script_path="scripts/agents/phase7/training_programs.py",
                    dependencies=[],
                    outputs=["training_programs", "training_tests"]
                ),
                AgentTask(
                    id="agent_7_2",
                    name="Weekly Scheduler",
                    script_path="scripts/agents/phase7/scheduler.py",
                    dependencies=["training_programs"],
                    outputs=["scheduler", "scheduler_tests"]
                ),
                AgentTask(
                    id="agent_7_3",
                    name="Training Philosophy",
                    script_path="scripts/agents/phase7/philosophy.py",
                    dependencies=["training_programs"],
                    outputs=["philosophy", "philosophy_tests"]
                ),
            ]
        ),

        # Phase 8: Scouting & Draft
        Phase(
            id="phase_8",
            name="Scouting & Draft",
            phase_dependencies=["phase_2", "phase_5"],
            tasks=[
                AgentTask(
                    id="agent_8_1",
                    name="True Scouting System",
                    script_path="scripts/agents/phase8/scouting.py",
                    dependencies=[],
                    outputs=["scouting_fog", "scouting_tests"]
                ),
                AgentTask(
                    id="agent_8_2",
                    name="Enhanced Combine",
                    script_path="scripts/agents/phase8/combine.py",
                    dependencies=["scouting_fog"],
                    outputs=["combine_v2", "combine_tests"]
                ),
                AgentTask(
                    id="agent_8_3",
                    name="Draft Day AI",
                    script_path="scripts/agents/phase8/draft_ai.py",
                    dependencies=["scouting_fog", "combine_v2"],
                    outputs=["draft_ai", "draft_tests"]
                ),
            ]
        ),

        # Phase 9: Playbook & AI
        Phase(
            id="phase_9",
            name="Playbook & AI",
            phase_dependencies=["phase_1", "phase_3"],
            tasks=[
                AgentTask(
                    id="agent_9_1",
                    name="Real-Time Coaching AI",
                    script_path="scripts/agents/phase9/rtc_ai.py",
                    dependencies=[],
                    outputs=["rtc_ai", "rtc_tests"]
                ),
                AgentTask(
                    id="agent_9_2",
                    name="Advanced RPO System",
                    script_path="scripts/agents/phase9/rpo.py",
                    dependencies=["rtc_ai"],
                    outputs=["rpo", "rpo_tests"]
                ),
                AgentTask(
                    id="agent_9_3",
                    name="Playbook Familiarity",
                    script_path="scripts/agents/phase9/familiarity.py",
                    dependencies=[],
                    outputs=["familiarity", "familiarity_tests"]
                ),
            ]
        ),

        # Phase 10: Stadium Effects
        Phase(
            id="phase_10",
            name="Stadium Effects",
            phase_dependencies=["phase_2"],
            tasks=[
                AgentTask(
                    id="agent_10_1",
                    name="Crowd Noise Impact",
                    script_path="scripts/agents/phase10/crowd.py",
                    dependencies=[],
                    outputs=["crowd_noise", "crowd_tests"]
                ),
            ]
        ),

        # Phase 11: Validation
        Phase(
            id="phase_11",
            name="Validation & Calibration",
            phase_dependencies=["phase_3", "phase_4", "phase_7"],
            tasks=[
                AgentTask(
                    id="agent_11_1",
                    name="Statistical Validator",
                    script_path="scripts/agents/phase11/validator.py",
                    dependencies=[],
                    outputs=["validator", "validator_tests"]
                ),
                AgentTask(
                    id="agent_11_2",
                    name="Auto-Tuner",
                    script_path="scripts/agents/phase11/auto_tuner.py",
                    dependencies=["validator"],
                    outputs=["auto_tuner", "tuner_tests"]
                ),
            ]
        ),

        # Phase 12: Database Schema
        Phase(
            id="phase_12",
            name="Database Schema",
            phase_dependencies=["phase_1"],
            tasks=[
                AgentTask(
                    id="agent_12_1",
                    name="Frame-Level Storage",
                    script_path="scripts/agents/phase12/frame_storage.py",
                    dependencies=[],
                    outputs=["frame_tables", "frame_migration"]
                ),
            ]
        ),
    ]

    return phases


# ============================================================================
# MAIN ENTRY POINTS
# ============================================================================

async def run_simulation() -> dict[str, bool]:
    """
    Run a simulated orchestration to verify the workflow.
    Does not execute real agent scripts.
    """
    logger.info("🔬 SIMULATION MODE")
    logger.info("   (No real agent scripts will be executed)")
    logger.info("")

    phases = create_nfl_sim_phases()

    # Configure simulation with varying task durations
    simulated_durations = {
        "agent_1_1": 0.3,  # Tick engine takes longer
        "agent_1_2": 0.2,
        "agent_1_3": 0.1,
        "agent_3_1": 0.25,  # QB physics
        "agent_3_2": 0.25,  # RB physics
    }

    executor = SimulatedAgentExecutor(
        simulated_durations=simulated_durations,
        base_delay=0.1
    )

    orchestrator = MasterOrchestrator(
        phases=phases,
        executor=executor,
        max_parallel_phases=4,
        max_parallel_tasks_per_phase=3
    )

    results = await orchestrator.run()

    # Print execution log
    logger.info("")
    logger.info("📋 SIMULATION EXECUTION LOG")
    logger.info("-"*40)
    for entry in executor.execution_log:
        logger.info(f"   {entry['task_name']}: {entry['simulated_duration']:.2f}s")

    return results


async def run_real_execution(work_dir: Path) -> dict[str, bool]:
    """
    Run real orchestration with actual agent scripts.
    """
    logger.info("🚀 REAL EXECUTION MODE")
    logger.info(f"   Work directory: {work_dir}")
    logger.info("")

    phases = create_nfl_sim_phases()
    marker_dir = work_dir / ".markers"

    executor = RealAgentExecutor(
        work_dir=work_dir,
        marker_dir=marker_dir
    )

    orchestrator = MasterOrchestrator(
        phases=phases,
        executor=executor,
        max_parallel_phases=4,
        max_parallel_tasks_per_phase=3
    )

    return await orchestrator.run()


def main():
    """Main entry point with argument parsing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="NFL Sim Engine Master Orchestrator"
    )
    parser.add_argument(
        "--simulate", "-s",
        action="store_true",
        help="Run in simulation mode (no real execution)"
    )
    parser.add_argument(
        "--execute", "-e",
        action="store_true",
        help="Run real execution mode"
    )
    parser.add_argument(
        "--work-dir", "-w",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Working directory for execution"
    )

    args = parser.parse_args()

    if args.simulate:
        asyncio.run(run_simulation())
    elif args.execute:
        asyncio.run(run_real_execution(args.work_dir))
    else:
        # Default to simulation
        asyncio.run(run_simulation())


if __name__ == "__main__":
    main()
