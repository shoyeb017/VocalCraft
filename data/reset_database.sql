-- ============================================================================
-- VocalCraft Database Reset Script
-- WARNING: This will DELETE ALL DATA!
-- ============================================================================

-- Step 1: Drop all tables
DROP TABLE IF EXISTS progress;
DROP TABLE IF EXISTS users;

-- Step 2: Drop views
DROP VIEW IF EXISTS user_stats;
DROP VIEW IF EXISTS daily_progress;

-- Step 3: Recreate users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    condition TEXT DEFAULT 'Dysarthria',
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 4: Recreate progress table
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

-- Step 5: Recreate indexes
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_progress_user ON progress (user_id);
CREATE INDEX idx_progress_date ON progress (date);
CREATE INDEX idx_progress_exercise ON progress (exercise_type);
CREATE INDEX idx_progress_score ON progress (score);

-- Step 6: Optimize
VACUUM;

-- Done! Database is now empty and ready for use.
