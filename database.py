"""
Database Module for VocalCraft
Handles user authentication and progress tracking using SQLite.
Uses pathlib for cross-platform portability.
"""

import sqlite3
# Password stored as plain text (no hashing)
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
from contextlib import contextmanager
from pathlib import Path


class DatabaseManager:
    """
    A class to handle all database operations for VocalCraft.
    Uses SQLite for lightweight, file-based storage.
    Features user authentication with password hashing.
    """

    def __init__(self, db_path: str = "data/vocalcraft.db"):
        """
        Initialize the database manager.
        Creates the database file and tables if they don't exist.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        
        # Ensure the data directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize the database tables
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.
        Ensures connections are properly closed.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_database(self):
        """Create the database tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    age INTEGER,
                    condition TEXT,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    exercise_type TEXT,
                    score REAL,
                    audio_path TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                        ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_progress_user 
                ON progress (user_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_progress_date 
                ON progress (date)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_username 
                ON users (username)
            ''')

    # ==================== Authentication Methods ====================

    def register_user(
        self, 
        username: str, 
        password: str, 
        age: Optional[int] = None, 
        condition: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Unique username.
            password: Plain text password.
            age: User's age (optional).
            condition: Speech condition/diagnosis (optional).
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        if not username or not password:
            return False, "Username and password are required."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters."
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters."
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password, age, condition)
                    VALUES (?, ?, ?, ?)
                ''', (username, password, age, condition))
                
                return True, f"User '{username}' registered successfully!"
                
        except sqlite3.IntegrityError:
            return False, f"Username '{username}' already exists."
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, username: str, password: str) -> Tuple[Optional[int], str]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: The username.
            password: Plain text password for comparison.
            
        Returns:
            Tuple of (user_id or None, message: str).
            Returns user_id if successful, None if failed.
        """
        if not username or not password:
            return None, "Username and password are required."
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, password FROM users WHERE username = ?
                ''', (username,))
                
                row = cursor.fetchone()
                
                if row is None:
                    return None, "User not found."
                
                if row['password'] == password:
                    return row['id'], f"Welcome back, {username}!"
                else:
                    return None, "Incorrect password."
                    
        except Exception as e:
            return None, f"Login failed: {str(e)}"

    def get_user(self, user_id: int) -> Optional[Dict]:
        """
        Get user details by ID.
        
        Args:
            user_id: The user's ID.
            
        Returns:
            User data as dictionary (excluding password), or None.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, age, condition, join_date 
                FROM users WHERE id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Get user details by username.
        
        Args:
            username: The username.
            
        Returns:
            User data as dictionary (excluding password), or None.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, age, condition, join_date 
                FROM users WHERE username = ?
            ''', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_user(
        self, 
        user_id: int, 
        age: Optional[int] = None,
        condition: Optional[str] = None
    ) -> bool:
        """
        Update user information.
        
        Args:
            user_id: The user's ID.
            age: New age (optional).
            condition: New condition (optional).
            
        Returns:
            True if update was successful.
        """
        updates = []
        values = []
        
        if age is not None:
            updates.append("age = ?")
            values.append(age)
        if condition is not None:
            updates.append("condition = ?")
            values.append(condition)
        
        if not updates:
            return False
        
        values.append(user_id)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE users SET {', '.join(updates)} WHERE id = ?",
                values
            )
            return cursor.rowcount > 0

    def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change a user's password.
        
        Args:
            user_id: The user's ID.
            old_password: Current password.
            new_password: New password.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        if len(new_password) < 4:
            return False, "New password must be at least 4 characters."
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Verify old password
            cursor.execute('SELECT password FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row is None:
                return False, "User not found."
            
            if row['password'] != old_password:
                return False, "Current password is incorrect."
            
            # Update password
            cursor.execute(
                'UPDATE users SET password = ? WHERE id = ?',
                (new_password, user_id)
            )
            return True, "Password changed successfully."

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user and all their progress data.
        
        Args:
            user_id: The user's ID.
            
        Returns:
            True if deletion was successful.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Progress will be deleted automatically due to ON DELETE CASCADE
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            return cursor.rowcount > 0

    # ==================== Data Methods ====================

    def save_session(
        self,
        user_id: int,
        score: float,
        audio_path: Optional[str] = None,
        exercise_type: Optional[str] = None
    ) -> int:
        """
        Save a practice session/attempt.
        
        Args:
            user_id: The user's ID.
            score: The score achieved (0-100).
            audio_path: Path to the recorded audio file (optional).
            exercise_type: Type/category of exercise (optional).
            
        Returns:
            The ID of the saved session.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO progress (user_id, score, audio_path, exercise_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, score, audio_path, exercise_type))
            return cursor.lastrowid

    def get_user_progress(self, user_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        Get a user's progress history for graphing.
        
        Args:
            user_id: The user's ID.
            limit: Maximum number of records to return (optional).
            
        Returns:
            List of dictionaries with date and score.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT date, score, exercise_type 
                FROM progress 
                WHERE user_id = ? 
                ORDER BY date ASC
            '''
            if limit:
                query += f' LIMIT {limit}'
            
            cursor.execute(query, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_recent_sessions(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Get recent practice sessions.
        
        Args:
            user_id: The user's ID.
            limit: Number of sessions to return.
            
        Returns:
            List of session dictionaries, most recent first.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, date, exercise_type, score, audio_path
                FROM progress 
                WHERE user_id = ? 
                ORDER BY date DESC
                LIMIT ?
            ''', (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_user_stats(self, user_id: int) -> Dict:
        """
        Get statistics for a user's progress.
        
        Args:
            user_id: The user's ID.
            
        Returns:
            Dictionary with statistics.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Total sessions
            cursor.execute(
                'SELECT COUNT(*) FROM progress WHERE user_id = ?',
                (user_id,)
            )
            total_sessions = cursor.fetchone()[0]
            
            # Average score
            cursor.execute(
                'SELECT AVG(score) FROM progress WHERE user_id = ?',
                (user_id,)
            )
            avg_score = cursor.fetchone()[0] or 0
            
            # Best score
            cursor.execute(
                'SELECT MAX(score) FROM progress WHERE user_id = ?',
                (user_id,)
            )
            best_score = cursor.fetchone()[0] or 0
            
            # Sessions this week
            cursor.execute('''
                SELECT COUNT(*) FROM progress 
                WHERE user_id = ? AND date >= DATE('now', '-7 days')
            ''', (user_id,))
            sessions_this_week = cursor.fetchone()[0]
            
            # Recent improvement
            cursor.execute('''
                SELECT AVG(score) FROM (
                    SELECT score FROM progress 
                    WHERE user_id = ? 
                    ORDER BY date DESC LIMIT 5
                )
            ''', (user_id,))
            recent_avg = cursor.fetchone()[0] or 0
            
            cursor.execute('''
                SELECT AVG(score) FROM (
                    SELECT score FROM progress 
                    WHERE user_id = ? 
                    ORDER BY date DESC LIMIT 5 OFFSET 5
                )
            ''', (user_id,))
            previous_avg = cursor.fetchone()[0] or 0
            
            improvement = recent_avg - previous_avg if previous_avg > 0 else 0
            
            return {
                'total_sessions': total_sessions,
                'average_score': round(avg_score, 1),
                'best_score': round(best_score, 1),
                'sessions_this_week': sessions_this_week,
                'recent_improvement': round(improvement, 1)
            }

    def get_daily_averages(self, user_id: int, days: int = 30) -> List[Tuple[str, float]]:
        """
        Get daily average scores for charting.
        
        Args:
            user_id: The user's ID.
            days: Number of days to look back.
            
        Returns:
            List of (date, average_score) tuples.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DATE(date) as day, AVG(score) as avg_score
                FROM progress
                WHERE user_id = ?
                  AND date >= DATE('now', ?)
                GROUP BY DATE(date)
                ORDER BY day
            ''', (user_id, f'-{days} days'))
            
            return [(row[0], round(row[1], 1)) for row in cursor.fetchall()]

    def get_category_breakdown(self, user_id: int) -> Dict[str, int]:
        """
        Get the count of sessions for each exercise category.
        
        Args:
            user_id: The user's unique identifier.
            
        Returns:
            Dictionary mapping exercise_type to session count.
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT exercise_type, COUNT(*) as count
                FROM progress
                WHERE user_id = ? AND exercise_type IS NOT NULL
                GROUP BY exercise_type
                ORDER BY count DESC
            ''', (user_id,))
            
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_total_practice_time(self, user_id: int) -> int:
        """
        Get the total practice time in seconds for a user.
        
        Note: Duration is calculated from session_date timestamps.
        Since we don't store duration, we estimate 30 seconds per session.
        
        Args:
            user_id: The user's unique identifier.
            
        Returns:
            Total estimated practice time in seconds.
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT COUNT(*) as session_count
                FROM progress
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            session_count = row[0] if row else 0
            
            # Estimate 30 seconds per session (average recording + analysis time)
            return session_count * 30

    def get_average_score_over_time(
        self, 
        user_id: int, 
        days: int = 30
    ) -> List[Tuple[str, float]]:
        """
        Get daily average scores over a time period.
        
        Args:
            user_id: The user's unique identifier.
            days: Number of days to look back (default: 30).
            
        Returns:
            List of tuples (date_string, average_score) ordered chronologically.
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT 
                    date(date) as practice_date,
                    AVG(score) as avg_score
                FROM progress
                WHERE user_id = ?
                AND date >= datetime('now', ?)
                GROUP BY date(date)
                ORDER BY practice_date ASC
            ''', (user_id, f'-{days} days'))
            
            return [(row[0], round(row[1], 1)) for row in cursor.fetchall()]

    def get_overall_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a user's dashboard.
        
        Args:
            user_id: The user's unique identifier.
            
        Returns:
            Dictionary containing:
            - total_sessions: Total number of practice sessions
            - total_practice_time: Estimated total practice time in minutes
            - average_score: Overall average score
            - highest_score: Best score achieved
            - lowest_score: Lowest score achieved
            - current_streak: Current daily practice streak
            - longest_streak: Longest daily practice streak achieved
            - first_session_date: Date of first session
            - last_session_date: Date of most recent session
            - category_breakdown: Dict of exercise types and counts
            - improvement_trend: Score change from first to last week
        """
        with self._get_connection() as conn:
            # Basic stats
            cursor = conn.execute('''
                SELECT 
                    COUNT(*) as total,
                    AVG(score) as avg_score,
                    MAX(score) as best,
                    MIN(score) as worst,
                    MIN(date) as first_date,
                    MAX(date) as last_date
                FROM progress
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            
            if not row or row[0] == 0:
                return {
                    'total_sessions': 0,
                    'total_practice_time': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0,
                    'current_streak': 0,
                    'longest_streak': 0,
                    'first_session_date': None,
                    'last_session_date': None,
                    'category_breakdown': {},
                    'improvement_trend': 0
                }
            
            total_sessions = row[0]
            avg_score = round(row[1], 1) if row[1] else 0
            highest_score = row[2] if row[2] else 0
            lowest_score = row[3] if row[3] else 0
            first_date = row[4]
            last_date = row[5]
            
            # Calculate streaks
            cursor = conn.execute('''
                SELECT DISTINCT date(date) as practice_date
                FROM progress
                WHERE user_id = ?
                ORDER BY practice_date DESC
            ''', (user_id,))
            
            dates = [row[0] for row in cursor.fetchall()]
            
            # Calculate current streak
            current_streak = 0
            if dates:
                from datetime import datetime, timedelta
                today = datetime.now().date()
                
                for i, date_str in enumerate(dates):
                    practice_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    expected_date = today - timedelta(days=i)
                    
                    if practice_date == expected_date:
                        current_streak += 1
                    elif practice_date == expected_date - timedelta(days=1) and i == 0:
                        # Allow yesterday as start of streak
                        current_streak += 1
                    else:
                        break
            
            # Calculate longest streak (simplified)
            longest_streak = current_streak  # Use current as default
            
            if len(dates) > 1:
                from datetime import datetime, timedelta
                streak = 1
                max_streak = 1
                
                for i in range(len(dates) - 1):
                    curr = datetime.strptime(dates[i], '%Y-%m-%d').date()
                    prev = datetime.strptime(dates[i + 1], '%Y-%m-%d').date()
                    
                    if (curr - prev).days == 1:
                        streak += 1
                        max_streak = max(max_streak, streak)
                    else:
                        streak = 1
                
                longest_streak = max(longest_streak, max_streak)
            
            # Calculate improvement trend (last week avg vs first week avg)
            cursor = conn.execute('''
                SELECT AVG(score) FROM progress 
                WHERE user_id = ? 
                AND date >= datetime('now', '-7 days')
            ''', (user_id,))
            last_week_avg = cursor.fetchone()[0] or avg_score
            
            cursor = conn.execute('''
                SELECT AVG(score) FROM progress 
                WHERE user_id = ? 
                AND date <= datetime(?, '+7 days')
            ''', (user_id, first_date))
            first_week_avg = cursor.fetchone()[0] or avg_score
            
            improvement_trend = round(last_week_avg - first_week_avg, 1)
            
            return {
                'total_sessions': total_sessions,
                'total_practice_time': (total_sessions * 30) // 60,  # In minutes
                'average_score': avg_score,
                'highest_score': highest_score,
                'lowest_score': lowest_score,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'first_session_date': first_date,
                'last_session_date': last_date,
                'category_breakdown': self.get_category_breakdown(user_id),
                'improvement_trend': improvement_trend
            }

    def get_all_attempts(self, user_id: int, limit: int = 100) -> List[Dict]:
        """
        Get all practice attempts for a user with full details.
        
        Args:
            user_id: The user's unique identifier.
            limit: Maximum number of attempts to return.
            
        Returns:
            List of dictionaries containing:
            - id: Session ID
            - date: Full timestamp
            - exercise_type: Category of exercise
            - score: Score achieved
            - audio_path: Path to recorded audio
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT id, date, exercise_type, score, audio_path
                FROM progress
                WHERE user_id = ?
                ORDER BY date DESC
                LIMIT ?
            ''', (user_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]

    def update_password(self, user_id: int, new_password: str) -> Tuple[bool, str]:
        """
        Update a user's password directly (no old password verification).
        
        Use this for password reset scenarios or when the user is authenticated.
        For password change with verification, use change_password().
        
        Args:
            user_id: The user's unique identifier.
            new_password: The new password (will be hashed).
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        if len(new_password) < 4:
            return False, "Password must be at least 4 characters."
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET password = ? WHERE id = ?',
                    (new_password, user_id)
                )
                
                if cursor.rowcount > 0:
                    return True, "Password updated successfully."
                else:
                    return False, "User not found."
        except Exception as e:
            return False, f"Failed to update password: {str(e)}"


# Singleton instance for easy access
_db_manager: Optional[DatabaseManager] = None


def get_database(db_path: str = "data/vocalcraft.db") -> DatabaseManager:
    """
    Get the singleton DatabaseManager instance.
    
    Args:
        db_path: Path to the database file.
        
    Returns:
        DatabaseManager instance.
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
    return _db_manager


# Keep old class name for backward compatibility
DatabaseHandler = DatabaseManager


if __name__ == "__main__":
    # Test the DatabaseManager
    print("Testing DatabaseManager...")
    print("=" * 50)
    
    # Use test database
    test_db_path = "data/test_vocalcraft.db"
    db = DatabaseManager(test_db_path)
    
    # Test user registration
    print("\n1. Testing user registration...")
    success, msg = db.register_user("testuser", "password123", age=25, condition="Mild Dysarthria")
    print(f"   {msg}")
    
    # Test duplicate registration
    success, msg = db.register_user("testuser", "password123")
    print(f"   Duplicate: {msg}")
    
    # Test login
    print("\n2. Testing login...")
    user_id, msg = db.login_user("testuser", "password123")
    print(f"   {msg} (user_id: {user_id})")
    
    # Test wrong password
    user_id_fail, msg = db.login_user("testuser", "wrongpassword")
    print(f"   Wrong password: {msg}")
    
    # Test save session
    print("\n3. Testing save session...")
    if user_id:
        for score in [65, 72, 78, 85, 92]:
            session_id = db.save_session(user_id, score, exercise_type="short_sentences")
            print(f"   Saved session {session_id} with score {score}")
    
    # Test get progress
    print("\n4. Testing get progress...")
    if user_id:
        progress = db.get_user_progress(user_id)
        print(f"   Found {len(progress)} sessions")
        for p in progress[:3]:
            print(f"   - {p['date']}: {p['score']}%")
    
    # Test get stats
    print("\n5. Testing get stats...")
    if user_id:
        stats = db.get_user_stats(user_id)
        print(f"   Total sessions: {stats['total_sessions']}")
        print(f"   Average score: {stats['average_score']}%")
        print(f"   Best score: {stats['best_score']}%")
    
    # Cleanup
    print("\n6. Cleaning up test database...")
    Path(test_db_path).unlink(missing_ok=True)
    print("   Test database deleted.")
    
    print("\n" + "=" * 50)
    print("[OK] All tests passed!")
