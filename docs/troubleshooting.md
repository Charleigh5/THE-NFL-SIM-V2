# Troubleshooting Guide

## MCP Server Issues

### Server Fails to Connect

**Symptoms**:

- Log message: `Failed to connect to MCP server <name>`
- Application startup takes a long time.

**Possible Causes**:

- **Incorrect Command**: Check `mcp_config.json`. Ensure the `command` and `args` are correct relative to the backend execution directory.
- **Missing Dependencies**: Ensure the server's dependencies are installed in the environment.
- **Environment Variables**: Check if required environment variables are set in `.env`.

**Resolution**:

1. Try running the server script manually: `python backend/mcp_servers/<name>/server.py`.
2. Check `backend_out.log` for specific error tracebacks.

### Tool Execution Errors

**Symptoms**:

- Log message: `Error calling tool <name> on server <server>: ...`

**Possible Causes**:

- **Invalid Arguments**: The LLM or caller provided arguments that don't match the tool definition.
- **Server-Side Error**: The tool logic failed (e.g., external API down).

**Resolution**:

1. Check the audit logs to see the arguments passed.
2. Verify the tool logic handles edge cases.

## Database Issues

### Connection Refused

**Symptoms**:

- `OperationalError: connection to server at "localhost", port 5432 failed`

**Resolution**:

1. Ensure Docker containers are running: `docker-compose up -d`.
2. Check database logs: `docker-compose logs db`.

## General Debugging

- **Logs**: Check `backend/logs/app.log` (if configured) or standard output.
- **Health Check**: The root endpoint `GET /` should return a welcome message.
