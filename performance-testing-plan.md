<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: PERFORMANCE_TESTING_WORKFLOW_AND_BENCHMARK_SUITE

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  The performance testing workflow (`.agent/workflows/performance_testing.md`) was originally conceived to validate three decoupled components:
  1. MCP (Model Context Protocol) tool call latencies (`benchmark_mcp.py`)
  2. Concurrent API request throughput and error rates (`load_test.py`)
  3. Real-time observability via Prometheus scraping (`/metrics`) and Grafana dashboards (`grafana_dashboard.json`)
  4. In-memory and distributed caching via Redis (`redis-cli monitor`).

- **Related Ideas:**
  - Modern SRE & chaos engineering load testing frameworks (Locust, k6, autocannon).
  - Multi-tier latency budgets: micro-benchmarks (<16ms 60Hz physics, <10ms 4th down) vs. macro-benchmarks (P95 < 250ms under 100 concurrent users).
  - Self-contained zero-dependency testing: load test utilities should work out of the box with the environment's existing async HTTP clients (`httpx`) without crashing when optional dependencies (`aiohttp`) are absent.

- **Future Potential:**
  For multi-user dynasty leagues running simultaneous weekly match simulations:
  - Backend must sustain 100+ concurrent simulated users with <1% error rate and P95 latency < 350ms.
  - Performance regressions must fail automated CI/CD pipelines via an exit code gate.
  - Real-time Prometheus metrics must export detailed histogram quantiles (`request_duration_seconds_bucket`).

- **Constraints:**
  - Must run cleanly both inside Docker (`docker-compose exec backend ...`) and in local virtual environments (`backend/.venv`).
  - No speculative abstractions or unrequested bloat.
  - Zero disruption to existing 1,605+ test suites.
  - Strict preservation of double-entry ledger invariants.

</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Maintain the existing ad-hoc scripts in `backend/scripts/`: run `load_test.py` and `benchmark_mcp.py` manually with default hardcoded URLs, assuming developers will manually install missing dependencies (`aiohttp`) and visually inspect console output without programmatic gates.

### Powerful Antithesis
1. **Dependency Fragility & Import Crash:** `load_test.py` strictly imports `aiohttp`, which is missing from `backend/.venv` (where `httpx` is the standard async client). Attempting to run `python scripts/load_test.py` immediately exits with code 1.
2. **Hardcoded Port & URL Assumptions:** `load_test.py` hardcodes `http://localhost:8000/`. When running with IPv6/IPv127 (`http://127.0.0.1:8000`) or behind a reverse proxy, the script cannot be redirected without modifying code.
3. **Single Shallow Endpoint Testing:** `load_test.py` only hits the root `/` endpoint, which does zero database interaction. It completely ignores high-throughput database endpoints like `/api/teams`, `/api/teams/1/roster`, and `/api/season/summary`.
4. **Environment Discrepancies in MCP:** `benchmark_mcp.py` invokes `"command": "python"`, which on Windows systems can execute Microsoft Store wrappers rather than the project virtualenv (`sys.executable`).
5. **Lack of Unified CI/CD Orchestration:** There is no single command that runs the entire benchmark suite, compares outputs to defined SLA budgets, and produces an authoritative pass/fail result.

### The Superior Synthesis
Transform the performance testing workflow into an institutional-grade, multi-client, parameterizable benchmark suite:
1. **Multi-Client Async Load Generator:** Refactor `load_test.py` to seamlessly use `httpx.AsyncClient` (already installed in `.venv`) with fallback to `aiohttp` or `urllib`, and add CLI flags (`--url`, `--concurrency`, `--requests`, `--endpoints`, `--budget-p95-ms`).
2. **Cross-Platform MCP Runner:** Standardize `benchmark_mcp.py` on `sys.executable` and support CLI `--iterations` and `--budget-ms` gates.
3. **Unified Benchmark Orchestrator (`run_all_benchmarks.py`):** Create an all-in-one runner that executes:
   - Part 1: Operational Latencies (Physics 16ms, Capology 40ms, Baldwin 10ms, Tension 2ms)
   - Part 2: MCP Tool Call Benchmark (Stats server < 500ms)
   - Part 3: Live API Load Test (Concurrency 50, 500 requests, P95 < 250ms)
   - Part 4: Prometheus Telemetry Probe (`/metrics` scrape)
   - Part 5: Redis Cache Diagnostic Probe
4. **Automated SLA Verification:** Exit with code 0 on all budgets met, or exit with code 1 on budget breach with detailed markdown reporting.

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Runtimes:** Python 3.11/3.13 (`backend/.venv`), Node.js 24 (`frontend/`).
- **HTTP Client:** `httpx.AsyncClient` (native async HTTP/2 support) with `aiohttp` fallback.
- **Protocol:** REST JSON, Server-Sent Events, Prometheus text exposition format (`0.0.4`), stdio MCP.
- **Target Latency Budgets:**
  - 60Hz Physics Tick: `< 16.00ms`
  - Baldwin 4th-Down Lookup: `< 10.00ms`
  - Capology Multi-Year Proration: `< 40.00ms`
  - Society Tension Evaluation: `< 2.00ms`
  - MCP Tool Call Latency: `< 500.00ms`
  - API Load Test (P95 at 50 concurrency): `< 250.00ms`

---

### 2. Actionable Step-by-Step Execution Plan

- [ ] **Step 1: Harden `load_test.py` with Multi-Client & CLI Parameterization.**
  - **File:** `backend/scripts/load_test.py`
  - **Implementation:**
    - Support `httpx.AsyncClient` as the primary async engine, falling back to `aiohttp`.
    - Add `argparse` CLI arguments:
      - `--url` (default: `http://127.0.0.1:8000`)
      - `--concurrency` (default: `50`)
      - `--requests` (default: `500`)
      - `--endpoints` (default: `["/", "/api/teams", "/api/teams/1/roster"]`)
      - `--budget-p95` (default: `250.0`)
      - `--output-format` (`table` or `json`)
    - Return non-zero exit code if error rate > 1% or P95 latency > budget.
  - **Verification:** Run `python scripts/load_test.py --requests 50 --concurrency 10`.

- [ ] **Step 2: Harden `benchmark_mcp.py` for Universal Cross-Platform Execution.**
  - **File:** `backend/scripts/benchmark_mcp.py`
  - **Implementation:**
    - Replace `"command": "python"` with `"command": sys.executable` to guarantee correct venv resolution.
    - Add CLI arguments: `--iterations` (default: `50`), `--budget-ms` (default: `500.0`).
    - Output structured JSON summary for automated ingestion.
  - **Verification:** Run `python scripts/benchmark_mcp.py --iterations 20`.

- [ ] **Step 3: Create Master Unified Benchmark Runner (`run_all_benchmarks.py`).**
  - **File:** `backend/scripts/run_all_benchmarks.py`
  - **Implementation:**
    - Executes the 4 operational latency benchmarks (`FramePhysicsEngine`, `CapologistPhysics`, `FourthDownCalculator`, `TensionEngine`).
    - Executes the MCP stats tool benchmark.
    - If live server is active, runs `load_test.py` against live endpoints and probes `/metrics`.
    - Compiles all metrics into a consolidated markdown and console telemetry table.
    - Enforces hard stop exit code 1 if any SLA is violated.
  - **Verification:** Run `python scripts/run_all_benchmarks.py`.

- [ ] **Step 4: Update Workflow Documentation & Instructions.**
  - **Files:** `.agent/workflows/performance_testing.md` and `docs/tasks/TASK-038_PERFORMANCE_TESTING_WORKFLOW_AND_BENCHMARK_PLAN.md`
  - **Implementation:**
    - Document exact execution commands for both Docker and local environments.
    - Provide troubleshooting steps for Redis connection and Prometheus scrape alerts.

---

### 3. Edge Cases & Error Handling

- **Case A: Live backend server is not running during load test:**
  - *Fallback:* `run_all_benchmarks.py` detects connection refusal on `8000`, marks API load test as `SKIPPED (Server Offline)`, and runs all in-process operational benchmarks without failing the test suite.
- **Case B: Redis server is offline or disabled:**
  - *Fallback:* `redis_cache.py` logs warning, disables cache, and falls back to in-memory/direct database queries without throwing unhandled exceptions.
- **Case C: Windows `aiohttp` import failure:**
  - *Fallback:* `load_test.py` gracefully switches to `httpx.AsyncClient` with zero user intervention.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Dependency Independence:** `load_test.py` executes cleanly in `backend/.venv` without requiring external manual pip installations.
- [ ] **Cross-Platform Compatibility:** `benchmark_mcp.py` executes via `sys.executable` on Windows, Linux, and macOS.
- [ ] **SLA Budget Enforcement:** All 5 performance pillars validated with strict mathematical thresholds.
- [ ] **Type Check & Integrity:** Python files type-checked with zero syntax or runtime errors.

</final_audit>

---

<baton_handoff>
Next Immediate Step: 
Execute Step 1 (harden `backend/scripts/load_test.py` with `httpx` async client and CLI flags), then run verification.
</baton_handoff>
