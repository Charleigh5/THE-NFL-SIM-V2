from fastapi import APIRouter
from app.schemas.spatial import CutsceneTriggerRequest, CutsceneStatusResponse
from app.engine.spatial.activation_gate import SpatialActivationGate
from app.engine.spatial.blender_service import BlenderService

router = APIRouter(prefix="/api/spatial", tags=["spatial-visualization"])
gate = SpatialActivationGate()
blender_service = BlenderService()


@router.post("/game/{game_id}/play/{play_id}/evaluate-cutscene", response_model=CutsceneStatusResponse)
async def evaluate_cutscene(game_id: int, play_id: int, req: CutsceneTriggerRequest, render_mode: str = "auto"):
    """Evaluates whether to render high-definition Blender cutscene or bypass."""
    should_trigger, _ = gate.should_trigger_cutscene(req.drama_index, req.impact_force)
    if not should_trigger:
        return CutsceneStatusResponse(
            play_id=play_id,
            status="SKIPPED_BELOW_THRESHOLD",
            video_url=None,
            render_duration_ms=0.0
        )
    return blender_service.request_cutscene_render(play_id, req.drama_index, req.impact_force, render_mode=render_mode)


@router.get("/status")
async def get_spatial_status():
    """Returns connectivity health of Blender MCP socket and spatial subsystem."""
    is_socket_open = blender_service.probe_socket()
    return {
        "subsystem": "GRIDIRON-3D-SPATIAL",
        "blender_mcp_port_9876": "OPEN" if is_socket_open else "CLOSED",
        "tier1_status": "ONLINE",
        "tier2_status": "ONLINE",
        "tier3_status": "ONLINE" if is_socket_open else "FALLBACK_THREEJS"
    }
