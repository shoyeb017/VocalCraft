-- ============================================================================
-- VocalCraft SQL Queries Reference
-- All common queries for the application
-- ============================================================================


-- ############################################################################
-- USER MANAGEMENT QUERIES
-- ############################################################################

-- INSERT: Register new user
INSERT INTO users (username, password, age, condition)
VALUES (?, ?, ?, ?);

-- SELECT: Get user by ID
SELECT id, username, age, condition, join_date 
FROM users 
WHERE id = ?;

-- SELECT: Get user by username
SELECT id, username, password, age, condition, join_date 
FROM users 
WHERE username = ?;

-- SELECT: Check if username exists
SELECT COUNT(*) as count FROM users WHERE username = ?;

-- SELECT: Get all users
SELECT id, username, age, condition, join_date 
FROM users 
ORDER BY join_date DESC;

-- UPDATE: Update user info
UPDATE users 
SET age = ?, condition = ?
WHERE id = ?;

-- UPDATE: Change password
UPDATE users 
SET password = ?
WHERE id = ?;

-- DELETE: Delete user (cascades to progress)
DELETE FROM users WHERE id = ?;


-- ############################################################################
-- PROGRESS/SESSION QUERIES
-- ############################################################################

-- INSERT: Save new session
INSERT INTO progress (user_id, score, audio_path, exercise_type)
VALUES (?, ?, ?, ?);

-- SELECT: Get all attempts for user
SELECT id, date, exercise_type, score, audio_path
FROM progress
WHERE user_id = ?
ORDER BY date DESC
LIMIT ?;

-- SELECT: Get user progress history
SELECT date, score, exercise_type 
FROM progress 
WHERE user_id = ? 
ORDER BY date ASC;

-- SELECT: Get recent sessions
SELECT id, date, exercise_type, score, audio_path
FROM progress 
WHERE user_id = ? 
ORDER BY date DESC
LIMIT ?;

-- DELETE: Delete specific session
DELETE FROM progress WHERE id = ?;

-- DELETE: Delete all sessions for user
DELETE FROM progress WHERE user_id = ?;


-- ############################################################################
-- STATISTICS QUERIES
-- ############################################################################

-- SELECT: Get user basic stats
SELECT 
    COUNT(*) as total_sessions,
    ROUND(AVG(score), 1) as average_score,
    MAX(score) as best_score,
    MIN(score) as lowest_score
FROM progress
WHERE user_id = ?;

-- SELECT: Get overall stats with dates
SELECT 
    COUNT(*) as total,
    AVG(score) as avg_score,
    MAX(score) as best,
    MIN(score) as worst,
    MIN(date) as first_date,
    MAX(date) as last_date
FROM progress
WHERE user_id = ?;

-- SELECT: Get category breakdown
SELECT 
    exercise_type, 
    COUNT(*) as count
FROM progress
WHERE user_id = ? AND exercise_type IS NOT NULL
GROUP BY exercise_type
ORDER BY count DESC;

-- SELECT: Get total practice time (estimated)
SELECT COUNT(*) as session_count
FROM progress
WHERE user_id = ?;

-- SELECT: Get daily averages (last N days)
SELECT 
    date(date) as practice_date,
    AVG(score) as avg_score
FROM progress
WHERE user_id = ?
AND date >= datetime('now', '-30 days')
GROUP BY date(date)
ORDER BY practice_date ASC;

-- SELECT: Sessions this week
SELECT COUNT(*) 
FROM progress 
WHERE user_id = ? 
AND date >= DATE('now', '-7 days');

-- SELECT: Get practice streak (distinct days)
SELECT DISTINCT date(date) as practice_date
FROM progress
WHERE user_id = ?
ORDER BY practice_date DESC;

-- SELECT: Last week average
SELECT AVG(score) 
FROM progress 
WHERE user_id = ? 
AND date >= datetime('now', '-7 days');

-- SELECT: First week average
SELECT AVG(score) 
FROM progress 
WHERE user_id = ? 
AND date <= datetime(?, '+7 days');


-- ############################################################################
-- DATA CLEANUP / DELETE QUERIES
-- ############################################################################

-- DELETE: Clear all progress data
DELETE FROM progress;

-- DELETE: Clear all users (will cascade to progress)
DELETE FROM users;

-- DELETE: Clear both tables
DELETE FROM progress;
DELETE FROM users;

-- DELETE: Reset auto-increment counters
DELETE FROM sqlite_sequence WHERE name = 'users';
DELETE FROM sqlite_sequence WHERE name = 'progress';

-- DELETE: Remove old sessions (older than 90 days)
DELETE FROM progress 
WHERE date < datetime('now', '-90 days');

-- DELETE: Remove low score sessions (optional cleanup)
DELETE FROM progress 
WHERE score < 10 AND user_id = ?;

-- DELETE: Remove orphaned progress (no matching user)
DELETE FROM progress 
WHERE user_id NOT IN (SELECT id FROM users);


-- ############################################################################
-- MAINTENANCE QUERIES
-- ############################################################################

-- Count records in each table
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM progress) as total_sessions;

-- Find orphaned records
SELECT p.* FROM progress p
LEFT JOIN users u ON p.user_id = u.id
WHERE u.id IS NULL;

-- Check table structure
PRAGMA table_info(users);
PRAGMA table_info(progress);

-- Check indexes
PRAGMA index_list(users);
PRAGMA index_list(progress);

-- Optimize database storage
VACUUM;

-- Analyze for query optimization
ANALYZE;


-- ############################################################################
-- REPORTING QUERIES
-- ############################################################################

-- Monthly summary
SELECT 
    strftime('%Y-%m', date) as month,
    COUNT(*) as total_sessions,
    COUNT(DISTINCT user_id) as active_users,
    ROUND(AVG(score), 1) as avg_score,
    MAX(score) as best_score
FROM progress
GROUP BY strftime('%Y-%m', date)
ORDER BY month DESC;

-- Weekly activity report
SELECT 
    strftime('%Y-W%W', date) as week,
    COUNT(*) as sessions,
    COUNT(DISTINCT user_id) as users,
    ROUND(AVG(score), 1) as avg_score
FROM progress
GROUP BY strftime('%Y-W%W', date)
ORDER BY week DESC
LIMIT 12;

-- Top performers (leaderboard)
SELECT 
    u.username,
    COUNT(p.id) as total_sessions,
    ROUND(AVG(p.score), 1) as avg_score,
    MAX(p.score) as best_score
FROM users u
JOIN progress p ON u.id = p.user_id
GROUP BY u.id
HAVING total_sessions >= 5
ORDER BY avg_score DESC
LIMIT 10;

-- Most practiced categories
SELECT 
    exercise_type,
    COUNT(*) as total_attempts,
    COUNT(DISTINCT user_id) as unique_users,
    ROUND(AVG(score), 1) as avg_score
FROM progress
WHERE exercise_type IS NOT NULL
GROUP BY exercise_type
ORDER BY total_attempts DESC;

-- Export data as CSV format
SELECT 
    u.username,
    p.date,
    p.exercise_type,
    p.score,
    p.audio_path
FROM progress p
JOIN users u ON p.user_id = u.id
ORDER BY p.date DESC;
