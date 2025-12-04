from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class Stadium(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String)
    state = Column(String)
    country = Column(String, default="USA")

    capacity = Column(Integer)
    type = Column(String) # Open, Dome, Retractable
    turf_type = Column(String) # Grass, Artificial Turf, Hybrid

    year_built = Column(Integer)

    # Weather factors (for simulation)
    altitude = Column(Integer, default=0) # e.g. Denver
    dome = Column(Boolean, default=False)

    # Visuals
    image_url = Column(String, nullable=True)

    # Relationship
    team = relationship("Team", back_populates="stadium", uselist=False)
    climate = relationship("StadiumClimate", uselist=False, back_populates="stadium")
