import pytest
import asyncio
import logging
from app.core.mcp_registry import registry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_mcp_server_health():
    """
    Integration test to verify health of all configured MCP servers.
    Checks:
    1. Connection establishment
    2. Tool discovery
    3. Graceful disconnection
    """
    # Load configuration
    # Point to the correct config file location relative to project root
    registry.config_path = "backend/mcp_config.json"
    registry.load_config()

    servers = registry.config.get("servers", [])
    assert len(servers) > 0, "No servers configured in mcp_config.json"

    results = {}

    for server_config in servers:
        name = server_config.get("name")
        logger.info(f"Testing health of MCP server: {name}")

        client = registry.get_client(name)
        if not client:
            # If client isn't in registry yet (because we haven't called initialize), create it temporarily
            from app.core.mcp_client import MCPHostClient
            # Resolve env vars if needed (registry usually does this)
            registry._resolve_env_vars(server_config)
            client = MCPHostClient(name, server_config)

        try:
            # 1. Test Connection
            await client.connect()
            assert client.session is not None, f"Failed to establish session with {name}"

            # 2. Test Tool Discovery
            tools = await client.list_tools()
            logger.info(f"Server {name} tools: {[t.name for t in tools] if tools else 'None'}")

            assert tools is not None, f"Failed to list tools for {name}"
            assert isinstance(tools, list), f"Tools response should be a list for {name}"
            # We expect at least one tool for these specific servers
            assert len(tools) > 0, f"No tools found for {name}"

            results[name] = "HEALTHY"

        except Exception as e:
            logger.error(f"Health check failed for {name}: {e}")
            results[name] = f"UNHEALTHY: {str(e)}"
            raise e # Fail the test if any server is unhealthy

        finally:
            # 3. Test Disconnection
            await client.disconnect()

    logger.info(f"Health Check Results: {results}")

    # Verify all expected servers were tested
    expected_servers = ["nfl_stats", "weather", "sports_news"]
    for expected in expected_servers:
        assert expected in results, f"Expected server {expected} was not tested"
        assert results[expected] == "HEALTHY", f"Server {expected} is not healthy"
