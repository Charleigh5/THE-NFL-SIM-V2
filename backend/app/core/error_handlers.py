"""
Global error handlers for the FastAPI application.
Provides consistent error responses and logging.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
import logging
from app.schemas.errors import ErrorResponse, ErrorDetail

logger = logging.getLogger(__name__)

def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", None)

async def database_exception_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (unique constraints, foreign keys, etc.)"""
    logger.error(f"Database integrity error: {exc}", extra={"request_id": get_request_id(request)})
    
    error_response = ErrorResponse(
        status_code=status.HTTP_409_CONFLICT,
        error=ErrorDetail(
            code="DB_INTEGRITY_ERROR",
            message="The operation conflicts with existing data constraints.",
            value=str(exc.orig) if hasattr(exc, 'orig') else str(exc)
        ),
        request_id=get_request_id(request)
    )
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response.model_dump()
    )


async def database_operational_error_handler(request: Request, exc: OperationalError):
    """Handle database operational errors (connection issues, etc.)"""
    logger.error(f"Database operational error: {exc}", extra={"request_id": get_request_id(request)})
    
    error_response = ErrorResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        error=ErrorDetail(
            code="DB_CONNECTION_ERROR",
            message="Unable to connect to the database. Please try again later.",
            value=str(exc.orig) if hasattr(exc, 'orig') else str(exc)
        ),
        request_id=get_request_id(request)
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors from FastAPI/Pydantic"""
    logger.warning(f"Validation error: {exc.errors()}", extra={"request_id": get_request_id(request)})
    
    details = []
    for e in exc.errors():
        details.append(ErrorDetail(
            code=e.get("type", "validation_error"),
            message=e.get("msg", "Invalid value"),
            field=str(e.get("loc", [])),
            value=str(e.get("ctx", {}))
        ))

    error_response = ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="The request data is invalid."
        ),
        details=details,
        request_id=get_request_id(request)
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def pydantic_validation_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Pydantic validation error: {exc.errors()}", extra={"request_id": get_request_id(request)})
    
    details = []
    for e in exc.errors():
        details.append(ErrorDetail(
            code=e.get("type", "validation_error"),
            message=e.get("msg", "Invalid value"),
            field=str(e.get("loc", [])),
            value=str(e.get("ctx", {}))
        ))

    error_response = ErrorResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=ErrorDetail(
            code="DATA_VALIDATION_ERROR",
            message="The data provided is invalid."
        ),
        details=details,
        request_id=get_request_id(request)
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all handler for unexpected exceptions"""
    logger.exception(f"Unhandled exception: {exc}", extra={"request_id": get_request_id(request)})
    
    error_response = ErrorResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please contact support if the issue persists.",
            value=str(exc) if logger.level == logging.DEBUG else None
        ),
        request_id=get_request_id(request)
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )
