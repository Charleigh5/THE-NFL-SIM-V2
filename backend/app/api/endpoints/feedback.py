import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.feedback import UserFeedback
from app.schemas.feedback import (
    BatchSubmitRequest,
    BatchSubmitResponse,
    FeedbackCreate,
    FeedbackResponse,
    IssueReportRequest,
    IssueReportResponse,
    ResearchRequest,
    ResearchResponse,
)
from app.services.ai_research_service import ai_research_service
from app.services.artifact_generator import (
    AIResearchData,
    AnnotationData,
    AnnotationElement,
    ArtifactGeneratorService,
    artifact_generator,
)
from app.services.issue_logger import IssueEntry, IssueLoggerService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize issue logger service
issue_logger = IssueLoggerService()


@router.post("/", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Submit user feedback for AI suggestions (Draft, Trade, etc.)
    """
    logger.info(f"Received feedback for {feedback.contextType} {feedback.contextId}")

    db_feedback = UserFeedback(
        context_id=feedback.contextId,
        context_type=feedback.contextType,
        is_helpful=feedback.isHelpful,
        comment=feedback.comment,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.post("/issue", response_model=IssueReportResponse)
async def report_issue(request: IssueReportRequest):
    """
    Report an issue from the frontend UI.

    Appends the issue to ISSUES.md in the project root.
    """
    logger.info(f"Received issue report from {request.context}: {request.message[:50]}...")

    entry = IssueEntry(message=request.message, context=request.context, page=request.page)

    success = await issue_logger.log_issue_async(entry)

    if success:
        return IssueReportResponse(success=True, message="Issue logged successfully")
    else:
        raise HTTPException(status_code=500, detail="Failed to log issue")


@router.post("/research", response_model=ResearchResponse)
async def research_task(request: ResearchRequest):
    """
    Research implementation best practices for a task.

    Uses AI to analyze the task and provide recommendations.
    """
    logger.info(f"Researching task: {request.task[:50]}...")

    result = await ai_research_service.research_task(request.task)

    return ResearchResponse(
        summary=result.summary,
        recommended_approach=result.recommended_approach,
        code_examples=result.code_examples,
        complexity=result.complexity.value,
        sources=result.sources,
    )


@router.post("/batch", response_model=BatchSubmitResponse)
async def submit_batch(request: BatchSubmitRequest):
    """
    Submit a batch of annotations.

    Creates a task list artifact and logs each issue.
    """
    logger.info(f"Received batch submission with {len(request.annotations)} annotations")

    try:
        # Convert to internal format
        annotations = []
        for ann in request.annotations:
            element = AnnotationElement(
                selector=ann.element.selector,
                tagName=ann.element.tagName,
                textContent=ann.element.textContent or "",
                className=ann.element.className,
            )

            ai_research = None
            if ann.aiResearch:
                ai_research = AIResearchData(
                    summary=ann.aiResearch.summary,
                    codeExamples=ann.aiResearch.codeExamples,
                    complexity=ann.aiResearch.complexity,
                    sources=ann.aiResearch.sources,
                )

            annotations.append(
                AnnotationData(
                    id=ann.id,
                    timestamp=ann.timestamp,
                    note=ann.note,
                    element=element,
                    aiResearch=ai_research,
                )
            )

        # Generate artifact
        artifact_path = await artifact_generator.generate_artifact_async(annotations)

        # Log each annotation as an issue
        for ann in request.annotations:
            entry = IssueEntry(
                message=f"[{ann.element.tagName}] {ann.note}",
                context="Design Mode",
                page=ann.element.selector,
            )
            await issue_logger.log_issue_async(entry)

        return BatchSubmitResponse(
            success=True, artifact_path=str(artifact_path), issues_logged=len(request.annotations)
        )
    except Exception as e:
        logger.error(f"Batch submit failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Batch submission failed: {str(e)}")


@router.post("/export", response_model=BatchSubmitResponse)
async def export_updates(request: BatchSubmitRequest):
    """
    Export annotations to a markdown file in docs/updates_and_enhancements.
    """
    logger.info(f"Received export request with {len(request.annotations)} annotations")

    try:
        # Convert to internal format (reusing logic)
        annotations = []
        for ann in request.annotations:
            element = AnnotationElement(
                selector=ann.element.selector,
                tagName=ann.element.tagName,
                textContent=ann.element.textContent or "",
                className=ann.element.className,
            )

            ai_research = None
            if ann.aiResearch:
                ai_research = AIResearchData(
                    summary=ann.aiResearch.summary,
                    codeExamples=ann.aiResearch.codeExamples,
                    complexity=ann.aiResearch.complexity,
                    sources=ann.aiResearch.sources,
                )

            annotations.append(
                AnnotationData(
                    id=ann.id,
                    timestamp=ann.timestamp,
                    note=ann.note,
                    element=element,
                    aiResearch=ai_research,
                )
            )

        # Use absolute path to docs/updates_and_enhancements
        import os
        from pathlib import Path

        # Get project root (assuming we are in app/api/endpoints)
        # ../../../..
        project_root = Path(
            os.getcwd()
        )  # Should be backend or project root. Assuming execution context.
        # Ensure we find the right docs folder.
        # If running from backend dir, docs is ../docs possibly?
        # Let's rely on absolute path construction relative to known anchor if possible.
        # Safer: Use absolute path c:\Users\cweir\Documents\GitHub\THE NFL SIM\docs\updates_and_enhancements
        # But for portability, let's try to resolve it.

        output_dir = Path(
            "c:/Users/cweir/Documents/GitHub/THE NFL SIM/docs/updates_and_enhancements"
        )

        # Initialize generator with specific output dir
        custom_generator = ArtifactGeneratorService(output_dir=output_dir)
        artifact_path = await custom_generator.generate_artifact_async(annotations)

        return BatchSubmitResponse(
            success=True, artifact_path=str(artifact_path), issues_logged=len(request.annotations)
        )
    except Exception as e:
        logger.error(f"Export failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
