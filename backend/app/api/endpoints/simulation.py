from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.schemas.play import PlayResult
from app.schemas.simulation import SimulationRequest
import asyncio

router = APIRouter(prefix="/api/simulation", tags=["simulation"])





# Instantiate the orchestrator at the module level
orchestrator = SimulationOrchestrator()


@router.post("/start", response_model=PlayResult)
def start_simulation(request: SimulationRequest):
    """
    Trigger a new simulation run using the SimulationOrchestrator.
    (Legacy endpoint - runs single play synchronously)
    """
    try:
        result = orchestrator.run_simulation()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start-live")
async def start_live_simulation(request: SimulationRequest, background_tasks: BackgroundTasks):
    """
    Start a continuous live simulation that broadcasts via WebSocket.
    
    This endpoint:
    1. Starts the simulation in the background
    2. Returns immediately
    3. Simulation broadcasts plays via WebSocket as they happen
    """
    if orchestrator.is_running:
        raise HTTPException(status_code=400, detail="Simulation already running")
    
    # Import WebSocket helpers
    from app.api.endpoints.websocket import broadcast_play_result, broadcast_game_update
    
    # Set up WebSocket callbacks
    async def on_play_complete(play_result: PlayResult):
        """Broadcast play result to all connected clients."""
        await broadcast_play_result(play_result.dict())
    
    async def on_game_update(game_state: dict):
        """Broadcast game state update to all connected clients."""
        await broadcast_game_update(game_state)
    
    orchestrator.on_play_complete = on_play_complete
    orchestrator.on_game_update = on_game_update
    
    # Initialize game session synchronously to get ID
    # Mocking Team IDs 1 and 2 for now
    orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, config=request.config)
    game_id = orchestrator.current_game_id
    
    # Start continuous simulation in background
    num_plays = request.num_plays or 100
    background_tasks.add_task(orchestrator.run_continuous_simulation, num_plays, request.config)
    
    return {
        "status": "started",
        "message": f"Live simulation started for {num_plays} plays",
        "game_id": game_id,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/stop")
def stop_simulation():
    """Stop the currently running simulation."""
    if not orchestrator.is_running:
        raise HTTPException(status_code=400, detail="No simulation is running")
    
    orchestrator.stop_simulation()
    return {
        "status": "stopped",
        "message": "Simulation stopped",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/status")
def get_simulation_status(simulation_id: Optional[str] = None):
    """Get the status of a running or completed simulation."""
    return {
        "isRunning": orchestrator.is_running,
        "currentQuarter": orchestrator.current_quarter,
        "timeLeft": orchestrator.time_left,
        "homeScore": orchestrator.home_score,
        "awayScore": orchestrator.away_score,
        "possession": getattr(orchestrator, 'possession', 'home'),
        "down": getattr(orchestrator, 'down', 1),
        "distance": getattr(orchestrator, 'distance', 10),
        "yardLine": getattr(orchestrator, 'yard_line', 25)
    }


@router.get("/{simulation_id}/plays", response_model=List[PlayResult])
def get_simulation_plays(simulation_id: str):
    """Retrieve play history for a simulation."""
    return orchestrator.get_history()


from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.game import Game

# ... (existing imports)

@router.get("/results/{simulation_id}")
def get_simulation_results(simulation_id: int, db: Session = Depends(get_db)):
    """Retrieve results from a completed simulation."""
    game = db.query(Game).filter(Game.id == simulation_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return {
        "simulation_id": game.id,
        "status": "completed" if game.is_played else "in_progress",
        "home_score": game.home_score,
        "away_score": game.away_score,
        "results": game.game_data or {},
        "timestamp": game.date.isoformat() if game.date else None
    }

