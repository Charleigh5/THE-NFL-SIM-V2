"""
Unit tests for Broadcast schemas, phase transitions, and serialization.
"""

import pytest
from pydantic import ValidationError
from app.schemas.broadcast import (
    BroadcastPhase,
    PHASE_TRANSITIONS,
    validate_phase_transition,
    CameraShot,
    OverlayCue,
    ClipCue,
    BroadcastPlayResult,
    BroadcastStateSchema,
    BroadcastEventSchema,
    ClipCueListResponse,
)


class TestBroadcastPhaseTransitions:
    """Test state machine phase transitions."""

    def test_legal_transitions(self):
        """Verify all valid transitions pass validation."""
        assert validate_phase_transition(BroadcastPhase.IDLE, BroadcastPhase.PRE_PLAY) is True
        assert validate_phase_transition(BroadcastPhase.PRE_PLAY, BroadcastPhase.PLAY_EXEC) is True
        assert validate_phase_transition(BroadcastPhase.PRE_PLAY, BroadcastPhase.IDLE) is True
        assert validate_phase_transition(BroadcastPhase.PLAY_EXEC, BroadcastPhase.POST_PLAY) is True
        assert validate_phase_transition(BroadcastPhase.PLAY_EXEC, BroadcastPhase.REPLAY) is True
        assert validate_phase_transition(BroadcastPhase.POST_PLAY, BroadcastPhase.REPLAY) is True
        assert validate_phase_transition(BroadcastPhase.POST_PLAY, BroadcastPhase.BETWEEN_DOWNS) is True
        assert validate_phase_transition(BroadcastPhase.REPLAY, BroadcastPhase.BETWEEN_DOWNS) is True
        assert validate_phase_transition(BroadcastPhase.BETWEEN_DOWNS, BroadcastPhase.PRE_PLAY) is True
        assert validate_phase_transition(BroadcastPhase.BETWEEN_DOWNS, BroadcastPhase.HALFTIME) is True
        assert validate_phase_transition(BroadcastPhase.HALFTIME, BroadcastPhase.BETWEEN_DOWNS) is True
        assert validate_phase_transition(BroadcastPhase.HALFTIME, BroadcastPhase.IDLE) is True

    def test_illegal_transitions_raise_value_error(self):
        """Verify illegal transitions raise ValueError with descriptive message."""
        with pytest.raises(ValueError, match="Illegal broadcast phase transition"):
            validate_phase_transition(BroadcastPhase.IDLE, BroadcastPhase.PLAY_EXEC)

        with pytest.raises(ValueError, match="Illegal broadcast phase transition"):
            validate_phase_transition(BroadcastPhase.PLAY_EXEC, BroadcastPhase.PRE_PLAY)

        with pytest.raises(ValueError, match="Illegal broadcast phase transition"):
            validate_phase_transition(BroadcastPhase.REPLAY, BroadcastPhase.PLAY_EXEC)


class TestBroadcastSchemas:
    """Test schema instantiation, validation, and JSON serialization."""

    def test_camera_shot_valid(self):
        shot = CameraShot(
            id="shot_001",
            position={"x": -10.0, "y": 5.0, "z": 20.0},
            target={"x": 0.0, "y": 0.0, "z": 0.0},
            fov=60.0,
            duration=2.5,
            interpolation="smooth"
        )
        assert shot.id == "shot_001"
        assert shot.position["x"] == -10.0
        assert shot.fov == 60.0

    def test_camera_shot_fov_bounds(self):
        with pytest.raises(ValidationError):
            CameraShot(
                id="shot_bad",
                position={"x": 0.0, "y": 0.0, "z": 0.0},
                target={"x": 0.0, "y": 0.0, "z": 0.0},
                fov=150.0  # ge 10, le 120
            )

    def test_overlay_cue_valid(self):
        overlay = OverlayCue(
            id="overlay_001",
            type="lower_third",
            data={"down": 3, "distance": 4, "yard_line": 35},
            duration=3.0,
            animation="slide",
            layer=5
        )
        assert overlay.id == "overlay_001"
        assert overlay.type == "lower_third"
        assert overlay.data["down"] == 3

    def test_clip_cue_roundtrip(self):
        clip = ClipCue(
            id="clip_001",
            clip_type="formation_sweep",
            cameras=[
                CameraShot(
                    id="shot_1",
                    position={"x": -15.0, "y": 8.0, "z": 25.0},
                    target={"x": 0.0, "y": 0.0, "z": 0.0},
                    duration=3.0
                )
            ],
            overlays=[
                OverlayCue(
                    id="ov_1",
                    type="matchup_card",
                    data={"qb": "Mahomes"}
                )
            ],
            duration=3.0,
            skippable=True
        )

        dumped = clip.model_dump()
        reconstructed = ClipCue.model_validate(dumped)
        assert reconstructed.id == clip.id
        assert len(reconstructed.cameras) == 1
        assert len(reconstructed.overlays) == 1
        assert reconstructed.cameras[0].id == "shot_1"

    def test_broadcast_play_result(self):
        play_res = BroadcastPlayResult(
            play_id=101,
            play_type="pass",
            outcome="complete",
            yards_gained=25,
            passer_id=1,
            receiver_id=2,
            tackler_ids=[3],
            start_time=100.0,
            end_time=108.0,
            is_highlight_worthy=True,
            is_sack=False
        )
        assert play_res.play_id == 101
        assert play_res.yards_gained == 25
        assert play_res.is_highlight_worthy is True

    def test_broadcast_state_schema(self):
        state = BroadcastStateSchema(
            phase=BroadcastPhase.PRE_PLAY,
            current_camera_index=0,
            reduced_motion=False
        )
        assert state.phase == BroadcastPhase.PRE_PLAY
        assert state.active_clip is None

    def test_clip_cue_list_response(self):
        clip = ClipCue(
            id="clip_sweep",
            clip_type="formation_sweep",
            duration=4.5,
            skippable=True
        )
        resp = ClipCueListResponse(
            play_id=200,
            clips=[clip],
            total_duration=4.5
        )
        assert resp.play_id == 200
        assert resp.total_duration == 4.5
        assert len(resp.clips) == 1
