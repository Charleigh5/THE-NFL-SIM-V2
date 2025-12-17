"""
2025 NFL Free Agent Signings Data
==================================

This file contains verified 2025 NFL free agent signings for seeding.
Data sourced from PFF, ESPN, NFL.com, and verified sports outlets.

LAST UPDATED: December 2024 (2025 Free Agency Period - March 2025)

AUTO-UPDATE NOTES:
------------------
This data should be refreshed from the following sources:
1. nflreadpy.load_rosters(2025) - When available (after August 26, 2025)
2. nflreadpy.load_contracts() - For updated contract data
3. nflreadpy.load_nextgen_stats(2025) - When 2025 season data becomes available
4. PFF Free Agent Tracker - https://www.pff.com/
5. NFL Transaction Wire - https://www.nfl.com/transactions

VISION: This NFL Sim Engine aims to be the definitive SOTA simulation that
exemplifies the true NFL experience - from the GM's war room to the coach's
sideline to every snap on the field. EA Sports-quality authenticity.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Position(str, Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"
    OT = "OT"
    OG = "OG"
    C = "C"
    DE = "DE"
    DT = "DT"
    EDGE = "EDGE"
    LB = "LB"
    CB = "CB"
    S = "S"
    K = "K"
    P = "P"

@dataclass
class FreeAgentSigning:
    """Represents a 2025 NFL Free Agent Signing."""
    first_name: str
    last_name: str
    position: str
    new_team: str  # Team abbreviation
    previous_team: str
    contract_years: int
    contract_total: int  # Total contract value in dollars
    contract_gtd: int  # Guaranteed money
    apy: int  # Average per year
    age: int
    # Ratings overrides based on real-world performance
    overall_rating: int
    speed: Optional[int] = None
    strength: Optional[int] = None
    awareness: Optional[int] = None
    # Key attribute for position
    primary_attribute: Optional[int] = None


# =============================================================================
# 2025 TOP FREE AGENT SIGNINGS
# =============================================================================
# Ranked by total contract value
# Data verified from PFF, ESPN, NFL.com (March 2025 Free Agency)

FREE_AGENT_SIGNINGS_2025: List[FreeAgentSigning] = [
    # RANK 1: Milton Williams - DT - Highest paid DT in free agency
    FreeAgentSigning(
        first_name="Milton", last_name="Williams",
        position="DT", new_team="NE", previous_team="PHI",
        contract_years=4, contract_total=104_000_000, contract_gtd=65_000_000, apy=26_000_000,
        age=26, overall_rating=88, strength=92, awareness=85, primary_attribute=90  # block_shed
    ),

    # RANK 2: Sam Darnold - QB - Bounce-back QB
    FreeAgentSigning(
        first_name="Sam", last_name="Darnold",
        position="QB", new_team="SEA", previous_team="MIN",
        contract_years=3, contract_total=100_500_000, contract_gtd=63_000_000, apy=33_500_000,
        age=28, overall_rating=82, speed=78, awareness=80, primary_attribute=85  # throw_power
    ),

    # RANK 3: Dan Moore Jr. - OT - Premium LT
    FreeAgentSigning(
        first_name="Dan", last_name="Moore Jr.",
        position="OT", new_team="TEN", previous_team="PIT",
        contract_years=4, contract_total=82_000_000, contract_gtd=50_000_000, apy=20_500_000,
        age=26, overall_rating=83, strength=88, awareness=82, primary_attribute=85  # pass_block
    ),

    # RANK 4: Josh Sweat - EDGE - Elite pass rusher
    FreeAgentSigning(
        first_name="Josh", last_name="Sweat",
        position="DE", new_team="ARI", previous_team="PHI",
        contract_years=4, contract_total=76_400_000, contract_gtd=45_000_000, apy=19_100_000,
        age=28, overall_rating=86, speed=88, strength=83, primary_attribute=87  # pass_rush_power
    ),

    # RANK 5: Ronnie Stanley - OT - Elite when healthy
    FreeAgentSigning(
        first_name="Ronnie", last_name="Stanley",
        position="OT", new_team="BAL", previous_team="BAL",
        contract_years=3, contract_total=60_000_000, contract_gtd=40_000_000, apy=20_000_000,
        age=31, overall_rating=85, strength=86, awareness=88, primary_attribute=89  # pass_block
    ),

    # RANK 6: Alaric Jackson - OT
    FreeAgentSigning(
        first_name="Alaric", last_name="Jackson",
        position="OT", new_team="LAR", previous_team="LAR",
        contract_years=3, contract_total=57_000_000, contract_gtd=35_000_000, apy=19_000_000,
        age=27, overall_rating=82, strength=85, awareness=80, primary_attribute=83  # pass_block
    ),

    # RANK 7: Chase Young - EDGE - Former #2 pick
    FreeAgentSigning(
        first_name="Chase", last_name="Young",
        position="DE", new_team="NO", previous_team="NO",
        contract_years=3, contract_total=51_000_000, contract_gtd=30_000_000, apy=17_000_000,
        age=26, overall_rating=84, speed=86, strength=84, primary_attribute=85  # pass_rush_power
    ),

    # RANK 8: Jonathan Allen - DT - Elite interior
    FreeAgentSigning(
        first_name="Jonathan", last_name="Allen",
        position="DT", new_team="MIN", previous_team="WAS",
        contract_years=3, contract_total=51_000_000, contract_gtd=32_000_000, apy=17_000_000,
        age=30, overall_rating=87, strength=90, awareness=86, primary_attribute=88  # block_shed
    ),

    # RANK 9: Dayo Odeyingbo - EDGE
    FreeAgentSigning(
        first_name="Dayo", last_name="Odeyingbo",
        position="DE", new_team="CHI", previous_team="IND",
        contract_years=3, contract_total=48_000_000, contract_gtd=28_000_000, apy=16_000_000,
        age=26, overall_rating=81, speed=84, strength=82, primary_attribute=83  # pass_rush_finesse
    ),

    # RANK 10: Jamien Sherwood - LB
    FreeAgentSigning(
        first_name="Jamien", last_name="Sherwood",
        position="LB", new_team="NYJ", previous_team="NYJ",
        contract_years=3, contract_total=45_000_000, contract_gtd=27_000_000, apy=15_000_000,
        age=26, overall_rating=82, speed=82, awareness=84, primary_attribute=85  # tackle
    ),

    # RANK 11: Devante Adams - WR - Elite route runner
    FreeAgentSigning(
        first_name="Devante", last_name="Adams",
        position="WR", new_team="LAR", previous_team="NYJ",
        contract_years=2, contract_total=44_000_000, contract_gtd=30_000_000, apy=22_000_000,
        age=32, overall_rating=91, speed=88, awareness=95, primary_attribute=97  # route_running
    ),

    # RANK 12: Grady Jarrett - DT
    FreeAgentSigning(
        first_name="Grady", last_name="Jarrett",
        position="DT", new_team="CHI", previous_team="ATL",
        contract_years=3, contract_total=43_500_000, contract_gtd=25_000_000, apy=14_500_000,
        age=31, overall_rating=85, strength=88, awareness=86, primary_attribute=86  # block_shed
    ),

    # RANK 13: Justin Fields - QB
    FreeAgentSigning(
        first_name="Justin", last_name="Fields",
        position="QB", new_team="NYJ", previous_team="PIT",
        contract_years=2, contract_total=40_000_000, contract_gtd=25_000_000, apy=20_000_000,
        age=26, overall_rating=80, speed=92, awareness=75, primary_attribute=78  # throw_accuracy_mid
    ),

    # RANK 14: Robert Spillane - LB
    FreeAgentSigning(
        first_name="Robert", last_name="Spillane",
        position="LB", new_team="NE", previous_team="LV",
        contract_years=3, contract_total=37_000_000, contract_gtd=22_000_000, apy=12_333_333,
        age=29, overall_rating=80, speed=80, awareness=83, primary_attribute=82  # tackle
    ),

    # RANK 15: Joshua Palmer - WR
    FreeAgentSigning(
        first_name="Joshua", last_name="Palmer",
        position="WR", new_team="BUF", previous_team="LAC",
        contract_years=3, contract_total=36_000_000, contract_gtd=20_000_000, apy=12_000_000,
        age=26, overall_rating=79, speed=86, awareness=78, primary_attribute=80  # catching
    ),

    # RANK 16: Ernest Jones - LB
    FreeAgentSigning(
        first_name="Ernest", last_name="Jones",
        position="LB", new_team="SEA", previous_team="SEA",
        contract_years=3, contract_total=33_000_000, contract_gtd=20_000_000, apy=11_000_000,
        age=26, overall_rating=81, speed=81, awareness=82, primary_attribute=83  # tackle
    ),

    # RANK 17: Dre Greenlaw - LB
    FreeAgentSigning(
        first_name="Dre", last_name="Greenlaw",
        position="LB", new_team="DEN", previous_team="SF",
        contract_years=3, contract_total=31_500_000, contract_gtd=18_000_000, apy=10_500_000,
        age=28, overall_rating=82, speed=84, awareness=85, primary_attribute=84  # tackle
    ),

    # RANK 18: Juwan Johnson - TE
    FreeAgentSigning(
        first_name="Juwan", last_name="Johnson",
        position="TE", new_team="NO", previous_team="NO",
        contract_years=3, contract_total=30_750_000, contract_gtd=18_000_000, apy=10_250_000,
        age=29, overall_rating=79, speed=80, awareness=78, primary_attribute=81  # catching
    ),

    # RANK 19: Jaylon Moore - OT
    FreeAgentSigning(
        first_name="Jaylon", last_name="Moore",
        position="OT", new_team="KC", previous_team="CHI",
        contract_years=2, contract_total=30_000_000, contract_gtd=18_000_000, apy=15_000_000,
        age=27, overall_rating=80, strength=84, awareness=79, primary_attribute=81  # pass_block
    ),

    # RANK 20: Javon Hargrave - DT
    FreeAgentSigning(
        first_name="Javon", last_name="Hargrave",
        position="DT", new_team="MIN", previous_team="SF",
        contract_years=2, contract_total=30_000_000, contract_gtd=18_000_000, apy=15_000_000,
        age=32, overall_rating=84, strength=87, awareness=84, primary_attribute=85  # block_shed
    ),

    # === ADDITIONAL NOTABLE SIGNINGS ===

    # Aaron Rodgers - Trade/Signing
    FreeAgentSigning(
        first_name="Aaron", last_name="Rodgers",
        position="QB", new_team="PIT", previous_team="NYJ",
        contract_years=1, contract_total=15_000_000, contract_gtd=15_000_000, apy=15_000_000,
        age=41, overall_rating=85, speed=72, awareness=97, primary_attribute=92  # throw_accuracy_deep
    ),

    # Russell Wilson
    FreeAgentSigning(
        first_name="Russell", last_name="Wilson",
        position="QB", new_team="NYG", previous_team="PIT",
        contract_years=1, contract_total=10_500_000, contract_gtd=10_500_000, apy=10_500_000,
        age=36, overall_rating=80, speed=80, awareness=88, primary_attribute=85  # throw_on_run
    ),

    # Aaron Jones
    FreeAgentSigning(
        first_name="Aaron", last_name="Jones",
        position="RB", new_team="MIN", previous_team="MIN",
        contract_years=2, contract_total=20_000_000, contract_gtd=12_000_000, apy=10_000_000,
        age=30, overall_rating=84, speed=88, awareness=82, primary_attribute=86  # agility
    ),

    # Khalil Mack
    FreeAgentSigning(
        first_name="Khalil", last_name="Mack",
        position="DE", new_team="LAC", previous_team="LAC",
        contract_years=1, contract_total=18_000_000, contract_gtd=18_000_000, apy=18_000_000,
        age=34, overall_rating=88, speed=82, strength=90, primary_attribute=92  # pass_rush_power
    ),

    # Joey Bosa
    FreeAgentSigning(
        first_name="Joey", last_name="Bosa",
        position="DE", new_team="BUF", previous_team="LAC",
        contract_years=1, contract_total=12_600_000, contract_gtd=12_600_000, apy=12_600_000,
        age=30, overall_rating=85, speed=82, strength=87, primary_attribute=88  # pass_rush_finesse
    ),

    # Haason Reddick
    FreeAgentSigning(
        first_name="Haason", last_name="Reddick",
        position="DE", new_team="TB", previous_team="NYJ",
        contract_years=1, contract_total=14_000_000, contract_gtd=14_000_000, apy=14_000_000,
        age=31, overall_rating=84, speed=86, strength=82, primary_attribute=86  # pass_rush_power
    ),

    # Nick Chubb
    FreeAgentSigning(
        first_name="Nick", last_name="Chubb",
        position="RB", new_team="HOU", previous_team="CLE",
        contract_years=1, contract_total=5_000_000, contract_gtd=5_000_000, apy=5_000_000,
        age=29, overall_rating=83, speed=85, strength=88, primary_attribute=90  # break_tackle
    ),

    # Najee Harris
    FreeAgentSigning(
        first_name="Najee", last_name="Harris",
        position="RB", new_team="LAC", previous_team="PIT",
        contract_years=1, contract_total=9_250_000, contract_gtd=6_000_000, apy=9_250_000,
        age=27, overall_rating=81, speed=84, strength=86, primary_attribute=85  # break_tackle
    ),
]


# =============================================================================
# HELPER FUNCTIONS FOR SEEDING
# =============================================================================

def get_all_free_agents() -> List[FreeAgentSigning]:
    """Return all 2025 free agent signings."""
    return FREE_AGENT_SIGNINGS_2025


def get_free_agents_by_team(team_abbr: str) -> List[FreeAgentSigning]:
    """Get free agents acquired by a specific team."""
    return [fa for fa in FREE_AGENT_SIGNINGS_2025 if fa.new_team == team_abbr]


def get_free_agents_by_position(position: str) -> List[FreeAgentSigning]:
    """Get free agents by position."""
    return [fa for fa in FREE_AGENT_SIGNINGS_2025 if fa.position == position]


def get_top_free_agents(n: int = 20) -> List[FreeAgentSigning]:
    """Get top N free agents by contract value."""
    sorted_fas = sorted(FREE_AGENT_SIGNINGS_2025, key=lambda x: x.contract_total, reverse=True)
    return sorted_fas[:n]


# =============================================================================
# AUTO-UPDATE CONFIGURATION
# =============================================================================

DATA_UPDATE_SOURCES = {
    "rosters": {
        "source": "nflreadpy.load_rosters",
        "update_frequency": "weekly",  # During season
        "notes": "Full roster updates including transactions, injuries, IR moves"
    },
    "contracts": {
        "source": "nflreadpy.load_contracts",
        "update_frequency": "daily",  # During free agency
        "notes": "Contract extensions, new signings, restructures"
    },
    "nextgen_stats": {
        "source": "nflreadpy.load_nextgen_stats",
        "update_frequency": "weekly",
        "notes": "Player performance metrics for ratings generation"
    },
    "combine": {
        "source": "nflreadpy.load_combine",
        "update_frequency": "annual",  # After NFL Combine (Feb/March)
        "notes": "Physical measurements and athletic testing"
    },
    "injuries": {
        "source": "nflreadpy.load_injuries",
        "update_frequency": "daily",
        "notes": "Injury reports, practice participation, game status"
    },
    "transactions": {
        "source": "nflreadpy.load_transactions",
        "update_frequency": "daily",
        "notes": "Trades, releases, signings, waiver claims"
    },
    "draft": {
        "source": "nflreadpy.load_draft_picks",
        "update_frequency": "annual",  # After NFL Draft (April)
        "notes": "Draft picks, round selections, compensatory picks"
    }
}

# Key dates for data updates
NFL_DATA_CALENDAR = {
    "combine": "Late February",
    "free_agency_start": "March 12",
    "draft": "Late April",
    "otas": "May-June",
    "training_camp": "Late July",
    "preseason": "August",
    "roster_cutdown": "August 26",
    "regular_season_start": "September 4",
    "trade_deadline": "Early November",
    "playoffs": "January",
    "super_bowl": "February 8, 2026"
}


if __name__ == "__main__":
    # Test the data
    print(f"=== 2025 NFL Free Agent Data ===")
    print(f"Total signings tracked: {len(FREE_AGENT_SIGNINGS_2025)}")
    print(f"\nTop 5 by contract value:")
    for i, fa in enumerate(get_top_free_agents(5), 1):
        print(f"  {i}. {fa.first_name} {fa.last_name} ({fa.position}) -> {fa.new_team}: ${fa.contract_total:,}")

    print(f"\n=== Data Update Sources ===")
    for source, info in DATA_UPDATE_SOURCES.items():
        print(f"  {source}: {info['source']} ({info['update_frequency']})")
