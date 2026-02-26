from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FeedbackCreate(BaseModel):
    contextId: str
    contextType: str
    isHelpful: bool
    comment: str | None = None

class FeedbackResponse(BaseModel):
    id: int
    context_id: str
    context_type: str
    is_helpful: bool
    comment: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# === Issue Reporting Schemas ===

class IssueReportRequest(BaseModel):
    """Request body for reporting an issue."""
    message: str
    context: str = "Frontend"
    page: str | None = None


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
    code_examples: list[str]
    complexity: str
    sources: list[str]


# === Batch Annotation Schemas ===

class ElementMetadata(BaseModel):
    """Element metadata from frontend."""
    selector: str
    tagName: str
    textContent: str | None = ""
    className: str | None = None


class AIResearchData(BaseModel):
    """AI research data attached to annotation."""
    summary: str
    codeExamples: list[str]
    complexity: str
    sources: list[str]


class BatchAnnotation(BaseModel):
    """Single annotation in a batch."""
    id: str
    timestamp: str
    note: str
    element: ElementMetadata
    aiResearch: AIResearchData | None = None


class BatchSubmitRequest(BaseModel):
    """Request body for batch submission."""
    annotations: list[BatchAnnotation]


class BatchSubmitResponse(BaseModel):
    """Response after batch submission."""
    success: bool
    artifact_path: str
    issues_logged: int


