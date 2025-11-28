from app.kernels.core.ecs_manager import Component
from pydantic import Field
from typing import Tuple

class S2Processor(Component):
    # Directive 3: S2 Score drives ProcessingLatency
    s2_score: int = Field(default=50, ge=0, le=100)
    processing_latency_ms: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        self.calculate_latency()

    def calculate_latency(self):
        # Directive 3: Low score = ~200ms delay
        # 100 score = 0ms, 50 score = 200ms, 0 score = 400ms
        self.processing_latency_ms = int((100 - self.s2_score) * 4)

class AttributeMasking(Component):
    # Directive 5: Attribute Masking (Fog of War)
    true_ratings: dict = Field(default_factory=dict)
    scouted_confidence: float = Field(default=0.5, ge=0.0, le=1.0) # 0.0 = Blind, 1.0 = Omniscient

    def get_rating_range(self, attribute: str) -> Tuple[int, int]:
        """
        Returns a Confidence Interval [Min, Max] instead of a single grade.
        """
        true_val = self.true_ratings.get(attribute, 70)
        uncertainty = int((1.0 - self.scouted_confidence) * 20) # Max +/- 20 variance
        
        min_rating = max(0, true_val - uncertainty)
        max_rating = min(99, true_val + uncertainty)
        
        return (min_rating, max_rating)

class FocusMonitor(Component):
    cognitive_load: float = 0.0 # 0-100%
    bandwidth: float = 100.0

    def apply_noise_pressure(self, decibels: float):
        # >90dB starts reducing bandwidth
        if decibels > 90:
            pressure = (decibels - 90) * 2
            self.bandwidth = max(0, 100 - pressure)
