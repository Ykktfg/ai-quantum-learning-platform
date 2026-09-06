-- ============================================================
-- AI QUANTUM LEARNING PLATFORM
-- AI Persistence Schema
-- Version: 002
-- ============================================================


-- ============================================================
-- 1. AI CONVERSATIONS
-- ============================================================

CREATE TABLE ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    title VARCHAR(255),
    context_type VARCHAR(100),

    circuit_id INTEGER,
    lesson_id INTEGER,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (circuit_id)
        REFERENCES circuits(id)
        ON DELETE SET NULL,

    FOREIGN KEY (lesson_id)
        REFERENCES lessons(id)
        ON DELETE SET NULL
);

CREATE INDEX idx_ai_conversations_user_id
    ON ai_conversations(user_id);

CREATE INDEX idx_ai_conversations_circuit_id
    ON ai_conversations(circuit_id);


-- ============================================================
-- 2. AI MESSAGES
-- ============================================================

CREATE TABLE ai_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    conversation_id INTEGER NOT NULL,

    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id)
        REFERENCES ai_conversations(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_ai_messages_conversation_id
    ON ai_messages(conversation_id);

CREATE INDEX idx_ai_messages_created_at
    ON ai_messages(created_at);


-- ============================================================
-- 3. AI CODE GENERATIONS
-- ============================================================

CREATE TABLE ai_code_generations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    request TEXT NOT NULL,
    generated_code TEXT,

    validation_status VARCHAR(50),
    validation_error TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_ai_code_generations_user_id
    ON ai_code_generations(user_id);


-- ============================================================
-- 4. AI DEBUG SESSIONS
-- ============================================================

CREATE TABLE ai_debug_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    circuit_id INTEGER,

    code TEXT,
    reported_error TEXT,

    validation_status VARCHAR(50),
    simulation_status VARCHAR(50),

    ai_explanation TEXT,
    corrected_code TEXT,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (circuit_id)
        REFERENCES circuits(id)
        ON DELETE SET NULL
);

CREATE INDEX idx_ai_debug_sessions_user_id
    ON ai_debug_sessions(user_id);

CREATE INDEX idx_ai_debug_sessions_circuit_id
    ON ai_debug_sessions(circuit_id);


-- ============================================================
-- 5. AI CIRCUIT EXPLANATIONS
-- ============================================================

CREATE TABLE ai_circuit_explanations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    circuit_id INTEGER,
    simulation_id INTEGER,

    question TEXT,
    explanation TEXT NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (circuit_id)
        REFERENCES circuits(id)
        ON DELETE SET NULL,

    FOREIGN KEY (simulation_id)
        REFERENCES simulations(id)
        ON DELETE SET NULL
);

CREATE INDEX idx_ai_circuit_explanations_user_id
    ON ai_circuit_explanations(user_id);

CREATE INDEX idx_ai_circuit_explanations_circuit_id
    ON ai_circuit_explanations(circuit_id);


-- ============================================================
-- END OF AI SCHEMA
-- ============================================================