-- ============================================================
-- AI QUANTUM LEARNING PLATFORM
-- AI Persistence Schema
-- Version: 002
-- ============================================================

CREATE TABLE ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(255),
    context_type VARCHAR(255),
    circuit_id INTEGER,
    lesson_id INTEGER,
    created_at DATETIME,
    updated_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (circuit_id) REFERENCES circuits(id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE INDEX idx_ai_conversations_user_id
    ON ai_conversations(user_id);

CREATE INDEX idx_ai_conversations_circuit_id
    ON ai_conversations(circuit_id);

CREATE INDEX idx_ai_conversations_lesson_id
    ON ai_conversations(lesson_id);


CREATE TABLE ai_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME,

    FOREIGN KEY (conversation_id)
        REFERENCES ai_conversations(id)
);


CREATE INDEX idx_ai_messages_conversation_id
    ON ai_messages(conversation_id);


CREATE TABLE ai_code_generations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    request TEXT NOT NULL,
    generated_code TEXT NOT NULL,
    validation_status VARCHAR(255),
    validation_error TEXT,
    timestamp DATETIME,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
);


CREATE INDEX idx_ai_code_generations_user_id
    ON ai_code_generations(user_id);


CREATE TABLE ai_debug_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    circuit_id INTEGER,
    code TEXT,
    reported_error TEXT,
    validation_status VARCHAR(255),
    simulation_status VARCHAR(255),
    ai_explanation TEXT,
    corrected_code TEXT,
    timestamp DATETIME,

    FOREIGN KEY (user_id)
        REFERENCES users(id),
    FOREIGN KEY (circuit_id)
        REFERENCES circuits(id)
);


CREATE INDEX idx_ai_debug_sessions_user_id
    ON ai_debug_sessions(user_id);

CREATE INDEX idx_ai_debug_sessions_circuit_id
    ON ai_debug_sessions(circuit_id);


CREATE TABLE ai_circuit_explanations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    circuit_id INTEGER,
    simulation_id INTEGER,
    question TEXT NOT NULL,
    explanation TEXT NOT NULL,
    timestamp DATETIME,

    FOREIGN KEY (user_id)
        REFERENCES users(id),
    FOREIGN KEY (circuit_id)
        REFERENCES circuits(id),
    FOREIGN KEY (simulation_id)
        REFERENCES simulations(id)
);


CREATE INDEX idx_ai_circuit_explanations_user_id
    ON ai_circuit_explanations(user_id);

CREATE INDEX idx_ai_circuit_explanations_circuit_id
    ON ai_circuit_explanations(circuit_id);

CREATE INDEX idx_ai_circuit_explanations_simulation_id
    ON ai_circuit_explanations(simulation_id);


-- ============================================================
-- END OF AI SCHEMA
-- ============================================================