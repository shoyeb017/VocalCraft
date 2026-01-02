"""
Exercises Module for VocalCraft
Handles loading and managing speech therapy exercises.
"""

import json
import os
from typing import List, Dict, Optional
import random


class ExerciseManager:
    """
    Manages speech therapy exercises loaded from JSON.
    Provides methods for browsing, filtering, and tracking exercises.
    """
    
    # Path to fallback exercises file
    DEFAULT_EXERCISES_PATH = "assets/default_exercises.json"

    def __init__(self, exercises_path: str = "assets/exercises.json"):
        """
        Initialize the ExerciseManager.
        
        Args:
            exercises_path: Path to the exercises JSON file.
        """
        self.exercises_path = exercises_path
        self.data: Dict = {}
        self.categories: List[Dict] = []
        
        # Navigation state
        self.current_category_id: Optional[str] = None
        self.current_exercise_index: int = 0
        self._current_exercises: List[Dict] = []
        
        self._load_exercises()

    def _load_exercises(self):
        """Load exercises from the JSON file."""
        try:
            if os.path.exists(self.exercises_path):
                with open(self.exercises_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    self.categories = self.data.get('categories', [])
            else:
                print(f"[WARN] Exercises file not found: {self.exercises_path}")
                self._load_default_exercises()
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in exercises file: {e}")
            self._load_default_exercises()
        except Exception as e:
            print(f"[ERROR] Failed to load exercises: {e}")
            self._load_default_exercises()

    def _load_default_exercises(self):
        """Load default exercises from the fallback JSON file."""
        try:
            if os.path.exists(self.DEFAULT_EXERCISES_PATH):
                with open(self.DEFAULT_EXERCISES_PATH, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    self.categories = self.data.get('categories', [])
                print(f"[INFO] Loaded default exercises from: {self.DEFAULT_EXERCISES_PATH}")
            else:
                print(f"[WARN] Default exercises file not found: {self.DEFAULT_EXERCISES_PATH}")
                self._create_minimal_fallback()
        except Exception as e:
            print(f"[ERROR] Failed to load default exercises: {e}")
            self._create_minimal_fallback()

    def _create_minimal_fallback(self):
        """Create minimal hardcoded fallback if all files fail."""
        self.categories = [
            {
                "id": "fallback",
                "name": "Fallback Exercises",
                "exercises": [
                    {"id": "fb_001", "text": "Hello.", "difficulty": 1, "targetDuration": 2}
                ]
            }
        ]

    def reload(self):
        """Reload exercises from file."""
        self._load_exercises()

    def get_categories(self) -> List[Dict]:
        """
        Get all exercise categories.
        
        Returns:
            List of category dictionaries.
        """
        return self.categories

    def get_category_names(self) -> List[str]:
        """
        Get list of category names.
        
        Returns:
            List of category name strings.
        """
        return [cat.get('name', 'Unknown') for cat in self.categories]

    def get_category_by_id(self, category_id: str) -> Optional[Dict]:
        """
        Get a category by its ID.
        
        Args:
            category_id: The category ID to find.
            
        Returns:
            Category dictionary or None.
        """
        for category in self.categories:
            if category.get('id') == category_id:
                return category
        return None

    def get_exercises_by_category(self, category_id: str) -> List[Dict]:
        """
        Get all exercises in a category.
        
        Args:
            category_id: The category ID.
            
        Returns:
            List of exercise dictionaries.
        """
        category = self.get_category_by_id(category_id)
        if category:
            return category.get('exercises', [])
        return []

    def get_exercise_by_id(self, exercise_id: str) -> Optional[Dict]:
        """
        Find an exercise by its ID across all categories.
        
        Args:
            exercise_id: The exercise ID to find.
            
        Returns:
            Exercise dictionary or None.
        """
        for category in self.categories:
            for exercise in category.get('exercises', []):
                if exercise.get('id') == exercise_id:
                    return exercise
        return None

    def get_exercises_by_difficulty(self, difficulty: int) -> List[Dict]:
        """
        Get all exercises with a specific difficulty level.
        
        Args:
            difficulty: Difficulty level (1-4).
            
        Returns:
            List of matching exercises.
        """
        exercises = []
        for category in self.categories:
            for exercise in category.get('exercises', []):
                if exercise.get('difficulty') == difficulty:
                    exercises.append(exercise)
        return exercises

    def get_all_exercises(self) -> List[Dict]:
        """
        Get all exercises from all categories.
        
        Returns:
            List of all exercise dictionaries.
        """
        exercises = []
        for category in self.categories:
            exercises.extend(category.get('exercises', []))
        return exercises

    def get_random_exercise(self, category_id: Optional[str] = None, difficulty: Optional[int] = None) -> Optional[Dict]:
        """
        Get a random exercise, optionally filtered by category or difficulty.
        
        Args:
            category_id: Optional category filter.
            difficulty: Optional difficulty filter.
            
        Returns:
            Random exercise dictionary or None.
        """
        if category_id:
            exercises = self.get_exercises_by_category(category_id)
        elif difficulty:
            exercises = self.get_exercises_by_difficulty(difficulty)
        else:
            exercises = self.get_all_exercises()
        
        if exercises:
            return random.choice(exercises)
        return None

    def get_total_count(self) -> int:
        """
        Get total number of exercises.
        
        Returns:
            Total exercise count.
        """
        return sum(len(cat.get('exercises', [])) for cat in self.categories)

    def get_metadata(self) -> Dict:
        """
        Get exercise metadata.
        
        Returns:
            Metadata dictionary.
        """
        return self.data.get('metadata', {})

    # ==================== Navigation Methods ====================

    def set_category(self, category_id: str) -> bool:
        """
        Set the current category for navigation.
        Resets the exercise index to 0.
        
        Args:
            category_id: The category ID to set.
            
        Returns:
            True if category was found and set, False otherwise.
        """
        category = self.get_category_by_id(category_id)
        if category:
            self.current_category_id = category_id
            self._current_exercises = category.get('exercises', [])
            self.current_exercise_index = 0
            return True
        return False

    def get_current_exercise(self) -> Optional[Dict]:
        """
        Get the current exercise based on navigation state.
        
        Returns:
            Current exercise dictionary or None.
        """
        if not self._current_exercises:
            return None
        
        if 0 <= self.current_exercise_index < len(self._current_exercises):
            return self._current_exercises[self.current_exercise_index]
        return None

    def get_next_exercise(self) -> Optional[Dict]:
        """
        Move to and return the next exercise in the current category.
        Wraps around to the first exercise if at the end.
        
        Returns:
            Next exercise dictionary or None if no exercises.
        """
        if not self._current_exercises:
            return None
        
        self.current_exercise_index += 1
        if self.current_exercise_index >= len(self._current_exercises):
            self.current_exercise_index = 0  # Wrap around
        
        return self.get_current_exercise()

    def get_previous_exercise(self) -> Optional[Dict]:
        """
        Move to and return the previous exercise in the current category.
        Wraps around to the last exercise if at the beginning.
        
        Returns:
            Previous exercise dictionary or None if no exercises.
        """
        if not self._current_exercises:
            return None
        
        self.current_exercise_index -= 1
        if self.current_exercise_index < 0:
            self.current_exercise_index = len(self._current_exercises) - 1  # Wrap around
        
        return self.get_current_exercise()

    def go_to_exercise(self, index: int) -> Optional[Dict]:
        """
        Jump to a specific exercise index.
        
        Args:
            index: The exercise index to jump to.
            
        Returns:
            Exercise at the index or None if invalid.
        """
        if not self._current_exercises:
            return None
        
        if 0 <= index < len(self._current_exercises):
            self.current_exercise_index = index
            return self.get_current_exercise()
        return None

    def get_exercise_position(self) -> tuple:
        """
        Get the current exercise position.
        
        Returns:
            Tuple of (current_index, total_count) - 1-based for display.
        """
        total = len(self._current_exercises)
        if total == 0:
            return (0, 0)
        return (self.current_exercise_index + 1, total)

    def has_next(self) -> bool:
        """Check if there's a next exercise (before wrapping)."""
        return self.current_exercise_index < len(self._current_exercises) - 1

    def has_previous(self) -> bool:
        """Check if there's a previous exercise (before wrapping)."""
        return self.current_exercise_index > 0

    def reset_navigation(self):
        """Reset navigation to the first exercise in current category."""
        self.current_exercise_index = 0


# Singleton instance for easy access
_exercise_manager: Optional[ExerciseManager] = None


def get_exercise_manager(exercises_path: str = "assets/exercises.json") -> ExerciseManager:
    """
    Get the singleton ExerciseManager instance.
    
    Args:
        exercises_path: Path to exercises JSON file.
        
    Returns:
        ExerciseManager instance.
    """
    global _exercise_manager
    if _exercise_manager is None:
        _exercise_manager = ExerciseManager(exercises_path)
    return _exercise_manager


if __name__ == "__main__":
    # Test the ExerciseManager
    print("Testing ExerciseManager...")
    
    manager = ExerciseManager()
    
    print(f"\nTotal exercises: {manager.get_total_count()}")
    print(f"Categories: {manager.get_category_names()}")
    
    print("\nExercises by category:")
    for cat in manager.get_categories():
        exercises = cat.get('exercises', [])
        print(f"  {cat['name']}: {len(exercises)} exercises")
    
    print("\nRandom exercise:")
    exercise = manager.get_random_exercise()
    if exercise:
        print(f"  {exercise['text']}")
        print(f"  Difficulty: {exercise.get('difficulty', 'N/A')}")
