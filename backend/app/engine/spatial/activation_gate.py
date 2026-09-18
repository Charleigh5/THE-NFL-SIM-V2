from typing import Tuple


class SpatialActivationGate:
    """Tier 2 Event-Driven Activation Gate (0ms bypass when calm)."""
    THRESHOLD = 75.0

    def should_trigger_cutscene(self, drama_index: float, impact_force: float) -> Tuple[bool, str]:
        if drama_index >= self.THRESHOLD:
            return True, "HIGH_DRAMA_INDEX"
        if impact_force >= self.THRESHOLD:
            return True, "ORTHOPEDIC_TRAUMA_IMPACT"
        return False, "BELOW_ACTIVATION_THRESHOLD"
