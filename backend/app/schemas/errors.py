from pydantic import BaseModel, Field
from typing import List, Optional, Any

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    field: Optional[str] = Field(None, description="The field that caused the error (for validation errors)")
    value: Optional[Any] = Field(None, description="The invalid value provided")

class ErrorResponse(BaseModel):
    status_code: int = Field(..., description="HTTP status code")
    error: ErrorDetail = Field(..., description="Main error details")
    details: Optional[List[ErrorDetail]] = Field(None, description="Additional error details (e.g. for multiple validation errors)")
    request_id: Optional[str] = Field(None, description="Unique request ID for tracking")
