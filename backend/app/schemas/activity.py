from pydantic import BaseModel


class ActivityCreate(BaseModel):
    activity_type: str
    course_id: int | None = None
    description: str
    xp_earned: int = 0


class ActivityResponse(BaseModel):
    id: int
    user_id: int
    activity_type: str
    course_id: int | None
    description: str
    xp_earned: int