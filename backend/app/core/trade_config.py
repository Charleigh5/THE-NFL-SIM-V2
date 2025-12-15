from typing import Dict, List, Any
from pydantic_settings import BaseSettings
from enum import Enum

class GMArchetype(str, Enum):
    AGGRESSIVE = "AGGRESSIVE" # Howie Roseman style: Upgrade at all costs
    HOARDER = "HOARDER"       # Sam Presti style: Accumulate assets
    SNIPER = "SNIPER"        # Brett Veach style: Surgical strikes for needs
    BALANCED = "BALANCED"     # Standard AI behavior

class TradeConfigSettings(BaseSettings):
    """
    Centralized configuration for the Trade Value System.
    Tunable parameters for value formulas, GM personalities, and league rules.
    """

    # -------------------------------------------------------------------------
    # 1. POSITIONAL VALUE TIERS (Impact Modifiers)
    # Based on PFF WAR (Wins Above Replacement) and modern contract data.
    # -------------------------------------------------------------------------
    POSITION_VALUE_TIERS: Dict[str, Dict[str, Any]] = {
        "ELITE": {
            "positions": ["QB"],
            "multiplier": 1.45,
            "description": "Franchise cornerstones. Hardest to acquire."
        },
        "PREMIUM": {
            "positions": ["EDGE", "LT", "WR", "CB"],
            "multiplier": 1.25,
            "description": "High-impact positions that paid at top of market."
        },
        "HIGH": {
            "positions": ["DT", "RT", "S"],
            "multiplier": 1.15,
            "description": "Core starters, increasing in modern value."
        },
        "STANDARD": {
            "positions": ["TE", "LB", "C", "OG", "RB"],
            "multiplier": 1.00,
            "description": "Dependent on scheme. Value flattened by market."
        },
        "DEPTH": {
            "positions": ["FB", "K", "P", "LS"],
            "multiplier": 0.65,
            "description": "Specialists and niche roles."
        }
    }

    # -------------------------------------------------------------------------
    # 2. GM ARCHETYPES
    # Personality profiles that alter trade behavior.
    # -------------------------------------------------------------------------
    GM_ARCHETYPES: Dict[GMArchetype, Dict[str, float]] = {
        GMArchetype.AGGRESSIVE: {
            "target_overvalue": 1.25,      # Willing to overpay for target
            "own_pick_value": 0.85,        # Undervalues own picks (willing to trade them)
            "future_discount": 0.90,       # Cares less about future (Win Now)
            "trade_frequency_mod": 1.5     # Trades more often
        },
        GMArchetype.HOARDER: {
            "target_overvalue": 0.90,      # Only buys at a discount
            "own_pick_value": 1.30,        # Overvalues own picks significantly
            "future_discount": 1.05,       # Values future assets highly
            "trade_frequency_mod": 0.7     # Trades less often
        },
        GMArchetype.SNIPER: {
            "target_overvalue": 1.10,      # Slight overpay for perfect fit
            "own_pick_value": 1.0,         # Fair value
            "need_focus_mod": 1.50,        # Heavily prioritizes team needs
            "trade_frequency_mod": 1.0     # Average frequency
        },
        GMArchetype.BALANCED: {
            "target_overvalue": 1.0,
            "own_pick_value": 1.0,
            "future_discount": 1.0,
            "trade_frequency_mod": 1.0
        }
    }

    # -------------------------------------------------------------------------
    # 3. PANIC & URGENCY FACTORS
    # Situational multipliers for logic overrides.
    # -------------------------------------------------------------------------
    PANIC_MULTIPLIERS: Dict[str, float] = {
        "QB_INJURY_CONTENDER": 2.0,   # "Bradford Rule": Contender loses QB -> Panic buy
        "DEADLINE_URGENCY": 1.5,      # Final week before deadline
        "JOB_SECURITY_LOW": 1.3,      # GM on hot seat buys veterans
    }

    # -------------------------------------------------------------------------
    # 4. LEAGUE RULES & CONSTRAINTS
    # -------------------------------------------------------------------------
    MAX_FUTURE_PICK_YEARS: int = 3    # Can only trade picks 3 years out (Current + 2)
    TOP_10_PICK_PREMIUM: float = 1.20 # 20% tax for trading into top 10

    def get_position_tier(self, position: str) -> str:
        """Finds the tier key for a given position."""
        for tier, data in self.POSITION_VALUE_TIERS.items():
            if position in data["positions"]:
                return tier
        return "STANDARD" # Default

    def get_position_multiplier(self, position: str) -> float:
        """Gets the value multiplier for a position."""
        tier = self.get_position_tier(position)
        return self.POSITION_VALUE_TIERS[tier]["multiplier"]

    def get_archetype_modifiers(self, archetype: GMArchetype) -> Dict[str, float]:
        """Returns modifiers for a specific GM archetype."""
        return self.GM_ARCHETYPES.get(archetype, self.GM_ARCHETYPES[GMArchetype.BALANCED])

trade_config = TradeConfigSettings()
