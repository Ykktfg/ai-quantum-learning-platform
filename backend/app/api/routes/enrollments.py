from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import (
    Enrollment,
    Course,
    Progress,
)
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
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
# ENROLL IN A COURSE
# ============================================================

@router.post(
    "/enrollments",
    response_model=EnrollmentResponse,
)
def enroll_in_course(
    enrollment: EnrollmentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Enroll the currently authenticated student in a course.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    # --------------------------------------------------------
    # Validate course ID
    # --------------------------------------------------------

    if enrollment.course_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID",
        )

    # --------------------------------------------------------
    # Check whether course exists
    # --------------------------------------------------------

    course = (
        db.query(Course)
        .filter(
            Course.id == enrollment.course_id
        )
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # --------------------------------------------------------
    # Check duplicate enrollment
    # --------------------------------------------------------

    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == enrollment.course_id,
        )
        .first()
    )

    if existing_enrollment is not None:
        raise HTTPException(
            status_code=409,
            detail="User is already enrolled in this course",
        )

    # --------------------------------------------------------
    # Create enrollment
    # --------------------------------------------------------

    new_enrollment = Enrollment(
        user_id=user_id,
        course_id=enrollment.course_id,
        status="active",
    )

    db.add(new_enrollment)

    try:
        db.commit()
        db.refresh(new_enrollment)

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create enrollment: {str(exc)}",
        )

    # --------------------------------------------------------
    # Create initial progress record
    # --------------------------------------------------------

    existing_progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.course_id == enrollment.course_id,
        )
        .first()
    )

    if existing_progress is None:

        progress = Progress(
            user_id=user_id,
            course_id=enrollment.course_id,
            completion_percentage=0,
            completed_lessons=0,
            status="not_started",
        )

        db.add(progress)

        try:
            db.commit()

        except Exception as exc:
            db.rollback()

            raise HTTPException(
                status_code=500,
                detail=(
                    "Enrollment was created, but "
                    "initial progress could not be created: "
                    f"{str(exc)}"
                ),
            )

    return new_enrollment


# ============================================================
# GET MY ENROLLMENTS
# ============================================================

@router.get(
    "/enrollments/me",
    response_model=list[EnrollmentResponse],
)
def get_my_enrollments(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all courses the currently authenticated user
    is enrolled in.
    """

    user_id = get_authenticated_user_id(
        current_user
    )

    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id
        )
        .order_by(
            Enrollment.id.desc()
        )
        .all()
    )

    return enrollments