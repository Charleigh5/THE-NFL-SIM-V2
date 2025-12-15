import logging
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.team import Team
from app.models.player import Player
from app.models.coach import Coach
from app.data.coaches import COACHES_DB
import random

# NFL Data Integration (optional)
try:
    from app.services.nflverse_service import NflverseService
    from app.services.ratings_generator import generate_player_ratings
    HAS_NFLVERSE = True
except ImportError:
    HAS_NFLVERSE = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NFL_TEAMS = [
    {"city": "Arizona", "name": "Cardinals", "abbreviation": "ARI", "conference": "NFC", "division": "West"},
    {"city": "Atlanta", "name": "Falcons", "abbreviation": "ATL", "conference": "NFC", "division": "South"},
    {"city": "Baltimore", "name": "Ravens", "abbreviation": "BAL", "conference": "AFC", "division": "North"},
    {"city": "Buffalo", "name": "Bills", "abbreviation": "BUF", "conference": "AFC", "division": "East"},
    {"city": "Carolina", "name": "Panthers", "abbreviation": "CAR", "conference": "NFC", "division": "South"},
    {"city": "Chicago", "name": "Bears", "abbreviation": "CHI", "conference": "NFC", "division": "North"},
    {"city": "Cincinnati", "name": "Bengals", "abbreviation": "CIN", "conference": "AFC", "division": "North"},
    {"city": "Cleveland", "name": "Browns", "abbreviation": "CLE", "conference": "AFC", "division": "North"},
    {"city": "Dallas", "name": "Cowboys", "abbreviation": "DAL", "conference": "NFC", "division": "East"},
    {"city": "Denver", "name": "Broncos", "abbreviation": "DEN", "conference": "AFC", "division": "West"},
    {"city": "Detroit", "name": "Lions", "abbreviation": "DET", "conference": "NFC", "division": "North"},
    {"city": "Green Bay", "name": "Packers", "abbreviation": "GB", "conference": "NFC", "division": "North"},
    {"city": "Houston", "name": "Texans", "abbreviation": "HOU", "conference": "AFC", "division": "South"},
    {"city": "Indianapolis", "name": "Colts", "abbreviation": "IND", "conference": "AFC", "division": "South"},
    {"city": "Jacksonville", "name": "Jaguars", "abbreviation": "JAX", "conference": "AFC", "division": "South"},
    {"city": "Kansas City", "name": "Chiefs", "abbreviation": "KC", "conference": "AFC", "division": "West"},
    {"city": "Las Vegas", "name": "Raiders", "abbreviation": "LV", "conference": "AFC", "division": "West"},
    {"city": "Los Angeles", "name": "Chargers", "abbreviation": "LAC", "conference": "AFC", "division": "West"},
    {"city": "Los Angeles", "name": "Rams", "abbreviation": "LAR", "conference": "NFC", "division": "West"},
    {"city": "Miami", "name": "Dolphins", "abbreviation": "MIA", "conference": "AFC", "division": "East"},
    {"city": "Minnesota", "name": "Vikings", "abbreviation": "MIN", "conference": "NFC", "division": "North"},
    {"city": "New England", "name": "Patriots", "abbreviation": "NE", "conference": "AFC", "division": "East"},
    {"city": "New Orleans", "name": "Saints", "abbreviation": "NO", "conference": "NFC", "division": "South"},
    {"city": "New York", "name": "Giants", "abbreviation": "NYG", "conference": "NFC", "division": "East"},
    {"city": "New York", "name": "Jets", "abbreviation": "NYJ", "conference": "AFC", "division": "East"},
    {"city": "Philadelphia", "name": "Eagles", "abbreviation": "PHI", "conference": "NFC", "division": "East"},
    {"city": "Pittsburgh", "name": "Steelers", "abbreviation": "PIT", "conference": "AFC", "division": "North"},
    {"city": "San Francisco", "name": "49ers", "abbreviation": "SF", "conference": "NFC", "division": "West"},
    {"city": "Seattle", "name": "Seahawks", "abbreviation": "SEA", "conference": "NFC", "division": "West"},
    {"city": "Tampa Bay", "name": "Buccaneers", "abbreviation": "TB", "conference": "NFC", "division": "South"},
    {"city": "Tennessee", "name": "Titans", "abbreviation": "TEN", "conference": "AFC", "division": "South"},
    {"city": "Washington", "name": "Commanders", "abbreviation": "WAS", "conference": "NFC", "division": "East"},
]

POSITIONS = {
    "QB": 3, "RB": 4, "WR": 6, "TE": 3, "OL": 9,
    "DL": 8, "LB": 7, "CB": 6, "S": 4, "K": 1, "P": 1
}

FIRST_NAMES = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Chris", "Dan", "Pat", "Steve", "Jim", "Tom", "Tim", "Rob", "Mike", "Bill", "Dave", "Rich", "Joe", "Chuck"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

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
            losses=0
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
        experience=random.randint(0, 15)
    )

from app.services.trait_service import TraitService, TRAIT_CATALOG
from app.models.trait import Trait, TraitSource

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
            tier=definition.tier,
            icon_url=f"/assets/traits/{key}.png" # Placeholder
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
            ("Head Coach", staff_data.head_coach, staff_data.playbook_offense.value, staff_data.playbook_defense.value),
            ("Offensive Coordinator", staff_data.offensive_coordinator, staff_data.playbook_offense.value, None),
            ("Defensive Coordinator", staff_data.defensive_coordinator, None, staff_data.playbook_defense.value),
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
        ratings = generate_player_ratings(p_data)

        player = Player(
            first_name=p_data.get("first_name", "Unknown"),
            last_name=p_data.get("last_name", "Player"),
            position=p_data.get("position", "WR"),
            team_id=team_id,
            college=p_data.get("college"),
            height=p_data.get("height", 72),
            weight=p_data.get("weight", 200),
            age=p_data.get("age", 25),
            experience=p_data.get("experience", 0),
            jersey_number=p_data.get("jersey_number", 0) or 0,
            overall_rating=ratings.get("overall_rating", 70),
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


def main():
    db = SessionLocal()
    seed_mode = os.getenv("SEED_MODE", "RANDOM").upper()

    try:
        seed_teams(db)
        seed_traits(db)

        if seed_mode == "REAL_2024" and HAS_NFLVERSE:
            logger.info("SEED_MODE=REAL_2024: Using real NFL data...")
            seed_players_from_nflverse(db, season=2024)
        else:
            logger.info("SEED_MODE=RANDOM: Using generated players...")
            seed_players(db)

        seed_coaches(db)
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

