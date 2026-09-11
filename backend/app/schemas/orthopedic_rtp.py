"""
Orthopedic RTP Projection Trajectory & Re-Injury Hazard Schemas
==============================================================
Pydantic V2 schemas for:
1. 12-week Gompertz tissue repair curves across treatment protocols
2. Elite outside specialist 2nd opinion referral centers & consult results
3. Live physics 60Hz cortisone hazard calculations
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class RTPCurvePoint(BaseModel):
    """Weekly milestone on the non-linear tissue recovery curve."""
    week: int = Field(..., ge=0, le=12, description="Week index (0-12)")
    health_percentage: float = Field(..., ge=0.0, le=100.0, description="Estimated tissue integrity percentage")
    re_injury_risk_pct: float = Field(..., ge=0.0, le=100.0, description="Re-injury probability percentage")
    on_field_effectiveness_pct: float = Field(..., ge=0.0, le=100.0, description="On-field athletic performance index")


class TreatmentTrajectory(BaseModel):
    """Comparative trajectory curve for a specific medical protocol."""
    protocol: Literal["CONSERVATIVE", "BIOLOGIC_PRP", "ARTHROSCOPIC", "OPEN_SURGERY", "CORTISONE"]
    label: str
    est_recovery_weeks: int = Field(..., ge=0, le=52)
    complication_risk_pct: float = Field(..., ge=0.0, le=100.0)
    total_medical_cost: int = Field(..., ge=0)
    curve: List[RTPCurvePoint]


class SecondOpinionCenter(BaseModel):
    """Elite outside orthopedic surgical & consultation center."""
    center_id: str
    name: str
    specialty_region: str
    chief_surgeon: str
    consultation_cost: int = Field(..., ge=0)
    turnaround_days: int = Field(..., ge=1, le=14)
    diagnostic_accuracy_boost: float = Field(..., ge=0.0, le=1.0)


class SecondOpinionRequest(BaseModel):
    """Request payload for dispatching athlete to an outside specialist."""
    player_id: int
    center_id: str


class SecondOpinionConsultResult(BaseModel):
    """Clinical findings report from outside specialist consultation."""
    player_id: int
    center_id: str
    center_name: str
    chief_surgeon: str
    original_diagnosis: str
    confirmed_diagnosis: str
    occult_pathology_detected: bool
    findings_narrative: str
    recommended_protocol: str
    complication_reduction_factor: float = Field(default=0.50, ge=0.1, le=1.0)
    consultation_cost: int


class CortisoneHazardCheckRequest(BaseModel):
    """Telemetry payload for in-game cortisone strain hazard check."""
    runner_has_cortisone: bool
    is_sharp_cut: bool = False
    g_force: float = 0.0
    momentum: float = 0.0  # kg * m/s


class CortisoneHazardCheckResponse(BaseModel):
    """Evaluation result for in-game tissue strain under cortisone masking."""
    catastrophic_rupture: bool
    hazard_multiplier: float
    effective_risk_pct: float
    event_message: str


class OrthopedicEvaluationResponse(BaseModel):
    """Comprehensive orthopedic evaluation containing all trajectories and specialist options."""
    player_id: int
    player_name: Optional[str] = None
    injury_type: str
    body_part: str
    severity_grade: int
    baseline_health: float
    is_cortisone_active: bool = False
    has_specialist_clearance: bool = False
    specialist_center_name: Optional[str] = None
    trajectories: List[TreatmentTrajectory]
    specialist_centers: List[SecondOpinionCenter]
    cortisone_in_game_hazard_multiplier: float = 2.5
    model_config = ConfigDict(from_attributes=True)
