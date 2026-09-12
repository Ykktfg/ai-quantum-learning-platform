from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.repositories.activity_repository import activity_repository
from app.schemas.activity import ActivityCreate, ActivityResponse


router = APIRouter()


# ============================================================
# CREATE ACTIVITY
# ============================================================

@router.post(
    "/activity",
    response_model=ActivityResponse,
)
def create_activity(
    activity: ActivityCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Record a learning activity for the logged-in user
    and add the earned XP to the user's profile.
    """

    user_id = int(current_user["sub"])

    # Create the activity record.
    new_activity = activity_repository.create(
        db=db,
        user_id=user_id,
        activity_type=activity.activity_type,
        course_id=activity.course_id,
        description=activity.description,
        xp_earned=activity.xp_earned,
    )

    # Update the user's total XP.
    user = db.query(User).filter(User.id == user_id).first()

    if user is not None and activity.xp_earned > 0:
        user.xp_points = (user.xp_points or 0) + activity.xp_earned
        db.commit()
        db.refresh(user)

    return new_activity


# ============================================================
# GET MY ACTIVITIES
# ============================================================

@router.get(
    "/activity/me",
    response_model=list[ActivityResponse],
)
def get_my_activities(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all learning activities for the logged-in user.
    """

    user_id = int(current_user["sub"])

    activities = activity_repository.get_by_user(
        db=db,
        user_id=user_id,
    )

    return activities
