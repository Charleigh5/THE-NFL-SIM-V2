import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import asyncio

sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.base import Base
from app.models.team import Team
from app.models.player import Player
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator

# Setup DB
DB_URL = "sqlite:///./verify_context.db"
if os.path.exists("verify_context.db"):
    os.remove("verify_context.db")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def create_data(db):
    print("Creating Teams and Players...")
    teams = []
    for i in range(1, 3): # 2 Teams
        team = Team(name=f"Team {i}", city=f"City {i}", abbreviation=f"T{i}", conference="AFC", division="North")
        db.add(team)
        teams.append(team)
    db.commit()
    
    # Create full roster for depth chart testing
    positions = ["QB", "RB", "WR", "TE", "OT", "OG", "C", "DE", "DT", "LB", "CB", "S", "K", "P"]
    
    for team in teams:
        for pos in positions:
            # Create 3 of each position to ensure depth
            for i in range(3):
                player = Player(
                    first_name=f"{pos}", 
                    last_name=f"{team.abbreviation}-{i}", 
                    position=pos,
                    team_id=team.id,
                    age=25,
                    overall_rating=70 + i # Vary ratings
                )
                db.add(player)
    db.commit()
    return teams

async def run_verify():
    db = SessionLocal()
    try:
        teams = create_data(db)
        
        print("\nInitializing Orchestrator...")
        orchestrator = SimulationOrchestrator()
        
        # We need to override the SessionLocal in orchestrator to use our test DB
        # But SimulationOrchestrator creates its own SessionLocal.
        # We can monkeypatch app.core.database.SessionLocal or just let it use the main DB if config allows.
        # Ideally we inject dependency, but for now let's just set the class attribute if possible, 
        # or better: update config to point to our test DB?
        # Since we imported SessionLocal from app.core.database in the orchestrator file,
        # we can patch it there.
        
        import app.orchestrator.simulation_orchestrator as orch_module
        orch_module.SessionLocal = SessionLocal
        
        print("Starting Game Session...")
        orchestrator.start_new_game_session(teams[0].id, teams[1].id)
        
        # Verify MatchContext
        if orchestrator.match_context:
            print("✅ MatchContext hydrated successfully.")
            print(f"   Home Roster: {len(orchestrator.match_context.home_roster)}")
            print(f"   Away Roster: {len(orchestrator.match_context.away_roster)}")
            
            # Verify Starters
            home_starters = orchestrator.match_context.get_starters("home")
            print(f"✅ Home Starters loaded: {len(home_starters)} positions filled.")
            if "QB" in home_starters:
                qb = home_starters["QB"]
                print(f"   QB1: {qb.first_name} {qb.last_name} (OVR: {qb.overall_rating})")
            else:
                print("❌ QB missing from starters!")
        else:
            print("❌ MatchContext is NONE!")
            
        # Run a play
        print("\nRunning 1 Play...")
        result = await orchestrator._execute_single_play()
        print(f"✅ Play Executed: {result.description}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        engine.dispose()
        if os.path.exists("verify_context.db"):
            try:
                os.remove("verify_context.db")
            except:
                pass

if __name__ == "__main__":
    asyncio.run(run_verify())
