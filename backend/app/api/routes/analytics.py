from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.db.database import get_db

from app.db.models import (
    User,
    Course,
    Progress,
    Enrollment,
    Challenge,
    ChallengeProgress,
    SkillProgress,
    Achievement,
    UserAchievement,
    Activity,
)

from app.schemas.analytics import (
    AnalyticsResponse,
    AnalyticsUser,
    AnalyticsProgress,
    SkillAnalytics,
    AchievementAnalytics,
    ActivityAnalytics,
    WeakTopicAnalytics,
    LearningRecommendation,
)


router = APIRouter()


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_SKILLS = [
    "Quantum Fundamentals",
    "Superposition",
    "Quantum Gates",
    "Entanglement",
    "Circuit Design",
    "Quantum Algorithms",
]


# ============================================================
# HELPERS
# ============================================================

def get_user_id(current_user: dict) -> int:
    """
    Safely extract authenticated user ID from JWT payload.
    """

    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

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


def get_authenticated_user(
    current_user: dict,
    db: Session,
) -> User:
    """
    Return the currently authenticated database user.
    """

    user_id = get_user_id(current_user)

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# ============================================================
# COMPLETE ANALYTICS
# ============================================================

@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
)
def get_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return complete personalized analytics
    for the currently authenticated user.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    user_id = user.id

    # ========================================================
    # ENROLLMENTS / MODULES
    # ========================================================

    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.status == "active",
        )
        .all()
    )

    total_modules = len(enrollments)

    # ========================================================
    # COURSE PROGRESS
    # ========================================================

    progress_records = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
        )
        .all()
    )

    completed_modules = sum(
        1
        for progress in progress_records
        if progress.status == "completed"
        or float(progress.completion_percentage or 0) >= 100
    )

    in_progress_modules = sum(
        1
        for progress in progress_records
        if (
            float(progress.completion_percentage or 0) > 0
            and float(progress.completion_percentage or 0) < 100
        )
    )

    if progress_records:
        overall_progress = round(
            sum(
                min(
                    max(
                        float(progress.completion_percentage or 0),
                        0.0,
                    ),
                    100.0,
                )
                for progress in progress_records
            )
            / len(progress_records),
            2,
        )
    else:
        overall_progress = 0.0

    # ========================================================
    # CHALLENGES
    # ========================================================

    total_challenges = (
        db.query(Challenge)
        .filter(
            Challenge.is_active.is_(True)
        )
        .count()
    )

    completed_challenges = (
        db.query(ChallengeProgress)
        .filter(
            ChallengeProgress.user_id == user_id,
            ChallengeProgress.status == "completed",
        )
        .count()
    )

    # ========================================================
    # SKILL PROGRESS
    # ========================================================

    skill_records = (
        db.query(SkillProgress)
        .filter(
            SkillProgress.user_id == user_id,
        )
        .order_by(
            SkillProgress.skill_name
        )
        .all()
    )

    skill_map = {
        skill.skill_name: skill
        for skill in skill_records
    }

    skills: List[SkillAnalytics] = []

    # Always return the six platform skills.
    for skill_name in DEFAULT_SKILLS:

        skill = skill_map.get(skill_name)

        if skill is None:

            skills.append(
                SkillAnalytics(
                    skill_name=skill_name,
                    progress_percentage=0.0,
                    completed_lessons=0,
                    total_lessons=0,
                )
            )

        else:

            percentage = min(
                max(
                    float(
                        skill.progress_percentage or 0
                    ),
                    0.0,
                ),
                100.0,
            )

            skills.append(
                SkillAnalytics(
                    skill_name=skill.skill_name,
                    progress_percentage=percentage,
                    completed_lessons=int(
                        skill.completed_lessons or 0
                    ),
                    total_lessons=int(
                        skill.total_lessons or 0
                    ),
                )
            )

    # Include any additional custom skills.
    for skill in skill_records:

        if skill.skill_name in DEFAULT_SKILLS:
            continue

        percentage = min(
            max(
                float(
                    skill.progress_percentage or 0
                ),
                0.0,
            ),
            100.0,
        )

        skills.append(
            SkillAnalytics(
                skill_name=skill.skill_name,
                progress_percentage=percentage,
                completed_lessons=int(
                    skill.completed_lessons or 0
                ),
                total_lessons=int(
                    skill.total_lessons or 0
                ),
            )
        )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    all_achievements = (
        db.query(Achievement)
        .order_by(
            Achievement.id
        )
        .all()
    )

    user_achievements = (
        db.query(UserAchievement)
        .filter(
            UserAchievement.user_id == user_id
        )
        .order_by(
            UserAchievement.earned_at.desc()
        )
        .all()
    )

    earned_map = {}

    for user_achievement in user_achievements:

        # Keep the latest earned record if duplicates exist.
        if (
            user_achievement.achievement_id
            not in earned_map
        ):
            earned_map[
                user_achievement.achievement_id
            ] = user_achievement

    achievements: List[AchievementAnalytics] = []

    for achievement in all_achievements:

        user_achievement = earned_map.get(
            achievement.id
        )

        achievements.append(
            AchievementAnalytics(
                id=achievement.id,
                name=achievement.name,
                description=achievement.description,
                badge_icon=achievement.badge_icon,
                xp_reward=int(
                    achievement.xp_reward or 0
                ),
                earned=(
                    user_achievement is not None
                ),
                earned_at=(
                    user_achievement.earned_at
                    if user_achievement
                    else None
                ),
            )
        )

    # ========================================================
    # RECENT ACTIVITY
    # ========================================================

    activity_records = (
        db.query(Activity)
        .filter(
            Activity.user_id == user_id
        )
        .order_by(
            Activity.created_at.desc()
        )
        .limit(20)
        .all()
    )

    recent_activity: List[ActivityAnalytics] = []

    for activity in activity_records:

        # created_at is required by schema.
        # Database model also makes it non-nullable.
        if activity.created_at is None:
            continue

        recent_activity.append(
            ActivityAnalytics(
                id=activity.id,
                activity_type=activity.activity_type,
                course_id=activity.course_id,
                description=activity.description,
                created_at=activity.created_at,
                xp_earned=int(
                    activity.xp_earned or 0
                ),
            )
        )

    # ========================================================
    # WEAK TOPICS
    # ========================================================

    weak_topics: List[WeakTopicAnalytics] = []

    for skill in skills:

        percentage = float(
            skill.progress_percentage
        )

        if percentage < 50:

            if percentage < 25:

                reason = (
                    "Very low progress. "
                    "This topic needs immediate attention."
                )

            else:

                reason = (
                    "Progress is below 50%. "
                    "More practice is recommended."
                )

            weak_topics.append(
                WeakTopicAnalytics(
                    skill_name=skill.skill_name,
                    progress_percentage=percentage,
                    reason=reason,
                )
            )

    # Sort weakest skills first.
    weak_topics.sort(
        key=lambda item: item.progress_percentage
    )

    # ========================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================

    recommendations: List[
        LearningRecommendation
    ] = []

    # --------------------------------------------------------
    # Recommendations from weak skills
    # --------------------------------------------------------

    for weak_topic in weak_topics[:3]:

        if weak_topic.progress_percentage < 25:
            priority = "high"
        else:
            priority = "medium"

        recommendations.append(
            LearningRecommendation(
                title=(
                    f"Improve "
                    f"{weak_topic.skill_name}"
                ),
                description=(
                    f"Continue studying "
                    f"{weak_topic.skill_name} "
                    "and complete additional "
                    "lessons or challenges."
                ),
                skill_name=weak_topic.skill_name,
                priority=priority,
            )
        )

    # --------------------------------------------------------
    # Recommendation from incomplete course
    # --------------------------------------------------------

    incomplete_progress = [
        progress
        for progress in progress_records
        if float(
            progress.completion_percentage or 0
        ) < 100
    ]

    if incomplete_progress:

        incomplete_progress.sort(
            key=lambda item: float(
                item.completion_percentage or 0
            )
        )

        selected_progress = (
            incomplete_progress[0]
        )

        course = (
            db.query(Course)
            .filter(
                Course.id
                == selected_progress.course_id
            )
            .first()
        )

        if course:

            recommendations.append(
                LearningRecommendation(
                    title=(
                        f"Continue "
                        f"{course.title}"
                    ),
                    description=(
                        "Continue your existing "
                        "course progress to improve "
                        "your overall completion."
                    ),
                    skill_name=None,
                    priority="medium",
                )
            )

    # ========================================================
    # RETURN COMPLETE ANALYTICS
    # ========================================================

    return AnalyticsResponse(

        user=AnalyticsUser(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar_url=user.avatar_url,
            role=user.role,
            joined_at=user.joined_at,
        ),

        progress=AnalyticsProgress(
            overall_progress=overall_progress,

            completed_modules=completed_modules,
            total_modules=total_modules,

            completed_challenges=completed_challenges,
            total_challenges=total_challenges,

            xp_points=int(
                user.xp_points or 0
            ),

            level=int(
                user.level or 1
            ),

            learning_streak=int(
                user.learning_streak or 0
            ),
        ),

        skills=skills,

        achievements=achievements,

        recent_activity=recent_activity,

        weak_topics=weak_topics,

        recommendations=recommendations,
    )


# ============================================================
# PROFILE
# ============================================================

@router.get(
    "/analytics/profile",
)
def get_analytics_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return profile information for the logged-in user.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "role": user.role,
        "joined_at": user.joined_at,
        "xp_points": int(
            user.xp_points or 0
        ),
        "level": int(
            user.level or 1
        ),
        "learning_streak": int(
            user.learning_streak or 0
        ),
    }


# ============================================================
# SKILLS
# ============================================================

@router.get(
    "/analytics/skills",
)
def get_skill_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return skill-wise progress for the logged-in user.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    skill_records = (
        db.query(SkillProgress)
        .filter(
            SkillProgress.user_id == user.id
        )
        .order_by(
            SkillProgress.skill_name
        )
        .all()
    )

    skill_map = {
        skill.skill_name: skill
        for skill in skill_records
    }

    skills = []

    # Always return standard platform skills.
    for skill_name in DEFAULT_SKILLS:

        skill = skill_map.get(skill_name)

        if skill is None:

            skills.append(
                {
                    "skill_name": skill_name,
                    "progress_percentage": 0.0,
                    "completed_lessons": 0,
                    "total_lessons": 0,
                }
            )

        else:

            skills.append(
                {
                    "skill_name": skill.skill_name,
                    "progress_percentage": min(
                        max(
                            float(
                                skill.progress_percentage
                                or 0
                            ),
                            0.0,
                        ),
                        100.0,
                    ),
                    "completed_lessons": int(
                        skill.completed_lessons or 0
                    ),
                    "total_lessons": int(
                        skill.total_lessons or 0
                    ),
                }
            )

    return {
        "skills": skills
    }


# ============================================================
# ACHIEVEMENTS
# ============================================================

@router.get(
    "/analytics/achievements",
)
def get_achievement_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all achievements and whether the
    logged-in user has earned them.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    achievements = (
        db.query(Achievement)
        .order_by(
            Achievement.id
        )
        .all()
    )

    user_achievements = (
        db.query(UserAchievement)
        .filter(
            UserAchievement.user_id == user.id
        )
        .order_by(
            UserAchievement.earned_at.desc()
        )
        .all()
    )

    earned_map = {}

    for user_achievement in user_achievements:

        if (
            user_achievement.achievement_id
            not in earned_map
        ):
            earned_map[
                user_achievement.achievement_id
            ] = user_achievement

    return {
        "achievements": [
            {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "badge_icon": achievement.badge_icon,
                "xp_reward": int(
                    achievement.xp_reward or 0
                ),
                "earned": (
                    achievement.id
                    in earned_map
                ),
                "earned_at": (
                    earned_map[
                        achievement.id
                    ].earned_at
                    if achievement.id
                    in earned_map
                    else None
                ),
            }
            for achievement in achievements
        ]
    }


# ============================================================
# RECENT ACTIVITY
# ============================================================

@router.get(
    "/analytics/activity",
)
def get_activity_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return the latest 20 learning activities
    for the logged-in user.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    activities = (
        db.query(Activity)
        .filter(
            Activity.user_id == user.id
        )
        .order_by(
            Activity.created_at.desc()
        )
        .limit(20)
        .all()
    )

    return {
        "activities": [
            {
                "id": activity.id,
                "activity_type": activity.activity_type,
                "course_id": activity.course_id,
                "description": activity.description,
                "created_at": activity.created_at,
                "xp_earned": int(
                    activity.xp_earned or 0
                ),
            }
            for activity in activities
            if activity.created_at is not None
        ]
    }


# ============================================================
# WEAK TOPICS
# ============================================================

@router.get(
    "/analytics/weak-topics",
)
def get_weak_topics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return skills where progress is below 50%.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    skills = (
        db.query(SkillProgress)
        .filter(
            SkillProgress.user_id == user.id
        )
        .all()
    )

    weak_topics = []

    for skill in skills:

        percentage = min(
            max(
                float(
                    skill.progress_percentage or 0
                ),
                0.0,
            ),
            100.0,
        )

        if percentage < 50:

            if percentage < 25:

                reason = (
                    "Very low progress. "
                    "This topic needs immediate attention."
                )

            else:

                reason = (
                    "Progress is below 50%. "
                    "More practice is recommended."
                )

            weak_topics.append(
                {
                    "skill_name": skill.skill_name,
                    "progress_percentage": percentage,
                    "reason": reason,
                }
            )

    weak_topics.sort(
        key=lambda item: item[
            "progress_percentage"
        ]
    )

    return {
        "weak_topics": weak_topics
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

@router.get(
    "/analytics/recommendations",
)
def get_recommendations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return personalized learning recommendations.
    """

    user = get_authenticated_user(
        current_user=current_user,
        db=db,
    )

    skills = (
        db.query(SkillProgress)
        .filter(
            SkillProgress.user_id == user.id
        )
        .order_by(
            SkillProgress.progress_percentage.asc()
        )
        .all()
    )

    recommendations = []

    for skill in skills:

        percentage = float(
            skill.progress_percentage or 0
        )

        if percentage >= 50:
            continue

        if percentage < 25:
            priority = "high"
        else:
            priority = "medium"

        recommendations.append(
            {
                "title": (
                    f"Improve "
                    f"{skill.skill_name}"
                ),
                "description": (
                    f"Practice more "
                    f"{skill.skill_name} "
                    "lessons and challenges."
                ),
                "skill_name": skill.skill_name,
                "priority": priority,
            }
        )

        if len(recommendations) >= 3:
            break

    return {
        "recommendations": recommendations
    }