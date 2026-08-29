from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ============================================================
# PROFILE
# ============================================================

class AnalyticsUser(BaseModel):
    id: int
    name: str
    email: str
    avatar_url: Optional[str] = None
    role: str
    joined_at: Optional[datetime] = None


# ============================================================
# OVERALL PROGRESS
# ============================================================

class AnalyticsProgress(BaseModel):
    overall_progress: float

    completed_modules: int
    total_modules: int

    completed_challenges: int
    total_challenges: int

    xp_points: int
    level: int
    learning_streak: int


# ============================================================
# SKILL PROGRESS
# ============================================================

class SkillAnalytics(BaseModel):
    skill_name: str
    progress_percentage: float
    completed_lessons: int
    total_lessons: int


# ============================================================
# ACHIEVEMENTS
# ============================================================

class AchievementAnalytics(BaseModel):
    id: int
    name: str
    description: str
    badge_icon: Optional[str] = None
    xp_reward: int
    earned_at: Optional[datetime] = None
    earned: bool


# ============================================================
# LEARNING ACTIVITY
# ============================================================

class ActivityAnalytics(BaseModel):
    id: int
    activity_type: str
    course_id: Optional[int] = None
    description: str
    created_at: datetime
    xp_earned: int


# ============================================================
# WEAK TOPIC
# ============================================================

class WeakTopicAnalytics(BaseModel):
    skill_name: str
    progress_percentage: float
    reason: str


# ============================================================
# RECOMMENDATION
# ============================================================

class LearningRecommendation(BaseModel):
    title: str
    description: str
    skill_name: Optional[str] = None
    priority: str


# ============================================================
# COMPLETE ANALYTICS RESPONSE
# ============================================================

class AnalyticsResponse(BaseModel):
    user: AnalyticsUser
    progress: AnalyticsProgress

    skills: List[SkillAnalytics]

    achievements: List[AchievementAnalytics]

    recent_activity: List[ActivityAnalytics]

    weak_topics: List[WeakTopicAnalytics]

    recommendations: List[LearningRecommendation]