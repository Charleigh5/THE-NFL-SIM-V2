import os
import sys
import shutil
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.base import Base
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player
from app.services.offseason_service import OffseasonService

# Configuration
REAL_DB_PATH = "backend/nfl_sim.db"
TEST_DB_PATH = "verify_offseason_real.db"
DB_URL = f"sqlite:///{TEST_DB_PATH}"

def setup_db_clone():
    """Clone the real database to a test file to avoid corrupting production data."""
    if not os.path.exists(REAL_DB_PATH):
        print(f"❌ Real database not found at {REAL_DB_PATH}. Cannot verify against real data.")
        return False
    
    print(f"📦 Cloning {REAL_DB_PATH} to {TEST_DB_PATH}...")
    shutil.copy2(REAL_DB_PATH, TEST_DB_PATH)
    return True

def run_verify():
    if not setup_db_clone():
        return

    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        print("\n🔍 Verifying Offseason Flow against REAL data clone...")
        
        # 1. Check for Active Season
        stmt = select(Season).where(Season.is_active == True)
        season = db.execute(stmt).scalar_one_or_none()
        
        if not season:
            print("⚠️ No active season found. Cannot verify offseason flow.")
            return

        print(f"   Active Season: {season.year} (Week {season.current_week}, Status: {season.status})")

        # 2. Check Teams
        team_count = db.query(Team).count()
        print(f"   Teams Found: {team_count}")
        if team_count < 32:
             print("⚠️ Warning: Less than 32 teams found.")

        service = OffseasonService(db)

        # 3. Simulate Offseason Steps (dry run style)
        if season.status == SeasonStatus.OFF_SEASON:
            print("\n   Season is already in OFF_SEASON. Running simulation steps...")
            
            # Progressions
            print("   ▶️ Simulating Progression...")
            prog_results = service.simulate_player_progression(season.id)
            print(f"      Processed {len(prog_results)} players.")

            # Draft
            print("   ▶️ Simulating Draft...")
            try:
                draft_results = service.simulate_draft(season.id)
                print(f"      Drafted {len(draft_results)} players.")
            except Exception as e:
                print(f"      ⚠️ Draft simulation failed (might be already complete): {e}")

            # Free Agency
            print("   ▶️ Simulating Free Agency...")
            fa_res = service.simulate_free_agency(season.id)
            print(f"      {fa_res['message']}")

        elif season.status == SeasonStatus.POST_SEASON:
            print("\n   Season is in POST_SEASON. Attempting to start offseason...")
            try:
                service.start_offseason(season.id)
                print("   ✅ Offseason started successfully.")
            except Exception as e:
                print(f"   ❌ Failed to start offseason: {e}")
        else:
             print("\n   Season is in REGULAR_SEASON. Skipping offseason simulation.")

        print("\n✅ Verification Complete (on cloned DB).")
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        engine.dispose()
        # Clean up
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
            print(f"🧹 Cleaned up {TEST_DB_PATH}")

if __name__ == "__main__":
    run_verify()
