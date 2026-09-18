import pytest
from pydantic import ValidationError
from app.schemas.spatial import BoundingBox3D, PlayerSpatialState, CutsceneTriggerRequest, BodyMorphType


def test_bounding_box_valid():
    bbox = BoundingBox3D(min_point=(-0.4, -0.4, 0.0), max_point=(0.4, 0.4, 1.9))
    assert bbox.min_point[2] >= 0.0
    assert bbox.max_point[2] > bbox.min_point[2]


def test_player_spatial_state_turf_clamping():
    with pytest.raises(ValidationError):
        # position_z must be >= 0.0 (no negative turf penetration)
        PlayerSpatialState(
            player_id=1,
            position_x=10.5,
            position_y=25.0,
            position_z=-0.05,
            facing_vector=(1.0, 0.0, 0.0),
            bounding_box=BoundingBox3D(min_point=(-0.4, -0.4, 0.0), max_point=(0.4, 0.4, 1.9)),
            morph_type=BodyMorphType.ATHLETIC
        )


def test_cutscene_trigger_request_bounds():
    req = CutsceneTriggerRequest(
        game_id=10,
        play_id=45,
        drama_index=85.0,
        impact_force=78.5,
        injured_player_id=12
    )
    assert req.drama_index == 85.0
    assert req.injured_player_id == 12

    with pytest.raises(ValidationError):
        CutsceneTriggerRequest(game_id=10, play_id=45, drama_index=150.0, impact_force=50.0)
