from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import User


router = APIRouter()


# ============================================================
# HELPER - GET AUTHENTICATED USER ID
# ============================================================

def get_authenticated_user_id(
    current_user: dict,
) -> int:
    """
    Extract and validate the authenticated user's ID.
    """

    user_id = current_user.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in authentication token",
        )

    if user_id <= 0:
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in authentication token",
        )

    return user_id


# ============================================================
# SERIALIZE USER PROFILE
# ============================================================

def serialize_user_profile(user: User) -> dict:
    """
    Convert a User database object into the
    frontend profile response.
    """

    join_date = getattr(user, "join_date", None)

    if isinstance(join_date, (datetime, date)):
        join_date = join_date.isoformat()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,

        # Profile
        "avatar_url": getattr(
            user,
            "avatar_url",
            None,
        ),

        "join_date": join_date,

        # Learning statistics
        "xp": getattr(
            user,
            "xp",
            0,
        ),

        "level": getattr(
            user,
            "level",
            1,
        ),

        "learning_streak": getattr(
            user,
            "learning_streak",
            0,
        ),
    }


# ============================================================
# GET CURRENT USER PROFILE
# ============================================================

@router.get("/users/me")
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return the complete profile of the
    currently authenticated user.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "success": True,

        "user": serialize_user_profile(
            user
        ),
    }