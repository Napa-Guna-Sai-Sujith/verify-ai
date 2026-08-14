from fastapi import APIRouter, HTTPException, status
import uuid
import logging

from app.models.schemas import ProfileCreateRequest, ProfileResponse
from app.services.db_service import create_user_profile, get_user_profile

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication & Profiles"])


@router.post("/register", response_model=ProfileResponse, status_code=201)
def register_profile(req: ProfileCreateRequest):
    """Register a new user profile in Neon PostgreSQL. Returns 409 if email already exists."""
    # Check if email already registered
    existing = get_user_profile(req.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists. Please sign in instead."
        )

    user_id = str(uuid.uuid4())
    profile = create_user_profile(
        user_id=user_id,
        full_name=req.full_name,
        email=req.email,
        preferred_language=req.preferred_language or "English"
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save user profile. Please try again."
        )

    return ProfileResponse(
        id=str(profile["id"]),
        full_name=profile.get("full_name", ""),
        email=profile["email"],
        preferred_language=profile.get("preferred_language", "English"),
        created_at=str(profile.get("created_at", ""))
    )


@router.put("/profile", response_model=ProfileResponse)
def update_existing_profile(req: ProfileCreateRequest):
    """Update existing user profile in Neon PostgreSQL."""
    existing = get_user_profile(req.email)
    user_id = str(existing["id"]) if existing else str(uuid.uuid4())
    
    profile = create_user_profile(
        user_id=user_id,
        full_name=req.full_name,
        email=req.email,
        preferred_language=req.preferred_language or "English"
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile in Neon PostgreSQL database."
        )

    return ProfileResponse(
        id=str(profile["id"]),
        full_name=profile.get("full_name", ""),
        email=profile["email"],
        preferred_language=profile.get("preferred_language", "English"),
        created_at=str(profile.get("created_at", ""))
    )


@router.get("/profile", response_model=ProfileResponse)
def fetch_profile(email: str):
    """Look up a user profile by email. Returns 404 if not found."""
    profile = get_user_profile(email)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with that email address."
        )

    return ProfileResponse(
        id=str(profile["id"]),
        full_name=profile.get("full_name", ""),
        email=profile["email"],
        preferred_language=profile.get("preferred_language", "English"),
        created_at=str(profile.get("created_at", ""))
    )


@router.get("/analyses")
def fetch_user_analyses(user_id: str):
    """Retrieve all analysis history for a user from Neon PostgreSQL."""
    from app.services.db_service import get_user_analyses
    return get_user_analyses(user_id)
