from typing import List
from app.schemas.spatial import PlayerSpatialState, BoundingBox3D


class SpatialAccumulator:
    """Tier 1 Deterministic Spatial Accumulator (<2ms per 22 players)."""

    def accumulate_frame(self, players: List[PlayerSpatialState]) -> List[PlayerSpatialState]:
        resolved: List[PlayerSpatialState] = []
        for p in players:
            # Enforce non-negative turf elevation
            clamped_z = max(0.0, p.position_z)

            # Recalculate world AABB
            min_pt = (p.position_x - 0.3, p.position_y - 0.3, clamped_z)
            max_pt = (p.position_x + 0.3, p.position_y + 0.3, clamped_z + 1.85)

            resolved.append(
                PlayerSpatialState(
                    player_id=p.player_id,
                    position_x=p.position_x,
                    position_y=p.position_y,
                    position_z=clamped_z,
                    facing_vector=p.facing_vector,
                    bounding_box=BoundingBox3D(min_point=min_pt, max_point=max_pt),
                    morph_type=p.morph_type
                )
            )
        return resolved
