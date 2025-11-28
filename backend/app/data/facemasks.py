from pydantic import BaseModel
from typing import List, Optional

class FaceMaskModel(BaseModel):
    code: str
    manufacturer: str
    style_type: str # Open, Semi-Open, Closed, Full Cage
    positions: List[str]
    material: str
    weight_oz: float
    visibility_rating: float # 0.0 - 1.0
    features: List[str]

FACEMASK_CATALOG = {
    # QB/WR/CB - Open
    "S2EG": FaceMaskModel(
        code="S2EG",
        manufacturer="Riddell",
        style_type="Open",
        positions=["QB", "WR", "CB"],
        material="Carbon Steel",
        weight_oz=10.0,
        visibility_rating=0.95,
        features=["2-bar design", "Maximum field of vision", "E-gap"]
    ),
    "AXIOM_2B_TI": FaceMaskModel(
        code="AXIOM 2B-TI",
        manufacturer="Riddell",
        style_type="Open",
        positions=["QB", "WR", "CB"],
        material="Titanium",
        weight_oz=6.5,
        visibility_rating=0.98,
        features=["Titanium construction", "Panoramic view"]
    ),
    
    # RB/TE/S/LB - Semi-Open
    "S2BD": FaceMaskModel(
        code="S2BD",
        manufacturer="Riddell",
        style_type="Semi-Open",
        positions=["RB", "TE", "S", "LB"],
        material="Carbon Steel",
        weight_oz=14.0,
        visibility_rating=0.85,
        features=["2-bar D-cage", "Enhanced oral protection"]
    ),
    "F7_ROPO_SW": FaceMaskModel(
        code="F7 ROPO-SW-NB-VC",
        manufacturer="Schutt",
        style_type="Semi-Open",
        positions=["RB", "TE", "S", "LB"],
        material="Titanium",
        weight_oz=9.5,
        visibility_rating=0.90,
        features=["Single Wire", "Titanium", "Reinforced Oral Protection"]
    ),

    # FB/MLB - Closed
    "SF_2BDC_TX": FaceMaskModel(
        code="SF-2BDC-TX-HD",
        manufacturer="Riddell",
        style_type="Closed",
        positions=["FB", "MLB"],
        material="Carbon Steel",
        weight_oz=18.0,
        visibility_rating=0.75,
        features=["Heavy Duty", "Jaw protection", "3-4 horizontal bars"]
    ),

    # Linemen - Full Cage
    "F7_ROPO_DW": FaceMaskModel(
        code="F7 ROPO-DW-O-NB-VC",
        manufacturer="Schutt",
        style_type="Full Cage",
        positions=["OL", "DL"],
        material="Carbon Steel",
        weight_oz=22.0,
        visibility_rating=0.65,
        features=["Double Wire", "Full oral protection", "Max durability"]
    )
}
