import json
import os
import sys
from pathlib import Path

def verify_mcp_config(config_path="backend/mcp_config.json"):
    """
    Verifies the MCP configuration file.
    """
    print(f"Verifying MCP config at: {config_path}")

    # 1. Check file existence
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config file: {e}")
        return False

    servers = config.get("servers", [])
    if not servers:
        print("⚠️ No servers configured.")
        return True

    all_valid = True

    for server in servers:
        name = server.get("name", "Unknown")
        print(f"\nChecking server: {name}")

        # Check required fields
        if not server.get("command"):
            print(f"  ❌ Missing 'command'")
            all_valid = False

        args = server.get("args", [])
        if not args:
             print(f"  ⚠️ No 'args' specified (might be intentional)")

        # Check if script path exists (if it's a python script in args)
        if server.get("command") == "python" and args:
            script_path = args[0]
            # Handle relative paths
            if not os.path.isabs(script_path):
                # Try relative to project root (cwd)
                abs_path = os.path.abspath(script_path)
                if not os.path.exists(abs_path):
                     print(f"  ❌ Script file not found: {script_path} (checked {abs_path})")
                     all_valid = False
                else:
                    print(f"  ✅ Script file found: {script_path}")
            else:
                 if not os.path.exists(script_path):
                     print(f"  ❌ Script file not found: {script_path}")
                     all_valid = False
                 else:
                    print(f"  ✅ Script file found: {script_path}")

        # Check environment variables
        env = server.get("env", {})
        for key, value in env.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                if env_var not in os.environ:
                    print(f"  ⚠️ Environment variable referenced but not set: {env_var}")

    if all_valid:
        print("\n✅ MCP Configuration is VALID")
    else:
        print("\n❌ MCP Configuration has ERRORS")

    return all_valid

if __name__ == "__main__":
    # Adjust path if running from backend dir or root
    if os.path.exists("mcp_config.json"):
        config_path = "mcp_config.json"
    elif os.path.exists("backend/mcp_config.json"):
        config_path = "backend/mcp_config.json"
    else:
        # Fallback to absolute path assumption or default
        config_path = "backend/mcp_config.json"

    success = verify_mcp_config(config_path)
    sys.exit(0 if success else 1)
