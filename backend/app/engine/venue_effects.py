#!/usr/bin/env python3
"""
Venue Effects Engine
====================
Calculates atmosphere and home-field modifiers based on venue,
game type, and special occasions (Thanksgiving, playoffs, etc).
"""

from typing import Any

from app.data.special_jerseys import THANKSGIVING_HOSTS, is_thanksgiving_host


class VenueEffects:
    """
    Calculates venue-specific modifiers for game simulation.
    Handles home-field advantage, crowd effects, and special game atmospheres.
    """

    # Base home-field advantage
    BASE_HOME_BOOST = 0.03  # 3% across the board

    # Crowd energy multipliers by game type
    CROWD_ENERGY = {
        "REGULAR": 1.0,
        "THANKSGIVING": 1.2,
        "PRIMETIME": 1.15,
        "PLAYOFF": 1.3,
        "SUPER_BOWL": 1.0,  # Neutral site
    }

    def __init__(self, home_team_abbr: str, game_type: str = "REGULAR"):
        self.home_team = home_team_abbr
        self.game_type = game_type

    def get_home_field_modifier(self) -> float:
        """
        Calculate total home-field advantage modifier.

        Returns:
            Float modifier (e.g., 0.08 = 8% boost)
        """
        modifier = self.BASE_HOME_BOOST

        # Thanksgiving host bonus
        if self.game_type == "THANKSGIVING" and is_thanksgiving_host(self.home_team):
            modifier += THANKSGIVING_HOSTS[self.home_team]["home_field_boost"]

        # Playoff intensity
        if self.game_type == "PLAYOFF":
            modifier += 0.02

        return modifier

    def get_crowd_energy(self) -> float:
        """
        Get crowd energy multiplier for the game.

        Returns:
            Float multiplier (1.0 = baseline)
        """
        return self.CROWD_ENERGY.get(self.game_type, 1.0)

    def get_fatigue_modifier(self) -> float:
        """
        Calculate fatigue modifier based on venue/atmosphere.
        Higher crowd energy = more adrenaline = less early fatigue.

        Returns:
            Float modifier (< 1.0 = reduced fatigue)
        """
        crowd = self.get_crowd_energy()
        # Higher crowd energy reduces early fatigue for home team
        return 1.0 - (crowd - 1.0) * 0.1

    def get_penalty_modifier(self) -> float:
        """
        Calculate penalty probability modifier for away team.
        Hostile crowds increase false start/delay of game risk.

        Returns:
            Float modifier for away team penalty chance
        """
        crowd = self.get_crowd_energy()
        return 1.0 + (crowd - 1.0) * 0.5  # 50% of crowd energy effect

    def get_all_modifiers(self) -> dict[str, float]:
        """Get all venue modifiers as a dictionary."""
        return {
            "home_field_boost": self.get_home_field_modifier(),
            "crowd_energy": self.get_crowd_energy(),
            "home_fatigue_modifier": self.get_fatigue_modifier(),
            "away_penalty_modifier": self.get_penalty_modifier(),
            "is_thanksgiving": self.game_type == "THANKSGIVING",
            "is_traditional_host": is_thanksgiving_host(self.home_team)
            if self.game_type == "THANKSGIVING"
            else False,
        }


def get_thanksgiving_atmosphere(home_team: str) -> dict[str, Any]:
    """
    Get full Thanksgiving game atmosphere settings.

    Args:
        home_team: Team abbreviation

    Returns:
        Dictionary with all Thanksgiving-specific settings
    """
    effects = VenueEffects(home_team, "THANKSGIVING")

    atmosphere = effects.get_all_modifiers()
    atmosphere["madden_celebration"] = True
    atmosphere["turkey_leg_award"] = True

    if home_team in THANKSGIVING_HOSTS:
        host_data = THANKSGIVING_HOSTS[home_team]
        atmosphere["tradition_started"] = host_data["tradition_started"]
        atmosphere["game_slot"] = host_data["game_slot"]

    return atmosphere
