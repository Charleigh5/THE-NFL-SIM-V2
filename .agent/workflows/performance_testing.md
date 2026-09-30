---
description: How to run performance tests, benchmarks, and load tests
---

# Performance Testing Workflow

This workflow describes how to run the multi-tier performance benchmark suite, load tests, and observability probes for the NFL Sim Engine.

## Prerequisites

1. **Option A: Containerized (Docker Compose)**
   ```bash
   docker-compose up -d
   ```
2. **Option B: Local Virtual Environment**
   - Backend running on `http://127.0.0.1:8000` (`.venv/Scripts/python.exe -m uvicorn app.main:app --port 8000`)
   - Dependencies: `httpx`, `numpy`, `sqlalchemy` (pre-installed in `.venv`)

---

## 1. Master All-In-One Benchmark Runner

Executes all 4 performance tiers (Operational Kernels, MCP Tool Calls, Concurrent Load Tests, and Prometheus Scrape Probes) with consolidated SLA verification:

```bash
# Run locally
python scripts/run_all_benchmarks.py --url http://127.0.0.1:8000

# Run inside the backend container
docker-compose exec backend python scripts/run_all_benchmarks.py
```

---

## 2. Run Operational Latency Benchmarks (Micro-Budgets)

Benchmarks live mathematical simulation engines against strict production ceilings:
- 60Hz Physics & Telemetry Frame: `< 16.00ms`
- Capology Proration & AI GM Bidding: `< 40.00ms`
- Baldwin 4th-Down Decision Model: `< 10.00ms`
- Society Chemistry 53-Man Evaluation: `< 2.00ms`

```bash
# Run locally
python scripts/benchmark_operational_latencies.py --iterations 100

# Run inside Docker
docker-compose exec backend python scripts/benchmark_operational_latencies.py
```

---

## 3. Run MCP Tool Latency Benchmark

Benchmarks stdio-based Model Context Protocol tool execution against an SLA budget of `< 500ms`:

```bash
# Run locally
python scripts/benchmark_mcp.py --iterations 50 --budget-ms 500

# Run inside Docker
docker-compose exec backend python scripts/benchmark_mcp.py
```

---

## 4. Run Concurrent API Load Test

Simulates concurrent HTTP clients hitting live API endpoints with percentile latency tracking (P95, P99, Max):

```bash
# Basic Root Load Test
python scripts/load_test.py --url http://127.0.0.1:8000 --endpoint / --concurrency 50 --requests 500 --budget-p95 250

# Roster Database Endpoint Load Test
python scripts/load_test.py --url http://127.0.0.1:8000 --endpoint /api/teams/1/roster --concurrency 20 --requests 100

# JSON Output for CI/CD Pipeline Ingestion
python scripts/load_test.py --format json --requests 200
```

---

## 5. View Prometheus Metrics & Grafana Dashboards

1. **Prometheus Scraping:** Exposes live metrics at `http://localhost:8000/metrics`.
2. **Prometheus UI:** Access at `http://localhost:9090` (configured via `prometheus.yml`).
3. **Grafana Dashboards:**
   - Access at `http://localhost:3000` (default login: `admin` / `admin`).
   - Import dashboard from `grafana_dashboard.json` or `monitoring/grafana-dashboard.json`.
   - Monitor Request Rates, P95 Latencies, HTTP Status Codes, and Database Pool Saturation.

---

## 6. Check Redis Cache Diagnostics

To verify Redis caching for chemistry and roster metadata:

```bash
# Monitor live cache operations in Docker
docker-compose exec redis redis-cli monitor

# Or check Redis keys and memory locally
redis-cli -p 6379 info memory
```
