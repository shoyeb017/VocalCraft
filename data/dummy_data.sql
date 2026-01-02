-- ============================================================================
-- VocalCraft Dummy Data for Testing
-- 3 Patient Users with Progress History
-- Generated: January 1, 2026
-- ============================================================================

-- ############################################################################
-- CREDENTIALS REFERENCE (Save these!)
-- ############################################################################
-- 
-- User 1: Ahmed Rahman
--   Username: ahmed
--   Password: ahmed123
--   Progress: 3 days (Dec 29-31, 2025)
--   Sessions: 15 practice sessions
--
-- User 2: Fatima Khan  
--   Username: fatima
--   Password: fatima123
--   Progress: 5 days (Dec 27-31, 2025)
--   Sessions: 28 practice sessions
--
-- User 3: Karim Hossain
--   Username: karim
--   Password: karim123
--   Progress: 7 days (Dec 25-31, 2025)
--   Sessions: 42 practice sessions
--
-- ############################################################################


-- ============================================================================
-- CLEAR EXISTING DATA (Optional - uncomment if needed)
-- ============================================================================
DELETE FROM progress;
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name IN ('users', 'progress');


-- ============================================================================
-- INSERT USERS
-- Plain text passwords for simple authentication
-- ============================================================================

-- User 1: ahmed / ahmed123
INSERT INTO users (username, password, age, condition, join_date) 
VALUES ('ahmed', 'ahmed123', 28, 'Dysarthria', '2025-12-28 09:00:00');

-- User 2: fatima / fatima123
INSERT INTO users (username, password, age, condition, join_date) 
VALUES ('fatima', 'fatima123', 35, 'Dysarthria', '2025-12-26 10:30:00');

-- User 3: karim / karim123
INSERT INTO users (username, password, age, condition, join_date) 
VALUES ('karim', 'karim123', 42, 'Dysarthria', '2025-12-24 08:15:00');


-- ============================================================================
-- USER 1: AHMED - 3 Days of Progress (Dec 29-31, 2025)
-- Starting weak, showing improvement
-- ============================================================================

-- Day 1: December 29, 2025 (5 sessions - struggling)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(1, '2025-12-29 09:15:00', 'breathing', 45.5, 'data/recordings/ahmed/2025-12-29/recording_001.wav'),
(1, '2025-12-29 09:22:00', 'breathing', 52.0, 'data/recordings/ahmed/2025-12-29/recording_002.wav'),
(1, '2025-12-29 10:05:00', 'vowels', 38.5, 'data/recordings/ahmed/2025-12-29/recording_003.wav'),
(1, '2025-12-29 10:12:00', 'vowels', 41.0, 'data/recordings/ahmed/2025-12-29/recording_004.wav'),
(1, '2025-12-29 14:30:00', 'short_sentences', 35.0, 'data/recordings/ahmed/2025-12-29/recording_005.wav');

-- Day 2: December 30, 2025 (5 sessions - improving)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(1, '2025-12-30 10:00:00', 'breathing', 58.0, 'data/recordings/ahmed/2025-12-30/recording_001.wav'),
(1, '2025-12-30 10:08:00', 'breathing', 62.5, 'data/recordings/ahmed/2025-12-30/recording_002.wav'),
(1, '2025-12-30 11:15:00', 'vowels', 55.0, 'data/recordings/ahmed/2025-12-30/recording_003.wav'),
(1, '2025-12-30 11:22:00', 'short_sentences', 48.5, 'data/recordings/ahmed/2025-12-30/recording_004.wav'),
(1, '2025-12-30 15:45:00', 'short_sentences', 52.0, 'data/recordings/ahmed/2025-12-30/recording_005.wav');

-- Day 3: December 31, 2025 (5 sessions - good progress)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(1, '2025-12-31 09:30:00', 'breathing', 72.0, 'data/recordings/ahmed/2025-12-31/recording_001.wav'),
(1, '2025-12-31 09:38:00', 'vowels', 68.5, 'data/recordings/ahmed/2025-12-31/recording_002.wav'),
(1, '2025-12-31 10:45:00', 'vowels', 71.0, 'data/recordings/ahmed/2025-12-31/recording_003.wav'),
(1, '2025-12-31 14:00:00', 'short_sentences', 65.0, 'data/recordings/ahmed/2025-12-31/recording_004.wav'),
(1, '2025-12-31 14:10:00', 'functional_phrases', 58.5, 'data/recordings/ahmed/2025-12-31/recording_005.wav');


-- ============================================================================
-- USER 2: FATIMA - 5 Days of Progress (Dec 27-31, 2025)
-- Steady improvement with consistent practice
-- ============================================================================

-- Day 1: December 27, 2025 (5 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(2, '2025-12-27 08:30:00', 'breathing', 55.0, 'data/recordings/fatima/2025-12-27/recording_001.wav'),
(2, '2025-12-27 08:40:00', 'breathing', 58.5, 'data/recordings/fatima/2025-12-27/recording_002.wav'),
(2, '2025-12-27 09:15:00', 'vowels', 48.0, 'data/recordings/fatima/2025-12-27/recording_003.wav'),
(2, '2025-12-27 09:25:00', 'vowels', 52.0, 'data/recordings/fatima/2025-12-27/recording_004.wav'),
(2, '2025-12-27 16:00:00', 'short_sentences', 42.5, 'data/recordings/fatima/2025-12-27/recording_005.wav');

-- Day 2: December 28, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(2, '2025-12-28 09:00:00', 'breathing', 62.0, 'data/recordings/fatima/2025-12-28/recording_001.wav'),
(2, '2025-12-28 09:10:00', 'breathing', 65.5, 'data/recordings/fatima/2025-12-28/recording_002.wav'),
(2, '2025-12-28 10:30:00', 'vowels', 58.0, 'data/recordings/fatima/2025-12-28/recording_003.wav'),
(2, '2025-12-28 10:40:00', 'vowels', 61.0, 'data/recordings/fatima/2025-12-28/recording_004.wav'),
(2, '2025-12-28 14:15:00', 'short_sentences', 52.5, 'data/recordings/fatima/2025-12-28/recording_005.wav'),
(2, '2025-12-28 14:25:00', 'short_sentences', 55.0, 'data/recordings/fatima/2025-12-28/recording_006.wav');

-- Day 3: December 29, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(2, '2025-12-29 08:45:00', 'breathing', 70.0, 'data/recordings/fatima/2025-12-29/recording_001.wav'),
(2, '2025-12-29 08:55:00', 'vowels', 65.5, 'data/recordings/fatima/2025-12-29/recording_002.wav'),
(2, '2025-12-29 09:30:00', 'vowels', 68.0, 'data/recordings/fatima/2025-12-29/recording_003.wav'),
(2, '2025-12-29 11:00:00', 'short_sentences', 60.5, 'data/recordings/fatima/2025-12-29/recording_004.wav'),
(2, '2025-12-29 11:10:00', 'functional_phrases', 55.0, 'data/recordings/fatima/2025-12-29/recording_005.wav'),
(2, '2025-12-29 15:30:00', 'tongue_twisters', 45.0, 'data/recordings/fatima/2025-12-29/recording_006.wav');

-- Day 4: December 30, 2025 (5 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(2, '2025-12-30 09:15:00', 'breathing', 75.5, 'data/recordings/fatima/2025-12-30/recording_001.wav'),
(2, '2025-12-30 09:25:00', 'vowels', 72.0, 'data/recordings/fatima/2025-12-30/recording_002.wav'),
(2, '2025-12-30 10:45:00', 'short_sentences', 68.5, 'data/recordings/fatima/2025-12-30/recording_003.wav'),
(2, '2025-12-30 10:55:00', 'functional_phrases', 64.0, 'data/recordings/fatima/2025-12-30/recording_004.wav'),
(2, '2025-12-30 16:20:00', 'tongue_twisters', 52.5, 'data/recordings/fatima/2025-12-30/recording_005.wav');

-- Day 5: December 31, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(2, '2025-12-31 08:30:00', 'breathing', 82.0, 'data/recordings/fatima/2025-12-31/recording_001.wav'),
(2, '2025-12-31 08:40:00', 'breathing', 85.5, 'data/recordings/fatima/2025-12-31/recording_002.wav'),
(2, '2025-12-31 09:45:00', 'vowels', 78.0, 'data/recordings/fatima/2025-12-31/recording_003.wav'),
(2, '2025-12-31 10:00:00', 'short_sentences', 74.5, 'data/recordings/fatima/2025-12-31/recording_004.wav'),
(2, '2025-12-31 14:30:00', 'functional_phrases', 70.0, 'data/recordings/fatima/2025-12-31/recording_005.wav'),
(2, '2025-12-31 14:45:00', 'tongue_twisters', 62.5, 'data/recordings/fatima/2025-12-31/recording_006.wav');


-- ============================================================================
-- USER 3: KARIM - 7 Days of Progress (Dec 25-31, 2025)
-- Experienced user, high scores with consistent practice
-- ============================================================================

-- Day 1: December 25, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-25 09:00:00', 'breathing', 60.0, 'data/recordings/karim/2025-12-25/recording_001.wav'),
(3, '2025-12-25 09:10:00', 'breathing', 63.5, 'data/recordings/karim/2025-12-25/recording_002.wav'),
(3, '2025-12-25 10:00:00', 'vowels', 55.0, 'data/recordings/karim/2025-12-25/recording_003.wav'),
(3, '2025-12-25 10:15:00', 'vowels', 58.0, 'data/recordings/karim/2025-12-25/recording_004.wav'),
(3, '2025-12-25 14:30:00', 'short_sentences', 50.5, 'data/recordings/karim/2025-12-25/recording_005.wav'),
(3, '2025-12-25 14:45:00', 'short_sentences', 53.0, 'data/recordings/karim/2025-12-25/recording_006.wav');

-- Day 2: December 26, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-26 08:30:00', 'breathing', 68.0, 'data/recordings/karim/2025-12-26/recording_001.wav'),
(3, '2025-12-26 08:42:00', 'breathing', 70.5, 'data/recordings/karim/2025-12-26/recording_002.wav'),
(3, '2025-12-26 09:30:00', 'vowels', 62.0, 'data/recordings/karim/2025-12-26/recording_003.wav'),
(3, '2025-12-26 09:42:00', 'vowels', 65.5, 'data/recordings/karim/2025-12-26/recording_004.wav'),
(3, '2025-12-26 11:15:00', 'short_sentences', 58.0, 'data/recordings/karim/2025-12-26/recording_005.wav'),
(3, '2025-12-26 15:00:00', 'functional_phrases', 52.5, 'data/recordings/karim/2025-12-26/recording_006.wav');

-- Day 3: December 27, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-27 09:15:00', 'breathing', 74.0, 'data/recordings/karim/2025-12-27/recording_001.wav'),
(3, '2025-12-27 09:25:00', 'vowels', 70.5, 'data/recordings/karim/2025-12-27/recording_002.wav'),
(3, '2025-12-27 10:30:00', 'vowels', 72.0, 'data/recordings/karim/2025-12-27/recording_003.wav'),
(3, '2025-12-27 10:42:00', 'short_sentences', 65.5, 'data/recordings/karim/2025-12-27/recording_004.wav'),
(3, '2025-12-27 14:00:00', 'functional_phrases', 60.0, 'data/recordings/karim/2025-12-27/recording_005.wav'),
(3, '2025-12-27 14:15:00', 'tongue_twisters', 48.5, 'data/recordings/karim/2025-12-27/recording_006.wav');

-- Day 4: December 28, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-28 08:45:00', 'breathing', 78.5, 'data/recordings/karim/2025-12-28/recording_001.wav'),
(3, '2025-12-28 08:55:00', 'breathing', 80.0, 'data/recordings/karim/2025-12-28/recording_002.wav'),
(3, '2025-12-28 09:45:00', 'vowels', 75.0, 'data/recordings/karim/2025-12-28/recording_003.wav'),
(3, '2025-12-28 10:00:00', 'short_sentences', 70.5, 'data/recordings/karim/2025-12-28/recording_004.wav'),
(3, '2025-12-28 11:30:00', 'functional_phrases', 66.0, 'data/recordings/karim/2025-12-28/recording_005.wav'),
(3, '2025-12-28 15:15:00', 'tongue_twisters', 55.5, 'data/recordings/karim/2025-12-28/recording_006.wav');

-- Day 5: December 29, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-29 09:00:00', 'breathing', 82.0, 'data/recordings/karim/2025-12-29/recording_001.wav'),
(3, '2025-12-29 09:12:00', 'vowels', 78.5, 'data/recordings/karim/2025-12-29/recording_002.wav'),
(3, '2025-12-29 10:15:00', 'vowels', 80.0, 'data/recordings/karim/2025-12-29/recording_003.wav'),
(3, '2025-12-29 10:28:00', 'short_sentences', 75.5, 'data/recordings/karim/2025-12-29/recording_004.wav'),
(3, '2025-12-29 14:45:00', 'functional_phrases', 70.0, 'data/recordings/karim/2025-12-29/recording_005.wav'),
(3, '2025-12-29 15:00:00', 'tongue_twisters', 62.5, 'data/recordings/karim/2025-12-29/recording_006.wav');

-- Day 6: December 30, 2025 (6 sessions)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-30 08:30:00', 'breathing', 85.0, 'data/recordings/karim/2025-12-30/recording_001.wav'),
(3, '2025-12-30 08:42:00', 'breathing', 87.5, 'data/recordings/karim/2025-12-30/recording_002.wav'),
(3, '2025-12-30 09:30:00', 'vowels', 82.0, 'data/recordings/karim/2025-12-30/recording_003.wav'),
(3, '2025-12-30 09:45:00', 'short_sentences', 78.5, 'data/recordings/karim/2025-12-30/recording_004.wav'),
(3, '2025-12-30 11:00:00', 'functional_phrases', 74.0, 'data/recordings/karim/2025-12-30/recording_005.wav'),
(3, '2025-12-30 14:30:00', 'tongue_twisters', 68.5, 'data/recordings/karim/2025-12-30/recording_006.wav');

-- Day 7: December 31, 2025 (6 sessions - peak performance)
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES
(3, '2025-12-31 09:00:00', 'breathing', 90.0, 'data/recordings/karim/2025-12-31/recording_001.wav'),
(3, '2025-12-31 09:12:00', 'breathing', 92.5, 'data/recordings/karim/2025-12-31/recording_002.wav'),
(3, '2025-12-31 10:00:00', 'vowels', 88.0, 'data/recordings/karim/2025-12-31/recording_003.wav'),
(3, '2025-12-31 10:15:00', 'short_sentences', 85.5, 'data/recordings/karim/2025-12-31/recording_004.wav'),
(3, '2025-12-31 14:00:00', 'functional_phrases', 82.0, 'data/recordings/karim/2025-12-31/recording_005.wav'),
(3, '2025-12-31 14:20:00', 'tongue_twisters', 75.0, 'data/recordings/karim/2025-12-31/recording_006.wav');


-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check user count
SELECT 'Total Users' as metric, COUNT(*) as value FROM users
UNION ALL
SELECT 'Total Sessions', COUNT(*) FROM progress;

-- Sessions per user
SELECT u.username, COUNT(p.id) as sessions, 
       ROUND(AVG(p.score), 1) as avg_score,
       MIN(DATE(p.date)) as first_day,
       MAX(DATE(p.date)) as last_day
FROM users u
LEFT JOIN progress p ON u.id = p.user_id
GROUP BY u.id;

-- Daily breakdown per user
SELECT u.username, DATE(p.date) as practice_date, 
       COUNT(*) as sessions, ROUND(AVG(p.score), 1) as avg_score
FROM users u
JOIN progress p ON u.id = p.user_id
GROUP BY u.id, DATE(p.date)
ORDER BY u.username, practice_date;
