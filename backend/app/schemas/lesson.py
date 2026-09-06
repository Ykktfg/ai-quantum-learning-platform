from pydantic import BaseModel, Field


# ============================================================
# CREATE LESSON
# ============================================================

class LessonCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str | None = None

    content: str = Field(
        min_length=1,
    )

    order: int = Field(
        default=1,
        ge=1,
    )

    duration: str | None = None


# ============================================================
# LESSON RESPONSE
# ============================================================

class LessonResponse(BaseModel):

    id: int

    course_id: int

    title: str

    description: str | None

    content: str

    order: int

    duration: str | None