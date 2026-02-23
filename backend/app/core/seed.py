import logging
import os
import random

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.data.coaches import COACHES_DB
from app.data.scouts import TEAM_SCOUTS
from app.models.coach import Coach
from app.models.player import Player
from app.models.scout import Scout
from app.models.team import Team

# NFL Data Integration (optional)
try:
    from app.data.career_accomplishments import PLAYER_ACCOMPLISHMENTS
    from app.services.nflverse_service import NflverseService
    from app.services.ratings_generator import (
        calculate_overall_rating_modifier,
        generate_player_ratings,
    )

    HAS_NFLVERSE = True
except ImportError:
    HAS_NFLVERSE = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NFL_TEAMS = [
    {
        "city": "Arizona",
        "name": "Cardinals",
        "abbreviation": "ARI",
        "conference": "NFC",
        "division": "West",
    },
    {
        "city": "Atlanta",
        "name": "Falcons",
        "abbreviation": "ATL",
        "conference": "NFC",
        "division": "South",
    },
    {
        "city": "Baltimore",
        "name": "Ravens",
        "abbreviation": "BAL",
        "conference": "AFC",
        "division": "North",
    },
    {
        "city": "Buffalo",
        "name": "Bills",
        "abbreviation": "BUF",
        "conference": "AFC",
        "division": "East",
    },
    {
        "city": "Carolina",
        "name": "Panthers",
        "abbreviation": "CAR",
        "conference": "NFC",
        "division": "South",
    },
    {
        "city": "Chicago",
        "name": "Bears",
        "abbreviation": "CHI",
        "conference": "NFC",
        "division": "North",
    },
    {
        "city": "Cincinnati",
        "name": "Bengals",
        "abbreviation": "CIN",
        "conference": "AFC",
        "division": "North",
    },
    {
        "city": "Cleveland",
        "name": "Browns",
        "abbreviation": "CLE",
        "conference": "AFC",
        "division": "North",
    },
    {
        "city": "Dallas",
        "name": "Cowboys",
        "abbreviation": "DAL",
        "conference": "NFC",
        "division": "East",
    },
    {
        "city": "Denver",
        "name": "Broncos",
        "abbreviation": "DEN",
        "conference": "AFC",
        "division": "West",
    },
    {
        "city": "Detroit",
        "name": "Lions",
        "abbreviation": "DET",
        "conference": "NFC",
        "division": "North",
    },
    {
        "city": "Green Bay",
        "name": "Packers",
        "abbreviation": "GB",
        "conference": "NFC",
        "division": "North",
    },
    {
        "city": "Houston",
        "name": "Texans",
        "abbreviation": "HOU",
        "conference": "AFC",
        "division": "South",
    },
    {
        "city": "Indianapolis",
        "name": "Colts",
        "abbreviation": "IND",
        "conference": "AFC",
        "division": "South",
    },
    {
        "city": "Jacksonville",
        "name": "Jaguars",
        "abbreviation": "JAX",
        "conference": "AFC",
        "division": "South",
    },
    {
        "city": "Kansas City",
        "name": "Chiefs",
        "abbreviation": "KC",
        "conference": "AFC",
        "division": "West",
    },
    {
        "city": "Las Vegas",
        "name": "Raiders",
        "abbreviation": "LV",
        "conference": "AFC",
        "division": "West",
    },
    {
        "city": "Los Angeles",
        "name": "Chargers",
        "abbreviation": "LAC",
        "conference": "AFC",
        "division": "West",
    },
    {
        "city": "Los Angeles",
        "name": "Rams",
        "abbreviation": "LAR",
        "conference": "NFC",
        "division": "West",
    },
    {
        "city": "Miami",
        "name": "Dolphins",
        "abbreviation": "MIA",
        "conference": "AFC",
        "division": "East",
    },
    {
        "city": "Minnesota",
        "name": "Vikings",
        "abbreviation": "MIN",
        "conference": "NFC",
        "division": "North",
    },
    {
        "city": "New England",
        "name": "Patriots",
        "abbreviation": "NE",
        "conference": "AFC",
        "division": "East",
    },
    {
        "city": "New Orleans",
        "name": "Saints",
        "abbreviation": "NO",
        "conference": "NFC",
        "division": "South",
    },
    {
        "city": "New York",
        "name": "Giants",
        "abbreviation": "NYG",
        "conference": "NFC",
        "division": "East",
    },
    {
        "city": "New York",
        "name": "Jets",
        "abbreviation": "NYJ",
        "conference": "AFC",
        "division": "East",
    },
    {
        "city": "Philadelphia",
        "name": "Eagles",
        "abbreviation": "PHI",
        "conference": "NFC",
        "division": "East",
    },
    {
        "city": "Pittsburgh",
        "name": "Steelers",
        "abbreviation": "PIT",
        "conference": "AFC",
        "division": "North",
    },
    {
        "city": "San Francisco",
        "name": "49ers",
        "abbreviation": "SF",
        "conference": "NFC",
        "division": "West",
    },
    {
        "city": "Seattle",
        "name": "Seahawks",
        "abbreviation": "SEA",
        "conference": "NFC",
        "division": "West",
    },
    {
        "city": "Tampa Bay",
        "name": "Buccaneers",
        "abbreviation": "TB",
        "conference": "NFC",
        "division": "South",
    },
    {
        "city": "Tennessee",
        "name": "Titans",
        "abbreviation": "TEN",
        "conference": "AFC",
        "division": "South",
    },
    {
        "city": "Washington",
        "name": "Commanders",
        "abbreviation": "WAS",
        "conference": "NFC",
        "division": "East",
    },
]

POSITIONS = {
    "QB": 3,
    "RB": 4,
    "WR": 6,
    "TE": 3,
    "OL": 9,
    "DL": 8,
    "LB": 7,
    "CB": 6,
    "S": 4,
    "K": 1,
    "P": 1,
}

FIRST_NAMES = [
    "James",
    "John",
    "Robert",
    "Michael",
    "William",
    "David",
    "Richard",
    "Joseph",
    "Thomas",
    "Charles",
    "Chris",
    "Dan",
    "Pat",
    "Steve",
    "Jim",
    "Tom",
    "Tim",
    "Rob",
    "Mike",
    "Bill",
    "Dave",
    "Rich",
    "Joe",
    "Chuck",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
]


def seed_teams(db: Session):
    existing_teams = db.query(Team).count()
    if existing_teams > 0:
        logger.info(f"Teams already seeded ({existing_teams} found). Skipping.")
        return

    logger.info("Seeding 32 NFL Teams...")
    teams = []
    for team_data in NFL_TEAMS:
        team = Team(
            city=team_data["city"],
            name=team_data["name"],
            abbreviation=team_data["abbreviation"],
            conference=team_data["conference"],
            division=team_data["division"],
            wins=0,
            losses=0,
        )
        teams.append(team)

    db.add_all(teams)
    db.commit()
    logger.info("Teams seeded successfully.")


def generate_player(position: str, team_id: int) -> Player:
    return Player(
        first_name=random.choice(FIRST_NAMES),
        last_name=random.choice(LAST_NAMES),
        position=position,
        jersey_number=random.randint(1, 99),
        overall_rating=random.randint(60, 99),
        team_id=team_id,
        age=random.randint(21, 35),
        experience=random.randint(0, 15),
    )


from app.models.trait import Trait, TraitEffectType, TraitSource
from app.services.trait_service import TRAIT_CATALOG, TraitService


def seed_traits(db: Session):
    """Seed traits from the catalog into the database."""
    existing_traits = db.query(Trait).count()
    if existing_traits > 0:
        logger.info(f"Traits already seeded ({existing_traits} found). Skipping.")
        return

    logger.info("Seeding Traits from Catalog...")
    traits_to_add = []
    for key, definition in TRAIT_CATALOG.items():
        trait = Trait(
            name=definition.name,
            description=definition.description,
            # Map effect type if available
            effect_type=getattr(definition, "effect_type", TraitEffectType.PASSIVE)
            if hasattr(definition, "effect_type")
            else TraitEffectType.PASSIVE,
            effect_value=getattr(definition, "effect_value", 0.0)
            if hasattr(definition, "effect_value")
            else 0.0,
        )
        traits_to_add.append(trait)

    db.add_all(traits_to_add)
    db.commit()
    logger.info(f"Seeded {len(traits_to_add)} traits successfully.")


def seed_players(db: Session):
    existing_players = db.query(Player).count()
    if existing_players > 0:
        logger.info(f"Players already seeded ({existing_players} found). Skipping.")
        return

    logger.info("Seeding rosters for all teams...")
    teams = db.query(Team).all()

    all_players = []
    elite_qbs = []

    for team in teams:
        for pos, count in POSITIONS.items():
            for _ in range(count):
                player = generate_player(pos, team.id)
                all_players.append(player)

                # Track elite QBs for trait assignment
                if pos == "QB" and player.overall_rating >= 90:
                    elite_qbs.append(player)

    # Batch insert for performance
    db.add_all(all_players)
    db.commit()
    logger.info(f"Seeded {len(all_players)} players successfully.")

    # Assign Field General to elite QBs
    # We need to refresh/get trait ID first
    field_general = db.query(Trait).filter(Trait.name == "Field General").first()
    if field_general and elite_qbs:
        logger.info(f"Assigning Field General to {len(elite_qbs)} elite QBs...")
        for qb in elite_qbs:
            # Need to refresh qb to get ID if not eager loaded
            db.refresh(qb)
            TraitService.assign_trait(db, qb.id, field_general.id, TraitSource.DEVELOPMENT)
        logger.info("Trait assignment complete.")


def seed_scouts(db: Session):
    """Seed scouts for all 32 NFL teams from static data."""
    existing_scouts = db.query(Scout).count()
    if existing_scouts > 0:
        logger.info(f"Scouts already seeded ({existing_scouts} found). Skipping.")
        return

    logger.info("Seeding scouts for all 32 teams...")
    scouts_created = 0

    for scout_data in TEAM_SCOUTS:
        team = db.query(Team).filter(Team.abbreviation == scout_data.team_abbr).first()
        if not team:
            logger.warning(f"Team {scout_data.team_abbr} not found for scout. Skipping...")
            continue

        scout = Scout(
            name=scout_data.name,
            team_id=team.id,
            region=scout_data.region.value
            if hasattr(scout_data.region, "value")
            else scout_data.region,
            bias=scout_data.bias.value if hasattr(scout_data.bias, "value") else scout_data.bias,
            position_specialty=scout_data.specialty,
            evaluation_ability=scout_data.evaluation_ability,
            efficiency=scout_data.efficiency,
            reputation=scout_data.reputation,
        )
        db.add(scout)
        scouts_created += 1

    db.commit()
    logger.info(f"Seeded {scouts_created} scouts successfully.")


def seed_coaches(db: Session):
    """Seed 2025 NFL coaching staff for all 32 teams."""
    existing_coaches = db.query(Coach).count()
    if existing_coaches > 0:
        logger.info(f"Coaches already seeded ({existing_coaches} found). Skipping.")
        return

    logger.info("Seeding 2025 NFL coaching staff...")
    coaches_created = 0

    for team_abbr, staff_data in COACHES_DB.items():
        team = db.query(Team).filter(Team.abbreviation == team_abbr).first()
        if not team:
            logger.warning(f"Team {team_abbr} not found. Skipping...")
            continue

        roles = [
            (
                "Head Coach",
                staff_data.head_coach,
                staff_data.playbook_offense.value,
                staff_data.playbook_defense.value,
            ),
            (
                "Offensive Coordinator",
                staff_data.offensive_coordinator,
                staff_data.playbook_offense.value,
                None,
            ),
            (
                "Defensive Coordinator",
                staff_data.defensive_coordinator,
                None,
                staff_data.playbook_defense.value,
            ),
        ]

        philosophy_dict = {
            "run_pass_ratio": staff_data.philosophy.run_pass_ratio,
            "blitz_frequency": staff_data.philosophy.blitz_frequency,
            "aggressiveness": staff_data.philosophy.aggressiveness,
            "tempo": staff_data.philosophy.tempo,
        }

        for role, coach_data, off_scheme, def_scheme in roles:
            coach = Coach(
                first_name=coach_data.first_name,
                last_name=coach_data.last_name,
                role=role,
                team_id=team.id,
                playbook_offense=off_scheme,
                playbook_defense=def_scheme,
                philosophy=philosophy_dict if role == "Head Coach" else {},
                offense_rating=70 if role in ["Head Coach", "Offensive Coordinator"] else 50,
                defense_rating=70 if role in ["Head Coach", "Defensive Coordinator"] else 50,
                development_rating=65,
            )
            db.add(coach)
            coaches_created += 1

    db.commit()
    logger.info(f"Seeded {coaches_created} coaches successfully.")


def seed_players_from_nflverse(db: Session, season: int = 2024):
    """
    Seed players using real NFL data from nflreadpy.

    Args:
        db: Database session.
        season: NFL season to import (default 2024).
    """
    if not HAS_NFLVERSE:
        logger.warning("nflreadpy not available. Falling back to random seeding.")
        seed_players(db)
        return

    existing_players = db.query(Player).count()
    if existing_players > 0:
        logger.info(f"Players already seeded ({existing_players} found). Skipping NFL import.")
        return

    logger.info(f"Seeding players from NFL {season} rosters...")

    # Build team lookup
    teams = db.query(Team).all()
    team_lookup = {t.abbreviation: t.id for t in teams}

    # Fetch real data
    service = NflverseService(season=season)
    players_data = service.get_all_active_players()

    players_to_add = []
    for p_data in players_data:
        team_abbr = p_data.get("team_abbr", "")
        team_id = team_lookup.get(team_abbr)

        if not team_id:
            continue  # Skip players without a valid team

        # Generate ratings from real data
        ratings = generate_player_ratings(
            p_data, ngstats=p_data.get("ngs"), standard_stats=p_data.get("stats")
        )

        # Calculate overall rating with modifiers
        base_rating = sum(ratings.values()) / len(ratings) if ratings else 70
        accolades = PLAYER_ACCOMPLISHMENTS.get((p_data.get("first_name"), p_data.get("last_name")))
        final_overall = calculate_overall_rating_modifier(base_rating, p_data, accolades)

        # Helper function for safe int conversion
        def safe_int(value, default=0):
            if value is None:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        player = Player(
            first_name=p_data.get("first_name", "Unknown"),
            last_name=p_data.get("last_name", "Player"),
            position=p_data.get("position", "WR"),
            team_id=team_id,
            college=p_data.get("college"),
            height=safe_int(p_data.get("height"), 72),
            weight=safe_int(p_data.get("weight"), 200),
            age=safe_int(p_data.get("age"), 25),
            experience=safe_int(p_data.get("experience"), 0),
            jersey_number=safe_int(p_data.get("jersey_number"), 0),
            # Contracts (Real Data)
            contract_years=safe_int(p_data.get("contract_years"), 1),
            contract_salary=safe_int(p_data.get("contract_salary"), 1000000),
            overall_rating=final_overall,
            # Apply generated ratings
            speed=ratings.get("speed", 50),
            acceleration=ratings.get("acceleration", 50),
            strength=ratings.get("strength", 50),
            agility=ratings.get("agility", 50),
            awareness=ratings.get("awareness", 50),
            throw_power=ratings.get("throw_power", 50),
            throw_accuracy_short=ratings.get("throw_accuracy_short", 50),
            throw_accuracy_mid=ratings.get("throw_accuracy_mid", 50),
            throw_accuracy_deep=ratings.get("throw_accuracy_deep", 50),
            catching=ratings.get("catching", 50),
            route_running=ratings.get("route_running", 50),
            pass_block=ratings.get("pass_block", 50),
            run_block=ratings.get("run_block", 50),
            tackle=ratings.get("tackle", 50),
            hit_power=ratings.get("hit_power", 50),
            block_shed=ratings.get("block_shed", 50),
            man_coverage=ratings.get("man_coverage", 50),
            zone_coverage=ratings.get("zone_coverage", 50),
            pass_rush_power=ratings.get("pass_rush_power", 50),
            pass_rush_finesse=ratings.get("pass_rush_finesse", 50),
            play_recognition=ratings.get("play_recognition", 50),
            pocket_presence=ratings.get("pocket_presence", 50),
            quick_release=ratings.get("quick_release", 50),
        )
        players_to_add.append(player)

    db.add_all(players_to_add)
    db.commit()
    logger.info(f"Seeded {len(players_to_add)} real NFL players successfully.")


# =============================================================================
# 2025 FREE AGENT SEEDING
# =============================================================================
# AUTO-UPDATE NOTES:
# This section seeds verified 2025 free agent signings with accurate ratings.
# To keep this simulation SOTA and EA Sports-caliber:
# 1. Update free_agents_2025.py after major free agency signings
# 2. Run data_sync_service.py to check for new nflverse data
# 3. After August 26, 2025: Use nflreadpy.load_rosters(2025) for full rosters
# 4. Monitor: PFF, ESPN, NFL.com for breaking transactions


def seed_free_agents_2025(db: Session):
    """
    Seed 2025 free agent signings with verified ratings.

    This provides accurate player data for the 2025 season before
    the official nflverse roster data is available.
    """
    from app.data.free_agents_2025 import FREE_AGENT_SIGNINGS_2025

    # Get team lookup
    teams = db.query(Team).all()
    team_lookup = {t.abbreviation: t.id for t in teams}

    players_added = 0
    players_updated = 0

    for fa in FREE_AGENT_SIGNINGS_2025:
        team_id = team_lookup.get(fa.new_team)
        if not team_id:
            logger.warning(f"Unknown team {fa.new_team} for {fa.first_name} {fa.last_name}")
            continue

        # Check if player exists
        existing = (
            db.query(Player)
            .filter(Player.first_name == fa.first_name, Player.last_name == fa.last_name)
            .first()
        )

        if existing:
            # Update existing player with new team and ratings
            existing.team_id = team_id
            existing.contract_years = fa.contract_years
            existing.contract_salary = fa.apy
            existing.overall_rating = fa.overall_rating
            if fa.speed:
                existing.speed = fa.speed
            if fa.strength:
                existing.strength = fa.strength
            if fa.awareness:
                existing.awareness = fa.awareness
            players_updated += 1
        else:
            # Create new player with position-based defaults
            # Height in inches, weight in lbs (approximate by position)
            position_defaults = {
                "QB": (75, 220),
                "RB": (70, 210),
                "WR": (72, 195),
                "TE": (77, 250),
                "OT": (78, 315),
                "OG": (76, 310),
                "C": (75, 305),
                "DE": (76, 270),
                "DT": (75, 310),
                "EDGE": (76, 255),
                "LB": (74, 240),
                "CB": (71, 190),
                "S": (72, 205),
                "K": (72, 200),
                "P": (74, 210),
            }
            default_h, default_w = position_defaults.get(fa.position, (74, 225))

            player = Player(
                first_name=fa.first_name,
                last_name=fa.last_name,
                position=fa.position,
                team_id=team_id,
                age=fa.age,
                height=default_h,
                weight=default_w,
                overall_rating=fa.overall_rating,
                contract_years=fa.contract_years,
                contract_salary=fa.apy,
                speed=fa.speed or 75,
                strength=fa.strength or 75,
                awareness=fa.awareness or 75,
            )
            db.add(player)
            players_added += 1

    db.commit()
    logger.info(f"2025 Free Agents: Added {players_added}, Updated {players_updated}")


def main():
    """
    Main seeding function with multi-mode support.

    SEED_MODE options:
    - RANDOM: Generate random players (default)
    - REAL_2024: Use nflreadpy 2024 roster data
    - REAL_2025: Use 2024 base + 2025 free agent updates

    AUTO-UPDATE STRATEGY:
    ---------------------
    To maintain SOTA simulation quality:
    1. Weekly: Check nflverse for roster/stats updates
    2. Daily (during FA): Sync contract and transaction data
    3. After Draft: Import rookie data from load_draft_picks()
    4. September: Switch to load_rosters(2025) when available

    Run data_sync_service.py for automated recommendations.
    """
    db = SessionLocal()
    seed_mode = os.getenv("SEED_MODE", "RANDOM").upper()

    try:
        seed_teams(db)
        seed_traits(db)

        if seed_mode == "REAL_2025" and HAS_NFLVERSE:
            # 2025 Mode: Base 2024 rosters + 2025 free agent updates
            logger.info("SEED_MODE=REAL_2025: Using 2024 base + 2025 free agents...")
            seed_players_from_nflverse(db, season=2024)
            seed_free_agents_2025(db)

        elif seed_mode == "REAL_2024" and HAS_NFLVERSE:
            logger.info("SEED_MODE=REAL_2024: Using real NFL data...")
            seed_players_from_nflverse(db, season=2024)
        else:
            logger.info("SEED_MODE=RANDOM: Using generated players...")
            seed_players(db)

        seed_coaches(db)
        seed_scouts(db)

        # Log update recommendations
        logger.info("=" * 50)
        logger.info("DATA UPDATE RECOMMENDATIONS:")
        logger.info("  1. Run: python -m app.services.data_sync_service")
        logger.info("  2. Check: free_agents_2025.py for new signings")
        logger.info("  3. After Aug 26: Use SEED_MODE=REAL_2025 with full rosters")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
