import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.team import Team
from app.models.player import Player
import random

# Configure logging
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

def seed_players(db: Session):
    existing_players = db.query(Player).count()
    if existing_players > 0:
        logger.info(f"Players already seeded ({existing_players} found). Skipping.")
        return

    logger.info("Seeding rosters for all teams...")
    teams = db.query(Team).all()
    
    all_players = []
    for team in teams:
        for pos, count in POSITIONS.items():
            for _ in range(count):
                player = generate_player(pos, team.id)
                all_players.append(player)
    
    # Batch insert for performance
    db.add_all(all_players)
    db.commit()
    logger.info(f"Seeded {len(all_players)} players successfully.")

def main():
    db = SessionLocal()
    try:
        seed_teams(db)
        seed_players(db)
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
