from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import (
    User,
    Course,
    Enrollment,
    Progress,
    Circuit,
    Simulation,
)
from app.schemas.dashboard import DashboardResponse


router = APIRouter()


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
def get_dashboard(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return real dashboard information for
    the authenticated user.
    """

    # ========================================================
    # GET AUTHENTICATED USER ID
    # ========================================================

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

    # ========================================================
    # FIND USER
    # ========================================================

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # ========================================================
    # GET ACTIVE ENROLLMENTS
    # ========================================================

    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.status == "active",
        )
        .all()
    )

    courses_enrolled = len(enrollments)

    # ========================================================
    # GET PROGRESS RECORDS
    # ========================================================

    progress_records = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id
        )
        .order_by(
            Progress.id.desc()
        )
        .all()
    )

    # ========================================================
    # CALCULATE COMPLETED COURSES
    # ========================================================

    courses_completed = sum(
        1
        for progress in progress_records
        if progress.status == "completed"
    )

    # ========================================================
    # CALCULATE OVERALL PROGRESS
    # ========================================================

    if progress_records:
        overall_progress = round(
            sum(
                float(
                    progress.completion_percentage
                )
                for progress in progress_records
            )
            / len(progress_records),
            2,
        )
    else:
        overall_progress = 0.0

    # ========================================================
    # COUNT CIRCUITS CREATED
    # ========================================================

    circuits_created = (
        db.query(Circuit)
        .filter(
            Circuit.user_id == user_id
        )
        .count()
    )

    # ========================================================
    # COUNT SIMULATIONS RUN
    # ========================================================

    simulations_run = (
        db.query(Simulation)
        .filter(
            Simulation.user_id == user_id
        )
        .count()
    )

    # ========================================================
    # BUILD RECENT PROGRESS
    # ========================================================

    recent_progress: list[dict[str, Any]] = []

    for progress in progress_records[:5]:

        course = (
            db.query(Course)
            .filter(
                Course.id == progress.course_id
            )
            .first()
        )

        recent_progress.append(
            {
                "course_id": progress.course_id,
                "course_title": (
                    course.title
                    if course
                    else "Unknown Course"
                ),
                "completion_percentage": float(
                    progress.completion_percentage
                ),
                "completed_lessons": (
                    progress.completed_lessons
                ),
                "status": progress.status,
            }
        )

    # ========================================================
    # RETURN DASHBOARD
    # ========================================================

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },

        "stats": {
            "courses_enrolled": courses_enrolled,
            "courses_completed": courses_completed,
            "overall_progress": overall_progress,
            "circuits_created": circuits_created,
            "simulations_run": simulations_run,
        },

        "recent_progress": recent_progress,

        "message": (
            "Welcome to your quantum learning dashboard!"
        ),
    }