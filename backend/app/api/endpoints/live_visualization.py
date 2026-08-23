"""
Live Game Visualization API
Provides real-time game state streaming for 3D visualization
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import Dict, List, Optional, Any
import asyncio
import logging
from datetime import datetime, timezone

from app.models.player import Player
from app.models.team import Team
from app.models.game import Game
from app.core.database import get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/live", tags=["live-visualization"])

# Connection manager for WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)
        logger.info(f"Client connected to game {game_id}")
    
    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
        logger.info(f"Client disconnected from game {game_id}")
    
    async def broadcast(self, game_id: str, message: dict):
        if game_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.warning(f"Failed to send to client: {e}")
                    disconnected.append(connection)
            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(conn, game_id)

manager = ConnectionManager()

@router.websocket("/ws/game/{game_id}")
async def game_websocket(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for live game visualization updates"""
    await manager.connect(websocket, game_id)
    try:
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Handle client messages (e.g., camera control requests)
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)

@router.get("/game/{game_id}/roster")
async def get_game_roster(game_id: int, db: Session = Depends(get_db)):
    """Get roster data with visual asset information for both teams"""
    
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    home_team = db.query(Team).filter(Team.id == game.home_team_id).first()
    away_team = db.query(Team).filter(Team.id == game.away_team_id).first()
    
    def get_player_visual_data(player: Player) -> dict:
        """Extract visual-relevant player data"""
        return {
            "id": player.id,
            "name": player.name,
            "number": player.jersey_number,
            "position": player.position,
            "position_group": get_position_group(player.position),
            "height": player.height,
            "weight": player.weight,
            "team_id": player.team_id,
            "visuals": {
                "body_type": get_body_type_for_position(player.position, player.attributes),
                "jersey_color_primary": home_team.primary_color if player.team_id == home_team.id else away_team.primary_color,
                "jersey_color_secondary": home_team.secondary_color if player.team_id == home_team.id else away_team.secondary_color,
                "helmet_design": get_helmet_design(player.team_id, db),
                "face_mask_color": get_face_mask_color(player.position),
                "cleat_color": get_cleat_color(player.position),
                "accessories": get_accessories(player),
            }
        }
    
    # Get active rosters (simplified - in production use depth chart)
    home_players = db.query(Player).filter(
        Player.team_id == home_team.id,
        Player.injury_status == "healthy"
    ).limit(53).all()
    
    away_players = db.query(Player).filter(
        Player.team_id == away_team.id,
        Player.injury_status == "healthy"
    ).limit(53).all()
    
    return {
        "game_id": game_id,
        "home_team": {
            "id": home_team.id,
            "name": home_team.name,
            "abbreviation": home_team.abbreviation,
            "primary_color": home_team.primary_color,
            "secondary_color": home_team.secondary_color,
            "logo_url": f"/logos/{home_team.abbreviation}.png",
            "players": [get_player_visual_data(p) for p in home_players]
        },
        "away_team": {
            "id": away_team.id,
            "name": away_team.name,
            "abbreviation": away_team.abbreviation,
            "primary_color": away_team.primary_color,
            "secondary_color": away_team.secondary_color,
            "logo_url": f"/logos/{away_team.abbreviation}.png",
            "players": [get_player_visual_data(p) for p in away_players]
        }
    }

def get_position_group(position: str) -> str:
    """Map position to position group for visual categorization"""
    offense_positions = ["QB", "RB", "FB", "WR", "TE", "OT", "OG", "C"]
    defense_positions = ["DE", "DT", "LB", "CB", "S"]
    special_teams = ["K", "P", "LS"]
    
    if position in offense_positions:
        return "offense"
    elif position in defense_positions:
        return "defense"
    elif position in special_teams:
        return "special_teams"
    return "unknown"

def get_body_type_for_position(position: str, attributes) -> str:
    """Determine body type based on position and attributes"""
    if not attributes:
        return "average"
    
    # Use actual player attributes to determine body type
    weight_factor = getattr(attributes, 'strength', 50)
    speed_factor = getattr(attributes, 'speed', 50)
    
    if position in ["OT", "OG", "C", "DT", "DE"]:
        return "large" if weight_factor > 70 else "medium"
    elif position in ["WR", "CB", "S", "RB"]:
        return "lean" if speed_factor > 70 else "athletic"
    elif position == "QB":
        return "athletic" if speed_factor > 60 else "pocket"
    elif position in ["LB", "TE", "FB"]:
        return "muscular"
    elif position in ["K", "P"]:
        return "lean"
    return "average"

def get_helmet_design(team_id: int, db: Session) -> dict:
    """Get helmet design configuration for team"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return {"base": "plain", "stripe": "none", "logo_side": False}
    
    # In production, this would come from team branding config
    return {
        "base": team.primary_color,
        "stripe": team.secondary_color,
        "logo_side": True,
        "facemask": "gray"
    }

def get_face_mask_color(position: str) -> str:
    """Get face mask color based on position"""
    if position in ["QB", "K", "P"]:
        return "light_gray"
    elif position in ["OT", "OG", "C", "DT", "DE", "LB"]:
        return "dark_gray"
    return "gray"

def get_cleat_color(position: str) -> str:
    """Get cleat color based on position and style"""
    # Could be customized per player in future
    if position in ["WR", "RB", "CB", "S"]:
        return "neon"  # Flashy for skill positions
    elif position in ["K", "P"]:
        return "white"
    return "black"

def get_accessories(player: Player) -> list:
    """Get list of accessories based on player preferences/position"""
    accessories = []
    
    # Position-based defaults
    if player.position in ["WR", "RB", "CB", "S"]:
        accessories.append("gloves")
    if player.position in ["OT", "OG", "C", "DT", "DE", "LB"]:
        accessories.append("wrist_bands")
    if player.position == "QB":
        accessories.append("hand_glove")  # QB glove
    
    # Could add more based on player traits/preferences
    return accessories

@router.get("/game/{game_id}/formation/{play_id}")
async def get_formation_data(game_id: int, play_id: int, db: Session = Depends(get_db)):
    """Get formation and player positioning data for a specific play"""
    
    # This would integrate with the play engine to get actual positions
    # For now, return a template structure
    return {
        "play_id": play_id,
        "formation": {
            "offense": {
                "name": "Shotgun Spread",
                "players": [
                    {"position": "QB", "x": -5, "y": 0, "z": 0},
                    {"position": "RB", "x": -7, "y": 0, "z": 0},
                    {"position": "WR", "x": 0, "y": 0, "z": -12},
                    {"position": "WR", "x": 0, "y": 0, "z": 12},
                    {"position": "TE", "x": 0, "y": 0, "z": -6},
                ]
            },
            "defense": {
                "name": "Nickel 4-3",
                "players": [
                    {"position": "DE", "x": 2, "y": 0, "z": -4},
                    {"position": "DT", "x": 2, "y": 0, "z": -1},
                    {"position": "DT", "x": 2, "y": 0, "z": 1},
                    {"position": "DE", "x": 2, "y": 0, "z": 4},
                ]
            }
        }
    }

@router.post("/game/{game_id}/camera/{client_id}")
async def update_camera_angle(game_id: int, client_id: str, angle_data: dict):
    """Update camera angle for a specific client (optional feature)"""
    # Would broadcast to other clients if implementing shared camera
    return {"status": "ok", "angle": angle_data}
