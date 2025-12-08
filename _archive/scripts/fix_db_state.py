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
from app.models.game import Game
from app.models.stats import PlayerGameStats
from app.models.playoff import PlayoffMatchup
from app.models.draft import DraftPick

def fix_state():
    db = SessionLocal()
    try:
        print("Cleaning up seasons...")
        # Get all seasons
        seasons = db.query(Season).all()
        
        target_year = 2026
        target_season = None
        
        for s in seasons:
            if s.year == target_year:
                target_season = s
            else:
                print(f"Deleting season {s.year} (ID: {s.id})")
                
                # Get games
                games = db.query(Game).filter(Game.season_id == s.id).all()
                game_ids = [g.id for g in games]
                
                if game_ids:
                    # Delete stats
                    print(f"  Deleting stats for {len(game_ids)} games...")
                    db.query(PlayerGameStats).filter(PlayerGameStats.game_id.in_(game_ids)).delete(synchronize_session=False)
                
                # Delete playoff matchups
                print("  Deleting playoff matchups...")
                db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == s.id).delete()
                
                # Delete draft picks
                print("  Deleting draft picks...")
                db.query(DraftPick).filter(DraftPick.season_id == s.id).delete()
                
                # Delete games
                print("  Deleting games...")
                db.query(Game).filter(Game.season_id == s.id).delete()
                
                # Delete season
                db.delete(s)
        
        if target_season:
            print(f"Keeping season {target_season.year} (ID: {target_season.id})")
            target_season.is_active = True
        else:
            print(f"Target season {target_year} not found. You might need to create it via UI after cleanup.")
            
        db.commit()
        print("Cleanup complete.")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_state()
