"""
NFL Coaching Staff Database (2025 Season)
==========================================
Complete coaching staff data for all 32 NFL teams.

Data includes:
- Head Coach, Offensive Coordinator, Defensive Coordinator
- Offensive scheme (West Coast, Zone Run, Power Run, Air Raid, RPO)
- Defensive scheme (4-3, 3-4)
- Coaching philosophy traits
"""

from enum import Enum

from pydantic import BaseModel


class OffensiveScheme(str, Enum):
    """Offensive philosophy/concept."""

    WEST_COAST = "WEST_COAST"
    ZONE_RUN = "ZONE_RUN"
    POWER_RUN = "POWER_RUN"
    AIR_RAID = "AIR_RAID"
    RPO = "RPO"


class DefensiveScheme(str, Enum):
    """Base defensive alignment."""

    FOUR_THREE = "4-3"
    THREE_FOUR = "3-4"


class CoachData(BaseModel):
    """Individual coach information."""

    first_name: str
    last_name: str
    defensive_disguise: int = 50  # Playbook Phase 11: Capability to mask coverage


class CoachingPhilosophy(BaseModel):
    """Team coaching philosophy traits."""

    run_pass_ratio: int = 50  # 0 = all pass, 100 = all run
    blitz_frequency: int = 30  # 0-100 scale
    aggressiveness: int = 50  # General aggressiveness
    tempo: int = 50  # 0 = slow, 100 = hurry-up

    # New Phase 2 Personality Fields
    fourth_down_aggression: int = 50  # Specific 4th down tendency (0-100)
    clock_management_style: str = "BALANCED"  # CONSERVATIVE, AGGRESSIVE
    trick_play_frequency: int = 5  # 0-100 scale
    two_pt_conversion_threshold: int = 50  # Multiplier for "chart" logic
    timeout_aggressiveness: int = 50  # Willingness to use timeouts early


class TeamCoachingStaff(BaseModel):
    """Complete coaching staff for a team."""

    head_coach: CoachData
    offensive_coordinator: CoachData
    defensive_coordinator: CoachData
    playbook_offense: OffensiveScheme
    playbook_defense: DefensiveScheme
    philosophy: CoachingPhilosophy


# =============================================================================
# 2025 NFL COACHING STAFF DATABASE
# =============================================================================

COACHES_DB: dict[str, TeamCoachingStaff] = {
    # AFC EAST
    "BUF": TeamCoachingStaff(
        head_coach=CoachData(first_name="Sean", last_name="McDermott"),
        offensive_coordinator=CoachData(first_name="Joe", last_name="Brady"),
        defensive_coordinator=CoachData(first_name="Bobby", last_name="Babich"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=35, aggressiveness=65, tempo=55
        ),
    ),
    "MIA": TeamCoachingStaff(
        head_coach=CoachData(first_name="Mike", last_name="McDaniel"),
        offensive_coordinator=CoachData(first_name="Frank", last_name="Smith"),
        defensive_coordinator=CoachData(first_name="Anthony", last_name="Weaver"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=40, blitz_frequency=30, aggressiveness=60, tempo=75
        ),
    ),
    "NE": TeamCoachingStaff(
        head_coach=CoachData(first_name="Mike", last_name="Vrabel"),
        offensive_coordinator=CoachData(first_name="Josh", last_name="McDaniels"),
        defensive_coordinator=CoachData(first_name="Terrell", last_name="Williams"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50, blitz_frequency=25, aggressiveness=45, tempo=45
        ),
    ),
    "NYJ": TeamCoachingStaff(
        head_coach=CoachData(first_name="Aaron", last_name="Glenn"),
        offensive_coordinator=CoachData(first_name="Tanner", last_name="Engstrand"),
        defensive_coordinator=CoachData(
            first_name="Steve", last_name="Wilks", defensive_disguise=80
        ),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=40, aggressiveness=50, tempo=50
        ),
    ),
    # AFC NORTH
    "BAL": TeamCoachingStaff(
        head_coach=CoachData(first_name="John", last_name="Harbaugh"),
        offensive_coordinator=CoachData(first_name="Todd", last_name="Monken"),
        defensive_coordinator=CoachData(first_name="Zach", last_name="Orr"),
        playbook_offense=OffensiveScheme.POWER_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=60, blitz_frequency=45, aggressiveness=70, tempo=60
        ),
    ),
    "CIN": TeamCoachingStaff(
        head_coach=CoachData(first_name="Zac", last_name="Taylor"),
        offensive_coordinator=CoachData(first_name="Dan", last_name="Pitcher"),
        defensive_coordinator=CoachData(first_name="Al", last_name="Golden"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=35, blitz_frequency=30, aggressiveness=55, tempo=55
        ),
    ),
    "CLE": TeamCoachingStaff(
        head_coach=CoachData(first_name="Kevin", last_name="Stefanski"),
        offensive_coordinator=CoachData(first_name="Tommy", last_name="Rees"),
        defensive_coordinator=CoachData(first_name="Jim", last_name="Schwartz"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=55, blitz_frequency=25, aggressiveness=50, tempo=50
        ),
    ),
    "PIT": TeamCoachingStaff(
        head_coach=CoachData(first_name="Mike", last_name="Tomlin"),
        offensive_coordinator=CoachData(first_name="Arthur", last_name="Smith"),
        defensive_coordinator=CoachData(first_name="Teryl", last_name="Austin"),
        playbook_offense=OffensiveScheme.POWER_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=55, blitz_frequency=50, aggressiveness=55, tempo=45
        ),
    ),
    # AFC SOUTH
    "HOU": TeamCoachingStaff(
        head_coach=CoachData(first_name="DeMeco", last_name="Ryans"),
        offensive_coordinator=CoachData(first_name="Nick", last_name="Caley"),
        defensive_coordinator=CoachData(first_name="Matt", last_name="Burke"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=35, aggressiveness=60, tempo=55
        ),
    ),
    "IND": TeamCoachingStaff(
        head_coach=CoachData(first_name="Shane", last_name="Steichen"),
        offensive_coordinator=CoachData(first_name="Jim Bob", last_name="Cooter"),
        defensive_coordinator=CoachData(
            first_name="Lou", last_name="Anarumo", defensive_disguise=82
        ),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50, blitz_frequency=30, aggressiveness=55, tempo=55
        ),
    ),
    "JAX": TeamCoachingStaff(
        head_coach=CoachData(first_name="Liam", last_name="Coen"),
        offensive_coordinator=CoachData(first_name="Grant", last_name="Udinski"),
        defensive_coordinator=CoachData(first_name="Anthony", last_name="Campanile"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=40, blitz_frequency=35, aggressiveness=60, tempo=65
        ),
    ),
    "TEN": TeamCoachingStaff(
        head_coach=CoachData(first_name="Brian", last_name="Callahan"),
        offensive_coordinator=CoachData(first_name="Nick", last_name="Holz"),
        defensive_coordinator=CoachData(first_name="Dennard", last_name="Wilson"),
        playbook_offense=OffensiveScheme.POWER_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=55, blitz_frequency=30, aggressiveness=45, tempo=45
        ),
    ),
    # AFC WEST
    "DEN": TeamCoachingStaff(
        head_coach=CoachData(first_name="Sean", last_name="Payton"),
        offensive_coordinator=CoachData(first_name="Joe", last_name="Lombardi"),
        defensive_coordinator=CoachData(first_name="Vance", last_name="Joseph"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=35, aggressiveness=65, tempo=55
        ),
    ),
    "KC": TeamCoachingStaff(
        head_coach=CoachData(first_name="Andy", last_name="Reid"),
        offensive_coordinator=CoachData(first_name="Matt", last_name="Nagy"),
        defensive_coordinator=CoachData(
            first_name="Steve", last_name="Spagnuolo", defensive_disguise=85
        ),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=40,
            blitz_frequency=35,
            aggressiveness=70,
            tempo=60,
            trick_play_frequency=30,
        ),
    ),
    "LV": TeamCoachingStaff(
        head_coach=CoachData(first_name="Pete", last_name="Carroll"),
        offensive_coordinator=CoachData(first_name="Chip", last_name="Kelly"),
        defensive_coordinator=CoachData(first_name="Patrick", last_name="Graham"),
        playbook_offense=OffensiveScheme.RPO,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50, blitz_frequency=25, aggressiveness=55, tempo=70
        ),
    ),
    "LAC": TeamCoachingStaff(
        head_coach=CoachData(first_name="Jim", last_name="Harbaugh"),
        offensive_coordinator=CoachData(first_name="Greg", last_name="Roman"),
        defensive_coordinator=CoachData(first_name="Jesse", last_name="Minter"),
        playbook_offense=OffensiveScheme.POWER_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=60, blitz_frequency=40, aggressiveness=60, tempo=45
        ),
    ),
    # NFC EAST
    "DAL": TeamCoachingStaff(
        head_coach=CoachData(first_name="Brian", last_name="Schottenheimer"),
        offensive_coordinator=CoachData(first_name="Klayton", last_name="Adams"),
        defensive_coordinator=CoachData(first_name="Matt", last_name="Eberflus"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=30, aggressiveness=50, tempo=50
        ),
    ),
    "NYG": TeamCoachingStaff(
        head_coach=CoachData(first_name="Brian", last_name="Daboll"),
        offensive_coordinator=CoachData(first_name="Mike", last_name="Kafka"),
        defensive_coordinator=CoachData(first_name="Charlie", last_name="Bullen"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=35, aggressiveness=55, tempo=55
        ),
    ),
    "PHI": TeamCoachingStaff(
        head_coach=CoachData(first_name="Nick", last_name="Sirianni"),
        offensive_coordinator=CoachData(first_name="Kevin", last_name="Patullo"),
        defensive_coordinator=CoachData(
            first_name="Vic", last_name="Fangio", defensive_disguise=88
        ),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=55, blitz_frequency=30, aggressiveness=65, tempo=55
        ),
    ),
    "WAS": TeamCoachingStaff(
        head_coach=CoachData(first_name="Dan", last_name="Quinn"),
        offensive_coordinator=CoachData(first_name="Kliff", last_name="Kingsbury"),
        defensive_coordinator=CoachData(
            first_name="Joe", last_name="Whitt Jr."
        ),  # Quinn is HC/DC essentially
        playbook_offense=OffensiveScheme.AIR_RAID,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=35, blitz_frequency=40, aggressiveness=70, tempo=70
        ),
    ),
    # NFC NORTH
    "CHI": TeamCoachingStaff(
        head_coach=CoachData(first_name="Ben", last_name="Johnson"),
        offensive_coordinator=CoachData(first_name="Declan", last_name="Doyle"),
        defensive_coordinator=CoachData(first_name="Dennis", last_name="Allen"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50, blitz_frequency=30, aggressiveness=65, tempo=60
        ),
    ),
    "DET": TeamCoachingStaff(
        head_coach=CoachData(first_name="Dan", last_name="Campbell"),
        offensive_coordinator=CoachData(first_name="John", last_name="Morton"),
        defensive_coordinator=CoachData(first_name="Kelvin", last_name="Sheppard"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50,
            blitz_frequency=35,
            aggressiveness=80,
            tempo=60,
            fourth_down_aggression=95,
            trick_play_frequency=25,
            two_pt_conversion_threshold=70,
        ),
    ),
    "GB": TeamCoachingStaff(
        head_coach=CoachData(first_name="Matt", last_name="LaFleur"),
        offensive_coordinator=CoachData(first_name="Adam", last_name="Stenavich"),
        defensive_coordinator=CoachData(first_name="Jeff", last_name="Hafley"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=30, aggressiveness=60, tempo=55
        ),
    ),
    "MIN": TeamCoachingStaff(
        head_coach=CoachData(first_name="Kevin", last_name="O'Connell"),
        offensive_coordinator=CoachData(first_name="Wes", last_name="Phillips"),
        defensive_coordinator=CoachData(
            first_name="Brian", last_name="Flores", defensive_disguise=90
        ),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=40, blitz_frequency=55, aggressiveness=60, tempo=55
        ),
    ),
    # NFC SOUTH
    "ATL": TeamCoachingStaff(
        head_coach=CoachData(first_name="Raheem", last_name="Morris"),
        offensive_coordinator=CoachData(first_name="Zac", last_name="Robinson"),
        defensive_coordinator=CoachData(first_name="Jeff", last_name="Ulbrich"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50, blitz_frequency=40, aggressiveness=55, tempo=55
        ),
    ),
    "CAR": TeamCoachingStaff(
        head_coach=CoachData(first_name="Dave", last_name="Canales"),
        offensive_coordinator=CoachData(first_name="Brad", last_name="Idzik"),
        defensive_coordinator=CoachData(first_name="Ejiro", last_name="Evero"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=30, aggressiveness=50, tempo=50
        ),
    ),
    "NO": TeamCoachingStaff(
        head_coach=CoachData(first_name="Kellen", last_name="Moore"),
        offensive_coordinator=CoachData(first_name="Doug", last_name="Nussmeier"),
        defensive_coordinator=CoachData(first_name="Brandon", last_name="Staley"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=40, blitz_frequency=35, aggressiveness=60, tempo=60
        ),
    ),
    "TB": TeamCoachingStaff(
        head_coach=CoachData(first_name="Todd", last_name="Bowles"),
        offensive_coordinator=CoachData(first_name="Josh", last_name="Grizzard"),
        defensive_coordinator=CoachData(first_name="Larry", last_name="Foote"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=50, aggressiveness=55, tempo=50
        ),
    ),
    # NFC WEST
    "ARI": TeamCoachingStaff(
        head_coach=CoachData(first_name="Jonathan", last_name="Gannon"),
        offensive_coordinator=CoachData(first_name="Drew", last_name="Petzing"),
        defensive_coordinator=CoachData(first_name="Nick", last_name="Rallis"),
        playbook_offense=OffensiveScheme.WEST_COAST,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=35, aggressiveness=55, tempo=55
        ),
    ),
    "LAR": TeamCoachingStaff(
        head_coach=CoachData(first_name="Sean", last_name="McVay"),
        offensive_coordinator=CoachData(first_name="Mike", last_name="LaFleur"),
        defensive_coordinator=CoachData(first_name="Chris", last_name="Shula"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=30, aggressiveness=65, tempo=65
        ),
    ),
    "SF": TeamCoachingStaff(
        head_coach=CoachData(first_name="Kyle", last_name="Shanahan"),
        offensive_coordinator=CoachData(first_name="Klay", last_name="Kubiak"),
        defensive_coordinator=CoachData(first_name="Robert", last_name="Saleh"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.FOUR_THREE,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=50, blitz_frequency=30, aggressiveness=60, tempo=55
        ),
    ),
    "SEA": TeamCoachingStaff(
        head_coach=CoachData(first_name="Mike", last_name="Macdonald"),
        offensive_coordinator=CoachData(first_name="Klint", last_name="Kubiak"),
        defensive_coordinator=CoachData(first_name="Aden", last_name="Durde"),
        playbook_offense=OffensiveScheme.ZONE_RUN,
        playbook_defense=DefensiveScheme.THREE_FOUR,
        philosophy=CoachingPhilosophy(
            run_pass_ratio=45, blitz_frequency=45, aggressiveness=55, tempo=55
        ),
    ),
}


def get_coaching_staff(team_abbr: str) -> TeamCoachingStaff:
    """
    Get coaching staff for a team.

    Args:
        team_abbr: Team abbreviation (e.g., 'KC', 'SF')

    Returns:
        TeamCoachingStaff object

    Raises:
        KeyError: If team not found
    """
    if team_abbr not in COACHES_DB:
        raise KeyError(f"Team '{team_abbr}' not found. Valid teams: {list(COACHES_DB.keys())}")
    return COACHES_DB[team_abbr]


def get_all_head_coaches() -> list:
    """Get list of all head coaches with their teams."""
    return [
        {"team": abbr, "name": f"{staff.head_coach.first_name} {staff.head_coach.last_name}"}
        for abbr, staff in COACHES_DB.items()
    ]


__all__ = [
    "COACHES_DB",
    "TeamCoachingStaff",
    "CoachData",
    "CoachingPhilosophy",
    "OffensiveScheme",
    "DefensiveScheme",
    "get_coaching_staff",
    "get_all_head_coaches",
]
