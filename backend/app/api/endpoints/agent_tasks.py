"""
Agent Tasks API Endpoints

Provides endpoints for generating implementation plans from task lists
using MCP infrastructure.
"""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.agent_generator import AgentGeneratorService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize agent generator
agent_generator = AgentGeneratorService()


class TaskItem(BaseModel):
    """Single task item from Mission Control."""
    id: str
    note: str
    element_type: str
    screenshot_path: str | None = None
    has_research: bool = False


class GeneratePlanRequest(BaseModel):
    """Request body for plan generation."""
    tasks: list[TaskItem]
    project_context: str | None = None


class GeneratePlanResponse(BaseModel):
    """Response after plan generation."""
    success: bool
    artifact_path: str
    task_count: int
    summary: str


@router.post("/generate-plan", response_model=GeneratePlanResponse)
async def generate_implementation_plan(request: GeneratePlanRequest):
    """
    Generate an implementation plan from a task list using MCP.

    Takes task items and uses MCP infrastructure to create a structured
    implementation plan artifact.
    """
    logger.info(f"Generating implementation plan for {len(request.tasks)} tasks")

    if not request.tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")

    try:
        result = await agent_generator.generate_plan(
            tasks=request.tasks,
            project_context=request.project_context
        )

        return GeneratePlanResponse(
            success=True,
            artifact_path=str(result.artifact_path),
            task_count=len(request.tasks),
            summary=result.summary
        )

    except Exception as e:
        logger.error(f"Plan generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate implementation plan: {str(e)}"
        )
