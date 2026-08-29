from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
)

from app.db.database import Base


# ============================================================
# USER MODEL
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    name = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
        default="student",
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    # ========================================================
    # PROFILE
    # ========================================================

    avatar_url = Column(
        String,
        nullable=True,
    )

    joined_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # ========================================================
    # GAMIFICATION
    # ========================================================

    xp_points = Column(
        Integer,
        nullable=False,
        default=0,
    )

    level = Column(
        Integer,
        nullable=False,
        default=1,
    )

    learning_streak = Column(
        Integer,
        nullable=False,
        default=0,
    )

    last_activity_date = Column(
        DateTime,
        nullable=True,
    )


# ============================================================
# COURSE MODEL
# ============================================================

class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    level = Column(
        String,
        nullable=False,
        default="beginner",
    )

    duration = Column(
        String,
        nullable=False,
    )

    category = Column(
        String,
        nullable=False,
        default="quantum-computing",
    )


# ============================================================
# LESSON MODEL
# ============================================================

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    content = Column(
        Text,
        nullable=False,
    )

    order = Column(
        Integer,
        nullable=False,
        default=1,
    )

    duration = Column(
        String,
        nullable=True,
    )


# ============================================================
# ENROLLMENT MODEL
# ============================================================

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="active",
    )


# ============================================================
# PROGRESS MODEL
# ============================================================

class Progress(Base):
    __tablename__ = "progress"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    completion_percentage = Column(
        Float,
        nullable=False,
        default=0,
    )

    completed_lessons = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String,
        nullable=False,
        default="not_started",
    )


# ============================================================
# SKILL PROGRESS MODEL
# ============================================================

class SkillProgress(Base):
    __tablename__ = "skill_progress"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    skill_name = Column(
        String,
        nullable=False,
        index=True,
    )

    progress_percentage = Column(
        Float,
        nullable=False,
        default=0,
    )

    completed_lessons = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_lessons = Column(
        Integer,
        nullable=False,
        default=0,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


# ============================================================
# CHALLENGE MODEL
# ============================================================

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    skill_name = Column(
        String,
        nullable=False,
        index=True,
    )

    difficulty = Column(
        String,
        nullable=False,
        default="beginner",
    )

    xp_reward = Column(
        Integer,
        nullable=False,
        default=10,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


# ============================================================
# CHALLENGE PROGRESS MODEL
# ============================================================

class ChallengeProgress(Base):
    __tablename__ = "challenge_progress"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    challenge_id = Column(
        Integer,
        ForeignKey("challenges.id"),
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="not_started",
    )

    score = Column(
        Float,
        nullable=False,
        default=0,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )


# ============================================================
# CIRCUIT MODEL
# ============================================================

class Circuit(Base):
    __tablename__ = "circuits"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    circuit_data = Column(
        Text,
        nullable=False,
    )


# ============================================================
# SIMULATION MODEL
# ============================================================

class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    circuit_id = Column(
        Integer,
        ForeignKey("circuits.id"),
        nullable=False,
        index=True,
    )

    job_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    backend = Column(
        String,
        nullable=False,
        default="qiskit",
    )

    shots = Column(
        Integer,
        nullable=False,
        default=1024,
    )

    status = Column(
        String,
        nullable=False,
        default="completed",
    )

    result_data = Column(
        Text,
        nullable=True,
    )


# ============================================================
# ACTIVITY MODEL
# ============================================================

class Activity(Base):
    __tablename__ = "activities"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    activity_type = Column(
        String,
        nullable=False,
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=True,
        index=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    xp_earned = Column(
        Integer,
        nullable=False,
        default=0,
    )


# ============================================================
# ACHIEVEMENT MODEL
# ============================================================

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
        unique=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    badge_icon = Column(
        String,
        nullable=True,
    )

    xp_reward = Column(
        Integer,
        nullable=False,
        default=0,
    )


# ============================================================
# USER ACHIEVEMENT MODEL
# ============================================================

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    achievement_id = Column(
        Integer,
        ForeignKey("achievements.id"),
        nullable=False,
        index=True,
    )

    earned_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )