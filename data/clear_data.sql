-- ============================================================================
-- VocalCraft Data Clearing Scripts
-- Choose the appropriate section based on what you want to delete
-- ============================================================================


-- ############################################################################
-- OPTION 1: CLEAR ALL DATA (Keep Tables)
-- Removes all data but keeps table structure
-- ############################################################################

DELETE FROM progress;
DELETE FROM users;

-- Reset auto-increment to start from 1
DELETE FROM sqlite_sequence WHERE name = 'users';
DELETE FROM sqlite_sequence WHERE name = 'progress';


-- ############################################################################
-- OPTION 2: CLEAR PROGRESS ONLY (Keep Users)
-- Removes all session history but keeps user accounts
-- ############################################################################

DELETE FROM progress;
DELETE FROM sqlite_sequence WHERE name = 'progress';


-- ############################################################################
-- OPTION 3: CLEAR SPECIFIC USER DATA
-- Replace ? with user_id
-- ############################################################################

-- Delete all progress for a specific user
DELETE FROM progress WHERE user_id = ?;

-- Delete user and their progress (cascades)
DELETE FROM users WHERE id = ?;

-- Delete user by username
DELETE FROM users WHERE username = ?;


-- ############################################################################
-- OPTION 4: CLEAR OLD DATA
-- Data retention cleanup
-- ############################################################################

-- Delete sessions older than 30 days
DELETE FROM progress 
WHERE date < datetime('now', '-30 days');

-- Delete sessions older than 90 days
DELETE FROM progress 
WHERE date < datetime('now', '-90 days');

-- Delete sessions older than 1 year
DELETE FROM progress 
WHERE date < datetime('now', '-365 days');


-- ############################################################################
-- OPTION 5: CLEAR BY CRITERIA
-- Selective deletion
-- ############################################################################

-- Delete all sessions with score below threshold
DELETE FROM progress WHERE score < 10;

-- Delete sessions for specific exercise type
DELETE FROM progress WHERE exercise_type = ?;

-- Delete sessions without audio files
DELETE FROM progress WHERE audio_path IS NULL;

-- Delete inactive users (no sessions in 90 days)
DELETE FROM users 
WHERE id NOT IN (
    SELECT DISTINCT user_id 
    FROM progress 
    WHERE date >= datetime('now', '-90 days')
);


-- ############################################################################
-- VERIFICATION QUERIES
-- Run after deletion to verify
-- ############################################################################

-- Count remaining records
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'progress' as table_name, COUNT(*) as count FROM progress;

-- Verify no orphaned records
SELECT COUNT(*) as orphaned_progress 
FROM progress p
LEFT JOIN users u ON p.user_id = u.id
WHERE u.id IS NULL;
