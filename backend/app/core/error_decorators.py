from functools import wraps
from fastapi import HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from pydantic import ValidationError
from datetime import datetime, timezone
import logging
import asyncio

logger = logging.getLogger(__name__)

def handle_errors(func):
    """
    Decorator to wrap endpoint functions with comprehensive error handling.
    Catches common exceptions and returns appropriate HTTP responses.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract request object for context if available
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        
        # Try to get request_id from state, or use 'unknown'
        request_id = 'unknown'
        if request and hasattr(request, 'state') and hasattr(request.state, 'request_id'):
            request_id = request.state.request_id
        
        try:
            # Call the actual endpoint function
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
            
        except HTTPException:
            # Re-raise HTTPExceptions (already handled)
            raise
            
        except IntegrityError as e:
            logger.error(
                f"Database integrity error in {func.__name__}",
                extra={
                    "request_id": request_id,
                    "function": func.__name__,
                    "error_type": "IntegrityError",
                    "error": str(e)
                },
                exc_info=True
            )
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Integrity Error",
                    "message": "Operation conflicts with existing data",
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
        except OperationalError as e:
            logger.error(
                f"Database operational error in {func.__name__}",
                extra={
                    "request_id": request_id,
                    "function": func.__name__,
                    "error_type": "OperationalError"
                },
                exc_info=True
            )
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Service Unavailable",
                    "message": "Database connection error. Please try again later.",
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
        except ValidationError as e:
            logger.warning(
                f"Validation error in {func.__name__}",
                extra={
                    "request_id": request_id,
                    "function": func.__name__,
                    "errors": e.errors()
                }
            )
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "Validation Error",
                    "message": "Invalid data provided",
                    "details": e.errors(),
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
        except ValueError as e:
             # Business logic errors often raise ValueError
            logger.warning(
                f"Value error in {func.__name__}: {str(e)}",
                extra={
                    "request_id": request_id,
                    "function": func.__name__
                }
            )
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "Bad Request",
                    "message": str(e),
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

        except Exception as e:
            logger.exception(
                f"Unexpected error in {func.__name__}",
                extra={
                    "request_id": request_id,
                    "function": func.__name__,
                    "error_type": type(e).__name__
                }
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
    
    return wrapper
