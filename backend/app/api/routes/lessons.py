from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db
from app.db.models import Course, Lesson
from app.schemas.lesson import LessonCreate


router = APIRouter()


# ============================================================
# HELPER - GET AUTHENTICATED USER ID
# ============================================================

def get_authenticated_user_id(
    current_user: dict,
) -> int:
    """
    Extract and validate authenticated user's ID.
    """

    user_id = current_user.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    try:
        return int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in authentication token",
        )


# ============================================================
# CREATE LESSON
# ============================================================

@router.post("/courses/{course_id}/lessons")
def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a lesson for a course.

    Currently authenticated users can create lessons.
    """

    get_authenticated_user_id(current_user)

    # --------------------------------------------------------
    # Validate course ID
    # --------------------------------------------------------

    if course_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID",
        )

    # --------------------------------------------------------
    # Find course
    # --------------------------------------------------------

    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # --------------------------------------------------------
    # Create lesson
    # --------------------------------------------------------

    lesson = Lesson(
        course_id=course_id,
        title=lesson_data.title,
        description=lesson_data.description,
        content=lesson_data.content,
        order=lesson_data.order,
        duration=lesson_data.duration,
    )

    db.add(lesson)

    try:
        db.commit()
        db.refresh(lesson)

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to create lesson: {str(exc)}",
        )

    return {
        "success": True,
        "message": "Lesson created successfully",
        "lesson": {
            "id": lesson.id,
            "course_id": lesson.course_id,
            "title": lesson.title,
            "description": lesson.description,
            "content": lesson.content,
            "order": lesson.order,
            "duration": lesson.duration,
        },
    }


# ============================================================
# GET ALL LESSONS FOR COURSE
# ============================================================

@router.get("/courses/{course_id}/lessons")
def get_course_lessons(
    course_id: int,
    db: Session = Depends(get_db),
):
    """
    Return all lessons belonging to a course.
    """

    if course_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid course ID",
        )

    # --------------------------------------------------------
    # Verify course exists
    # --------------------------------------------------------

    course = (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # --------------------------------------------------------
    # Get lessons
    # --------------------------------------------------------

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.course_id == course_id
        )
        .order_by(
            Lesson.order.asc(),
            Lesson.id.asc(),
        )
        .all()
    )

    return {
        "success": True,
        "course_id": course_id,
        "total_lessons": len(lessons),
        "lessons": [
            {
                "id": lesson.id,
                "course_id": lesson.course_id,
                "title": lesson.title,
                "description": lesson.description,
                "content": lesson.content,
                "order": lesson.order,
                "duration": lesson.duration,
            }
            for lesson in lessons
        ],
    }


# ============================================================
# GET LESSON BY ID
# ============================================================

@router.get("/lessons/{lesson_id}")
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a single lesson.
    """

    if lesson_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID",
        )

    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    return {
        "success": True,
        "lesson": {
            "id": lesson.id,
            "course_id": lesson.course_id,
            "title": lesson.title,
            "description": lesson.description,
            "content": lesson.content,
            "order": lesson.order,
            "duration": lesson.duration,
        },
    }


# ============================================================
# UPDATE LESSON
# ============================================================

@router.put("/lessons/{lesson_id}")
def update_lesson(
    lesson_id: int,
    lesson_data: LessonCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing lesson.
    """

    get_authenticated_user_id(current_user)

    if lesson_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID",
        )

    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    lesson.title = lesson_data.title
    lesson.description = lesson_data.description
    lesson.content = lesson_data.content
    lesson.order = lesson_data.order
    lesson.duration = lesson_data.duration

    try:
        db.commit()
        db.refresh(lesson)

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update lesson: {str(exc)}",
        )

    return {
        "success": True,
        "message": "Lesson updated successfully",
        "lesson": {
            "id": lesson.id,
            "course_id": lesson.course_id,
            "title": lesson.title,
            "description": lesson.description,
            "content": lesson.content,
            "order": lesson.order,
            "duration": lesson.duration,
        },
    }


# ============================================================
# DELETE LESSON
# ============================================================

@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a lesson.
    """

    get_authenticated_user_id(current_user)

    if lesson_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid lesson ID",
        )

    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    db.delete(lesson)

    try:
        db.commit()

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete lesson: {str(exc)}",
        )

    return {
        "success": True,
        "message": "Lesson deleted successfully",
        "lesson_id": lesson_id,
    }