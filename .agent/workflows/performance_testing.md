---
description: How to run performance tests and benchmarks
---

# Performance Testing Workflow

This workflow describes how to run the performance benchmarks and load tests for the NFL Sim Engine.

## Prerequisites

1. Ensure the application stack is running:
   ```bash
   docker-compose up -d
   ```
2. Ensure you have the necessary python dependencies installed in your local environment if running scripts locally, or run them inside the backend container.

## 1. Run MCP Benchmark

This script benchmarks the latency of MCP tool calls.

```bash
# Run inside the backend container
docker-compose exec backend python scripts/benchmark_mcp.py
```

## 2. Run Load Test

This script simulates concurrent users hitting the API.

```bash
# Run inside the backend container
docker-compose exec backend python scripts/load_test.py
```

## 3. View Metrics

1. Access Grafana at `http://localhost:3000`.
2. Login with `admin` / `admin`.
3. Import the dashboard from `grafana_dashboard.json`.
4. View real-time metrics for Request Rate, Latency, and Errors.

## 4. Check Redis Cache

To verify Redis caching is working:

```bash
docker-compose exec redis redis-cli monitor
```

Then run the benchmark or use the app. You should see `GET` and `SET` commands.
