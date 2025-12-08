import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Setup DB connection to test_manual.db
db_path = os.path.join(os.getcwd(), "test_manual.db")
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_teams():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) FROM team"))
        count = result.scalar()
        print(f"Total Teams: {count}")
        if count == 32:
            print("VERIFICATION SUCCESS: 32 teams found.")
        else:
            print(f"VERIFICATION FAILED: Expected 32 teams, found {count}.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    verify_teams()
