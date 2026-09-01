import argparse
import sys
import os
import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.models.team import Team
from app.models.player import Player
from app.services.visuals.player_asset_service import PlayerAssetService, PlayerVisualAssetMetadata

# Adjust root as necessary
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_ASSETS_DIR = PROJECT_ROOT / "frontend" / "public" / "assets" / "players"

def generate_mock_svg(pose: str, meta: PlayerVisualAssetMetadata, team_color: str) -> str:
    """Generate a high-quality standardized SVG placeholder."""
    return f"""<svg width="800" height="800" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{team_color};stop-opacity:1" />
            <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="url(#grad1)" />
    <text x="50%" y="40%" font-family="Arial" font-size="48" fill="white" text-anchor="middle" dominant-baseline="middle">
        #{meta.jersey_number} {meta.first_name} {meta.last_name}
    </text>
    <text x="50%" y="50%" font-family="Arial" font-size="36" fill="white" text-anchor="middle" dominant-baseline="middle">
        {meta.position} - {meta.team_abbreviation}
    </text>
    <text x="50%" y="60%" font-family="Arial" font-size="32" fill="white" text-anchor="middle" dominant-baseline="middle">
        {pose.replace('_', ' ').title()}
    </text>
</svg>"""

def process_player(player: Player, team: Team, pose: str, args) -> None:
    meta = PlayerVisualAssetMetadata(
        player_id=player.id,
        team_abbreviation=team.abbreviation,
        jersey_number=player.jersey_number or 0,
        first_name=player.first_name,
        last_name=player.last_name,
        position=player.position,
        height_inches=player.height,
        weight_lbs=player.weight,
        skin_tone="medium_brown", # default mock
    )
    
    prompt = PlayerAssetService.build_parametric_prompt(
        meta=meta,
        pose=pose,
        team_name=team.name,
        primary_color_name=team.primary_color or "home team colors"
    )
    
    # Path calculation
    team_abbr = team.abbreviation.upper()
    dest_path = FRONTEND_ASSETS_DIR / team_abbr / str(player.id) / f"{pose}.webp"
    svg_dest_path = FRONTEND_ASSETS_DIR / team_abbr / str(player.id) / f"{pose}.svg"
    
    if args.dry_run:
        print(f"[DRY-RUN] Would generate {pose} for {player.first_name} {player.last_name} (ID: {player.id})")
        print(f"   Prompt: {prompt}")
        print(f"   Dest: {dest_path}")
        return
        
    if dest_path.exists() and not args.force and not (args.mock and svg_dest_path.exists()):
        print(f"Skipping {dest_path} - already exists (use --force to overwrite)")
        return
        
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.mock:
        svg_content = generate_mock_svg(pose, meta, team.primary_color or "#000000")
        with open(svg_dest_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated mock SVG asset for {player.first_name} {player.last_name} at {svg_dest_path}")
    else:
        # We simulate hitting an API or generating a webp file.
        # Since we don't have an API key right now, we'll just create a dummy webp file.
        # In a real scenario, this would call GenAI.
        with open(dest_path, "wb") as f:
            f.write(b"WEBP_DUMMY_CONTENT")
        print(f"Generated asset for {player.first_name} {player.last_name} at {dest_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Player Visual Assets")
    parser.add_argument("--team", type=str, help="Filter by team abbreviation (e.g. DET, GB, KC)")
    parser.add_argument("--all", action="store_true", help="Process all teams")
    parser.add_argument("--pose", type=str, default="all", choices=["headshot", "hero_pose", "action_pose", "celebration", "all"], help="Specific pose")
    parser.add_argument("--dry-run", action="store_true", help="Output generated prompts and destination paths without writing image files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing assets")
    parser.add_argument("--mock", action="store_true", help="Generate high-quality standardized SVG / WebP gradient placeholder assets")
    
    args = parser.parse_args()
    
    if not args.all and not args.team:
        print("Error: Must specify either --team <ABBR> or --all")
        sys.exit(1)
        
    db: Session = SessionLocal()
    
    try:
        query = select(Team)
        if args.team:
            query = query.where(Team.abbreviation == args.team)
            
        teams = db.execute(query).scalars().all()
        
        if not teams:
            print(f"No teams found matching criteria.")
            sys.exit(0)
            
        poses_to_generate = ["headshot", "hero_pose", "action_pose", "celebration"] if args.pose == "all" else [args.pose]
        
        for team in teams:
            print(f"Processing Team: {team.name} ({team.abbreviation})")
            players = db.execute(select(Player).where(Player.team_id == team.id)).scalars().all()
            
            for player in players:
                for pose in poses_to_generate:
                    process_player(player, team, pose, args)
                    
    finally:
        db.close()

if __name__ == "__main__":
    main()
