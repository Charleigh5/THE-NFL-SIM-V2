# Import all models to register them with Base
from app.core.database import engine
from app.models.base import Base

# Create all tables
print(f"Creating tables in: {engine.url}")
print(f"Registered tables: {list(Base.metadata.tables.keys())}")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
