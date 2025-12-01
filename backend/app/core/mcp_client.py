import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.types import Tool

logger = logging.getLogger(__name__)

class MCPHostClient:
    """
    Client for interacting with MCP servers.
    Supports both Stdio and SSE (HTTP) transports.
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._tools: List[Tool] = []

    async def connect(self):
        """Establish connection to the MCP server."""
        transport_type = self.config.get("transport")

        try:
            if transport_type == "stdio":
                await self._connect_stdio()
            elif transport_type == "sse" or transport_type == "http":
                await self._connect_sse()
            else:
                raise ValueError(f"Unsupported transport type: {transport_type}")

            # Initialize session
            await self.session.initialize()
            logger.info(f"Connected to MCP server: {self.name}")

            # List tools
            result = await self.session.list_tools()
            self._tools = result.tools
            logger.info(f"Discovered {len(self._tools)} tools for server {self.name}")

        except Exception as e:
            logger.error(f"Failed to connect to MCP server {self.name}: {e}")
            raise

    async def _connect_stdio(self):
        command = self.config.get("command")
        args = self.config.get("args", [])
        env = self.config.get("env", None)

        if not command:
            raise ValueError("Command is required for stdio transport")

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )

        read, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )

    async def _connect_sse(self):
        url = self.config.get("url")
        headers = self.config.get("headers", {})

        if not url:
            raise ValueError("URL is required for SSE transport")

        read, write = await self.exit_stack.enter_async_context(
            sse_client(url=url, headers=headers)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )

    async def disconnect(self):
        """Close the connection."""
        await self.exit_stack.aclose()
        self.session = None
        logger.info(f"Disconnected from MCP server: {self.name}")

    async def list_tools(self) -> List[Tool]:
        """Return list of available tools."""
        if not self.session:
            raise RuntimeError("Client is not connected")
        return self._tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a specific tool on the server."""
        if not self.session:
            raise RuntimeError("Client is not connected")

        try:
            result = await self.session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            logger.error(f"Error calling tool {tool_name} on server {self.name}: {e}")
            raise

    async def ping(self) -> bool:
        """Check if server is responsive."""
        if not self.session:
            return False
        try:
            # MCP doesn't have a standard ping, but we can list tools as a health check
            await self.session.list_tools()
            return True
        except Exception:
            return False
