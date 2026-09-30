#!/usr/bin/env python3
"""
High-Throughput Concurrent Load Testing Harness
================================================
Simulates concurrent clients hitting live API endpoints.
Supports both httpx.AsyncClient (default) and aiohttp.ClientSession.

Usage:
    python scripts/load_test.py --url http://127.0.0.1:8000 --concurrency 50 --requests 500
    python scripts/load_test.py --endpoint /api/teams --budget-p95 200
"""

import asyncio
import time
import statistics
import sys
import argparse
import json
from typing import List, Tuple, Optional

# Try httpx first (standard in FastAPI / .venv), fall back to aiohttp
try:
    import httpx
except ImportError:
    httpx = None

try:
    import aiohttp
except ImportError:
    aiohttp = None


async def make_request_httpx(client: "httpx.AsyncClient", url: str) -> Tuple[float, int]:
    """Execute a single HTTP request using httpx."""
    start = time.perf_counter()
    try:
        response = await client.get(url, timeout=10.0)
        return (time.perf_counter() - start) * 1000.0, response.status_code
    except Exception:
        return (time.perf_counter() - start) * 1000.0, 0


async def make_request_aiohttp(session: "aiohttp.ClientSession", url: str) -> Tuple[float, int]:
    """Execute a single HTTP request using aiohttp."""
    start = time.perf_counter()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10.0)) as response:
            await response.read()
            return (time.perf_counter() - start) * 1000.0, response.status
    except Exception:
        return (time.perf_counter() - start) * 1000.0, 0


async def run_load_test(
    base_url: str,
    endpoint: str,
    concurrency: int,
    total_requests: int,
    budget_p95_ms: float = 250.0,
    output_format: str = "table",
    engine: str = "auto",
) -> dict:
    """Run concurrent load test and return summary telemetry."""
    if httpx is None and aiohttp is None:
        print("ERROR: Neither 'httpx' nor 'aiohttp' is installed. Please install httpx or aiohttp.")
        sys.exit(1)

    full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    if engine == "aiohttp" and aiohttp is not None:
        engine_name = "aiohttp"
    elif engine == "httpx" and httpx is not None:
        engine_name = "httpx"
    else:
        # Prefer aiohttp for high-concurrency low-latency benchmarking when available
        engine_name = "aiohttp" if aiohttp is not None else "httpx"

    if output_format == "table":
        print("=" * 72)
        print("THE-NFL-SIM-V2: ASYNC API LOAD TEST HARNESS")
        print("=" * 72)
        print(f"Target URL:        {full_url}")
        print(f"Engine:            {engine_name}")
        print(f"Concurrency:       {concurrency}")
        print(f"Total Requests:    {total_requests}")
        print(f"P95 Latency SLA:   < {budget_p95_ms:.1f}ms")
        print("-" * 72)

    semaphore = asyncio.Semaphore(concurrency)
    results: List[Tuple[float, int]] = []

    if engine_name == "httpx":
        limits = httpx.Limits(max_connections=concurrency * 2, max_keepalive_connections=concurrency)
        async with httpx.AsyncClient(limits=limits, follow_redirects=True) as client:
            # Pre-warm connection pool to establish persistent keep-alive connections
            warm_tasks = [make_request_httpx(client, full_url) for _ in range(concurrency)]
            await asyncio.gather(*warm_tasks)

            async def bounded_httpx():
                async with semaphore:
                    return await make_request_httpx(client, full_url)

            tasks = [bounded_httpx() for _ in range(total_requests)]
            start_time = time.perf_counter()
            results = await asyncio.gather(*tasks)
            total_time = time.perf_counter() - start_time
    else:
        conn = aiohttp.TCPConnector(limit=concurrency * 2)
        async with aiohttp.ClientSession(connector=conn) as session:
            # Pre-warm connection pool to establish persistent keep-alive connections
            warm_tasks = [make_request_aiohttp(session, full_url) for _ in range(concurrency)]
            await asyncio.gather(*warm_tasks)

            async def bounded_aiohttp():
                async with semaphore:
                    return await make_request_aiohttp(session, full_url)

            tasks = [bounded_aiohttp() for _ in range(total_requests)]
            start_time = time.perf_counter()
            results = await asyncio.gather(*tasks)
            total_time = time.perf_counter() - start_time

    latencies = [r[0] for r in results]
    statuses = [r[1] for r in results]

    success_count = sum(1 for s in statuses if 200 <= s < 400)
    error_count = total_requests - success_count
    req_per_sec = total_requests / total_time if total_time > 0 else 0.0

    avg_lat = statistics.mean(latencies) if latencies else 0.0
    min_lat = min(latencies) if latencies else 0.0
    max_lat = max(latencies) if latencies else 0.0
    p95_lat = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else avg_lat
    p99_lat = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else p95_lat

    passed = (p95_lat <= budget_p95_ms) and (error_count / total_requests <= 0.01)

    summary = {
        "url": full_url,
        "engine": engine_name,
        "concurrency": concurrency,
        "total_requests": total_requests,
        "total_time_seconds": round(total_time, 3),
        "requests_per_second": round(req_per_sec, 2),
        "success_count": success_count,
        "error_count": error_count,
        "avg_latency_ms": round(avg_lat, 2),
        "min_latency_ms": round(min_lat, 2),
        "p95_latency_ms": round(p95_lat, 2),
        "p99_latency_ms": round(p99_lat, 2),
        "max_latency_ms": round(max_lat, 2),
        "budget_p95_ms": budget_p95_ms,
        "passed": passed,
    }

    if output_format == "json":
        print(json.dumps(summary, indent=2))
    else:
        status_label = "PASS" if passed else "FAIL (SLA Breach)"
        print("Load Test Results:")
        print(f"Total Duration:    {total_time:.2f}s")
        print(f"Throughput:        {req_per_sec:.2f} req/sec")
        print(f"Successful:        {success_count}/{total_requests} ({success_count / total_requests * 100:.1f}%)")
        print(f"Errors:            {error_count}")
        print(f"Min Latency:       {min_lat:.2f}ms")
        print(f"Avg Latency:       {avg_lat:.2f}ms")
        print(f"P95 Latency:       {p95_lat:.2f}ms (Budget: {budget_p95_ms:.1f}ms)")
        print(f"P99 Latency:       {p99_lat:.2f}ms")
        print(f"Max Latency:       {max_lat:.2f}ms")
        print(f"Overall Status:    {status_label}")
        print("=" * 72)

    return summary


def main():
    parser = argparse.ArgumentParser(description="NFL Sim Engine Load Testing Harness")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="Base URL for target server")
    parser.add_argument("--endpoint", default="/", help="Endpoint path to test (e.g. /, /api/teams)")
    parser.add_argument("--concurrency", "-c", type=int, default=50, help="Number of concurrent workers")
    parser.add_argument("--requests", "-n", type=int, default=500, help="Total requests to dispatch")
    parser.add_argument("--budget-p95", type=float, default=250.0, help="P95 latency SLA threshold in ms")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    parser.add_argument("--engine", choices=["auto", "aiohttp", "httpx"], default="auto", help="HTTP client engine")
    args = parser.parse_args()

    summary = asyncio.run(
        run_load_test(
            base_url=args.url,
            endpoint=args.endpoint,
            concurrency=args.concurrency,
            total_requests=args.requests,
            budget_p95_ms=args.budget_p95,
            output_format=args.format,
            engine=args.engine,
        )
    )

    if not summary["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
