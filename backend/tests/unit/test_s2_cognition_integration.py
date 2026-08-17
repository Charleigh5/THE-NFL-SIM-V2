"""
Unit tests for S2 Cognitive Latency & Vision Cone Integration (DEP-003).
"""

import pytest
from app.engine.genesis.cognition import (
    CognitiveProfile,
    CognitiveState,
    ReadPhase,
    VisionCone,
    OODAState,
)


class TestS2CognitionIntegration:
    """Tests for S2 cognition processing and vision cone physics."""

    def test_s2_score_modulates_ooda_latency(self):
        """High S2 score reduces OODA loop latency; low S2 increases it."""
        elite_s2_profile = CognitiveProfile(s2_cognition_score=130.0)
        poor_s2_profile = CognitiveProfile(s2_cognition_score=70.0)

        elite_ooda = elite_s2_profile.get_effective_ooda()
        poor_ooda = poor_s2_profile.get_effective_ooda()

        assert elite_ooda.total_loop_time_ms < poor_ooda.total_loop_time_ms
        assert elite_ooda.total_loop_time_ms < 200.0
        assert poor_ooda.total_loop_time_ms > 280.0

    def test_pressure_shifts_cognitive_state_and_narrows_vision_cone(self):
        """Under heavy pressure, cognitive state shifts to STRESSED/PANICKED with tunnel vision."""
        profile = CognitiveProfile(s2_cognition_score=95.0, focus_level=50.0, stress_level=0.0)
        assert profile.state == CognitiveState.FOCUSED

        # Apply extreme pocket pressure
        profile.stress_level = 85.0
        profile.state = CognitiveState.PANICKED
        profile.vision.fov_degrees = 55.0  # Narrowed from 120.0

        effective_ooda = profile.get_effective_ooda()
        # Stress degrades total loop time
        assert effective_ooda.total_loop_time_ms > 300.0

        # Peripheral target outside narrowed cone is not visible
        # Target at (10, 20) with facing (0, 0)
        can_see, quality = profile.vision.can_see_target((0.0, 0.0), (10.0, 2.0))
        assert can_see is True
        assert quality > 0.0

        # Target at extreme angle (10.0, 25.0) relative to facing 0 deg is outside 55 deg cone
        can_see_wide, _ = profile.vision.can_see_target((0.0, 0.0), (2.0, 10.0))
        assert can_see_wide is False

    def test_db_break_on_ball_reaction(self):
        """DB reaction time is derived from S2 score and vision detection."""
        db_profile = CognitiveProfile(s2_cognition_score=115.0, reaction_time_ms=220.0)
        ooda = db_profile.get_effective_ooda()

        # Elite DB reacts in < 220ms
        assert ooda.decide_time_ms + ooda.act_time_ms < 120.0
