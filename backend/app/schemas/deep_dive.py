"""
Deep Dive Simulation Subsystems Schemas
========================================
Pydantic V2 schemas for:
1. Dynamic Scouting Fog of War & Draft AI
2. Coaching Dynasty Trees & Staff Chemistry
3. Orthopedic Trauma Triage & Hazard Curves
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# ============================================================================
# 1. SCOUTING FOG OF WAR & DRAFT INTELLIGENCE SCHEMAS
# ============================================================================

class ScoutBiasLens(str, Enum):
    """Scouting evaluation lens representing different front office philosophies."""
    CONSENSUS = "CONSENSUS"
    FILM_TRADITIONALIST = "FILM_TRADITIONALIST"
    ANALYTICS_METRICS = "ANALYTICS_METRICS"
    REGIONAL_SCOUT = "REGIONAL_SCOUT"


class ProspectIntelligence(BaseModel):
    """Deep scouting intelligence profile for draft prospects."""
    id: int
    name: str
    position: str
    college: str
    true_ovr: int = Field(..., description="Actual underlying overall rating")
    consensus_ovr: int = Field(..., description="National consensus media rating")
    perceived_ovr: Dict[str, int] = Field(
        default_factory=dict,
        description="Perceived OVR under each ScoutBiasLens"
    )
    s2_cognition_score: int = Field(..., ge=0, le=100, description="S2 Cognitive test score")
    gps_speed_max: float = Field(..., ge=15.0, le=24.0, description="Peak on-field GPS speed in MPH")
    burst_score: float = Field(..., ge=0.0, le=100.0, description="First-step acceleration index")
    boom_bust_factor: float = Field(..., ge=0.0, le=1.0, description="Variance in career trajectory")
    scheme_fit_percentage: int = Field(..., ge=0, le=100, description="Fit percentage with team scheme")
    medical_grade: str = Field(..., description="PASS, CONCERN, or FAIL")
    draft_projection_round: int = Field(..., ge=1, le=7)


class DraftTradeUrgency(BaseModel):
    """Real-time dynamic draft trade-up pressure and market valuation."""
    team_id: str
    target_position: str
    urgency_index: float = Field(..., ge=0.0, le=1.0)
    willing_to_overpay_pct: float = Field(..., ge=0.0, le=0.50)
    suggested_package_value: int


# ============================================================================
# 2. COACHING DYNASTY & STAFF CHEMISTRY SCHEMAS
# ============================================================================

class CoachingBranch(str, Enum):
    """Three core branches of head coach & coordinator skill trees."""
    SCHEME_TACTICS = "SCHEME_TACTICS"
    DEVELOPMENT = "DEVELOPMENT"
    PROGRAM_CULTURE = "PROGRAM_CULTURE"


class CoachingSkillNode(BaseModel):
    """Single unlockable node in a coaching skill tree."""
    id: str
    name: str
    branch: CoachingBranch
    tier: int = Field(..., ge=1, le=4, description="Tier 1-3 standard, Tier 4 Mastery")
    unlocked: bool = False
    sp_cost: int = Field(..., ge=1, le=5, description="Skill points required to unlock")
    bonus_description: str
    prerequisites: List[str] = Field(default_factory=list)
    stat_multiplier: float = Field(default=1.05, description="Multiplier effect e.g. 1.05 for +5%")


class StaffSynergyBreakdown(BaseModel):
    """Calculated chemistry and synergy between HC, OC, DC, and position coaches."""
    head_coach_id: str
    offensive_coord_id: str
    defensive_coord_id: str
    offensive_synergy_score: int = Field(..., ge=0, le=100)
    defensive_synergy_score: int = Field(..., ge=0, le=100)
    overall_chemistry_score: int = Field(..., ge=0, le=100)
    active_synergy_perks: List[str] = Field(default_factory=list)
    scheme_alignment_notes: List[str] = Field(default_factory=list)


class CoachDynastyProfile(BaseModel):
    """Comprehensive dynasty progression state for a coach."""
    coach_id: str
    name: str
    role: str
    level: int
    current_sp: int
    total_sp_earned: int
    archetype: str
    tree_nodes: Dict[str, CoachingSkillNode] = Field(default_factory=dict)


# ============================================================================
# 3. ORTHOPEDIC TRAUMA TRIAGE & HAZARD SCHEMAS
# ============================================================================

class MedicalProtocolType(str, Enum):
    """Clinical recovery and stabilization pathways."""
    REST = "REST"
    PRP_THERAPY = "PRP_THERAPY"
    ARTHROSCOPIC_SURGERY = "ARTHROSCOPIC_SURGERY"
    RECONSTRUCTIVE_SURGERY = "RECONSTRUCTIVE_SURGERY"
    CORTISONE_STABILIZATION = "CORTISONE_STABILIZATION"


class OrthopedicProtocolOption(BaseModel):
    """Evaluation metrics for a specific clinical treatment protocol."""
    protocol: MedicalProtocolType
    name: str
    estimated_recovery_weeks: int
    complication_risk_pct: float = Field(..., ge=0.0, le=1.0)
    target_integrity_restore: float = Field(..., ge=0.0, le=100.0)
    re_injury_hazard_multiplier: float = Field(..., ge=0.5, le=3.0)
    game_availability_status: str # "OUT" | "DOUBTFUL" | "QUESTIONABLE" | "ACTIVE"
    description: str
    clinical_note: Optional[str] = None


class TriageDecisionResult(BaseModel):
    """Outcome of an applied orthopedic triage protocol."""
    player_id: int
    zone_key: str
    protocol_applied: MedicalProtocolType
    projected_recovery_weeks: int
    complication_occurred: bool
    final_integrity_forecast: float
    re_injury_risk_index: float
    message: str
