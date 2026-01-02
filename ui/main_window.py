"""
Main Window Module for VocalCraft
The primary GUI using CustomTkinter with modern sidebar navigation.

This module provides the main application window with:
- Sidebar navigation (Practice, My Stats, History, Profile, Logout)
- Dynamic content area that switches between views
- User session management
"""

import customtkinter as ctk
import threading
import json
import os
from typing import Optional, Callable, Dict, Any, List
from abc import ABC, abstractmethod
from datetime import datetime

# Matplotlib imports for dashboard charts
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Import project modules
from audio_processor import AudioRecorder
from speech_analyzer import SpeechAnalyzer
from ui.charts import AudioVisualizer, ProgressChart
from ui.rocket_feedback import RocketFeedback
from database import DatabaseManager, get_database
from exercises import ExerciseManager, get_exercise_manager


# ============================================================================
# BASE VIEW CLASS
# ============================================================================

class BaseView(ctk.CTkFrame):
    """
    Abstract base class for all content views.
    
    All views that can be displayed in the content area should inherit from this.
    Provides common interface for view lifecycle management.
    """

    def __init__(self, master: ctk.CTkFrame, main_window: 'VocalCraftMainWindow', **kwargs):
        """
        Initialize the base view.
        
        Args:
            master: The parent frame (content area).
            main_window: Reference to the main window for accessing shared resources.
            **kwargs: Additional arguments passed to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.main_window = main_window
        self.configure(fg_color="transparent")

    @abstractmethod
    def on_show(self) -> None:
        """Called when the view becomes visible. Override to refresh data."""
        pass

    def on_hide(self) -> None:
        """Called when the view is about to be hidden. Override for cleanup."""
        pass


# ============================================================================
# PRACTICE VIEW
# ============================================================================

class PracticeView(BaseView):
    """
    The main practice view for speech therapy exercises.
    
    Displays:
    - Target sentence to practice
    - Record button with microphone error handling
    - Audio visualization (waveform and spectrogram)
    - Rocket feedback widget for gamification
    - Score and feedback display
    """

    def __init__(self, master: ctk.CTkFrame, main_window: 'VocalCraftMainWindow', **kwargs):
        """
        Initialize the practice view.
        
        Args:
            master: The parent frame (content area).
            main_window: Reference to the main window.
        """
        super().__init__(master, main_window, **kwargs)
        
        # State variables
        self.is_recording: bool = False
        self.is_processing: bool = False
        self.has_completed_exercise: bool = False
        self.microphone_available: bool = True
        self.current_audio_file: Optional[str] = None
        
        # Get shared resources from main window
        self.audio_recorder = main_window.audio_recorder
        self.speech_analyzer = main_window.speech_analyzer
        self.exercise_manager = main_window.exercise_manager
        
        # Set initial category
        self.exercise_manager.set_category("short_sentences")
        
        # Build UI
        self._create_widgets()
        self._update_exercise_display()

    def _create_widgets(self) -> None:
        """Create all UI widgets for the practice view."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Rocket feedback column
        self.grid_rowconfigure(0, weight=0)  # Target sentence
        self.grid_rowconfigure(1, weight=0)  # Controls
        self.grid_rowconfigure(2, weight=1)  # Visualization
        self.grid_rowconfigure(3, weight=0)  # Feedback

        # ===== Category Selector (top bar) =====
        self.category_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.category_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.category_label = ctk.CTkLabel(
            self.category_frame,
            text="Category:",
            font=ctk.CTkFont(size=14)
        )
        self.category_label.pack(side="left", padx=(0, 10))

        self.category_menu = ctk.CTkOptionMenu(
            self.category_frame,
            values=["Breathing", "Vowels", "Short Sentences", "Consonants", "Functional"],
            command=self._on_category_change,
            width=180
        )
        self.category_menu.set("Short Sentences")
        self.category_menu.pack(side="left")

        # ===== Target Sentence Section =====
        self.target_frame = ctk.CTkFrame(self, corner_radius=15)
        self.target_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=(0, 15))

        self.target_title = ctk.CTkLabel(
            self.target_frame,
            text="Target Sentence",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray40", "gray70")
        )
        self.target_title.pack(pady=(15, 5))

        self.progress_label = ctk.CTkLabel(
            self.target_frame,
            text="Exercise 1 of 1 | Difficulty: *",
            font=ctk.CTkFont(size=12),
            text_color=("#3498db", "#5dade2")
        )
        self.progress_label.pack(pady=(0, 5))

        self.target_sentence = ctk.CTkLabel(
            self.target_frame,
            text="Loading...",
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=700
        )
        self.target_sentence.pack(pady=(10, 20), padx=30)

        # ===== Controls Section =====
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=2, column=0, sticky="ew", pady=10, padx=(0, 15))

        # Navigation buttons
        self.prev_button = ctk.CTkButton(
            self.controls_frame,
            text="< Previous",
            font=ctk.CTkFont(size=14),
            width=120,
            height=40,
            corner_radius=20,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            command=self._prev_exercise
        )
        self.prev_button.pack(side="left", padx=10)

        # Record button
        self.record_button = ctk.CTkButton(
            self.controls_frame,
            text="Record",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=180,
            height=55,
            corner_radius=27,
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226"),
            command=self._on_record_click
        )
        self.record_button.pack(side="left", padx=30)

        self.next_button = ctk.CTkButton(
            self.controls_frame,
            text="Next >",
            font=ctk.CTkFont(size=14),
            width=120,
            height=40,
            corner_radius=20,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            command=self._next_exercise
        )
        self.next_button.pack(side="left", padx=10)

        # Status label
        self.status_label = ctk.CTkLabel(
            self.controls_frame,
            text="Press Record to start",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        self.status_label.pack(side="right", padx=20)

        # ===== Visualization Section =====
        self.viz_frame = ctk.CTkFrame(self, corner_radius=15)
        self.viz_frame.grid(row=3, column=0, sticky="nsew", pady=15, padx=(0, 15))

        self.visualizer = AudioVisualizer(self.viz_frame)

        # ===== Rocket Feedback (right side) =====
        self.rocket_feedback = RocketFeedback(self, width=140, height=350)
        self.rocket_feedback.grid(row=1, column=1, rowspan=3, sticky="ns", pady=(0, 15))

        # ===== Score/Feedback Section =====
        self.feedback_frame = ctk.CTkFrame(self, corner_radius=15)
        self.feedback_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(15, 0))

        self.score_frame = ctk.CTkFrame(self.feedback_frame, fg_color="transparent")
        self.score_frame.pack(pady=15)

        self.score_label = ctk.CTkLabel(
            self.score_frame,
            text="Score: --",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2ecc71", "#27ae60")
        )
        self.score_label.pack()

        self.feedback_text = ctk.CTkLabel(
            self.score_frame,
            text="Record your voice to receive feedback",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray60")
        )
        self.feedback_text.pack(pady=(5, 0))

    def on_show(self) -> None:
        """Called when the practice view becomes visible."""
        self._update_exercise_display()

    def _on_category_change(self, category: str) -> None:
        """
        Handle category selection change.
        
        Args:
            category: The selected category display name.
        """
        # Map display names to category IDs
        category_map: Dict[str, str] = {
            "Breathing": "breathing",
            "Vowels": "vowels",
            "Short Sentences": "short_sentences",
            "Consonants": "consonants",
            "Functional": "functional"
        }
        category_id = category_map.get(category, "short_sentences")
        self.exercise_manager.set_category(category_id)
        self._update_exercise_display()
        self._reset_feedback()

    def _update_exercise_display(self) -> None:
        """Update the displayed exercise from the exercise manager."""
        exercise = self.exercise_manager.get_current_exercise()
        if not exercise:
            self.target_sentence.configure(text="No exercises available")
            self.progress_label.configure(text="")
            return

        text = exercise.get('text', 'No text available')
        difficulty = exercise.get('difficulty', 1)
        current, total = self.exercise_manager.get_exercise_position()

        self.target_sentence.configure(text=text)
        
        # Create difficulty stars (using asterisks for Windows compatibility)
        stars = "*" * difficulty
        self.progress_label.configure(
            text=f"Exercise {current} of {total} | Difficulty: {stars}"
        )

    def _next_exercise(self) -> None:
        """Navigate to the next exercise. Only allowed after completing current exercise."""
        if not self.has_completed_exercise:
            self.status_label.configure(
                text="Complete this exercise first!",
                text_color=("#e74c3c", "#c0392b")
            )
            return
        
        self.exercise_manager.get_next_exercise()
        self._update_exercise_display()
        self._reset_feedback()
        self.has_completed_exercise = False

    def _prev_exercise(self) -> None:
        """Navigate to the previous exercise."""
        self.exercise_manager.get_previous_exercise()
        self._update_exercise_display()
        self._reset_feedback()
        self.has_completed_exercise = False

    def _reset_feedback(self) -> None:
        """Reset all feedback displays to initial state."""
        self.rocket_feedback.reset()
        self.score_label.configure(text="Score: --")
        self.feedback_text.configure(text="Record your voice to receive feedback")
        self.visualizer.clear()

    # ==================== Recording Logic ====================

    def _on_record_click(self) -> None:
        """
        Handle record button click.
        
        Toggles between recording and stopped states.
        Includes error handling for microphone issues.
        """
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self) -> None:
        """
        Start audio recording with error handling.
        
        Attempts to start the microphone. If it fails (e.g., no microphone detected),
        shows an error dialog and disables the record button.
        Disables the record button during recording to prevent double-clicks.
        """
        try:
            # Disable button immediately to prevent double-clicks
            self.record_button.configure(
                state="disabled",
                text="Recording...",
                fg_color=("#3498db", "#2980b9")
            )
            
            # Attempt to start recording
            success = self.audio_recorder.start_recording()
            
            if not success:
                # Recording failed to start - re-enable button
                self.record_button.configure(
                    state="normal",
                    text="Record",
                    fg_color=("#e74c3c", "#c0392b")
                )
                self._show_microphone_error("Failed to start recording. Please check your microphone.")
                return
            
            # Recording started successfully
            self.is_recording = True
            self.microphone_available = True
            
            # Update UI to show recording state (button stays disabled)
            self.status_label.configure(
                text="Recording... Click Stop when done",
                text_color=("#e74c3c", "#c0392b")
            )
            
            # Re-enable button for stopping (but with Stop text)
            self.record_button.configure(
                state="normal",
                text="Stop",
                fg_color=("#3498db", "#2980b9"),
                hover_color=("#2980b9", "#1f6dad")
            )
            
        except OSError as e:
            # PyAudio OSError - typically "No Default Input Device Available"
            error_msg = str(e)
            if "input" in error_msg.lower() or "device" in error_msg.lower():
                self._show_microphone_error(
                    "Microphone not detected.\n\nPlease check your settings and ensure a microphone is connected."
                )
            else:
                self._show_microphone_error(f"Audio error: {error_msg}")
                
        except Exception as e:
            # Catch any other unexpected errors
            self._show_microphone_error(f"Unexpected error: {str(e)}")

    def _show_microphone_error(self, message: str) -> None:
        """
        Display a microphone error dialog and disable recording.
        
        Args:
            message: The error message to display to the user.
        """
        self.microphone_available = False
        self.is_recording = False
        
        # Disable record button
        self.record_button.configure(
            state="disabled",
            text="Mic Unavailable",
            fg_color=("gray60", "gray40")
        )
        self.status_label.configure(
            text="Microphone error - check settings",
            text_color=("#e74c3c", "#c0392b")
        )
        
        # Create error dialog
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Microphone Error")
        error_dialog.geometry("400x200")
        error_dialog.resizable(False, False)
        error_dialog.transient(self.main_window)
        error_dialog.grab_set()
        
        # Center the dialog
        error_dialog.update_idletasks()
        x = self.main_window.winfo_x() + (self.main_window.winfo_width() - 400) // 2
        y = self.main_window.winfo_y() + (self.main_window.winfo_height() - 200) // 2
        error_dialog.geometry(f"400x200+{x}+{y}")
        
        # Error icon and message
        error_label = ctk.CTkLabel(
            error_dialog,
            text="[!] Microphone Error",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#e74c3c", "#e74c3c")
        )
        error_label.pack(pady=(25, 10))
        
        message_label = ctk.CTkLabel(
            error_dialog,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=350
        )
        message_label.pack(pady=10)
        
        # Retry button
        def retry_microphone() -> None:
            """Attempt to re-enable the microphone."""
            error_dialog.destroy()
            self.record_button.configure(
                state="normal",
                text="Record",
                fg_color=("#e74c3c", "#c0392b")
            )
            self.status_label.configure(
                text="Press Record to try again",
                text_color=("gray50", "gray60")
            )
            self.microphone_available = True
        
        retry_button = ctk.CTkButton(
            error_dialog,
            text="Retry",
            width=100,
            command=retry_microphone
        )
        retry_button.pack(pady=15)

    def _stop_recording(self) -> None:
        """
        Stop recording and process the audio.
        
        Saves the recording to the user's folder and initiates analysis.
        Keeps the record button disabled during processing.
        """
        self.is_recording = False
        self.is_processing = True
        
        # Disable button and show analyzing state
        self.record_button.configure(
            state="disabled",
            text="Analyzing...",
            fg_color=("#f39c12", "#e67e22")
        )
        self.status_label.configure(
            text="Analyzing your speech...",
            text_color=("#f39c12", "#e67e22")
        )
        
        # Stop recording
        self.audio_recorder.stop_recording()
        
        # Save to user folder using the new save_recording method
        username = self.main_window.current_username or "guest"
        audio_file = self.audio_recorder.save_recording(username)
        
        if audio_file:
            self.current_audio_file = audio_file
            # Process in background thread
            threading.Thread(
                target=self._process_recording,
                args=(audio_file,),
                daemon=True
            ).start()
        else:
            # Fallback to simple save
            audio_file = "output.wav"
            self.audio_recorder.save_wav(audio_file)
            self.current_audio_file = audio_file
            threading.Thread(
                target=self._process_recording,
                args=(audio_file,),
                daemon=True
            ).start()

    def _process_recording(self, audio_file: str) -> None:
        """
        Process the recorded audio file in a background thread.
        
        Analyzes the audio, generates visualizations, and computes the score.
        
        Args:
            audio_file: Path to the WAV file to process.
        """
        try:
            # Get visual data (waveform and spectrogram)
            visual_data = self.speech_analyzer.get_visual_data(audio_file)
            
            # Update visualization on main thread
            self.after(0, lambda: self.visualizer.update_full(
                visual_data['waveform'],
                visual_data['spectrogram'],
                visual_data['sample_rate']
            ))
            
            # Get current target text for comparison
            exercise = self.exercise_manager.get_current_exercise()
            target_text = exercise.get('text', '') if exercise else ''
            
            # Score the speech using transcription and Levenshtein distance
            try:
                result = self.speech_analyzer.score_speech(audio_file, target_text)
            except Exception as score_error:
                print(f"Scoring error: {score_error}")
                # Fallback result if scoring fails completely
                result = {
                    'score': 50.0,
                    'transcribed': None,
                    'method': 'fallback',
                    'error': str(score_error)
                }
            
            # Update UI with results on main thread
            self.after(0, lambda: self._update_feedback(result))
            
        except Exception as e:
            error_msg = str(e)
            print(f"Processing error: {error_msg}")
            # Create a fallback result to ensure UI updates
            fallback_result = {
                'score': 0.0,
                'transcribed': None,
                'method': 'error',
                'error': error_msg
            }
            self.after(0, lambda: self._update_feedback(fallback_result))
            self.after(0, lambda: self.status_label.configure(
                text=f"Error: {error_msg[:50]}...",
                text_color=("#e74c3c", "#c0392b")
            ))

    def _update_feedback(self, result: Dict[str, Any]) -> None:
        """
        Update the feedback display with scoring results.
        
        Re-enables the record button after analysis is complete.
        Results persist on screen until user records again or navigates.
        
        Args:
            result: Dictionary containing score, transcribed text, and method used.
        """
        score: float = result.get('score', 0)
        transcribed: str = result.get('transcribed', '')
        method: str = result.get('method', 'transcription')
        
        # Mark exercise as completed and processing as done
        self.has_completed_exercise = True
        self.is_processing = False
        
        # Re-enable the record button
        self.record_button.configure(
            state="normal",
            text="Record Again",
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226")
        )
        
        # Update rocket feedback widget
        self.rocket_feedback.update_fuel(score)
        
        # Update score display
        self.score_label.configure(text=f"Score: {score:.0f}%")
        
        # Update feedback text based on results
        if transcribed:
            self.feedback_text.configure(text=f'You said: "{transcribed}"')
        elif method == 'intensity':
            self.feedback_text.configure(text="Scored based on voice intensity")
        else:
            self.feedback_text.configure(text="Could not transcribe. Try speaking clearer.")
        
        # Update status with appropriate message based on score
        if score >= 70:
            self.status_label.configure(
                text="Great job! Click 'Next >' to continue or record again.",
                text_color=("#27ae60", "#2ecc71")
            )
        else:
            self.status_label.configure(
                text="Try again or click 'Next >' to continue.",
                text_color=("gray50", "gray60")
            )
        
        # Save session to database
        if self.main_window.current_user_id and self.current_audio_file:
            exercise = self.exercise_manager.get_current_exercise()
            exercise_type = exercise.get('id', 'unknown') if exercise else 'unknown'
            
            self.main_window.database.save_session(
                user_id=self.main_window.current_user_id,
                exercise_type=exercise_type,
                score=score,
                audio_path=self.current_audio_file
            )


# ============================================================================
# STATS VIEW (DASHBOARD)
# ============================================================================

class StatsView(BaseView):
    """
    Comprehensive statistics dashboard view.
    
    Shows:
    - Summary cards (Total Time, Avg Score, Total Exercises)
    - Category breakdown pie/bar chart
    - Improvement over time line chart
    """

    def __init__(self, master: ctk.CTkFrame, main_window: 'VocalCraftMainWindow', **kwargs):
        """
        Initialize the dashboard view.
        
        Args:
            master: The parent frame (content area).
            main_window: Reference to the main window.
        """
        super().__init__(master, main_window, **kwargs)
        plt.style.use('dark_background')
        self.category_canvas = None
        self.progress_canvas = None
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create the dashboard widgets with grid layout."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Statistics Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(15, 20))

        # ===== TOP ROW: Summary Cards =====
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=30)

        self.stat_cards: Dict[str, ctk.CTkFrame] = {}
        stats_config = [
            ("total_time", "⏱️ Total Practice Time", "0 min", "#9b59b6"),
            ("avg_score", "📈 Average Score", "0%", "#3498db"),
            ("total_exercises", "🎯 Total Exercises", "0", "#27ae60"),
        ]

        for i, (key, label, default, color) in enumerate(stats_config):
            card = self._create_stat_card(self.cards_frame, label, default, color)
            card.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
            self.stat_cards[key] = card
            self.cards_frame.grid_columnconfigure(i, weight=1)

        # ===== CHARTS ROW =====
        self.charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_frame.pack(fill="both", expand=True, padx=30, pady=15)
        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)
        self.charts_frame.grid_rowconfigure(0, weight=1)

        # Chart 1: Category Breakdown (Left)
        self.category_frame = ctk.CTkFrame(self.charts_frame, corner_radius=15)
        self.category_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.category_title = ctk.CTkLabel(
            self.category_frame,
            text="📊 Practice by Category",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.category_title.pack(pady=(15, 5))

        self.category_chart_container = ctk.CTkFrame(
            self.category_frame,
            fg_color="transparent"
        )
        self.category_chart_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Chart 2: Progress Over Time (Right)
        self.progress_frame = ctk.CTkFrame(self.charts_frame, corner_radius=15)
        self.progress_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.progress_title = ctk.CTkLabel(
            self.progress_frame,
            text="📈 Improvement Over Time",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.progress_title.pack(pady=(15, 5))

        self.progress_chart_container = ctk.CTkFrame(
            self.progress_frame,
            fg_color="transparent"
        )
        self.progress_chart_container.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_stat_card(
        self, 
        parent: ctk.CTkFrame, 
        label: str, 
        value: str,
        color: str = "#3498db"
    ) -> ctk.CTkFrame:
        """Create a summary statistic card with icon and value."""
        card = ctk.CTkFrame(parent, corner_radius=15, height=120)
        card.pack_propagate(False)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=(color, color)
        )
        value_label.pack(pady=(25, 5))
        card.value_label = value_label

        text_label = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        text_label.pack()

        return card

    def _create_category_chart(self, category_data: Dict[str, int]) -> None:
        """Create a bar chart showing category breakdown."""
        # Clear previous chart
        for widget in self.category_chart_container.winfo_children():
            widget.destroy()

        if not category_data:
            placeholder = ctk.CTkLabel(
                self.category_chart_container,
                text="No category data yet.\nStart practicing!",
                font=ctk.CTkFont(size=13),
                text_color=("gray50", "gray60")
            )
            placeholder.pack(expand=True)
            return

        # Create figure
        fig = Figure(figsize=(4, 3), dpi=100, facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')

        # Prepare data
        categories = list(category_data.keys())
        counts = list(category_data.values())
        
        # Truncate long category names
        short_categories = [c[:15] + '...' if len(c) > 15 else c for c in categories]
        
        # Colors
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
        bar_colors = [colors[i % len(colors)] for i in range(len(categories))]

        # Create horizontal bar chart
        y_pos = np.arange(len(categories))
        ax.barh(y_pos, counts, color=bar_colors, height=0.6)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(short_categories, fontsize=9, color='white')
        ax.set_xlabel('Sessions', fontsize=10, color='gray')
        ax.tick_params(colors='gray')
        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_color('gray')

        fig.tight_layout()

        # Embed in tkinter
        self.category_canvas = FigureCanvasTkAgg(fig, master=self.category_chart_container)
        self.category_canvas.draw()
        self.category_canvas.get_tk_widget().pack(fill='both', expand=True)

    def _create_progress_chart(self, progress_data: List[tuple]) -> None:
        """Create a line chart showing score improvement over time."""
        # Clear previous chart
        for widget in self.progress_chart_container.winfo_children():
            widget.destroy()

        if not progress_data:
            placeholder = ctk.CTkLabel(
                self.progress_chart_container,
                text="No progress data yet.\nStart practicing!",
                font=ctk.CTkFont(size=13),
                text_color=("gray50", "gray60")
            )
            placeholder.pack(expand=True)
            return

        # Create figure
        fig = Figure(figsize=(4, 3), dpi=100, facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')

        # Prepare data
        dates = [d[0] for d in progress_data]
        scores = [d[1] for d in progress_data]

        # Format dates for display
        short_dates = []
        for d in dates:
            try:
                dt = datetime.strptime(d, '%Y-%m-%d')
                short_dates.append(dt.strftime('%m/%d'))
            except:
                short_dates.append(d[-5:])

        x = range(len(dates))
        
        # Plot line with markers
        ax.plot(x, scores, color='#2ecc71', linewidth=2, marker='o', markersize=5)
        ax.fill_between(x, scores, alpha=0.2, color='#2ecc71')

        # Add trend line if enough data
        if len(scores) > 2:
            z = np.polyfit(list(x), scores, 1)
            p = np.poly1d(z)
            ax.plot(x, p(list(x)), '--', color='#3498db', linewidth=1.5, alpha=0.7, label='Trend')
            ax.legend(loc='lower right', fontsize=8)

        ax.set_ylabel('Avg Score (%)', fontsize=10, color='gray')
        ax.set_xlabel('Date', fontsize=10, color='gray')
        ax.set_ylim([0, 100])
        ax.tick_params(colors='gray')

        # X-axis labels
        if len(short_dates) <= 7:
            ax.set_xticks(list(x))
            ax.set_xticklabels(short_dates, rotation=45, ha='right', fontsize=8)
        else:
            # Show fewer labels for many dates
            step = max(1, len(short_dates) // 5)
            ax.set_xticks(list(x)[::step])
            ax.set_xticklabels(short_dates[::step], rotation=45, ha='right', fontsize=8)

        for spine in ax.spines.values():
            spine.set_color('gray')

        fig.tight_layout()

        # Embed in tkinter
        self.progress_canvas = FigureCanvasTkAgg(fig, master=self.progress_chart_container)
        self.progress_canvas.draw()
        self.progress_canvas.get_tk_widget().pack(fill='both', expand=True)

    def on_show(self) -> None:
        """Load and display dashboard data when view becomes visible."""
        self._load_dashboard()

    def on_hide(self) -> None:
        """Cleanup matplotlib figures to prevent memory leaks."""
        plt.close('all')

    def _load_dashboard(self) -> None:
        """Load all dashboard data from the database."""
        if not self.main_window.current_user_id:
            return

        try:
            user_id = self.main_window.current_user_id
            db = self.main_window.database

            # Get overall stats
            stats = db.get_overall_stats(user_id)

            # Update summary cards
            total_time = stats.get('total_practice_time', 0)
            if total_time < 60:
                time_str = f"{total_time} min"
            else:
                hours = total_time // 60
                mins = total_time % 60
                time_str = f"{hours}h {mins}m"
            self.stat_cards['total_time'].value_label.configure(text=time_str)

            avg_score = stats.get('average_score', 0)
            self.stat_cards['avg_score'].value_label.configure(text=f"{avg_score:.0f}%")

            total_sessions = stats.get('total_sessions', 0)
            self.stat_cards['total_exercises'].value_label.configure(text=str(total_sessions))

            # Load category breakdown chart
            category_data = db.get_category_breakdown(user_id)
            self._create_category_chart(category_data)

            # Load progress over time chart
            progress_data = db.get_average_score_over_time(user_id, days=30)
            self._create_progress_chart(progress_data)

        except Exception as e:
            print(f"Error loading dashboard: {e}")


# ============================================================================
# HISTORY VIEW
# ============================================================================

class HistoryView(BaseView):
    """
    Detailed session history view with scrollable cards.
    
    Shows each practice attempt with:
    - Date and time (formatted nicely)
    - Category and target sentence
    - Score (color-coded)
    """

    def __init__(self, master: ctk.CTkFrame, main_window: 'VocalCraftMainWindow', **kwargs):
        """
        Initialize the history view.
        
        Args:
            master: The parent frame (content area).
            main_window: Reference to the main window.
        """
        super().__init__(master, main_window, **kwargs)
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create the history view widgets."""
        # Header frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(20, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="📜 Session History",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(side="left")

        self.count_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray60")
        )
        self.count_label.pack(side="right")

        # Column headers
        self.header_row = ctk.CTkFrame(self, fg_color=("gray85", "gray25"), corner_radius=10)
        self.header_row.pack(fill="x", padx=40, pady=(5, 5))

        headers = [
            ("Date & Time", 180),
            ("Category", 150),
            ("Exercise", 350),
            ("Score", 100)
        ]
        for text, width in headers:
            lbl = ctk.CTkLabel(
                self.header_row,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor="w"
            )
            lbl.pack(side="left", padx=10, pady=8)

        # Scrollable frame for history items
        self.history_scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=15,
            fg_color=("gray95", "gray17")
        )
        self.history_scroll.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    def on_show(self) -> None:
        """Load session history when view becomes visible."""
        self._load_history()

    def _load_history(self) -> None:
        """Load and display detailed session history from database."""
        if not self.main_window.current_user_id:
            return

        try:
            # Clear existing items
            for widget in self.history_scroll.winfo_children():
                widget.destroy()

            # Get all attempts from database
            attempts = self.main_window.database.get_all_attempts(
                self.main_window.current_user_id,
                limit=100
            )

            if not attempts:
                self._show_placeholder()
                self.count_label.configure(text="0 sessions")
                return

            self.count_label.configure(text=f"{len(attempts)} sessions")

            # Load exercise data for sentence lookup
            exercises = {}
            try:
                exercise_mgr = self.main_window.exercise_manager
                for cat in exercise_mgr.get_categories():
                    cat_id = cat.get('id', '')
                    for ex in exercise_mgr.get_exercises_by_category(cat_id):
                        ex_id = ex.get('id', '')
                        exercises[ex_id] = ex.get('text', 'Unknown exercise')
            except:
                pass

            # Create history cards
            for attempt in attempts:
                self._create_history_card(attempt, exercises)

        except Exception as e:
            print(f"Error loading history: {e}")
            self._show_placeholder()

    def _show_placeholder(self) -> None:
        """Show placeholder when no history exists."""
        placeholder = ctk.CTkLabel(
            self.history_scroll,
            text="📝 No sessions recorded yet.\n\nStart practicing to see your history here!",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray60")
        )
        placeholder.pack(pady=80)

    def _create_history_card(self, attempt: Dict[str, Any], exercises: Dict[str, str]) -> None:
        """
        Create a detailed history card for an attempt.
        
        Args:
            attempt: Dictionary with id, date, exercise_type, score, audio_path.
            exercises: Dictionary mapping exercise_id to sentence text.
        """
        card = ctk.CTkFrame(
            self.history_scroll,
            corner_radius=10,
            height=70,
            fg_color=("gray90", "gray20")
        )
        card.pack(fill="x", pady=4, padx=5)
        card.pack_propagate(False)

        # Date & Time (formatted nicely)
        date_str = attempt.get('date', '')
        try:
            dt = datetime.fromisoformat(date_str)
            formatted_date = dt.strftime("%b %d, %Y")
            formatted_time = dt.strftime("%I:%M %p")
        except:
            formatted_date = date_str[:10] if len(date_str) > 10 else date_str
            formatted_time = ""

        date_frame = ctk.CTkFrame(card, fg_color="transparent", width=180)
        date_frame.pack(side="left", padx=10, pady=5)
        date_frame.pack_propagate(False)

        ctk.CTkLabel(
            date_frame,
            text=formatted_date,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkLabel(
            date_frame,
            text=formatted_time,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w"
        ).pack(anchor="w")

        # Category
        exercise_type = attempt.get('exercise_type', 'Unknown')
        category_label = ctk.CTkLabel(
            card,
            text=exercise_type.replace('_', ' ').title() if exercise_type else "Unknown",
            font=ctk.CTkFont(size=12),
            text_color=("#3498db", "#5dade2"),
            width=150,
            anchor="w"
        )
        category_label.pack(side="left", padx=10)

        # Exercise sentence (with wrapping)
        sentence = exercises.get(exercise_type, "Exercise completed")
        if len(sentence) > 50:
            sentence = sentence[:47] + "..."
        
        sentence_label = ctk.CTkLabel(
            card,
            text=sentence,
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
            width=350,
            anchor="w",
            wraplength=340
        )
        sentence_label.pack(side="left", padx=10, expand=True)

        # Score (color-coded)
        score = attempt.get('score', 0) or 0
        if score >= 80:
            score_color = "#27ae60"  # Green
            score_bg = ("#d5f5e3", "#1e4d2b")
        elif score >= 50:
            score_color = "#f39c12"  # Orange
            score_bg = ("#fef9e7", "#4a3c1f")
        else:
            score_color = "#e74c3c"  # Red
            score_bg = ("#fadbd8", "#4a1f1f")

        score_frame = ctk.CTkFrame(
            card,
            fg_color=score_bg,
            corner_radius=8,
            width=80,
            height=40
        )
        score_frame.pack(side="right", padx=15, pady=15)
        score_frame.pack_propagate(False)

        score_label = ctk.CTkLabel(
            score_frame,
            text=f"{score:.0f}%",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=(score_color, score_color)
        )
        score_label.pack(expand=True)


# ============================================================================
# PROFILE VIEW
# ============================================================================

class ProfileView(BaseView):
    """
    User profile and settings view.
    
    Shows:
    - User information (read-only)
    - Change password form
    - Account settings
    """

    def __init__(self, master: ctk.CTkFrame, main_window: 'VocalCraftMainWindow', **kwargs):
        """
        Initialize the profile view.
        
        Args:
            master: The parent frame (content area).
            main_window: Reference to the main window.
        """
        super().__init__(master, main_window, **kwargs)
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create the profile view widgets."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="👤 Profile & Settings",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(20, 30))

        # Main container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=60)

        # ===== User Information Section =====
        self.info_frame = ctk.CTkFrame(self.container, corner_radius=15)
        self.info_frame.pack(fill="x", pady=10)

        self.info_title = ctk.CTkLabel(
            self.info_frame,
            text="📋 Account Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.info_title.pack(anchor="w", padx=20, pady=(20, 15))

        # Username (read-only)
        self.username_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.username_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            self.username_frame,
            text="Username:",
            font=ctk.CTkFont(size=13),
            width=120,
            anchor="w"
        ).pack(side="left")

        self.username_value = ctk.CTkLabel(
            self.username_frame,
            text=self.main_window.current_username or "Unknown",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#3498db", "#5dade2")
        )
        self.username_value.pack(side="left", padx=10)

        # Condition (read-only)
        self.condition_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.condition_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            self.condition_frame,
            text="Condition:",
            font=ctk.CTkFont(size=13),
            width=120,
            anchor="w"
        ).pack(side="left")

        self.condition_value = ctk.CTkLabel(
            self.condition_frame,
            text="Dysarthria",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray60")
        )
        self.condition_value.pack(side="left", padx=10)

        # Member since
        self.member_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.member_frame.pack(fill="x", padx=20, pady=(5, 20))

        ctk.CTkLabel(
            self.member_frame,
            text="Member Since:",
            font=ctk.CTkFont(size=13),
            width=120,
            anchor="w"
        ).pack(side="left")

        self.member_value = ctk.CTkLabel(
            self.member_frame,
            text="Loading...",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray60")
        )
        self.member_value.pack(side="left", padx=10)

        # ===== Change Password Section =====
        self.password_frame = ctk.CTkFrame(self.container, corner_radius=15)
        self.password_frame.pack(fill="x", pady=20)

        self.password_title = ctk.CTkLabel(
            self.password_frame,
            text="🔒 Change Password",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.password_title.pack(anchor="w", padx=20, pady=(20, 15))

        # New Password
        self.new_password_frame = ctk.CTkFrame(self.password_frame, fg_color="transparent")
        self.new_password_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            self.new_password_frame,
            text="New Password:",
            font=ctk.CTkFont(size=13),
            width=140,
            anchor="w"
        ).pack(side="left")

        self.new_password_entry = ctk.CTkEntry(
            self.new_password_frame,
            placeholder_text="Enter new password",
            show="•",
            width=250,
            height=35
        )
        self.new_password_entry.pack(side="left", padx=10)

        # Confirm Password
        self.confirm_frame = ctk.CTkFrame(self.password_frame, fg_color="transparent")
        self.confirm_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            self.confirm_frame,
            text="Confirm Password:",
            font=ctk.CTkFont(size=13),
            width=140,
            anchor="w"
        ).pack(side="left")

        self.confirm_password_entry = ctk.CTkEntry(
            self.confirm_frame,
            placeholder_text="Confirm new password",
            show="•",
            width=250,
            height=35
        )
        self.confirm_password_entry.pack(side="left", padx=10)

        # Update button and status
        self.button_frame = ctk.CTkFrame(self.password_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=20, pady=(15, 20))

        self.update_button = ctk.CTkButton(
            self.button_frame,
            text="Update Password",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=150,
            height=40,
            corner_radius=10,
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#1f6dad"),
            command=self._on_update_password
        )
        self.update_button.pack(side="left")

        self.status_label = ctk.CTkLabel(
            self.button_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        self.status_label.pack(side="left", padx=20)

        # ===== Statistics Summary =====
        self.stats_frame = ctk.CTkFrame(self.container, corner_radius=15)
        self.stats_frame.pack(fill="x", pady=10)

        self.stats_title = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Quick Stats",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.stats_title.pack(anchor="w", padx=20, pady=(20, 15))

        self.stats_content = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        self.stats_content.pack(fill="x", padx=20, pady=(0, 20))

        self.stats_labels: Dict[str, ctk.CTkLabel] = {}
        stats_items = [
            ("total", "Total Sessions:"),
            ("best", "Best Score:"),
            ("streak", "Current Streak:")
        ]

        for key, label in stats_items:
            frame = ctk.CTkFrame(self.stats_content, fg_color="transparent")
            frame.pack(fill="x", pady=3)

            ctk.CTkLabel(
                frame,
                text=label,
                font=ctk.CTkFont(size=13),
                width=150,
                anchor="w"
            ).pack(side="left")

            value_label = ctk.CTkLabel(
                frame,
                text="--",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#27ae60", "#2ecc71")
            )
            value_label.pack(side="left", padx=10)
            self.stats_labels[key] = value_label

    def on_show(self) -> None:
        """Load user data when view becomes visible."""
        self._load_user_data()

    def _load_user_data(self) -> None:
        """Load user information from database."""
        if not self.main_window.current_user_id:
            return

        try:
            user_id = self.main_window.current_user_id
            db = self.main_window.database

            # Get user info
            user = db.get_user(user_id)
            if user:
                # Update member since
                join_date = user.get('join_date', '')
                try:
                    dt = datetime.fromisoformat(join_date)
                    self.member_value.configure(text=dt.strftime("%B %d, %Y"))
                except:
                    self.member_value.configure(text=join_date[:10] if join_date else "Unknown")

                # Update condition if available
                condition = user.get('condition', 'Dysarthria')
                self.condition_value.configure(text=condition or "Dysarthria")

            # Get stats
            stats = db.get_overall_stats(user_id)
            
            self.stats_labels['total'].configure(
                text=str(stats.get('total_sessions', 0))
            )
            self.stats_labels['best'].configure(
                text=f"{stats.get('highest_score', 0):.0f}%"
            )
            self.stats_labels['streak'].configure(
                text=f"{stats.get('current_streak', 0)} days"
            )

        except Exception as e:
            print(f"Error loading user data: {e}")

    def _on_update_password(self) -> None:
        """Handle password update button click."""
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        # Validate inputs
        if not new_password or not confirm_password:
            self._show_status("Please fill in both fields.", error=True)
            return

        if new_password != confirm_password:
            self._show_status("Passwords do not match.", error=True)
            return

        if len(new_password) < 4:
            self._show_status("Password must be at least 4 characters.", error=True)
            return

        # Update password
        try:
            success, message = self.main_window.database.update_password(
                self.main_window.current_user_id,
                new_password
            )

            if success:
                self._show_status("✓ Password updated successfully!", error=False)
                self.new_password_entry.delete(0, 'end')
                self.confirm_password_entry.delete(0, 'end')
            else:
                self._show_status(message, error=True)

        except Exception as e:
            self._show_status(f"Error: {str(e)}", error=True)

    def _show_status(self, message: str, error: bool = False) -> None:
        """Display status message."""
        color = ("#e74c3c", "#c0392b") if error else ("#27ae60", "#2ecc71")
        self.status_label.configure(text=message, text_color=color)

        # Clear message after 5 seconds
        self.after(5000, lambda: self.status_label.configure(text=""))


# ============================================================================
# MAIN WINDOW
# ============================================================================

class VocalCraftMainWindow(ctk.CTk):
    """
    Main application window for VocalCraft speech therapy tool.
    
    Features:
    - Sidebar navigation with view switching
    - Dynamic content area that displays different views
    - User session management
    - Logout functionality returning to login screen
    """

    def __init__(
        self, 
        user_id: Optional[int] = None, 
        username: Optional[str] = None,
        on_logout: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the main window.
        
        Args:
            user_id: The logged-in user's database ID.
            username: The logged-in user's username (used for folder paths).
            on_logout: Callback function to execute on logout.
        """
        super().__init__()

        # Current user info
        self.current_user_id: Optional[int] = user_id
        self.current_username: Optional[str] = username
        self.on_logout_callback: Optional[Callable[[], None]] = on_logout

        # Window configuration
        title = "VocalCraft - Speech Therapy Tool"
        if username:
            title += f" - {username}"
        self.title(title)
        self.geometry("1300x850")
        self.minsize(1000, 700)

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize shared components
        self.audio_recorder = AudioRecorder()
        self.speech_analyzer = SpeechAnalyzer()
        self.database = get_database()
        self.exercise_manager = get_exercise_manager()

        # Pre-warm the speech analyzer in background to avoid first-run delay
        self._warm_up_thread = threading.Thread(
            target=self._warm_up_analyzer,
            daemon=True
        )
        self._warm_up_thread.start()

        # View management
        self.current_view: Optional[BaseView] = None
        self.views: Dict[str, BaseView] = {}

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)  # Sidebar (fixed width)
        self.grid_columnconfigure(1, weight=1)  # Content area (expandable)
        self.grid_rowconfigure(0, weight=1)

        # Build UI
        self._create_sidebar()
        self._create_content_area()

        # Show default view
        self._show_practice_view()

    def _warm_up_analyzer(self) -> None:
        """
        Pre-warm the speech analyzer in background thread.
        
        This triggers librosa's Numba JIT compilation before the user
        records, eliminating the delay on first recording analysis.
        """
        try:
            self.speech_analyzer.warm_up()
        except Exception as e:
            print(f"Analyzer warm-up error (non-critical): {e}")

    def _create_sidebar(self) -> None:
        """Create the sidebar navigation panel with navigation buttons."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)  # Push logout to bottom
        self.sidebar.grid_propagate(False)

        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="VocalCraft",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Speech Therapy Tool",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        # User info
        if self.current_username:
            self.user_label = ctk.CTkLabel(
                self.sidebar,
                text=f"Welcome, {self.current_username}",
                font=ctk.CTkFont(size=12),
                text_color=("#3498db", "#5dade2")
            )
            self.user_label.grid(row=2, column=0, padx=20, pady=(0, 20))

        # Navigation buttons
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        
        nav_items: List[tuple] = [
            ("practice", "🏠 Home / Practice", self._show_practice_view),
            ("stats", "📊 Dashboard", self._show_stats_view),
            ("history", "📜 History", self._show_history_view),
            ("profile", "👤 Profile", self._show_profile_view),
        ]

        for i, (key, text, command) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=ctk.CTkFont(size=14),
                height=45,
                corner_radius=10,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=command
            )
            btn.grid(row=i + 3, column=0, padx=15, pady=5, sticky="ew")
            self.nav_buttons[key] = btn

        # Appearance mode selector
        self.appearance_label = ctk.CTkLabel(
            self.sidebar,
            text="Appearance",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60")
        )
        self.appearance_label.grid(row=7, column=0, padx=20, pady=(20, 5), sticky="w")

        self.appearance_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light", "System"],
            command=self._change_appearance,
            width=180
        )
        self.appearance_menu.set("Dark")
        self.appearance_menu.grid(row=8, column=0, padx=20, pady=(0, 15))

        # Logout button at the bottom
        self.logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=10,
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226"),
            command=self._on_logout
        )
        self.logout_button.grid(row=9, column=0, padx=20, pady=(10, 30), sticky="ew")

    def _create_content_area(self) -> None:
        """Create the main content area where views will be displayed."""
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

    def _clear_content_area(self) -> None:
        """Clear all widgets from the content area."""
        if self.current_view:
            self.current_view.on_hide()
            self.current_view.destroy()
            self.current_view = None

    def _update_nav_selection(self, selected_key: str) -> None:
        """
        Update the visual state of navigation buttons.
        
        Args:
            selected_key: The key of the currently selected navigation item.
        """
        for key, btn in self.nav_buttons.items():
            if key == selected_key:
                btn.configure(fg_color=("#3498db", "#2980b9"))
            else:
                btn.configure(fg_color="transparent")

    # ==================== View Navigation ====================

    def _show_practice_view(self) -> None:
        """Show the practice/home view."""
        self._clear_content_area()
        self._update_nav_selection("practice")
        
        self.current_view = PracticeView(self.content_area, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.current_view.on_show()

    def _show_stats_view(self) -> None:
        """Show the statistics view."""
        self._clear_content_area()
        self._update_nav_selection("stats")
        
        self.current_view = StatsView(self.content_area, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.current_view.on_show()

    def _show_history_view(self) -> None:
        """Show the history view."""
        self._clear_content_area()
        self._update_nav_selection("history")
        
        self.current_view = HistoryView(self.content_area, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.current_view.on_show()

    def _show_profile_view(self) -> None:
        """Show the profile/settings view."""
        self._clear_content_area()
        self._update_nav_selection("profile")
        
        self.current_view = ProfileView(self.content_area, self)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.current_view.on_show()

    # ==================== Actions ====================

    def _change_appearance(self, mode: str) -> None:
        """
        Change the application appearance mode.
        
        Args:
            mode: The appearance mode ('Dark', 'Light', or 'System').
        """
        ctk.set_appearance_mode(mode.lower())

    def _on_logout(self) -> None:
        """Handle logout button click - return to login screen."""
        # Confirm logout
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirm Logout")
        confirm.geometry("300x150")
        confirm.resizable(False, False)
        confirm.transient(self)
        confirm.grab_set()

        # Center the dialog
        confirm.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 300) // 2
        y = self.winfo_y() + (self.winfo_height() - 150) // 2
        confirm.geometry(f"300x150+{x}+{y}")

        label = ctk.CTkLabel(
            confirm,
            text="Are you sure you want to logout?",
            font=ctk.CTkFont(size=14)
        )
        label.pack(pady=25)

        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack()

        def do_logout() -> None:
            """Execute the logout."""
            confirm.destroy()
            self.destroy()
            
            # Re-launch login window
            from ui.login_window import LoginWindow
            
            def on_login_success(user_id: int, username: str) -> None:
                """Callback for successful re-login."""
                new_app = VocalCraftMainWindow(
                    user_id=user_id,
                    username=username
                )
                new_app.mainloop()
            
            login = LoginWindow(on_login_success=on_login_success)
            login.mainloop()

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            fg_color=("gray70", "gray30"),
            command=confirm.destroy
        )
        cancel_btn.pack(side="left", padx=10)

        logout_btn = ctk.CTkButton(
            btn_frame,
            text="Logout",
            width=100,
            fg_color=("#e74c3c", "#c0392b"),
            command=do_logout
        )
        logout_btn.pack(side="left", padx=10)


def main() -> None:
    """Application entry point for testing."""
    app = VocalCraftMainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
