import sys
import os

sys.path.append(os.getcwd())

try:
    print("Importing nfl_stats_server...")
    from backend.mcp_servers.nfl_stats_server import server as nfl_server
    print("Success.")

    print("Importing weather_server...")
    from backend.mcp_servers.weather_server import server as weather_server
    print("Success.")

    print("Importing sports_news_server...")
    from backend.mcp_servers.sports_news_server import server as news_server
    print("Success.")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
