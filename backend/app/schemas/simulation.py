from typing import Any

from pydantic import BaseModel


class SimulationRequest(BaseModel):
    """Request model for triggering a simulation."""

    scenario: str | None = "default"
    config: dict[str, Any] | None = None
    num_plays: int | None = 100
