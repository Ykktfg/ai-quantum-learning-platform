from typing import List

from pydantic import BaseModel


# ============================================================
# DASHBOARD USER
# ============================================================

class DashboardUser(BaseModel):
    id: int
    name: str
    email: str
    role: str


# ============================================================
# DASHBOARD STATS
# ============================================================

class DashboardStats(BaseModel):
    courses_enrolled: int
    courses_completed: int
    overall_progress: float
    circuits_created: int
    simulations_run: int


# ============================================================
# RECENT PROGRESS
# ============================================================

class RecentProgress(BaseModel):
    course_id: int
    course_title: str
    completion_percentage: float
    completed_lessons: int
    status: str


# ============================================================
# DASHBOARD RESPONSE
# ============================================================

class DashboardResponse(BaseModel):
    user: DashboardUser
    stats: DashboardStats
    recent_progress: List[RecentProgress]
    message: str