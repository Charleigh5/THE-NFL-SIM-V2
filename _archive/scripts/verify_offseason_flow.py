import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.base import Base
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.services.offseason_service import OffseasonService

DB_URL = "sqlite:///./verify_offseason.db"
if os.path.exists("verify_offseason.db"):
    os.remove("verify_offseason.db")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def create_data(db):
    print("Creating Data...")
    # Teams
    teams = []
    for i in range(1, 5): # 4 Teams
        team = Team(name=f"Team {i}", city=f"City {i}", abbreviation=f"T{i}", conference="AFC", division="North")
        db.add(team)
        teams.append(team)
    db.commit()
    
    # Players with Contracts
    import random
    for team in teams:
        # 5 players per team
        for i in range(5):
            player = Player(
                first_name=f"Player", 
                last_name=f"{team.abbreviation}-{i}", 
                position="QB", 
                team_id=team.id,
                age=25,
                experience=3,
                overall_rating=80,
                contract_years=1 if i < 2 else 3,
                contract_salary=1000000
            )
            db.add(player)
    db.commit()
    return teams

def create_dummy_history(db, season_id, teams):
    print("Creating Dummy History (Games)...")
    # Create some games so standings work
    # Team 1 beats Team 2
    g1 = Game(season_id=season_id, week=1, home_team_id=teams[0].id, away_team_id=teams[1].id, 
              home_score=21, away_score=10, is_played=True)
    # Team 3 beats Team 4
    g2 = Game(season_id=season_id, week=1, home_team_id=teams[2].id, away_team_id=teams[3].id, 
              home_score=21, away_score=10, is_played=True)
    db.add(g1)
    db.add(g2)
    db.commit()

def run_verify():
    db = SessionLocal()
    try:
        # Create Season first so we have ID
        season = Season(
            year=2025,
            current_week=22, # After Super Bowl
            is_active=True,
            status=SeasonStatus.OFF_SEASON,
            total_weeks=18
        )
        db.add(season)
        db.commit()

        teams = create_data(db)
        create_dummy_history(db, season.id, teams)
        
        service = OffseasonService(db)
        
        # 1. Start Offseason
        print("\n1. Starting Offseason (Contracts & Retirements)...")
        res = service.start_offseason(season.id)
        print(f"   Result: {res}")
        
        # Check free agents
        fas = db.query(Player).filter(Player.team_id == None).count()
        print(f"   Free Agents created: {fas} (Expected ~8)")
        
        # 2. Progression
        print("\n2. Simulating Progression...")
        prog_results = service.simulate_player_progression(season.id)
        print(f"   Processed {len(prog_results)} players.")
        if prog_results:
            p = prog_results[0]
            print(f"   Sample: {p.name} {p.old_rating}->{p.new_rating} ({p.change})")
            
        # 3. Draft Order is auto-generated in start_offseason usually, let's check
        # Actually start_offseason calls generate_draft_order
        from app.models.draft import DraftPick
        picks = db.query(DraftPick).filter(DraftPick.season_id == season.id).count()
        print(f"\n3. Draft Picks Generated: {picks} (Expected 4 teams * 7 rounds = 28)")
        
        # 4. Simulate Draft
        print("\n4. Simulating Draft...")
        draft_results = service.simulate_draft(season.id)
        print(f"   Drafted {len(draft_results)} players.")
        
        # 5. Free Agency
        print("\n5. Simulating Free Agency...")
        fa_results = service.simulate_free_agency(season.id)
        print(f"   Signed {fa_results['signed_count']} players.")
        
        print("\n✅ Offseason Verification Complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        engine.dispose()
        if os.path.exists("verify_offseason.db"):
            try:
                os.remove("verify_offseason.db")
            except:
                pass

if __name__ == "__main__":
    run_verify()
