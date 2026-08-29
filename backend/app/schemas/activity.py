from pydantic import BaseModel


class ActivityCreate(BaseModel):
    activity_type: str
    course_id: int | None = None
    description: str


class ActivityResponse(BaseModel):
    id: int
    user_id: int
    activity_type: str
    course_id: int | None
    description: str