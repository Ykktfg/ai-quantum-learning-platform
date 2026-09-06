-- ============================================================
-- AI QUANTUM LEARNING PLATFORM
-- Initial Database Schema
-- Version: 001
-- ============================================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'student',
    password_hash VARCHAR NOT NULL,
    avatar_url VARCHAR,
    joined_at DATETIME,
    xp_points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    learning_streak INTEGER DEFAULT 0,
    last_activity_date DATETIME
);

CREATE INDEX ix_users_id ON users(id);
CREATE INDEX ix_users_email ON users(email);


CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    level VARCHAR DEFAULT 'beginner',
    duration VARCHAR NOT NULL,
    category VARCHAR DEFAULT 'quantum-computing'
);

CREATE INDEX ix_courses_id ON courses(id);


CREATE TABLE lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    content VARCHAR NOT NULL,
    "order" INTEGER DEFAULT 1,
    duration VARCHAR,

    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE INDEX ix_lessons_id ON lessons(id);
CREATE INDEX ix_lessons_course_id ON lessons(course_id);


CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    status VARCHAR DEFAULT 'active',

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE INDEX ix_enrollments_id ON enrollments(id);
CREATE INDEX ix_enrollments_user_id ON enrollments(user_id);
CREATE INDEX ix_enrollments_course_id ON enrollments(course_id);


CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    completion_percentage FLOAT DEFAULT 0,
    completed_lessons INTEGER DEFAULT 0,
    status VARCHAR DEFAULT 'not_started',

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE INDEX ix_progress_id ON progress(id);
CREATE INDEX ix_progress_user_id ON progress(user_id);
CREATE INDEX ix_progress_course_id ON progress(course_id);


CREATE TABLE skill_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name VARCHAR NOT NULL,
    progress_percentage FLOAT DEFAULT 0,
    completed_lessons INTEGER DEFAULT 0,
    total_lessons INTEGER DEFAULT 0,
    updated_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX ix_skill_progress_id ON skill_progress(id);
CREATE INDEX ix_skill_progress_user_id ON skill_progress(user_id);
CREATE INDEX ix_skill_progress_skill_name ON skill_progress(skill_name);


CREATE TABLE challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description VARCHAR,
    skill_name VARCHAR,
    difficulty VARCHAR DEFAULT 'beginner',
    xp_reward INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT 1
);

CREATE INDEX ix_challenges_id ON challenges(id);
CREATE INDEX ix_challenges_skill_name ON challenges(skill_name);


CREATE TABLE challenge_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    challenge_id INTEGER NOT NULL,
    status VARCHAR DEFAULT 'not_started',
    score FLOAT DEFAULT 0,
    completed_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

CREATE INDEX ix_challenge_progress_id ON challenge_progress(id);
CREATE INDEX ix_challenge_progress_user_id ON challenge_progress(user_id);
CREATE INDEX ix_challenge_progress_challenge_id ON challenge_progress(challenge_id);


CREATE TABLE circuits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    description VARCHAR,
    circuit_data VARCHAR NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX ix_circuits_id ON circuits(id);
CREATE INDEX ix_circuits_user_id ON circuits(user_id);


CREATE TABLE simulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    circuit_id INTEGER NOT NULL,
    job_id VARCHAR NOT NULL UNIQUE,
    backend VARCHAR DEFAULT 'qiskit',
    shots INTEGER DEFAULT 1024,
    status VARCHAR DEFAULT 'completed',
    result_data VARCHAR,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (circuit_id) REFERENCES circuits(id)
);

CREATE INDEX ix_simulations_id ON simulations(id);
CREATE INDEX ix_simulations_user_id ON simulations(user_id);
CREATE INDEX ix_simulations_job_id ON simulations(job_id);


CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR NOT NULL,
    course_id INTEGER,
    description VARCHAR NOT NULL,
    created_at DATETIME,
    xp_earned INTEGER DEFAULT 0,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE INDEX ix_activities_id ON activities(id);
CREATE INDEX ix_activities_user_id ON activities(user_id);
CREATE INDEX ix_activities_created_at ON activities(created_at);


CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR NOT NULL,
    badge_icon VARCHAR,
    xp_reward INTEGER DEFAULT 0
);

CREATE INDEX ix_achievements_id ON achievements(id);


CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    earned_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
);

CREATE INDEX ix_user_achievements_id ON user_achievements(id);
CREATE INDEX ix_user_achievements_user_id ON user_achievements(user_id);


-- ============================================================
-- END OF INITIAL SCHEMA
-- ============================================================