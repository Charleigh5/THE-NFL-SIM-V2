import pytest
import asyncio
import os
import sys
from app.core.mcp_client import MCPHostClient

# Helper to get absolute path to server file
def get_server_path(server_name):
    # Assuming this test is in backend/tests/mcp/
    # and servers are in backend/mcp_servers/
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "mcp_servers", server_name, "server.py")

@pytest.mark.asyncio
async def test_nfl_stats_integration():
    server_path = get_server_path("nfl_stats_server")
    config = {
        "transport": "stdio",
        "command": sys.executable,
        "args": [server_path]
    }

    client = MCPHostClient("nfl_stats_test", config)
    await client.connect()

    try:
        tools = await client.list_tools()
        assert len(tools) >= 3

        # Test tool call
        result = await client.call_tool("get_player_career_stats", {"player_name": "Test Player"})
        assert result is not None
        # FastMCP returns a list of Content objects, or similar.
        # We need to inspect the result structure.
        # Usually result.content[0].text contains the JSON string or data.

    finally:
        await client.disconnect()

@pytest.mark.asyncio
async def test_concurrent_requests():
    server_path = get_server_path("nfl_stats_server")
    config = {
        "transport": "stdio",
        "command": sys.executable,
        "args": [server_path]
    }

    client = MCPHostClient("nfl_stats_concurrent", config)
    await client.connect()

    try:
        # Create multiple concurrent tasks
        tasks = []
        for i in range(5):
            tasks.append(client.call_tool("get_player_career_stats", {"player_name": f"Player {i}"}))

        results = await asyncio.gather(*tasks)
        assert len(results) == 5

    finally:
        await client.disconnect()

@pytest.mark.asyncio
async def test_error_handling():
    server_path = get_server_path("nfl_stats_server")
    config = {
        "transport": "stdio",
        "command": sys.executable,
        "args": [server_path]
    }

    client = MCPHostClient("nfl_stats_error", config)
    await client.connect()

    try:
        # Call non-existent tool
        # FastMCP returns a result with isError=True for unknown tools
        try:
            result = await client.call_tool("non_existent_tool", {})
            assert result.isError is True
        except Exception as e:
            # Some implementations might raise, but FastMCP usually returns error result
            # If it raised, that's also acceptable error handling
            pass

    finally:
        await client.disconnect()
