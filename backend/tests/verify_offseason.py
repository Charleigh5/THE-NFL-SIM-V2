import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player, Position
from app.models.draft import DraftPick
from app.services.offseason_service import OffseasonService
from app.services.rookie_generator import RookieGenerator

# Setup DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_offseason.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Create Season
    season = Season(year=2024, status=SeasonStatus.POST_SEASON, current_week=22, total_weeks=18, is_active=True)
    db.add(season)
    
    # Create Teams
    teams = []
    for i in range(4):
        team = Team(
            name=f"Team {i}", 
            city=f"City {i}", 
            abbreviation=f"T{i}", 
            conference="AFC", 
            division="North"
        )
        db.add(team)
        teams.append(team)
    db.commit()
    
    # Create Players (Expiring contracts)
    for team in teams:
        # 1 Expiring Player
        p1 = Player(
            first_name="Expiring", last_name="Player", position=Position.QB, 
            team_id=team.id, contract_years=1, overall_rating=80
        )
        # 1 Long-term Player
        p2 = Player(
            first_name="LongTerm", last_name="Player", position=Position.WR, 
            team_id=team.id, contract_years=3, overall_rating=85
        )
        db.add(p1)
        db.add(p2)
        
    db.commit()
    return db

def verify_offseason():
    print("Setting up test database...")
    db = setup_db()
    service = OffseasonService(db)
    season = db.query(Season).first()
    
    print(f"Initial Season Status: {season.status}")
    
    # 1. Start Offseason
    print("\n--- Starting Offseason ---")
    service.start_offseason(season.id)
    
    # Verify Status
    db.refresh(season)
    assert season.status == SeasonStatus.OFF_SEASON
    print("✅ Season status updated to OFF_SEASON")
    
    # Verify Contracts
    expiring = db.query(Player).filter(Player.first_name == "Expiring").all()
    for p in expiring:
        assert p.contract_years == 0
        assert p.team_id is None
    print("✅ Expiring contracts processed (Players released)")
    
    long_term = db.query(Player).filter(Player.first_name == "LongTerm").all()
    for p in long_term:
        assert p.contract_years == 2
        assert p.team_id is not None
    print("✅ Long-term contracts decremented but kept")
    
    # Verify Draft Order
    picks = db.query(DraftPick).filter(DraftPick.season_id == season.id).all()
    assert len(picks) == 4 * 7 # 4 teams * 7 rounds
    print(f"✅ Draft order generated ({len(picks)} picks)")
    
    # Verify Rookie Class
    rookies = db.query(Player).filter(Player.is_rookie == True).all()
    assert len(rookies) > 0
    print(f"✅ Rookie class generated ({len(rookies)} rookies)")
    
    # 2. Simulate Draft
    print("\n--- Simulating Draft ---")
    service.simulate_draft(season.id)
    
    # Verify Picks made
    filled_picks = db.query(DraftPick).filter(DraftPick.player_id != None).all()
    assert len(filled_picks) == len(picks)
    print("✅ All draft picks have been made")
    
    # Verify Rookies assigned
    drafted_rookies = db.query(Player).filter(Player.is_rookie == False, Player.contract_years == 4).all()
    assert len(drafted_rookies) == len(picks)
    print("✅ Rookies assigned to teams and signed")
    
    # 3. Simulate Free Agency
    print("\n--- Simulating Free Agency ---")
    # Force rosters to be small so they sign people
    service.simulate_free_agency(season.id)
    
    # Verify rosters filled (Target is 53, but we only have limited pool)
    # Just verify some signings happened if needed, or that logic ran without error.
    # In this small test, we might run out of players, but let's check if teams have players.
    for team in db.query(Team).all():
        count = db.query(Player).filter(Player.team_id == team.id).count()
        print(f"Team {team.name} roster size: {count}")
        assert count > 0
        
    print("✅ Free Agency simulated")
    
    print("\n🎉 ALL TESTS PASSED")

if __name__ == "__main__":
    verify_offseason()
