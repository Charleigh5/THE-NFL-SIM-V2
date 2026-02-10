#!/usr/bin/env python3
"""
Special Jerseys Data Module
===========================
Defines special/throwback uniforms for NFL teams, particularly for
Thanksgiving Day games and other special occasions.
"""

from typing import Any

# ============================================================================
# THANKSGIVING JERSEYS
# ============================================================================

THANKSGIVING_JERSEYS: dict[str, dict[str, Any]] = {
    "DET": {
        "name": "Lions 1950s Throwback",
        "description": "Classic Honolulu blue with silver accents, worn annually on Thanksgiving",
        "helmet": {
            "color": "Silver",
            "logo": "Classic Lion",
            "facemask": "Gray",
        },
        "jersey": {
            "color": "Honolulu Blue",
            "style": "Classic",
            "numbers": "Silver with White Outline",
        },
        "pants": {
            "color": "Silver",
            "stripe": "Blue",
        },
        "socks": "Blue",
        "years_worn": [2001, 2002, 2003, 2004, 2008, 2010, 2017, 2018, 2020, 2023, 2025],
    },
    "DET_COLOR_RUSH": {
        "name": "Lions Color Rush",
        "description": "All-silver modern look",
        "helmet": {"color": "Silver", "logo": "Classic Lion", "facemask": "Silver"},
        "jersey": {"color": "Silver", "style": "Color Rush", "numbers": "Blue"},
        "pants": {"color": "Silver", "stripe": "None"},
        "socks": "Silver",
        "years_worn": [2019, 2022],
    },
    "DAL": {
        "name": "Cowboys 1960s Double-Star",
        "description": "Inaugural season throwback with white helmet and navy jerseys",
        "helmet": {
            "color": "White",
            "logo": "Blue Star",
            "facemask": "Gray",
        },
        "jersey": {
            "color": "Navy Blue",
            "style": "Double-Star Shoulders",
            "numbers": "White",
        },
        "pants": {
            "color": "White",
            "stripe": "Navy/Silver",
        },
        "socks": "Navy",
        "years_worn": [2022, 2023, 2024, 2025],
    },
    "DAL_WHITE": {
        "name": "Cowboys 1994 White Throwback",
        "description": "White Double-Star jerseys from Color Rush era",
        "helmet": {"color": "Silver", "logo": "Blue Star", "facemask": "Gray"},
        "jersey": {"color": "White", "style": "Double-Star Shoulders", "numbers": "Navy"},
        "pants": {"color": "White", "stripe": "Navy/Silver"},
        "socks": "White",
        "years_worn": [2015],
    },
}

# ============================================================================
# SPECIAL GAME TRADITIONS
# ============================================================================

THANKSGIVING_TRADITIONS = {
    "john_madden_celebration": {
        "name": "John Madden Thanksgiving Celebration",
        "started": 2022,
        "description": "Dedicated to legendary coach/broadcaster John Madden",
        "features": [
            "Madden headset patch on all player jerseys",
            "Special coin with Madden silhouette and turducken",
            "Turkey Leg Award to game MVP",
        ],
    },
    "turkey_leg_award": {
        "name": "Turkey Leg Award",
        "started": 1989,
        "popularized_by": "John Madden",
        "description": "MVP of each Thanksgiving game receives a turkey leg",
    },
}

# ============================================================================
# TRADITIONAL THANKSGIVING HOSTS
# ============================================================================

THANKSGIVING_HOSTS = {
    "DET": {
        "team_name": "Detroit Lions",
        "tradition_started": 1934,
        "all_time_record": "38-45-2",
        "game_slot": "early_afternoon",  # 12:30 PM ET
        "home_field_boost": 0.05,
    },
    "DAL": {
        "team_name": "Dallas Cowboys",
        "tradition_started": 1966,
        "all_time_record": "35-22-1",
        "game_slot": "late_afternoon",  # 4:30 PM ET
        "home_field_boost": 0.05,
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_thanksgiving_jersey(team_abbr: str, year: int = None) -> dict[str, Any]:
    """
    Get the Thanksgiving jersey for a team.

    Args:
        team_abbr: Team abbreviation (e.g., "DET", "DAL")
        year: Optional year to get specific jersey variant

    Returns:
        Jersey definition dict or None if not a Thanksgiving host
    """
    if team_abbr in THANKSGIVING_JERSEYS:
        return THANKSGIVING_JERSEYS[team_abbr]
    return None


def is_thanksgiving_host(team_abbr: str) -> bool:
    """Check if team is a traditional Thanksgiving host."""
    return team_abbr in THANKSGIVING_HOSTS


def get_thanksgiving_boost(team_abbr: str) -> float:
    """Get the extra home field boost for Thanksgiving hosts."""
    if team_abbr in THANKSGIVING_HOSTS:
        return THANKSGIVING_HOSTS[team_abbr]["home_field_boost"]
    return 0.0
