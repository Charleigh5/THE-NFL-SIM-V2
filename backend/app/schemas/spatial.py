from enum import StrEnum

from pydantic import BaseModel, Field


class BodyMorphType(StrEnum):
    LEAN = "lean"
    ATHLETIC = "athletic"
    MUSCULAR = "muscular"
    LARGE = "large"


class BoundingBox3D(BaseModel):
    min_point: tuple[float, float, float] = Field(
        ..., description="[min_x, min_y, min_z] in meters"
    )
    max_point: tuple[float, float, float] = Field(
        ..., description="[max_x, max_y, max_z] in meters"
    )


class PlayerSpatialState(BaseModel):
    player_id: int
    position_x: float
    position_y: float
    position_z: float = Field(ge=0.0, description="Elevation above turf (Z-up >= 0.0)")
    facing_vector: tuple[float, float, float]
    bounding_box: BoundingBox3D
    morph_type: BodyMorphType


class CutsceneTriggerRequest(BaseModel):
    game_id: int
    play_id: int
    drama_index: float = Field(ge=0.0, le=100.0)
    impact_force: float = Field(ge=0.0, le=100.0)
    injured_player_id: int | None = None


class CutsceneStatusResponse(BaseModel):
    play_id: int
    status: str  # "RENDERED" | "SKIPPED_BELOW_THRESHOLD" | "FALLBACK_THREEJS"
    video_url: str | None = None
    render_duration_ms: float
