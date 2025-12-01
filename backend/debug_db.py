from sqlalchemy import create_engine, text
from app.core.config import settings

print(f"Database URL: {settings.DATABASE_URL}")

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT count(*) FROM team"))
        print(f"Team count: {result.scalar()}")
        
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        print("Tables:", [row[0] for row in result])
except Exception as e:
    print(f"Error: {e}")
