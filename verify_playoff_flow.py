import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.base import Base
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.game import Game
from app.services.schedule_generator import ScheduleGenerator
from app.services.week_simulator import WeekSimulator
from app.services.playoff_service import PlayoffService
from app.services.standings_calculator import StandingsCalculator

# Setup DB
DB_URL = "sqlite:///./verify_playoff.db"
if os.path.exists("verify_playoff.db"):
    os.remove("verify_playoff.db")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def create_teams(db):
    print("Creating teams...")
    teams = []
    conferences = ["NFC", "AFC"]
    divisions = ["North", "South", "East", "West"]
    
    count = 0
    for conf in conferences:
        for div in divisions:
            # Create 4 teams per division = 32 teams
            for i in range(4):
                count += 1
                team = Team(
                    name=f"Team {count}",
                    city=f"City {count}",
                    abbreviation=f"T{count}",
                    conference=conf,
                    division=div
                )
                db.add(team)
                teams.append(team)
    db.commit()
    print(f"Created {len(teams)} teams.")
    return teams

def run_verify():
    db = SessionLocal()
    try:
        # 1. Setup
        create_teams(db)
        
        # 2. Create Season
        print("\nInitializing Season...")
        season = Season(
            year=2025,
            current_week=1,
            is_active=True,
            status=SeasonStatus.REGULAR_SEASON,
            total_weeks=18,
            playoff_weeks=4
        )
        db.add(season)
        db.commit()
        
        # 3. Generate Schedule
        print("Generating Schedule...")
        generator = ScheduleGenerator(db)
        teams = db.query(Team).all()
        generator.generate_schedule(season.id, teams)
        
        # 4. Simulate Regular Season
        print("Simulating Regular Season...")
        simulator = WeekSimulator(db)
        
        for week in range(1, 19):
            print(f"Simulating Week {week}...", end="\r")
            simulator.simulate_week(season.id, week, play_count=10, use_fast_sim=True)
            season.current_week = week + 1
            db.commit()
        print("\nRegular Season Complete.")
        
        # 5. Advance to Playoffs
        print("\nAdvancing to Playoffs...")
        season.status = SeasonStatus.POST_SEASON
        season.current_week = 1
        db.commit()
        
        playoff_service = PlayoffService(db)
        playoff_service.generate_playoffs(season.id)
        
        bracket = playoff_service.get_bracket(season.id)
        print(f"Generated Bracket with {len(bracket)} matchups.")
        
        # 6. Simulate Playoffs
        rounds = ["Wild Card", "Divisional", "Conference", "Super Bowl"]
        
        for r_name in rounds:
            print(f"\nSimulating {r_name} Round...")
            # Simulate games in this round
            current_bracket = playoff_service.get_bracket(season.id)
            
            # Find games to simulate (those with 2 teams but no winner)
            games_to_sim = []
            for m in current_bracket:
                if m.home_team_id and m.away_team_id and not m.winner_id:
                    game = db.query(Game).filter(Game.id == m.game_id).first()
                    if game and not game.is_played:
                        games_to_sim.append(game)
            
            print(f"  Found {len(games_to_sim)} games to simulate.")
            
            for game in games_to_sim:
                # Simple sim: High score wins
                import random
                game.home_score = random.randint(10, 40)
                game.away_score = random.randint(10, 40)
                while game.home_score == game.away_score:
                    game.home_score += 3
                
                game.is_played = True
                db.commit()
                print(f"    Game {game.id}: Home {game.home_score} - Away {game.away_score}")
            
            # Advance Round
            try:
                playoff_service.advance_round(season.id)
                print(f"  Advanced to next round.")
            except ValueError as e:
                if "Season is over" in str(e):
                    print("  Super Bowl Complete! Season Over.")
                    break
                else:
                    print(f"  Error advancing: {e}")
        
        # 7. Verify Winner
        champion = playoff_service.get_champion(season.id)
        if champion:
            print(f"\n🏆 Super Bowl Champion: {champion.name} ({champion.city})")
        else:
            print("\n⚠️ No Champion Found!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        engine.dispose()
        if os.path.exists("verify_playoff.db"):
            try:
                os.remove("verify_playoff.db")
            except PermissionError:
                print("Warning: Could not remove verify_playoff.db (file locked)")

if __name__ == "__main__":
    run_verify()
