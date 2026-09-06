-- ============================================================
-- AI QUANTUM LEARNING PLATFORM
-- Initial Database Schema
-- Version: 001
-- ============================================================

-- ============================================================
-- 1. USERS
-- ============================================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'student',
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),

    xp_points INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    learning_streak INTEGER NOT NULL DEFAULT 0,

    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_activity_date DATETIME
);

CREATE INDEX idx_users_email ON users(email);


-- ============================================================
-- 2. COURSES
-- ============================================================

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    level VARCHAR(50),
    duration VARCHAR(100),
    category VARCHAR(100)
);


-- ============================================================
-- 3. LESSONS
-- ============================================================

CREATE TABLE lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT,

    "order" INTEGER NOT NULL DEFAULT 0,
    duration INTEGER,

    FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_lessons_course_id ON lessons(course_id);


-- ============================================================
-- 4. ENROLLMENTS
-- ============================================================

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,

    status VARCHAR(50) NOT NULL DEFAULT 'active',

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE,

    UNIQUE(user_id, course_id)
);

CREATE INDEX idx_enrollments_user_id ON enrollments(user_id);
CREATE INDEX idx_enrollments_course_id ON enrollments(course_id);


-- ============================================================
-- 5. COURSE PROGRESS
-- ============================================================

CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,

    completion_percentage REAL NOT NULL DEFAULT 0,
    completed_lessons INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'not_started',

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE,

    UNIQUE(user_id, course_id)
);

CREATE INDEX idx_progress_user_id ON progress(user_id);


-- ============================================================
-- 6. SKILL PROGRESS
-- ============================================================

CREATE TABLE skill_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    skill_name VARCHAR(255) NOT NULL,
    progress_percentage REAL NOT NULL DEFAULT 0,

    completed_lessons INTEGER NOT NULL DEFAULT 0,
    total_lessons INTEGER NOT NULL DEFAULT 0,

    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE(user_id, skill_name)
);

CREATE INDEX idx_skill_progress_user_id
    ON skill_progress(user_id);


-- ============================================================
-- 7. CHALLENGES
-- ============================================================

CREATE TABLE challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title VARCHAR(255) NOT NULL,
    description TEXT,

    skill_name VARCHAR(255),
    difficulty VARCHAR(50),

    xp_reward INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1
);


-- ============================================================
-- 8. CHALLENGE PROGRESS
-- ============================================================

CREATE TABLE challenge_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,
    challenge_id INTEGER NOT NULL,

    status VARCHAR(50) NOT NULL DEFAULT 'not_started',
    score INTEGER NOT NULL DEFAULT 0,

    completed_at DATETIME,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (challenge_id)
        REFERENCES challenges(id)
        ON DELETE CASCADE,

    UNIQUE(user_id, challenge_id)
);

CREATE INDEX idx_challenge_progress_user_id
    ON challenge_progress(user_id);


-- ============================================================
-- 9. CIRCUITS
-- ============================================================

CREATE TABLE circuits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- JSON stored as TEXT for SQLite compatibility
    circuit_data TEXT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_circuits_user_id
    ON circuits(user_id);


-- ============================================================
-- 10. SIMULATIONS
-- ============================================================

CREATE TABLE simulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,
    circuit_id INTEGER,

    job_id VARCHAR(255) NOT NULL UNIQUE,

    backend VARCHAR(100),
    shots INTEGER NOT NULL DEFAULT 1000,

    status VARCHAR(50) NOT NULL DEFAULT 'pending',

    -- Complete simulation result stored as JSON text
    result_data TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (circuit_id)
        REFERENCES circuits(id)
        ON DELETE SET NULL
);

CREATE INDEX idx_simulations_user_id
    ON simulations(user_id);

CREATE INDEX idx_simulations_circuit_id
    ON simulations(circuit_id);


-- ============================================================
-- 11. ACTIVITIES
-- ============================================================

CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    activity_type VARCHAR(100) NOT NULL,

    course_id INTEGER,
    description TEXT,

    xp_earned INTEGER NOT NULL DEFAULT 0,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE SET NULL
);

CREATE INDEX idx_activities_user_id
    ON activities(user_id);

CREATE INDEX idx_activities_created_at
    ON activities(created_at);


-- ============================================================
-- 12. ACHIEVEMENTS
-- ============================================================

CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,

    badge_icon VARCHAR(500),

    xp_reward INTEGER NOT NULL DEFAULT 0
);


-- ============================================================
-- 13. USER ACHIEVEMENTS
-- ============================================================

CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,

    earned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (achievement_id)
        REFERENCES achievements(id)
        ON DELETE CASCADE,

    UNIQUE(user_id, achievement_id)
);

CREATE INDEX idx_user_achievements_user_id
    ON user_achievements(user_id);


-- ============================================================
-- END OF INITIAL SCHEMA
-- ============================================================