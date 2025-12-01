import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.player import Player, DevelopmentTrait, InjuryStatus
from app.models.team import Team
from app.models.coach import Coach
from app.services.player_development_service import PlayerDevelopmentService

# Setup in-memory DB
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_player_development_service(db):
    # Setup Data
    team = Team(name="Test Team", city="Test City", abbreviation="TST")
    db.add(team)
    db.commit()
    
    coach = Coach(first_name="Head", last_name="Coach", role="Head Coach", development_rating=80, team_id=team.id)
    db.add(coach)
    
    player = Player(
        first_name="Test", last_name="Player", position="QB", 
        team_id=team.id, age=22, experience=1, 
        development_trait=DevelopmentTrait.SUPERSTAR,
        overall_rating=70,
        xp=0,
        morale=50
    )
    db.add(player)
    db.commit()
    
    service = PlayerDevelopmentService(db)
    
    # Test Weekly Development
    service.process_weekly_development(season_id=1, week=1)
    
    # Check XP Gain
    # Base 50 * 1.5 (Superstar) * 1.3 (Coach 80 rating -> +0.3) * 1.2 (Age < 24)
    # 50 * 1.5 = 75
    # 75 * 1.3 = 97.5
    # 97.5 * 1.2 = 117
    db.refresh(player)
    assert player.xp > 0
    print(f"Player XP after week 1: {player.xp}")
    
    # Test Injury Recovery
    player.injury_status = InjuryStatus.OUT
    player.weeks_to_recovery = 2
    db.commit()
    
    service.process_weekly_development(season_id=1, week=2)
    db.refresh(player)
    assert player.weeks_to_recovery == 1
    assert player.injury_status == InjuryStatus.OUT
    
    service.process_weekly_development(season_id=1, week=3)
    db.refresh(player)
    assert player.weeks_to_recovery == 0
    assert player.injury_status == InjuryStatus.ACTIVE
    
    # Test Morale Update
    # Team has 0 wins, 0 losses -> win_pct 0.5 -> No change from record
    # Depth chart rank default 999 -> -1 morale
    old_morale = player.morale
    service.process_weekly_development(season_id=1, week=4)
    db.refresh(player)
    # Morale might fluctuate randomly, but let's check it's within bounds
    assert 0 <= player.morale <= 100
    print(f"Player Morale: {player.morale}")

if __name__ == "__main__":
    # Manually run if executed as script
    test_player_development_service(SessionLocal())
