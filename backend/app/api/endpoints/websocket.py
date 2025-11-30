from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import asyncio
import json
import logging
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages active WebSocket connections for live simulation broadcasting."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from active list."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Dict with 'type' and 'payload' keys
        """
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


# Global connection manager instance
manager = ConnectionManager()


@router.websocket("/ws/simulation/live")
async def websocket_simulation_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for live simulation streaming.
    
    Clients connect here to receive real-time updates:
    - GAME_UPDATE: Game state changes (score, quarter, time)
    - PLAY_RESULT: Individual play outcomes
    - ENGINE_UPDATE: Data from specific engines (genesis, empire, etc.)
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and receive any client messages
            data = await websocket.receive_text()
            
            # Handle client commands if needed
            try:
                message = json.loads(data)
                if message.get("type") == "PING":
                    await websocket.send_text(json.dumps({"type": "PONG"}))
            except json.JSONDecodeError:
                logger.warning("Received invalid JSON from WebSocket client")
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        manager.disconnect(websocket)


async def broadcast_game_update(game_state: Dict[str, Any]):
    """Broadcast game state update to all connected clients."""
    await manager.broadcast({
        "type": "GAME_UPDATE",
        "payload": game_state
    })


async def broadcast_play_result(play_result: Dict[str, Any]):
    """Broadcast individual play result to all connected clients."""
    await manager.broadcast({
        "type": "PLAY_RESULT",
        "payload": play_result
    })


async def broadcast_engine_update(engine_name: str, data: Dict[str, Any]):
    """Broadcast engine-specific data to all connected clients."""
    await manager.broadcast({
        "type": "ENGINE_UPDATE",
        "engine": engine_name,
        "payload": data
    })
