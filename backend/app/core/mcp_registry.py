import asyncio
import json
import logging
import os
from typing import Dict, List, Optional

from app.core.mcp_client import MCPHostClient

logger = logging.getLogger(__name__)

class MCPRegistry:
    """
    Registry for managing multiple MCP server connections.
    """

    def __init__(self, config_path: str = "mcp_config.json"):
        self.config_path = config_path
        self.clients: Dict[str, MCPHostClient] = {}
        self.config: Dict = {}

    def load_config(self):
        """Load configuration from JSON file."""
        print(f"Loading config from {self.config_path}")
        if not os.path.exists(self.config_path):
            print(f"MCP config file not found at {self.config_path}")
            logger.warning(f"MCP config file not found at {self.config_path}")
            return

        with open(self.config_path, "r") as f:
            self.config = json.load(f)
        print(f"Loaded config: {self.config}")

    async def initialize(self):
        """Initialize all configured servers."""
        self.load_config()

        servers = self.config.get("servers", [])
        for server_config in servers:
            name = server_config.get("name")
            if not name:
                continue

            # Resolve environment variables in config
            self._resolve_env_vars(server_config)

        # Validate configuration after resolution
        self.validate_config()

        for server_config in servers:
            name = server_config.get("name")
            if not name:
                continue

            client = MCPHostClient(name, server_config)
            self.clients[name] = client

            try:
                print(f"Connecting to {name}...")
                await client.connect()
                print(f"Connected to {name}")
            except Exception as e:
                print(f"Failed to initialize MCP server {name}: {e}")
                logger.error(f"Failed to initialize MCP server {name}: {e}")

    def _resolve_env_vars(self, config: Dict):
        """Recursively resolve environment variables in configuration values."""
        for key, value in config.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                resolved = os.getenv(env_var)
                if resolved is None:
                    logger.warning(f"Missing environment variable: {env_var}")
                    # Keep the placeholder if missing, or could raise error
                    config[key] = value
                else:
                    config[key] = resolved
            elif isinstance(value, dict):
                self._resolve_env_vars(value)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
                        env_var = item[2:-1]
                        resolved = os.getenv(env_var)
                        if resolved is None:
                            logger.warning(f"Missing environment variable: {env_var}")
                        else:
                            value[i] = resolved

    def validate_config(self):
        """Validate that all required configuration is present."""
        servers = self.config.get("servers", [])
        for server in servers:
            # Check for unresolved environment variables
            self._check_unresolved(server)

    def _check_unresolved(self, config: Dict):
        """Recursively check for unresolved environment variables."""
        for key, value in config.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                logger.error(f"Configuration value for '{key}' is unresolved: {value}")
                # In a strict mode, we might want to raise an exception here
            elif isinstance(value, dict):
                self._check_unresolved(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
                        logger.error(f"Configuration item '{item}' is unresolved")

    async def shutdown(self):
        """Shutdown all connections."""
        for name, client in self.clients.items():
            await client.disconnect()
        self.clients.clear()

    def get_client(self, name: str) -> Optional[MCPHostClient]:
        return self.clients.get(name)

    async def get_all_tools(self) -> Dict[str, List]:
        """Get all tools from all connected servers."""
        all_tools = {}
        for name, client in self.clients.items():
            try:
                tools = await client.list_tools()
                all_tools[name] = tools
            except Exception as e:
                logger.error(f"Error listing tools for {name}: {e}")
        return all_tools

# Global registry instance
registry = MCPRegistry()
