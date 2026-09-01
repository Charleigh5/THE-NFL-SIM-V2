"""
Unit tests for PlayerAssetService and Parametric Prompt Synthesis.
"""

import pytest
import subprocess
import os
from pathlib import Path

from app.services.visuals.player_asset_service import (
    PlayerAssetService,
    PlayerVisualAssetMetadata,
)

from scripts.generate_player_assets import generate_mock_svg

def test_player_asset_urls_resolution():
    urls = PlayerAssetService.get_asset_urls(team_abbr="det", player_id=16)
    assert urls["headshot"] == "/assets/players/DET/16/headshot.webp"
    assert urls["hero_pose"] == "/assets/players/DET/16/hero_pose.webp"
    assert urls["action_pose"] == "/assets/players/DET/16/action_pose.webp"
    assert urls["celebration"] == "/assets/players/DET/16/celebration.webp"


def test_qb_headshot_prompt_synthesis():
    meta = PlayerVisualAssetMetadata(
        player_id=16,
        team_abbreviation="DET",
        jersey_number=16,
        first_name="Jared",
        last_name="Goff",
        position="QB",
        height_inches=76,
        weight_lbs=217,
        skin_tone="fair",
    )
    prompt = PlayerAssetService.build_parametric_prompt(
        meta=meta,
        pose="headshot",
        team_name="Detroit Lions",
        primary_color_name="Honolulu Blue",
    )

    assert "Jared Goff" in prompt
    assert "#16" in prompt
    assert "Detroit Lions" in prompt
    assert "6'4\"" in prompt
    assert "217 lbs" in prompt
    assert "Broadcast-quality" in prompt
    assert "QB" in prompt


def test_action_pose_prompt_position_dynamics():
    meta_wr = PlayerVisualAssetMetadata(
        player_id=14,
        team_abbreviation="DET",
        jersey_number=14,
        first_name="Amon-Ra",
        last_name="St. Brown",
        position="WR",
        height_inches=72,
        weight_lbs=202,
    )
    prompt = PlayerAssetService.build_parametric_prompt(
        meta=meta_wr,
        pose="action_pose",
        team_name="Detroit Lions",
    )

    assert "Amon-Ra St. Brown" in prompt
    assert "cutting upfield" in prompt
    assert "turf" in prompt


def test_celebration_prompt_synthesis():
    meta = PlayerVisualAssetMetadata(
        player_id=26,
        team_abbreviation="DET",
        jersey_number=26,
        first_name="Jahmyr",
        last_name="Gibbs",
        position="RB",
        height_inches=69,
        weight_lbs=199,
    )
    prompt = PlayerAssetService.build_parametric_prompt(
        meta=meta,
        pose="celebration",
        team_name="Detroit Lions",
    )

    assert "Jahmyr Gibbs" in prompt
    assert "touchdown" in prompt
    assert "celebration" in prompt.lower()


def test_generate_mock_svg():
    meta = PlayerVisualAssetMetadata(
        player_id=1,
        team_abbreviation="DET",
        jersey_number=14,
        first_name="Amon-Ra",
        last_name="St. Brown",
        position="WR",
        height_inches=72,
        weight_lbs=202,
    )
    svg = generate_mock_svg("headshot", meta, "#0076B6")
    
    assert "<svg" in svg
    assert "Amon-Ra St. Brown" in svg
    assert "#14" in svg
    assert "WR" in svg
    assert "DET" in svg
    assert "#0076B6" in svg
    assert "Headshot" in svg


def test_parametric_prompt_all_14_positions():
    positions = ["QB", "RB", "FB", "WR", "TE", "OT", "OG", "C", "DT", "DE", "LB", "CB", "S", "K", "P"]
    
    for pos in positions:
        meta = PlayerVisualAssetMetadata(
            player_id=1,
            team_abbreviation="TEST",
            jersey_number=99,
            first_name="Test",
            last_name="Player",
            position=pos,
            height_inches=72,
            weight_lbs=200,
        )
        
        prompt_action = PlayerAssetService.build_parametric_prompt(
            meta=meta,
            pose="action_pose",
            team_name="Test Team",
        )
        
        # Ensure it generated successfully and didn't fall back to generic unless it should
        assert pos in prompt_action
        assert "action photograph" in prompt_action or "in dynamic athletic game motion" in prompt_action or "cutting upfield" in prompt_action or "ready to fire a pass" in prompt_action or "exploding off the edge" in prompt_action


def test_cli_arguments(tmp_path):
    # This runs the CLI with --help to ensure arguments are accepted without error
    script_path = Path(__file__).resolve().parent.parent.parent / "scripts" / "generate_player_assets.py"
    result = subprocess.run(
        ["python", str(script_path), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--team" in result.stdout
    assert "--all" in result.stdout
    assert "--pose" in result.stdout
    assert "--dry-run" in result.stdout
    assert "--force" in result.stdout
    assert "--mock" in result.stdout

def test_cli_dry_run():
    # Test a dry run for a non-existent team to check execution flow
    script_path = Path(__file__).resolve().parent.parent.parent / "scripts" / "generate_player_assets.py"
    result = subprocess.run(
        ["python", str(script_path), "--team", "NON_EXISTENT", "--dry-run"],
        capture_output=True,
        text=True,
    )
    # The script should exit gracefully saying no teams found
    assert result.returncode == 0
    assert "No teams found matching criteria." in result.stdout
