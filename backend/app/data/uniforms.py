from pydantic import BaseModel
from typing import List, Dict, Optional

class UniformTier(BaseModel):
    name: str
    price_estimate: float
    material_composition: str
    fit_type: str
    features: List[str]

class UniformSet(BaseModel):
    team_id: str
    home_jersey: str
    away_jersey: str
    alternates: List[str]
    pants: List[str]
    socks: List[str]
    rivalry_uniform: Optional[str] = None

# Tiers
JERSEY_TIERS = {
    "ELITE": UniformTier(
        name="Vapor F.U.S.E. Elite",
        price_estimate=175.00,
        material_composition="88% Recycled Nylon / 12% Spandex",
        fit_type="Authentic On-Field",
        features=["Chrome Shield", "Sewn-on Logos", "Laser Perforation", "Chainmaille Mesh Grill"]
    ),
    "LIMITED": UniformTier(
        name="Vapor Limited",
        price_estimate=175.00,
        material_composition="Pique Knit / 100% Polyester",
        fit_type="Standard Athletic",
        features=["Chrome Shield", "Sewn-on Logos", "Heat-applied Twill"]
    ),
    "GAME": UniformTier(
        name="Game Jersey",
        price_estimate=120.00,
        material_composition="100% Polyester Tricot",
        fit_type="Relaxed",
        features=["Screen Print Graphics", "Sewn-on Shield", "Mesh Side Panels"]
    )
}

# Rivalry Program 2025
RIVALRY_UNIFORMS_2025 = {
    "ARI": "Built to Last (Sand/Copper)",
    "BUF": "Cold Front (Icy White)",
    "LAR": "Midnight Mode (Dark Navy/Sol)",
    "SF": "Black Alternate (Black/Red/Gold)",
    "NYJ": "Green Alternate (Action Green)",
    "MIA": "Aqua Alternate (Enhanced Aqua)",
    "NE": "Red Alternate (Modern Red)",
    "SEA": "Action Green (Color Rush)"
}
