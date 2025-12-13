"""
Firebase Authentication Module

This module handles Firebase Admin SDK initialization and token verification
for authenticating users in the NFL Sim Engine API.
"""

import os
from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header
import logging

logger = logging.getLogger(__name__)

# Global flag to track initialization
_firebase_initialized = False


def initialize_firebase():
    """
    Initialize Firebase Admin SDK.

    For local development: Uses service account key from GOOGLE_APPLICATION_CREDENTIALS
    For Cloud Run: Uses Application Default Credentials automatically
    """
    global _firebase_initialized

    if _firebase_initialized:
        logger.info("Firebase Admin SDK already initialized")
        return

    try:
        # Check if running on Cloud Run (uses default credentials)
        if os.getenv("K_SERVICE"):
            firebase_admin.initialize_app()
            logger.info("Firebase initialized with Application Default Credentials (Cloud Run)")
        else:
            # Local development: use service account key
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not cred_path:
                raise ValueError(
                    "GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
                    "Please download your service account key and set the path."
                )

            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Service account key not found at: {cred_path}")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info(f"Firebase initialized with service account: {cred_path}")

        _firebase_initialized = True

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise


def verify_token(token: str) -> dict:
    """
    Verify a Firebase ID token from the frontend.

    Args:
        token: The Firebase ID token string

    Returns:
        dict: Decoded token containing user information (uid, email, etc.)

    Raises:
        HTTPException: If token is invalid or expired
    """
    if not _firebase_initialized:
        raise HTTPException(
            status_code=500,
            detail="Firebase not initialized. Server configuration error."
        )

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Authentication token expired")
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    FastAPI dependency to extract and verify the current user from the Authorization header.

    Usage:
        @app.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"message": f"Hello {user['uid']}"}

    Args:
        authorization: The Authorization header (expected format: "Bearer <token>")

    Returns:
        dict: Decoded token with user information

    Raises:
        HTTPException: If authorization header is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    try:
        # Extract token from "Bearer <token>" format
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme. Use 'Bearer <token>'"
            )

        return verify_token(token)

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header format. Use 'Bearer <token>'"
        )
