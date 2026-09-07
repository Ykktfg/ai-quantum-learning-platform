from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import Course


router = APIRouter()


# ============================================================
# GET ALL COURSES
# ============================================================

@router.get("/courses")
def get_courses(
    db: Session = Depends(get_db),
):
    """
    Return all available quantum computing courses.
    """

    courses = (
        db.query(Course)
        .order_by(Course.id)
        .all()
    )

    return {
        "count": len(courses),
        "courses": [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "level": course.level,
                "duration": course.duration,
                "category": course.category,
            }
            for course in courses
        ],
    }


# ============================================================
# GET COURSE BY ID
# ============================================================

@router.get("/courses/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a single course by its ID.
    """

    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "level": course.level,
        "duration": course.duration,
        "category": course.category,
    }