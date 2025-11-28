from pydantic import BaseModel
from typing import Optional, Dict, Any

class SimulationRequest(BaseModel):
    """Request model for triggering a simulation."""
    scenario: Optional[str] = "default"
    config: Optional[Dict[str, Any]] = None
    num_plays: Optional[int] = 100
