import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.mcp_client import MCPHostClient

@pytest.mark.asyncio
async def test_mcp_client_init():
    config = {"transport": "stdio", "command": "python", "args": ["server.py"]}
    client = MCPHostClient("test_server", config)
    assert client.name == "test_server"
    assert client.config == config
    assert client.session is None

@pytest.mark.asyncio
async def test_connect_invalid_transport():
    config = {"transport": "invalid"}
    client = MCPHostClient("test_server", config)

    with pytest.raises(ValueError, match="Unsupported transport type"):
        await client.connect()

@pytest.mark.asyncio
async def test_connect_stdio_missing_command():
    config = {"transport": "stdio"}
    client = MCPHostClient("test_server", config)

    with pytest.raises(ValueError, match="Command is required"):
        await client.connect()

@pytest.mark.asyncio
async def test_connect_sse_missing_url():
    config = {"transport": "sse"}
    client = MCPHostClient("test_server", config)

    with pytest.raises(ValueError, match="URL is required"):
        await client.connect()
