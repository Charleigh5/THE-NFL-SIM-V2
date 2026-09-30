#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Latency Benchmark Harness
======================================================
Measures end-to-end execution latency for MCP tool calls over stdio.
Evaluates against defined latency SLA budgets (< 500ms target).

Usage:
    python scripts/benchmark_mcp.py --iterations 50 --budget-ms 500
"""

import asyncio
import time
import statistics
import sys
import os
import argparse
import json
from pathlib import Path
from typing import Dict, Any

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.mcp_client import MCPHostClient


async def run_mcp_benchmark(
    iterations: int = 50,
    budget_ms: float = 500.0,
    player_name: str = "Patrick Mahomes",
    output_format: str = "table",
) -> Dict[str, Any]:
    """Run MCP tool benchmark and return performance metrics."""
    server_path = str(backend_dir / "mcp_servers" / "nfl_stats_server" / "server.py")

    config = {
        "transport": "stdio",
        "command": sys.executable,
        "args": [server_path],
        "env": {"PYTHONPATH": str(backend_dir)},
    }

    if output_format == "table":
        print("=" * 72)
        print("THE-NFL-SIM-V2: MCP TOOL LATENCY BENCHMARK")
        print("=" * 72)
        print(f"Target Server:     {server_path}")
        print(f"Tool Name:         get_player_career_stats")
        print(f"Iterations:        {iterations}")
        print(f"Latency Budget:    < {budget_ms:.1f}ms")
        print("-" * 72)

    client = MCPHostClient("nfl_stats", config)
    latencies = []

    try:
        await client.connect()
        if output_format == "table":
            print("Connected to MCP server. Executing tool invocations...")

        for i in range(iterations):
            start = time.perf_counter()
            await client.call_tool(
                "get_player_career_stats",
                {
                    "player_name": player_name,
                    "start_year": 2020,
                    "end_year": 2024,
                },
            )
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            latencies.append(elapsed_ms)
            if output_format == "table" and (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{iterations} calls (last: {elapsed_ms:.2f}ms)")

    except Exception as e:
        print(f"ERROR during MCP benchmark: {e}", file=sys.stderr)
        return {
            "passed": False,
            "error": str(e),
            "iterations": len(latencies),
        }
    finally:
        await client.disconnect()

    if not latencies:
        return {"passed": False, "error": "No successful tool calls recorded"}

    avg_lat = statistics.mean(latencies)
    min_lat = min(latencies)
    max_lat = max(latencies)
    p95_lat = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else avg_lat
    passed = p95_lat <= budget_ms

    summary = {
        "server": "nfl_stats_server",
        "tool": "get_player_career_stats",
        "iterations": iterations,
        "avg_latency_ms": round(avg_lat, 2),
        "min_latency_ms": round(min_lat, 2),
        "p95_latency_ms": round(p95_lat, 2),
        "max_latency_ms": round(max_lat, 2),
        "budget_ms": budget_ms,
        "passed": passed,
    }

    if output_format == "json":
        print(json.dumps(summary, indent=2))
    else:
        status_label = "PASS" if passed else "FAIL (Budget Exceeded)"
        print("\nBenchmark Results:")
        print(f"Completed Calls:   {iterations}")
        print(f"Average Latency:   {avg_lat:.2f}ms")
        print(f"P95 Latency:       {p95_lat:.2f}ms (Budget: {budget_ms:.1f}ms)")
        print(f"Min Latency:       {min_lat:.2f}ms")
        print(f"Max Latency:       {max_lat:.2f}ms")
        print(f"Status:            {status_label}")
        print("=" * 72)

    return summary


def main():
    parser = argparse.ArgumentParser(description="MCP Tool Call Latency Benchmark Harness")
    parser.add_argument("--iterations", "-n", type=int, default=50, help="Total iterations")
    parser.add_argument("--budget-ms", type=float, default=500.0, help="P95 latency budget in ms")
    parser.add_argument("--player", default="Patrick Mahomes", help="Player name argument")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    args = parser.parse_args()

    summary = asyncio.run(
        run_mcp_benchmark(
            iterations=args.iterations,
            budget_ms=args.budget_ms,
            player_name=args.player,
            output_format=args.format,
        )
    )

    if not summary.get("passed", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
