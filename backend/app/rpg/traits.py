"""
DEPRECATED: This module is deprecated and will be removed in a future release.

Use the new trait system instead:
    from app.services.trait_service import TraitService, TRAIT_CATALOG, TraitDefinition

The new system provides:
    - 25 traits (vs 4 in this legacy module)
    - Database-backed persistence
    - Eligibility checking
    - Gameplay integration
"""

import warnings


class TraitSystem:
    """
    DEPRECATED: Legacy trait system with 4 hardcoded traits.
    Use TraitService from app.services.trait_service instead.
    """

    TRAITS = {
        "DeepBall": {
            "description": "Increases deep ball accuracy and reduces drag on long throws.",
            "effect": {"throw_accuracy_deep": 5, "drag_reduction": 0.1},
        },
        "Clutch": {
            "description": "Boosts all stats in 4th quarter.",
            "effect": {"all_stats": 5, "condition": "4th_quarter"},
        },
        "BrickWall": {
            "description": "Increases pass block rating against Bull Rush.",
            "effect": {"pass_block": 10, "condition": "vs_bull_rush"},
        },
        "BallHawk": {
            "description": "Increases interception chance.",
            "effect": {"catch_in_traffic": 10, "interception_rate": 1.2},
        },
    }

    def __init__(self):
        warnings.warn(
            "TraitSystem is deprecated. Use TraitService from app.services.trait_service instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    @staticmethod
    def get_trait_effect(trait_name: str) -> dict:
        warnings.warn(
            "TraitSystem.get_trait_effect is deprecated. Use TraitService.get_trait_by_name instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return TraitSystem.TRAITS.get(trait_name, {}).get("effect", {})
