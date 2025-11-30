import sys
import os
import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.base import Base
from app.models.player import Player
from app.models.team import Team
from app.models.game import Game

# Use the real database
DATABASE_URL = "sqlite:///./backend/nfl_sim.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def time_query(name, query_func):
    start = time.time()
    result = query_func()
    end = time.time()
    print(f"{name}: {end - start:.4f}s")
    return result

def verify_performance():
    print("Starting Manual Query Performance Verification...")
    print(f"Database: {DATABASE_URL}")
    
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print(f"Tables: {inspector.get_table_names()}")
    
    db = SessionLocal()
    try:
        # 1. Fetch all players
        def get_all_players():
            stmt = select(Player)
            return db.execute(stmt).scalars().all()
            
        players = time_query("Fetch all players", get_all_players)
        print(f"  Count: {len(players)}")
        
        # 2. Fetch all teams
        def get_all_teams():
            stmt = select(Team)
            return db.execute(stmt).scalars().all()
            
        teams = time_query("Fetch all teams", get_all_teams)
        print(f"  Count: {len(teams)}")
        
        if teams:
            first_team_id = teams[0].id
            # 3. Fetch roster for a team
            def get_roster():
                stmt = select(Player).where(Player.team_id == first_team_id)
                return db.execute(stmt).scalars().all()
                
            roster = time_query(f"Fetch roster for team {first_team_id}", get_roster)
            print(f"  Count: {len(roster)}")
            
        # 4. Fetch games
        def get_games():
            stmt = select(Game).limit(100)
            return db.execute(stmt).scalars().all()
            
        games = time_query("Fetch 100 games", get_games)
        print(f"  Count: {len(games)}")

    except Exception as e:
        print(f"Error during performance verification: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_performance()
