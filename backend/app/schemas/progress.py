from typing import List

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# PROGRESS UPDATE SCHEMA
# ============================================================

class ProgressUpdate(BaseModel):
    """
    Request schema for creating or updating student progress.
    """

    course_id: int = Field(
        ...,
        gt=0,
        description="ID of the course"
    )

    completion_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Course completion percentage"
    )

    completed_lessons: int = Field(
        ...,
        ge=0,
        description="Number of completed lessons"
    )


# ============================================================
# PROGRESS RESPONSE SCHEMA
# ============================================================

class ProgressResponse(BaseModel):
    """
    Response schema returned by progress endpoints.
    """

    id: int
    user_id: int
    course_id: int

    completion_percentage: float
    completed_lessons: int

    status: str

    # Allow Pydantic to read data directly from
    # SQLAlchemy ORM objects.
    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# MY PROGRESS RESPONSE
# ============================================================

class MyProgressResponse(BaseModel):
    """
    Response schema for a user's complete progress list.
    """

    progress: List[ProgressResponse]

    total_courses: int
    completed_courses: int
    in_progress_courses: int
    not_started_courses: int