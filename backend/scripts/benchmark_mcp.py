import asyncio
import time
import statistics
import sys
import os
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.mcp_client import MCPHostClient

async def benchmark_mcp():
    print("Starting MCP Benchmark...")

    config = {
        "transport": "stdio",
        "command": "python",
        "args": ["mcp_servers/nfl_stats_server/server.py"],
        "env": {"PYTHONPATH": "."}
    }

    client = MCPHostClient("nfl_stats", config)

    try:
        await client.connect()
        print("Connected to MCP server.")

        latencies = []
        iterations = 50

        print(f"Running {iterations} iterations...")

        for i in range(iterations):
            start = time.time()
            await client.call_tool("get_player_career_stats", {
                "player_name": "Patrick Mahomes",
                "start_year": 2020,
                "end_year": 2024
            })
            end = time.time()
            latencies.append((end - start) * 1000) # Convert to ms
            print(f"Iteration {i+1}: {latencies[-1]:.2f}ms")

        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18] # 95th percentile
        max_latency = max(latencies)
        min_latency = min(latencies)

        print("\nBenchmark Results:")
        print(f"Average Latency: {avg_latency:.2f}ms")
        print(f"P95 Latency: {p95_latency:.2f}ms")
        print(f"Min Latency: {min_latency:.2f}ms")
        print(f"Max Latency: {max_latency:.2f}ms")

        if p95_latency < 500:
            print("\nSUCCESS: P95 latency is under 500ms.")
        else:
            print("\nWARNING: P95 latency is over 500ms.")

    except Exception as e:
        print(f"Error during benchmark: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(benchmark_mcp())
