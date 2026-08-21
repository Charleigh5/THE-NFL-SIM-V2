"""
Live Game Visualization API

Provides real-time game state streaming, roster visual attributes, formation data,
and cutscene clip cues for 3D game visualization.
"""

import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.player import Player
from app.models.team import Team
from app.models.game import Game
from app.core.database import get_async_db
from app.schemas.broadcast import ClipCueListResponse, ClipCue, CameraShot, OverlayCue

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/live", tags=["live-visualization"])


class ConnectionManager:
    """Connection manager for WebSocket clients viewing 3D live game simulation."""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)
        logger.info(f"Client connected to live game {game_id}")

    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            if websocket in self.active_connections[game_id]:
                self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
        logger.info(f"Client disconnected from live game {game_id}")

    async def broadcast(self, game_id: str, message: dict):
        if game_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.warning(f"Failed to send to client: {e}")
                    disconnected.append(connection)
            for conn in disconnected:
                self.disconnect(conn, game_id)


manager = ConnectionManager()


@router.websocket("/ws/game/{game_id}")
async def game_websocket(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for live game visualization updates."""
    await manager.connect(websocket, game_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)


def get_position_group(position: str) -> str:
    """Map position to position group for visual categorization."""
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


def get_body_type_for_position(position: str, attributes: Optional[Any]) -> str:
    """Determine 3D body type based on position and attributes."""
    if not attributes:
        if position in ["OT", "OG", "C", "DT", "DE"]:
            return "large"
        if position in ["WR", "CB", "S", "RB"]:
            return "athletic"
        if position in ["LB", "TE", "FB"]:
            return "muscular"
        return "average"

    weight_factor = getattr(attributes, "strength", 50)
    speed_factor = getattr(attributes, "speed", 50)

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


def get_helmet_design(team: Optional[Team]) -> dict:
    """Get helmet design configuration for team."""
    if not team:
        return {"base": "plain", "stripe": "none", "logo_side": False, "facemask": "gray"}

    return {
        "base": team.primary_color or "#002244",
        "stripe": team.secondary_color or "#A5ACAF",
        "logo_side": True,
        "facemask": "gray"
    }


def get_face_mask_color(position: str) -> str:
    """Get face mask color based on position."""
    if position in ["QB", "K", "P"]:
        return "light_gray"
    elif position in ["OT", "OG", "C", "DT", "DE", "LB"]:
        return "dark_gray"
    return "gray"


def get_cleat_color(position: str) -> str:
    """Get cleat color based on position."""
    if position in ["WR", "RB", "CB", "S"]:
        return "neon"
    elif position in ["K", "P"]:
        return "white"
    return "black"


def get_accessories(player: Player) -> list:
    """Get list of visual accessories based on player position."""
    accessories = []
    if player.position in ["WR", "RB", "CB", "S"]:
        accessories.append("gloves")
    if player.position in ["OT", "OG", "C", "DT", "DE", "LB"]:
        accessories.append("wrist_bands")
    if player.position == "QB":
        accessories.append("hand_glove")
    return accessories


@router.get("/game/{game_id}/roster")
async def get_game_roster(game_id: int, db: AsyncSession = Depends(get_async_db)):
    """Get roster data with 3D visual asset information for both teams."""
    game_stmt = select(Game).where(Game.id == game_id)
    game_res = await db.execute(game_stmt)
    game = game_res.scalar_one_or_none()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    home_stmt = select(Team).where(Team.id == game.home_team_id)
    away_stmt = select(Team).where(Team.id == game.away_team_id)
    home_team = (await db.execute(home_stmt)).scalar_one_or_none()
    away_team = (await db.execute(away_stmt)).scalar_one_or_none()

    if not home_team or not away_team:
        raise HTTPException(status_code=404, detail="Teams for this game not found")

    def format_player_visual(player: Player, is_home: bool) -> dict:
        full_name = f"{player.first_name} {player.last_name}" if player.first_name and player.last_name else (player.first_name or player.last_name or f"Player #{player.jersey_number}")
        primary_col = home_team.primary_color if is_home else away_team.primary_color
        secondary_col = home_team.secondary_color if is_home else away_team.secondary_color
        team_obj = home_team if is_home else away_team

        return {
            "id": player.id,
            "name": full_name,
            "number": player.jersey_number,
            "position": player.position,
            "position_group": get_position_group(player.position),
            "height": player.height,
            "weight": player.weight,
            "team_id": player.team_id,
            "visuals": {
                "body_type": get_body_type_for_position(player.position, getattr(player, "attributes", None)),
                "jersey_color_primary": primary_col or "#002244",
                "jersey_color_secondary": secondary_col or "#A5ACAF",
                "helmet_design": get_helmet_design(team_obj),
                "face_mask_color": get_face_mask_color(player.position),
                "cleat_color": get_cleat_color(player.position),
                "accessories": get_accessories(player),
            }
        }

    home_players_stmt = select(Player).where(Player.team_id == home_team.id).options(selectinload(Player.attributes)).limit(53)
    away_players_stmt = select(Player).where(Player.team_id == away_team.id).options(selectinload(Player.attributes)).limit(53)

    home_players = (await db.execute(home_players_stmt)).scalars().all()
    away_players = (await db.execute(away_players_stmt)).scalars().all()

    return {
        "game_id": game_id,
        "home_team": {
            "id": home_team.id,
            "name": home_team.name,
            "abbreviation": home_team.abbreviation,
            "primary_color": home_team.primary_color,
            "secondary_color": home_team.secondary_color,
            "logo_url": f"/logos/{home_team.abbreviation}.png",
            "players": [format_player_visual(p, is_home=True) for p in home_players]
        },
        "away_team": {
            "id": away_team.id,
            "name": away_team.name,
            "abbreviation": away_team.abbreviation,
            "primary_color": away_team.primary_color,
            "secondary_color": away_team.secondary_color,
            "logo_url": f"/logos/{away_team.abbreviation}.png",
            "players": [format_player_visual(p, is_home=False) for p in away_players]
        }
    }


@router.get("/game/{game_id}/formation/{play_id}")
async def get_formation_data(game_id: int, play_id: int):
    """Get formation and player coordinate positioning data for a specific play."""
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


@router.get("/game/{game_id}/broadcast/{play_id}", response_model=ClipCueListResponse)
async def get_broadcast_clips(game_id: int, play_id: int):
    """Get ordered list of broadcast camera cues and overlays for a play."""
    clips = [
        ClipCue(
            id=f"preplay_{play_id}_sweep",
            clip_type="formation_sweep",
            cameras=[
                CameraShot(
                    id="sweep_start",
                    position={"x": -15.0, "y": 8.0, "z": 25.0},
                    target={"x": 0.0, "y": 0.0, "z": 0.0},
                    fov=60.0,
                    duration=2.5,
                    interpolation="smooth"
                ),
                CameraShot(
                    id="sweep_end",
                    position={"x": -5.0, "y": 4.0, "z": 15.0},
                    target={"x": 0.0, "y": 1.0, "z": 0.0},
                    fov=50.0,
                    duration=2.0,
                    interpolation="smooth"
                )
            ],
            overlays=[
                OverlayCue(
                    id="situation_bar",
                    type="lower_third",
                    data={"down": 1, "distance": 10, "yard_line": 25},
                    duration=4.5,
                    animation="slide",
                    layer=10
                )
            ],
            duration=4.5,
            audio_cue="preplay_buildup",
            skippable=True
        )
    ]

    total_duration = sum(c.duration for c in clips)
    return ClipCueListResponse(
        play_id=play_id,
        clips=clips,
        total_duration=total_duration
    )


@router.post("/game/{game_id}/camera/{client_id}")
async def update_camera_angle(game_id: int, client_id: str, angle_data: dict):
    """Update camera angle for a specific client (optional feature)."""
    return {"status": "ok", "game_id": game_id, "client_id": client_id, "angle": angle_data}
