import enum
from datetime import datetime, timedelta
from pydantic import BaseModel

class SeasonPhase(str, enum.Enum):
    PRESEASON = "Preseason"
    REGULAR_SEASON = "Regular Season"
    PLAYOFFS = "Playoffs"
    OFFSEASON = "Offseason"
    DRAFT = "Draft"
    FREE_AGENCY = "Free Agency"

class GameClock(BaseModel):
    quarter: int = 1
    time_remaining: int = 900 # 15 minutes in seconds
    play_clock: int = 40
    is_running: bool = False
    
    def tick(self, seconds: int = 1):
        if self.is_running:
            self.time_remaining = max(0, self.time_remaining - seconds)
            
    def reset_play_clock(self):
        self.play_clock = 40

class CalendarEngine:
    def __init__(self, current_year: int = 2025):
        self.current_year = current_year
        self.current_week = 1
        self.current_phase = SeasonPhase.PRESEASON
        
    def advance_week(self):
        self.current_week += 1
        self.check_phase_transition()
        
    def check_phase_transition(self):
        # Logic to transition phases based on week
        if self.current_phase == SeasonPhase.PRESEASON and self.current_week > 4:
            self.current_phase = SeasonPhase.REGULAR_SEASON
            self.current_week = 1
        elif self.current_phase == SeasonPhase.REGULAR_SEASON and self.current_week > 18:
            self.current_phase = SeasonPhase.PLAYOFFS
            self.current_week = 1
            
    def get_current_date(self) -> datetime:
        # Mock logic to return a date based on phase/week
        base_date = datetime(self.current_year, 8, 1) # Aug 1st start
        weeks_passed = self.current_week - 1
        if self.current_phase == SeasonPhase.REGULAR_SEASON:
            weeks_passed += 4
        elif self.current_phase == SeasonPhase.PLAYOFFS:
            weeks_passed += 22
            
        return base_date + timedelta(weeks=weeks_passed)
