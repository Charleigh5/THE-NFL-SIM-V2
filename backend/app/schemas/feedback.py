from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class FeedbackCreate(BaseModel):
    contextId: str
    contextType: str
    isHelpful: bool
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    context_id: str
    context_type: str
    is_helpful: bool
    comment: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# === Issue Reporting Schemas ===

class IssueReportRequest(BaseModel):
    """Request body for reporting an issue."""
    message: str
    context: str = "Frontend"
    page: Optional[str] = None


class IssueReportResponse(BaseModel):
    """Response after logging an issue."""
    success: bool
    message: str


# === AI Research Schemas ===

class ResearchRequest(BaseModel):
    """Request body for AI research."""
    task: str


class ResearchResponse(BaseModel):
    """Response with AI research results."""
    summary: str
    recommended_approach: str
    code_examples: List[str]
    complexity: str
    sources: List[str]


# === Batch Annotation Schemas ===

class ElementMetadata(BaseModel):
    """Element metadata from frontend."""
    selector: str
    tagName: str
    textContent: Optional[str] = ""
    className: Optional[str] = None


class AIResearchData(BaseModel):
    """AI research data attached to annotation."""
    summary: str
    codeExamples: List[str]
    complexity: str
    sources: List[str]


class BatchAnnotation(BaseModel):
    """Single annotation in a batch."""
    id: str
    timestamp: str
    note: str
    element: ElementMetadata
    aiResearch: Optional[AIResearchData] = None


class BatchSubmitRequest(BaseModel):
    """Request body for batch submission."""
    annotations: List[BatchAnnotation]


class BatchSubmitResponse(BaseModel):
    """Response after batch submission."""
    success: bool
    artifact_path: str
    issues_logged: int


