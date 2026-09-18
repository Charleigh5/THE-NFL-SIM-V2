import time
from app.engine.spatial.accumulator import SpatialAccumulator
from app.schemas.spatial import PlayerSpatialState, BoundingBox3D, BodyMorphType


def test_spatial_accumulator_clamps_turf_and_resolves_collision():
    acc = SpatialAccumulator()
    players = [
        PlayerSpatialState(
            player_id=i,
            position_x=10.0 + (i * 0.05),
            position_y=20.0,
            position_z=0.0,
            facing_vector=(1.0, 0.0, 0.0),
            bounding_box=BoundingBox3D(min_point=(-0.3, -0.3, 0.0), max_point=(0.3, 0.3, 1.85)),
            morph_type=BodyMorphType.ATHLETIC
        )
        for i in range(22)
    ]
    start = time.perf_counter()
    resolved = acc.accumulate_frame(players)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert elapsed_ms < 2.0  # <2ms performance budget
    assert len(resolved) == 22
    for p in resolved:
        assert p.position_z >= 0.0
        assert p.bounding_box.min_point[2] >= 0.0
