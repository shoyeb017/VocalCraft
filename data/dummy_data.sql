-- ============================================================================
-- VocalCraft Dummy Data for Testing
-- 3 Patient Users with Long-term Progress History
-- Generated: April 3, 2026
-- ============================================================================

-- ############################################################################
-- TEST CREDENTIALS (Save these!)
-- ############################################################################
-- 
-- User 1: Ahmed Farsi
--   Username: ahmed
--   Password: ahmed123
--   Progress: 30 days (Mar 4 - Apr 3, 2026)
--   Improvement: 35% → 72%
--
-- User 2: Fatima Al-Mansoori
--   Username: fatima
--   Password: fatima123
--   Progress: 40 days (Feb 22 - Apr 3, 2026)
--   Improvement: 28% → 78%
--
-- User 3: Karim Al-Khalili
--   Username: karim
--   Password: karim123
--   Progress: 50 days (Feb 13 - Apr 3, 2026)
--   Improvement: 35% → 87% (Best Results!)
--
-- ############################################################################

DELETE FROM progress;
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name IN ('users', 'progress');

INSERT INTO users (username, password, age, condition, join_date) VALUES ('ahmed', 'ahmed123', 32, 'Dysarthria', '2026-03-04 08:00:00');
INSERT INTO users (username, password, age, condition, join_date) VALUES ('fatima', 'fatima123', 28, 'Dysarthria', '2026-02-22 09:30:00');
INSERT INTO users (username, password, age, condition, join_date) VALUES ('karim', 'karim123', 45, 'Dysarthria', '2026-02-13 07:15:00');

-- Ahmed: 36 single-line INSERT statements
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-04 08:15:00', 'breathing', 32.5, 'data/recordings/ahmed/2026-03-04/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-04 14:30:00', 'vowels', 28.0, 'data/recordings/ahmed/2026-03-04/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-05 09:00:00', 'breathing', 35.5, 'data/recordings/ahmed/2026-03-05/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-05 15:45:00', 'short_sentences', 31.0, 'data/recordings/ahmed/2026-03-05/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-06 08:30:00', 'vowels', 33.0, 'data/recordings/ahmed/2026-03-06/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-06 13:15:00', 'breathing', 36.5, 'data/recordings/ahmed/2026-03-06/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-07 10:00:00', 'short_sentences', 29.5, 'data/recordings/ahmed/2026-03-07/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-08 09:30:00', 'breathing', 38.0, 'data/recordings/ahmed/2026-03-08/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-08 14:20:00', 'vowels', 34.5, 'data/recordings/ahmed/2026-03-08/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-09 11:00:00', 'short_sentences', 37.0, 'data/recordings/ahmed/2026-03-09/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-10 08:45:00', 'breathing', 40.0, 'data/recordings/ahmed/2026-03-10/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-11 09:15:00', 'vowels', 42.5, 'data/recordings/ahmed/2026-03-11/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-11 15:30:00', 'breathing', 45.0, 'data/recordings/ahmed/2026-03-11/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-12 10:00:00', 'short_sentences', 41.5, 'data/recordings/ahmed/2026-03-12/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-13 08:30:00', 'breathing', 47.0, 'data/recordings/ahmed/2026-03-13/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-13 14:15:00', 'vowels', 43.5, 'data/recordings/ahmed/2026-03-13/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-14 09:45:00', 'short_sentences', 46.0, 'data/recordings/ahmed/2026-03-14/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-15 10:30:00', 'breathing', 50.0, 'data/recordings/ahmed/2026-03-15/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-16 08:15:00', 'vowels', 48.5, 'data/recordings/ahmed/2026-03-16/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-17 11:00:00', 'short_sentences', 52.0, 'data/recordings/ahmed/2026-03-17/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-18 09:30:00', 'breathing', 55.5, 'data/recordings/ahmed/2026-03-18/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-18 15:00:00', 'vowels', 53.0, 'data/recordings/ahmed/2026-03-18/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-19 10:15:00', 'short_sentences', 57.5, 'data/recordings/ahmed/2026-03-19/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-20 09:00:00', 'breathing', 59.0, 'data/recordings/ahmed/2026-03-20/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-20 14:30:00', 'vowels', 56.5, 'data/recordings/ahmed/2026-03-20/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-21 08:45:00', 'short_sentences', 61.0, 'data/recordings/ahmed/2026-03-21/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-22 10:00:00', 'breathing', 62.5, 'data/recordings/ahmed/2026-03-22/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-23 09:15:00', 'vowels', 59.5, 'data/recordings/ahmed/2026-03-23/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-24 11:30:00', 'short_sentences', 64.0, 'data/recordings/ahmed/2026-03-24/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-25 09:45:00', 'breathing', 65.5, 'data/recordings/ahmed/2026-03-25/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-26 10:30:00', 'vowels', 67.0, 'data/recordings/ahmed/2026-03-26/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-27 08:15:00', 'short_sentences', 68.5, 'data/recordings/ahmed/2026-03-27/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-28 09:00:00', 'breathing', 70.0, 'data/recordings/ahmed/2026-03-28/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-29 10:15:00', 'vowels', 69.5, 'data/recordings/ahmed/2026-03-29/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-03-30 11:00:00', 'short_sentences', 71.0, 'data/recordings/ahmed/2026-03-30/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-04-01 09:30:00', 'breathing', 72.5, 'data/recordings/ahmed/2026-04-01/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-04-02 10:45:00', 'vowels', 71.5, 'data/recordings/ahmed/2026-04-02/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (1, '2026-04-03 09:15:00', 'short_sentences', 72.0, 'data/recordings/ahmed/2026-04-03/rec_001.wav');

-- Fatima: 50 single-line INSERT statements
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-22 09:30:00', 'breathing', 25.0, 'data/recordings/fatima/2026-02-22/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-22 15:45:00', 'vowels', 22.5, 'data/recordings/fatima/2026-02-22/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-23 10:15:00', 'breathing', 28.5, 'data/recordings/fatima/2026-02-23/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-24 09:00:00', 'short_sentences', 26.0, 'data/recordings/fatima/2026-02-24/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-24 14:30:00', 'vowels', 24.5, 'data/recordings/fatima/2026-02-24/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-25 08:45:00', 'breathing', 29.0, 'data/recordings/fatima/2026-02-25/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-26 10:00:00', 'breathing', 32.0, 'data/recordings/fatima/2026-02-26/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-26 15:15:00', 'vowels', 27.5, 'data/recordings/fatima/2026-02-26/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-27 09:30:00', 'short_sentences', 31.0, 'data/recordings/fatima/2026-02-27/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-02-28 11:00:00', 'breathing', 34.5, 'data/recordings/fatima/2026-02-28/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-01 10:15:00', 'vowels', 38.5, 'data/recordings/fatima/2026-03-01/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-02 09:00:00', 'short_sentences', 41.0, 'data/recordings/fatima/2026-03-02/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-03 08:30:00', 'breathing', 43.5, 'data/recordings/fatima/2026-03-03/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-03 14:45:00', 'vowels', 41.0, 'data/recordings/fatima/2026-03-03/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-04 10:00:00', 'short_sentences', 45.5, 'data/recordings/fatima/2026-03-04/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-05 09:15:00', 'breathing', 47.0, 'data/recordings/fatima/2026-03-05/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-06 11:30:00', 'vowels', 44.5, 'data/recordings/fatima/2026-03-06/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-07 10:45:00', 'short_sentences', 49.0, 'data/recordings/fatima/2026-03-07/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-08 09:30:00', 'breathing', 51.5, 'data/recordings/fatima/2026-03-08/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-08 15:00:00', 'vowels', 52.0, 'data/recordings/fatima/2026-03-08/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-09 10:15:00', 'short_sentences', 54.5, 'data/recordings/fatima/2026-03-09/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-10 08:45:00', 'breathing', 56.0, 'data/recordings/fatima/2026-03-10/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-11 09:00:00', 'vowels', 55.5, 'data/recordings/fatima/2026-03-11/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-12 10:30:00', 'short_sentences', 58.5, 'data/recordings/fatima/2026-03-12/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-13 11:00:00', 'breathing', 59.0, 'data/recordings/fatima/2026-03-13/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-14 09:15:00', 'vowels', 60.5, 'data/recordings/fatima/2026-03-14/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-15 10:00:00', 'short_sentences', 62.0, 'data/recordings/fatima/2026-03-15/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-16 09:30:00', 'breathing', 64.5, 'data/recordings/fatima/2026-03-16/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-17 10:15:00', 'vowels', 63.0, 'data/recordings/fatima/2026-03-17/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-18 08:45:00', 'short_sentences', 66.0, 'data/recordings/fatima/2026-03-18/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-19 11:00:00', 'breathing', 67.5, 'data/recordings/fatima/2026-03-19/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-20 09:00:00', 'vowels', 68.5, 'data/recordings/fatima/2026-03-20/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-21 10:30:00', 'short_sentences', 72.0, 'data/recordings/fatima/2026-03-21/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-22 09:15:00', 'breathing', 73.0, 'data/recordings/fatima/2026-03-22/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-23 10:45:00', 'vowels', 74.5, 'data/recordings/fatima/2026-03-23/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-24 08:30:00', 'short_sentences', 75.0, 'data/recordings/fatima/2026-03-24/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-25 11:00:00', 'breathing', 75.5, 'data/recordings/fatima/2026-03-25/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-26 09:30:00', 'vowels', 76.0, 'data/recordings/fatima/2026-03-26/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-27 10:15:00', 'short_sentences', 76.5, 'data/recordings/fatima/2026-03-27/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-29 09:00:00', 'breathing', 77.0, 'data/recordings/fatima/2026-03-29/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-30 10:30:00', 'vowels', 77.5, 'data/recordings/fatima/2026-03-30/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-03-31 11:00:00', 'short_sentences', 78.0, 'data/recordings/fatima/2026-03-31/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-04-01 09:15:00', 'breathing', 78.5, 'data/recordings/fatima/2026-04-01/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-04-02 10:45:00', 'vowels', 77.5, 'data/recordings/fatima/2026-04-02/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (2, '2026-04-03 09:30:00', 'short_sentences', 78.0, 'data/recordings/fatima/2026-04-03/rec_001.wav');

-- Karim: 60 single-line INSERT statements
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-13 07:15:00', 'breathing', 32.0, 'data/recordings/karim/2026-02-13/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-13 14:45:00', 'vowels', 29.5, 'data/recordings/karim/2026-02-13/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-14 08:30:00', 'breathing', 35.0, 'data/recordings/karim/2026-02-14/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-15 09:00:00', 'short_sentences', 33.5, 'data/recordings/karim/2026-02-15/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-15 15:30:00', 'vowels', 31.0, 'data/recordings/karim/2026-02-15/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-16 10:15:00', 'breathing', 37.5, 'data/recordings/karim/2026-02-16/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-17 09:45:00', 'breathing', 39.0, 'data/recordings/karim/2026-02-17/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-17 14:30:00', 'vowels', 36.5, 'data/recordings/karim/2026-02-17/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-18 11:00:00', 'short_sentences', 40.5, 'data/recordings/karim/2026-02-18/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-19 10:00:00', 'breathing', 42.0, 'data/recordings/karim/2026-02-19/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-20 09:30:00', 'vowels', 44.5, 'data/recordings/karim/2026-02-20/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-21 10:15:00', 'short_sentences', 47.0, 'data/recordings/karim/2026-02-21/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-22 08:45:00', 'breathing', 49.0, 'data/recordings/karim/2026-02-22/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-22 15:00:00', 'vowels', 45.5, 'data/recordings/karim/2026-02-22/rec_002.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-23 09:00:00', 'short_sentences', 51.0, 'data/recordings/karim/2026-02-23/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-24 10:30:00', 'breathing', 52.5, 'data/recordings/karim/2026-02-24/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-25 11:15:00', 'vowels', 50.0, 'data/recordings/karim/2026-02-25/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-26 09:45:00', 'short_sentences', 54.0, 'data/recordings/karim/2026-02-26/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-27 10:00:00', 'breathing', 55.5, 'data/recordings/karim/2026-02-27/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-02-28 09:30:00', 'vowels', 57.0, 'data/recordings/karim/2026-02-28/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-01 08:15:00', 'short_sentences', 59.0, 'data/recordings/karim/2026-03-01/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-02 10:45:00', 'breathing', 60.5, 'data/recordings/karim/2026-03-02/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-03 09:00:00', 'vowels', 59.0, 'data/recordings/karim/2026-03-03/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-04 11:30:00', 'short_sentences', 62.0, 'data/recordings/karim/2026-03-04/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-05 10:15:00', 'breathing', 63.5, 'data/recordings/karim/2026-03-05/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-06 09:45:00', 'vowels', 65.0, 'data/recordings/karim/2026-03-06/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-07 10:30:00', 'short_sentences', 67.0, 'data/recordings/karim/2026-03-07/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-08 08:15:00', 'breathing', 68.5, 'data/recordings/karim/2026-03-08/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-09 11:00:00', 'vowels', 70.0, 'data/recordings/karim/2026-03-09/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-10 09:30:00', 'short_sentences', 71.0, 'data/recordings/karim/2026-03-10/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-11 10:15:00', 'breathing', 72.5, 'data/recordings/karim/2026-03-11/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-12 09:00:00', 'vowels', 71.5, 'data/recordings/karim/2026-03-12/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-13 10:45:00', 'short_sentences', 73.5, 'data/recordings/karim/2026-03-13/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-14 11:30:00', 'breathing', 75.0, 'data/recordings/karim/2026-03-14/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-15 09:15:00', 'vowels', 76.0, 'data/recordings/karim/2026-03-15/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-16 10:00:00', 'short_sentences', 77.5, 'data/recordings/karim/2026-03-16/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-17 08:30:00', 'breathing', 78.5, 'data/recordings/karim/2026-03-17/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-18 11:15:00', 'vowels', 79.0, 'data/recordings/karim/2026-03-18/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-19 09:45:00', 'short_sentences', 80.0, 'data/recordings/karim/2026-03-19/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-20 10:30:00', 'breathing', 81.0, 'data/recordings/karim/2026-03-20/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-21 09:00:00', 'vowels', 82.0, 'data/recordings/karim/2026-03-21/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-22 10:45:00', 'short_sentences', 82.5, 'data/recordings/karim/2026-03-22/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-23 08:15:00', 'breathing', 83.0, 'data/recordings/karim/2026-03-23/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-24 11:00:00', 'vowels', 83.5, 'data/recordings/karim/2026-03-24/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-25 09:30:00', 'short_sentences', 84.0, 'data/recordings/karim/2026-03-25/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-26 10:15:00', 'breathing', 84.5, 'data/recordings/karim/2026-03-26/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-27 11:00:00', 'vowels', 85.0, 'data/recordings/karim/2026-03-27/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-28 09:45:00', 'short_sentences', 85.5, 'data/recordings/karim/2026-03-28/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-29 10:30:00', 'breathing', 86.0, 'data/recordings/karim/2026-03-29/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-30 08:00:00', 'vowels', 86.5, 'data/recordings/karim/2026-03-30/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-03-31 11:15:00', 'short_sentences', 87.0, 'data/recordings/karim/2026-03-31/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-04-01 09:30:00', 'breathing', 86.5, 'data/recordings/karim/2026-04-01/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-04-02 10:45:00', 'vowels', 86.8, 'data/recordings/karim/2026-04-02/rec_001.wav');
INSERT INTO progress (user_id, date, exercise_type, score, audio_path) VALUES (3, '2026-04-03 09:00:00', 'short_sentences', 87.0, 'data/recordings/karim/2026-04-03/rec_001.wav');
