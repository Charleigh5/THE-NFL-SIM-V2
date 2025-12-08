import sys
import os

# Add backend directory to path
backend_dir = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_dir)

# Set DATABASE_URL to point to the existing db in backend
db_path = os.path.join(backend_dir, "nfl_sim.db")
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from app.core.database import SessionLocal
from app.models.season import Season
from app.models.team import Team

def check_state():
    db = SessionLocal()
    try:
        print("--- SEASONS ---")
        seasons = db.query(Season).all()
        for s in seasons:
            print(f"ID: {s.id}, Year: {s.year}, Active: {s.is_active}, Status: {s.status}, Current Week: {s.current_week}")
        
        print("\n--- TEAMS ---")
        teams = db.query(Team).all()
        print(f"Total Teams: {len(teams)}")
        for t in teams[:5]:
            print(f"ID: {t.id}, Name: {t.name}, Conf: {t.conference}, Div: {t.division}")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_state()
