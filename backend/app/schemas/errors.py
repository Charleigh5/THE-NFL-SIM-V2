from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    field: str | None = Field(None, description="The field that caused the error (for validation errors)")
    value: Any | None = Field(None, description="The invalid value provided")

class ErrorResponse(BaseModel):
    status_code: int = Field(..., description="HTTP status code")
    error: ErrorDetail = Field(..., description="Main error details")
    details: list[ErrorDetail] | None = Field(None, description="Additional error details (e.g. for multiple validation errors)")
    request_id: str | None = Field(None, description="Unique request ID for tracking")
