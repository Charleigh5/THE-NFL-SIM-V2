"""
Player Visual Asset Service
Handles parametric prompt synthesis, asset resolution, and fallback URLs for all player poses.
"""

from typing import Dict, Optional, Literal
from pydantic import BaseModel, ConfigDict


PoseType = Literal["headshot", "hero_pose", "action_pose", "celebration"]


class PlayerVisualAssetMetadata(BaseModel):
    player_id: int
    team_abbreviation: str
    jersey_number: int
    first_name: str
    last_name: str
    position: str
    height_inches: int
    weight_lbs: int
    skin_tone: Optional[str] = "medium_brown"
    visor_style: Optional[str] = None
    arm_gear: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PlayerAssetService:
    """Service governing player visual asset generation prompts and URL resolution."""

    BASE_ASSET_PATH = "/assets/players"

    @classmethod
    def get_asset_urls(cls, team_abbr: str, player_id: int) -> Dict[str, str]:
        """
        Get deterministic static asset URLs for all 4 player poses.
        """
        safe_team = team_abbr.upper().strip()
        base_dir = f"{cls.BASE_ASSET_PATH}/{safe_team}/{player_id}"
        return {
            "headshot": f"{base_dir}/headshot.webp",
            "hero_pose": f"{base_dir}/hero_pose.webp",
            "action_pose": f"{base_dir}/action_pose.webp",
            "celebration": f"{base_dir}/celebration.webp",
        }

    @classmethod
    def build_parametric_prompt(
        cls,
        meta: PlayerVisualAssetMetadata,
        pose: PoseType,
        team_name: str,
        primary_color_name: str = "home team colors"
    ) -> str:
        """
        Construct a photorealistic, studio-quality diffusion prompt for a player pose.
        """
        height_feet = meta.height_inches // 12
        height_rem_inches = meta.height_inches % 12
        height_str = f"{height_feet}'{height_rem_inches}\""
        build_str = f"{height_str}, {meta.weight_lbs} lbs athletic muscular build"

        # Position-specific equipment and accessories
        gear_items = []
        if meta.position in ["QB", "WR", "CB"]:
            gear_items.append("tinted visor, chrome facemask, white turf tape on forearms")
        elif meta.position in ["DE", "DT", "OT", "OG"]:
            gear_items.append("heavy knee braces, clear visor, taped fingers, reinforced neck roll")
        elif meta.position in ["RB", "LB", "S"]:
            gear_items.append("smoked eye shield, padded arm sleeves, towel on belt")

        gear_desc = ", ".join(gear_items)

        if pose == "headshot":
            return (
                f"Broadcast-quality NFL player studio headshot portrait of #{meta.jersey_number} "
                f"{meta.first_name} {meta.last_name}, playing {meta.position} for the {team_name} "
                f"wearing official {primary_color_name} uniform. {build_str}, {gear_desc}, "
                f"sharp direct eye contact, determined focused expression, high-end broadcast studio rim lighting, "
                f"shallow depth of field with subtle dark stadium bokeh, 8k resolution, photorealistic fabric texture."
            )

        if pose == "hero_pose":
            return (
                f"Full body studio portrait of #{meta.jersey_number} {meta.first_name} {meta.last_name} "
                f"({meta.position}) in {team_name} uniform, standing confident on the stadium tunnel turf holding "
                f"chrome football helmet under one arm, {build_str}, {gear_desc}, dramatic cinematic stadium rim lighting, "
                f"volumetric floodlights behind, 8k EA Sports Madden cover style presentation."
            )

        if pose == "action_pose":
            action_desc = "dropping back in the pocket ready to fire a pass" if meta.position == "QB" else (
                "explosively cutting upfield with the ball" if meta.position in ["RB", "WR"] else (
                    "exploding off the edge in a ferocious pass rush" if meta.position in ["DE", "LB"] else "in dynamic athletic game motion"
                )
            )
            return (
                f"Full body action photograph of #{meta.jersey_number} {meta.first_name} {meta.last_name} "
                f"({meta.position}) in {team_name} uniform, {action_desc} on natural green turf under "
                f"dramatic primetime stadium floodlights, grass turf blades kicking up from cleats, high kinetic energy, "
                f"8k sports photojournalism masterpiece."
            )

        if pose == "celebration":
            return (
                f"Full body celebration photograph of #{meta.jersey_number} {meta.first_name} {meta.last_name} "
                f"in {team_name} uniform, celebrating an electrifying touchdown on the field, emotional triumph, "
                f"roaring stadium crowd in blurred background, stadium lights lens flare, ultra-sharp 8k resolution."
            )

        return (
            f"NFL player photo of #{meta.jersey_number} {meta.first_name} {meta.last_name} in {team_name} uniform, 8k resolution."
        )
