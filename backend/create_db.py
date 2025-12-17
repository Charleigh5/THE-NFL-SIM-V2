from app.core.database import engine
from app.models.base import Base
# Import all models to register them with Base
import app.models

# Create all tables
print(f"Creating tables in: {engine.url}")
print(f"Registered tables: {list(Base.metadata.tables.keys())}")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
