-- ============================================================================
-- VocalCraft Database Schema
-- Speech Therapy Application
-- Version: 1.0
-- ============================================================================

-- ============================================================================
-- DROP TABLES (Clean Install)
-- Run these to completely reset the database
-- ============================================================================

DROP TABLE IF EXISTS progress;
DROP TABLE IF EXISTS users;

-- Reset auto-increment sequences
DROP TABLE IF EXISTS sqlite_sequence;

-- ============================================================================
-- CREATE TABLES
-- ============================================================================

-- USERS TABLE
-- Stores user account information
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    condition TEXT DEFAULT 'Dysarthria',
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PROGRESS TABLE
-- Stores practice session history and scores
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exercise_type TEXT,
    score REAL,
    audio_path TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
);

-- ============================================================================
-- CREATE INDEXES
-- For faster query performance
-- ============================================================================

CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_progress_user ON progress (user_id);
CREATE INDEX idx_progress_date ON progress (date);
CREATE INDEX idx_progress_exercise ON progress (exercise_type);
CREATE INDEX idx_progress_score ON progress (score);

-- ============================================================================
-- CREATE VIEWS (Optional)
-- ============================================================================

-- User statistics view
CREATE VIEW IF NOT EXISTS user_stats AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(p.id) as total_sessions,
    ROUND(AVG(p.score), 1) as avg_score,
    MAX(p.score) as best_score,
    MIN(p.score) as lowest_score,
    MIN(p.date) as first_session,
    MAX(p.date) as last_session
FROM users u
LEFT JOIN progress p ON u.id = p.user_id
GROUP BY u.id;

-- Daily progress view
CREATE VIEW IF NOT EXISTS daily_progress AS
SELECT 
    user_id,
    date(date) as practice_date,
    COUNT(*) as session_count,
    ROUND(AVG(score), 1) as avg_score,
    MAX(score) as best_score
FROM progress
GROUP BY user_id, date(date);
