import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Add backend directory to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.core.database import SessionLocal
from app.models.team import Team
from app.data.teams import TEAM_DB

def seed_teams():
    db: Session = SessionLocal()
    try:
        print("Seeding teams...")
        for team_id, data in TEAM_DB.items():
            # Check if team exists
            team = db.query(Team).filter(Team.abbreviation == data.abbreviation).first()
            
            logo_url = f"/logos/{data.abbreviation}.png"
            
            if not team:
                print(f"Creating {data.city} {data.mascot}...")
                team = Team(
                    name=data.mascot,
                    city=data.city,
                    abbreviation=data.abbreviation,
                    conference=data.conference,
                    division=data.division,
                    primary_color=data.colors.primary_hex,
                    secondary_color=data.colors.secondary_hex,
                    logo_url=logo_url,
                    # Defaults
                    wins=0, losses=0, ties=0,
                    prestige=75,
                    fan_support=75,
                    salary_cap_space=20000000
                )
                db.add(team)
            else:
                print(f"Updating {data.abbreviation}...")
                team.logo_url = logo_url
                team.primary_color = data.colors.primary_hex
                team.secondary_color = data.colors.secondary_hex
                # Update other fields if needed
            
        db.commit()
        print("Teams seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding teams: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_teams()
