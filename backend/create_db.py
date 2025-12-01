from app.core.database import engine
from app.models.base import Base
# Import all models to register them with Base
import app.models.player
import app.models.team
import app.models.stadium
import app.models.coach
import app.models.gm
import app.models.settings
import app.models.game
import app.models.stats
import app.models.season
import app.models.playoff
import app.models.draft
import app.models.history
import app.models.depth_chart

# Create all tables
print(f"Creating tables in: {engine.url}")
print(f"Registered tables: {list(Base.metadata.tables.keys())}")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
