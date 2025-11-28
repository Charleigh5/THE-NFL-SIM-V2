class TraitSystem:
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
    
    @staticmethod
    def get_trait_effect(trait_name: str) -> dict:
        return TraitSystem.TRAITS.get(trait_name, {}).get("effect", {})
