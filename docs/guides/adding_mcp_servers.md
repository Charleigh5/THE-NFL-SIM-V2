# Guide: Adding New MCP Servers

This guide explains how to create and integrate a new Model Context Protocol (MCP) server into the NFL Simulation Engine.

## 1. Create the Server Script

We recommend using the `fastmcp` library for Python-based servers.

1.  Create a new directory in `backend/mcp_servers/` (e.g., `my_new_server`).
2.  Create a `server.py` file inside it.

```python
from mcp.server.fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("my_new_server")

@mcp.tool()
def my_custom_tool(arg1: str, arg2: int) -> str:
    """
    Description of what this tool does.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    """
    return f"Processed {arg1} with {arg2}"

if __name__ == "__main__":
    mcp.run()
```

## 2. Register the Server

Add the new server to `backend/mcp_config.json`.

```json
{
  "servers": [
    ...,
    {
      "name": "my_new_server",
      "transport": "stdio",
      "command": "python",
      "args": [
        "mcp_servers/my_new_server/server.py"
      ],
      "env": {
        "PYTHONPATH": "."
      }
    }
  ]
}
```

## 3. Configuration (Optional)

If your server requires API keys or other secrets:

1.  Add the variable to `.env` (and `.env.example`).
2.  Reference it in `mcp_config.json` using the `${VAR_NAME}` syntax.

```json
    "env": {
      "PYTHONPATH": ".",
      "MY_API_KEY": "${MY_API_KEY}"
    }
```

## 4. Testing

1.  Restart the backend to load the new configuration.
2.  Verify the server connection in the logs:
    `Connected to MCP server: my_new_server`
3.  Use the `inspect_mcp.py` script (if available) or write a test case to verify the tool is callable.

## Best Practices

- **Type Hinting**: Always use Python type hints for tool arguments and return values.
- **Docstrings**: Write clear docstrings. These are used by the LLM to understand how to use the tool.
- **Error Handling**: Handle exceptions gracefully within your tools.
- **Statelessness**: Keep tools stateless whenever possible.
