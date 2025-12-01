import os
import sys
import urllib.request
from pathlib import Path

# Add backend directory to path so we can import app
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.data.teams import TEAM_DB

import ssl

def download_logos():
    # Setup paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parents[2]
    logos_dir = project_root / "frontend" / "public" / "logos"
    
    # Create directory if it doesn't exist
    logos_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading logos to: {logos_dir}")
    
    base_url = "https://a.espncdn.com/i/teamlogos/nfl/500"
    
    # Special mappings for ESPN codes if they differ from our DB
    espn_mapping = {
        "WAS": "wsh",
        "WSH": "wsh"
    }
    
    success_count = 0
    
    # Create unverified SSL context
    ssl_context = ssl._create_unverified_context()
    
    # Create an opener with the unverified context
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)
    
    for team_id, team_data in TEAM_DB.items():
        abbr = team_data.abbreviation
        espn_code = espn_mapping.get(abbr, abbr.lower())
        
        url = f"{base_url}/{espn_code}.png"
        target_file = logos_dir / f"{abbr}.png"
        
        try:
            print(f"Downloading {abbr} from {url}...")
            urllib.request.urlretrieve(url, target_file)
            success_count += 1
        except Exception as e:
            print(f"Error downloading {abbr}: {e}")
            # Try fallback for WAS/WSH if failed
            if abbr == "WAS":
                try:
                    print(f"Retrying WAS as 'was'...")
                    url = f"{base_url}/was.png"
                    urllib.request.urlretrieve(url, target_file)
                    success_count += 1
                except Exception as e2:
                    print(f"Failed fallback for WAS: {e2}")

    print(f"Finished. Downloaded {success_count}/{len(TEAM_DB)} logos.")

if __name__ == "__main__":
    download_logos()
