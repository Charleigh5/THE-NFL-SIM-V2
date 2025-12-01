from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    college: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    age: int
    experience: int = 0
    jersey_number: int
    overall_rating: int = 50
    depth_chart_rank: int = 999
    
    # Attributes
    speed: int = 50
    acceleration: int = 50
    strength: int = 50
    agility: int = 50
    awareness: int = 50
    
    # Offensive
    throw_power: int = 50
    throw_accuracy_short: int = 50
    throw_accuracy_mid: int = 50
    throw_accuracy_deep: int = 50
    catching: int = 50
    route_running: int = 50
    pass_block: int = 50
    run_block: int = 50
    
    # Defensive
    tackle: int = 50
    hit_power: int = 50
    block_shed: int = 50
    man_coverage: int = 50
    zone_coverage: int = 50
    pass_rush_power: int = 50
    pass_rush_finesse: int = 50
    
    # Special Teams
    kick_power: int = 50
    kick_accuracy: int = 50
    
    # Physics
    arm_slot: str = "OverTop"
    release_point_height: float = 6.0
    vision_cone_angle: int = 45
    break_tackle_threshold: float = 100.0
    
    # Progression
    development_trait: str = "NORMAL"
    traits: List[str] = []
    
    # Status
    injury_status: str = "ACTIVE"
    injury_type: Optional[str] = None
    weeks_to_recovery: int = 0
    morale: int = 50
    
    # Contract
    contract_years: int = 1
    contract_salary: int = 1000000
    is_rookie: bool = False
    
    # Visuals
    image_url: Optional[str] = None
    nano_id: Optional[str] = None

class PlayerCreate(PlayerBase):
    team_id: Optional[int] = None

class Player(PlayerBase):
    id: int
    team_id: Optional[int] = None
    xp: int = 0
    level: int = 1
    skill_points: int = 0
    is_retired: bool = False
    retirement_year: Optional[int] = None
    legacy_score: int = 0

    model_config = ConfigDict(from_attributes=True)
