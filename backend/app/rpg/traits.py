"""
Legacy Trait System Adapter (Deprecated)
========================================
DEPRECATED: This module delegates to the canonical TraitService in app.services.trait_service.

Use the canonical trait service directly:
    from app.services.trait_service import TraitService, TRAIT_CATALOG, TraitDefinition
"""
import warnings
from typing import Dict, Any, Optional

from app.services.trait_service import (
    TraitService,
    TRAIT_CATALOG,
    TraitDefinition,
    TraitRarity,
)


class TraitSystem:
    """
    Deprecated TraitSystem adapter that cleanly delegates to TraitService.
    """
    TRAITS = {
        "DeepBall": {
            "description": "Increases deep ball accuracy and reduces drag on long throws.",
            "effect": {"throw_accuracy_deep": 5, "drag_reduction": 0.1}
        },
        "Clutch": {
            "description": "Boosts all stats in 4th quarter.",
            "effect": {"all_stats": 5, "condition": "4th_quarter"}
        },
        "BrickWall": {
            "description": "Increases pass block rating against Bull Rush.",
            "effect": {"pass_block": 10, "condition": "vs_bull_rush"}
        },
        "BallHawk": {
            "description": "Increases interception chance.",
            "effect": {"catch_in_traffic": 10, "interception_rate": 1.2}
        }
    }

    def __init__(self, db: Optional[Any] = None):
        warnings.warn(
            "TraitSystem is deprecated. Use TraitService from app.services.trait_service instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self.service = TraitService(db=db)

    @staticmethod
    def get_trait_effect(trait_name: str) -> Dict[str, Any]:
        """
        Delegate effect lookup to canonical TraitService with fallback to legacy dict.
        """
        warnings.warn(
            "TraitSystem.get_trait_effect is deprecated. Use TraitService.get_trait_by_name instead.",
            DeprecationWarning,
            stacklevel=2
        )
        # Check canonical catalog first
        trait_def = TraitService.get_trait_by_name(trait_name)
        if not trait_def:
            trait_def = TraitService.get_trait_definition(trait_name.lower())

        if trait_def and trait_def.effects:
            return trait_def.effects

        # Fallback to legacy dictionary
        return TraitSystem.TRAITS.get(trait_name, {}).get("effect", {})


__all__ = [
    "TraitSystem",
    "TraitService",
    "TRAIT_CATALOG",
    "TraitDefinition",
    "TraitRarity",
]
