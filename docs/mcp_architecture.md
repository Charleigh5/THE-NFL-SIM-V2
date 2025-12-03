# MCP Architecture

## Overview

The Model Context Protocol (MCP) integration in the NFL Simulation Engine allows the backend to extend its capabilities by connecting to external tools and data sources. This architecture is designed to be modular, secure, and easily extensible.

## Core Components

### 1. MCP Registry (`app.core.mcp_registry`)

The `MCPRegistry` is the central manager for all MCP server connections.

- **Configuration Loading**: Reads `mcp_config.json` to identify available servers.
- **Environment Resolution**: Resolves environment variable placeholders (e.g., `${API_KEY}`) in the configuration.
- **Lifecycle Management**: Handles initialization (connection) and shutdown of all registered servers.
- **Tool Discovery**: Aggregates tools from all connected servers for easy access by the application.

### 2. MCP Host Client (`app.core.mcp_client`)

The `MCPHostClient` represents a single connection to an MCP server.

- **Transport Support**: Supports both `stdio` (local process) and `sse` (Server-Sent Events over HTTP) transports.
- **Security**: Implements request/response sanitization to prevent sensitive data (API keys, tokens) from leaking into logs.
- **Audit Logging**: Logs every tool execution, including arguments, duration, and results.
- **Error Handling**: Manages connection errors and tool execution failures.

### 3. MCP Servers

The application currently includes three reference MCP servers located in `backend/mcp_servers/`:

- **`nfl_stats`**: Provides historical player stats and league averages.
- **`weather`**: Simulates or fetches weather conditions for games.
- **`sports_news`**: Generates or fetches news headlines.

These servers are built using the `fastmcp` library for rapid development.

## Data Flow

1. **Initialization**: On startup, `main.py` initializes the `MCPRegistry`.
2. **Connection**: The registry iterates through `mcp_config.json`, creating an `MCPHostClient` for each server and establishing a connection.
3. **Tool Call**:
   - The application (e.g., `DraftAssistant` or `GMAgent`) requests a tool execution via the registry or a specific client.
   - The `MCPHostClient` sanitizes the request arguments.
   - The request is sent to the MCP server via the configured transport.
   - The server executes the tool and returns the result.
   - The client sanitizes the result and logs the transaction.
   - The result is returned to the caller.

## Configuration

Configuration is managed via `backend/mcp_config.json`.

```json
{
  "servers": [
    {
      "name": "nfl_stats",
      "transport": "stdio",
      "command": "python",
      "args": ["mcp_servers/nfl_stats_server/server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  ]
}
```

## Security

- **Isolation**: MCP servers run in separate processes (stdio) or containers.
- **Network**: In Docker, servers are isolated on the `app-network`.
- **Secrets**: Secrets are injected via environment variables, never hardcoded.

## Future Roadmap

- **Remote Servers**: Deploy MCP servers as standalone microservices.
- **Dynamic Discovery**: Implement a discovery mechanism for dynamic server registration.
- **Access Control**: Implement granular permissions for tool usage.
