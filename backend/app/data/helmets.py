from pydantic import BaseModel
from typing import List, Optional

class HelmetModel(BaseModel):
    name: str
    manufacturer: str
    weight_lbs: float
    dimensions: str # e.g. "11x9.5x10"
    shell_material: str
    safety_rating: float # 0.0 - 5.0
    features: List[str]
    compatible_facemasks: List[str]
    price_estimate: float

# Catalog
HELMET_CATALOG = {
    "SPEEDFLEX": HelmetModel(
        name="Riddell SpeedFlex",
        manufacturer="Riddell",
        weight_lbs=4.8,
        dimensions="11\" height, 9.5\" width, 10\" length",
        shell_material="Polycarbonate with flex panel system",
        safety_rating=4.8,
        features=[
            "Patented Flex System with crown flex panels",
            "Ratchet-Loc chinstrap system",
            "TPU cushioning",
            "4-point chinstrap attachment",
            "Cam-Loc quick release mechanism"
        ],
        compatible_facemasks=["SpeedFlex-specific"],
        price_estimate=450.00
    ),
    "AXIOM": HelmetModel(
        name="Riddell Axiom",
        manufacturer="Riddell",
        weight_lbs=3.35,
        dimensions="11\" height",
        shell_material="Polycarbonate with Surround Flex System",
        safety_rating=5.0,
        features=[
            "Multiple integrated flex panels",
            "Frontal Protection System",
            "Panoramic elliptical face mask",
            "Optically Correct Visor",
            "InSite Smart Helmet Technology"
        ],
        compatible_facemasks=["Cast cage construction"],
        price_estimate=1499.99
    ),
    "F7_2_0": HelmetModel(
        name="Schutt F7 2.0",
        manufacturer="Schutt",
        weight_lbs=4.3,
        dimensions="Standard varsity size",
        shell_material="Polycarbonate with Tektonic Plate Technology",
        safety_rating=4.9,
        features=[
            "TPU cushioning",
            "RFLX-S impact layer",
            "Tektonic plates",
            "Fast-access inflation point",
            "SUREFIT Air Liner",
            "Stacking pod system"
        ],
        compatible_facemasks=["F7 Series"],
        price_estimate=500.00
    ),
    "VICIS_ZERO2": HelmetModel(
        name="VICIS ZERO2",
        manufacturer="VICIS",
        weight_lbs=4.0, # "Lightest among premium" - estimated
        dimensions="Custom fit",
        shell_material="Multilayer deformable shell",
        safety_rating=5.0,
        features=[
            "RFLX 2.0 technology",
            "Deforms on impact",
            "DLTA Fit System",
            "Rapid Mount face guard attachment",
            "Fusion Elite Chin Strap"
        ],
        compatible_facemasks=["Rapid Mount"],
        price_estimate=900.00
    ),
    "VENGEANCE_A11": HelmetModel(
        name="Schutt Vengeance A11 2.0",
        manufacturer="Schutt",
        weight_lbs=3.9,
        dimensions="Standard",
        shell_material="Polycarbonate",
        safety_rating=4.0,
        features=["TPU cushioning", "Lightweight shell"],
        compatible_facemasks=["Vengeance Series"],
        price_estimate=250.00
    )
}
