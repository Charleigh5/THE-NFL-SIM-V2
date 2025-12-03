# Security Documentation

## Overview

This document outlines the security practices and configurations for the NFL Simulation Engine, specifically focusing on the Model Context Protocol (MCP) integration and general application security.

## Configuration Management

### Environment Variables

- All sensitive configuration (API keys, database credentials, secrets) must be stored in environment variables.
- A `.env.example` file is provided in the root directory to guide configuration.
- **NEVER** commit `.env` files or hardcode secrets in the codebase.

### API Key Validation

- The application validates the presence of required environment variables on startup.
- The `MCPRegistry` checks for any unresolved placeholders (e.g., `${OPENAI_API_KEY}`) in `mcp_config.json`.
- If a required variable is missing, the application will log a warning or error.

## MCP Security

### Request Sanitization

- All MCP tool calls (requests and responses) are logged for audit purposes.
- A sanitization layer (`MCPHostClient._sanitize`) automatically masks sensitive keys in logs, such as:
  - `api_key`
  - `password`
  - `token`
  - `secret`
- This ensures that secrets do not leak into application logs.

### Network Isolation

- The application uses Docker for containerization.
- A custom bridge network (`app-network`) is defined in `docker-compose.yml` to isolate application services.
- Future MCP servers deployed as containers should be attached to this network to restrict external access.

### Tool Execution

- MCP servers currently run as local processes (`stdio` transport) or via HTTP (`sse`).
- Ensure that `mcp_config.json` only defines trusted servers and commands.
- The `stdio` transport executes commands with the privileges of the parent process; ensure the backend runs with least privilege.

## Audit Logging

- All MCP interactions are logged with the following details:
  - Server Name
  - Tool Name
  - Arguments (Sanitized)
  - Execution Duration
  - Result (Sanitized)
- Logs are stored in the `logs/` directory and are rotated automatically.

## Security Review Checklist

- [ ] Verify `.env` is in `.gitignore`.
- [ ] Rotate API keys regularly.
- [ ] Review `mcp_config.json` for unauthorized server definitions.
- [ ] Monitor logs for any accidental leakage of sensitive data.
- [ ] Ensure Docker containers run as non-root users where possible.
