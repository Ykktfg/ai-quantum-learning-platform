from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import (
    Progress,
    Course,
    Enrollment,
    Lesson,
    Activity,
)
from app.schemas.progress import (
    ProgressUpdate,
    ProgressResponse,
)


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
# UPDATE / CREATE STUDENT PROGRESS
# ============================================================

@router.post(
    "/progress",
    response_model=ProgressResponse,
)
def update_progress(
    progress: ProgressUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create or update progress for the logged-in student.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    # --------------------------------------------------------
    # Check whether the course exists
    # --------------------------------------------------------

    course = (
        db.query(Course)
        .filter(
            Course.id == progress.course_id
        )
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # --------------------------------------------------------
    # Check whether the student is enrolled
    # --------------------------------------------------------

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == progress.course_id,
            Enrollment.status == "active",
        )
        .first()
    )

    if enrollment is None:
        raise HTTPException(
            status_code=403,
            detail=(
                "You must be enrolled in this course "
                "to update progress"
            ),
        )

    # --------------------------------------------------------
    # Determine progress status
    # --------------------------------------------------------

    if progress.completion_percentage >= 100:
        status = "completed"

    elif progress.completion_percentage > 0:
        status = "in_progress"

    else:
        status = "not_started"

    # --------------------------------------------------------
    # Find existing progress
    # --------------------------------------------------------

    existing_progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.course_id == progress.course_id,
        )
        .first()
    )

    # --------------------------------------------------------
    # Update existing progress
    # --------------------------------------------------------

    if existing_progress:

        existing_progress.completion_percentage = (
            progress.completion_percentage
        )

        existing_progress.completed_lessons = (
            progress.completed_lessons
        )

        existing_progress.status = status

        db.commit()
        db.refresh(existing_progress)

        return existing_progress

    # --------------------------------------------------------
    # Create new progress
    # --------------------------------------------------------

    new_progress = Progress(
        user_id=user_id,
        course_id=progress.course_id,
        completion_percentage=(
            progress.completion_percentage
        ),
        completed_lessons=(
            progress.completed_lessons
        ),
        status=status,
    )

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)

    return new_progress


# ============================================================
# GET MY PROGRESS
# ============================================================

@router.get(
    "/progress/me",
    response_model=List[ProgressResponse],
)
def get_my_progress(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all progress records belonging to
    the logged-in user.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    progress_records = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id
        )
        .order_by(
            Progress.id
        )
        .all()
    )

    return progress_records


# ============================================================
# GET PROGRESS FOR ONE COURSE
# ============================================================

@router.get(
    "/progress/{course_id}",
    response_model=ProgressResponse,
)
def get_course_progress(
    course_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return the logged-in user's progress
    for a specific course.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    progress_record = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.course_id == course_id,
        )
        .first()
    )

    if progress_record is None:
        raise HTTPException(
            status_code=404,
            detail="Progress not found for this course",
        )

    return progress_record


# ============================================================
# PROGRESS ANALYTICS
# ============================================================

@router.get(
    "/progress/analytics",
)
def get_progress_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return personalized progress analytics
    for the authenticated student.
    """

    user_id = get_authenticated_user_id(
        current_user
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

    enrolled_course_ids = [
        enrollment.course_id
        for enrollment in enrollments
    ]

    # ========================================================
    # GET PROGRESS
    # ========================================================

    progress_records = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id
        )
        .all()
    )

    # ========================================================
    # OVERALL PROGRESS
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
    # COMPLETED MODULES / LESSONS
    # ========================================================

    completed_modules = sum(
        int(
            progress.completed_lessons or 0
        )
        for progress in progress_records
    )

    # ========================================================
    # TOTAL MODULES / LESSONS
    # ========================================================

    if enrolled_course_ids:

        total_modules = (
            db.query(Lesson)
            .filter(
                Lesson.course_id.in_(
                    enrolled_course_ids
                )
            )
            .count()
        )

    else:
        total_modules = 0

    # ========================================================
    # XP CALCULATION
    # ========================================================
    #
    # Current rule:
    # 10 XP for every completed lesson.
    #
    # This is intentionally calculated from existing
    # database information. We will later move XP into
    # a dedicated XP/rewards system.
    # ========================================================

    xp = completed_modules * 10

    # ========================================================
    # LEVEL CALCULATION
    # ========================================================
    #
    # Every 500 XP = one level.
    # Level starts at 1.
    # ========================================================

    level = max(
        1,
        (xp // 500) + 1,
    )

    # ========================================================
    # LEARNING STREAK
    # ========================================================
    #
    # Activity currently stores activity records but does
    # not contain timestamps in the existing model.
    #
    # Therefore we cannot calculate a real calendar-day
    # streak yet.
    #
    # We return 0 until Activity gets a created_at field.
    # ========================================================

    learning_streak = 0

    # ========================================================
    # CHALLENGES
    # ========================================================
    #
    # There is currently no Challenge model/table.
    # Do not invent challenge data.
    # ========================================================

    challenges_completed = 0
    challenges_total = 0

    # ========================================================
    # COURSE BREAKDOWN
    # ========================================================

    course_progress = []

    for progress in progress_records:

        course = (
            db.query(Course)
            .filter(
                Course.id == progress.course_id
            )
            .first()
        )

        course_progress.append(
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
                "completed_lessons": int(
                    progress.completed_lessons or 0
                ),
                "status": progress.status,
            }
        )

    # ========================================================
    # RETURN ANALYTICS
    # ========================================================

    return {
        "success": True,

        "analytics": {
            "overall_progress": overall_progress,

            "modules": {
                "completed": completed_modules,
                "total": total_modules,
            },

            "challenges": {
                "completed": challenges_completed,
                "total": challenges_total,
            },

            "xp": xp,

            "level": level,

            "learning_streak": learning_streak,

            "courses": course_progress,
        },
    }