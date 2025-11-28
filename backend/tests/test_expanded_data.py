import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.data.helmets import HELMET_CATALOG
from app.data.facemasks import FACEMASK_CATALOG
from app.data.uniforms import JERSEY_TIERS, RIVALRY_UNIFORMS_2025
from app.data.teams import TEAM_DB
from app.data.stadiums import STADIUM_DB

def test_expanded_data():
    print("Testing Expanded Reference Data...")
    
    # 1. Helmets
    print(f"Helmets: Loaded {len(HELMET_CATALOG)} models")
    axiom = HELMET_CATALOG["AXIOM"]
    print(f"Helmets: Axiom Weight {axiom.weight_lbs} lbs")
    
    # 2. Face Masks
    print(f"Face Masks: Loaded {len(FACEMASK_CATALOG)} models")
    s2eg = FACEMASK_CATALOG["S2EG"]
    print(f"Face Masks: S2EG Visibility {s2eg.visibility_rating}")
    
    # 3. Uniforms
    print(f"Uniforms: Loaded {len(JERSEY_TIERS)} tiers")
    print(f"Uniforms: Loaded {len(RIVALRY_UNIFORMS_2025)} Rivalry Uniforms")
    print(f"Uniforms: Bills Rivalry: {RIVALRY_UNIFORMS_2025['BUF']}")
    
    # 4. Teams
    print(f"Teams: Loaded {len(TEAM_DB)} teams")
    buf = TEAM_DB["BUF"]
    print(f"Teams: BUF Primary Color {buf.colors.primary_hex}")
    
    # 5. Stadiums
    print(f"Stadiums: Loaded {len(STADIUM_DB)} stadiums")
    sofi = STADIUM_DB["SOFI"]
    print(f"Stadiums: SoFi Cost ${sofi.cost_billions}B")
    
    print("ALL EXPANDED DATA VERIFIED")

if __name__ == "__main__":
    test_expanded_data()
