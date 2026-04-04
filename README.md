# VocalCraft - Complete Project Manual

## Speech Therapy Desktop Application

**Version:** 1.0.0  
**Platform:** Windows / macOS / Linux  
**Language:** Python 3.8+  
**GUI Framework:** CustomTkinter

---

### Setup

1. Clone or download this repository

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Note for Windows users**: If PyAudio fails to install, try:

   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [System Requirements](#3-system-requirements)
4. [Installation Guide](#4-installation-guide)
5. [Project Structure](#5-project-structure)
6. [File Descriptions](#6-file-descriptions)
7. [Database Schema](#7-database-schema)
8. [User Interface Guide](#8-user-interface-guide)
9. [How It Works](#9-how-it-works)
10. [Configuration](#10-configuration)
11. [Troubleshooting](#11-troubleshooting)
12. [API Reference](#12-api-reference)
13. [Customization](#13-customization)

---

## 1. Project Overview

### What is VocalCraft?

VocalCraft is a modern desktop application designed to help patients with speech conditions (particularly Dysarthria) practice and improve their communication skills through guided exercises and real-time feedback.

### Purpose

- Provide structured speech therapy exercises
- Record and analyze patient speech
- Give visual and gamified feedback
- Track progress over time
- Help speech therapists monitor patient improvement

### Target Users

- **Patients** with Dysarthria or other speech conditions
- **Speech therapists** monitoring patient progress
- **Caregivers** helping patients practice at home

---

## 2. Features

### Core Features

| Feature                  | Description                                                                  |
| ------------------------ | ---------------------------------------------------------------------------- |
| **User Authentication**  | Secure login/signup with password hashing (SHA-256)                          |
| **Exercise Library**     | Categorized speech exercises (breathing, vowels, sentences, tongue twisters) |
| **Audio Recording**      | High-quality 44.1kHz mono recording using PyAudio                            |
| **Speech Recognition**   | Google Speech API for transcription                                          |
| **Scoring System**       | Levenshtein similarity comparison with target text                           |
| **Visual Feedback**      | Waveform and mel-spectrogram visualization                                   |
| **Gamification**         | Rocket fuel tank widget with animations                                      |
| **Progress Tracking**    | SQLite database storing all practice sessions                                |
| **Statistics Dashboard** | Charts showing category breakdown and improvement over time                  |
| **History View**         | Detailed log of all practice attempts                                        |
| **Profile Management**   | Change password and view account details                                     |

### Technical Features

- **Threaded Recording** - UI remains responsive during recording
- **Error Handling** - Graceful microphone detection and error messages
- **Dark/Light Mode** - Switchable appearance themes
- **Modular Architecture** - View-based design for maintainability
- **Cross-Platform** - Works on Windows, macOS, Linux

---

## 3. System Requirements

### Minimum Requirements

| Component            | Requirement                             |
| -------------------- | --------------------------------------- |
| **Operating System** | Windows 10, macOS 10.14+, Ubuntu 18.04+ |
| **Python**           | 3.8 or higher                           |
| **RAM**              | 4 GB minimum                            |
| **Storage**          | 500 MB free space                       |
| **Audio**            | Microphone (built-in or external)       |
| **Display**          | 1024x768 resolution minimum             |

### Recommended

- **Python** 3.10+
- **RAM** 8 GB
- **External USB microphone** for better audio quality

---

## 4. Installation Guide

### Step 1: Clone/Download the Project

```bash
cd your-projects-folder
git clone <repository-url>
cd VocalCraft
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify PyAudio Installation

PyAudio requires special handling on some systems:

**Windows:**

```bash
pip install pyaudio
```

**macOS:**

```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### Step 5: Run the Application

```bash
python main.py
```

---

## 5. Project Structure

```
VocalCraft/
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project readme
├── MANUAL.md                  # This documentation file
│
├── audio_processor.py         # Audio recording module
├── speech_analyzer.py         # Speech recognition & scoring
├── database.py                # Database operations
├── exercises.py               # Exercise management
│
├── ui/                        # User Interface modules
│   ├── __init__.py           # Package initializer
│   ├── main_window.py        # Main application window & views
│   ├── login_window.py       # Login/Signup window
│   ├── charts.py             # Audio visualization charts
│   └── rocket_feedback.py    # Gamification widget
│
├── assets/                    # Static assets
│   ├── exercises.json        # Exercise definitions
│   └── default_exercises.json # Fallback exercises
│
└── data/                      # Data storage
    ├── vocalcraft.db         # SQLite database
    ├── schema.sql            # Database schema
    ├── queries.sql           # SQL query reference
    ├── reset_database.sql    # Database reset script
    ├── clear_data.sql        # Data clearing options
    └── recordings/           # Saved audio files
        └── {username}/       # User-specific folders
            └── {date}/       # Date-organized recordings
```

---

## 6. File Descriptions

### 6.1 Core Python Files

---

#### `main.py` - Application Entry Point

**Purpose:** Initializes and launches the VocalCraft application.

**Key Functions:**

| Function                | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `setup_appearance()`    | Configures CustomTkinter theme (dark mode, blue theme) |
| `initialize_database()` | Creates/connects to SQLite database                    |
| `main()`                | Application entry point, shows LoginWindow first       |

**Flow:**

1. Fix Windows console encoding for Unicode
2. Set up appearance (dark mode)
3. Initialize database
4. Show LoginWindow
5. On successful login → Show MainWindow with user context

**Code Snippet:**

```python
def main():
    setup_appearance()
    db = initialize_database()

    def on_login_success(user_id: int, username: str):
        app = VocalCraftMainWindow(user_id=user_id, username=username)
        app.mainloop()

    login = LoginWindow(on_login_success=on_login_success)
    login.mainloop()
```

---

#### `audio_processor.py` - Audio Recording Module

**Purpose:** Handles all microphone recording functionality.

**Class:** `AudioRecorder`

**Configuration Constants:**
| Constant | Value | Description |
|----------|-------|-------------|
| `SAMPLE_RATE` | 44100 Hz | CD-quality audio |
| `CHANNELS` | 1 | Mono recording |
| `FORMAT` | paInt16 | 16-bit audio |
| `CHUNK_SIZE` | 1024 | Buffer size |

**Key Methods:**

| Method                     | Parameters | Returns | Description                             |
| -------------------------- | ---------- | ------- | --------------------------------------- |
| `start_recording()`        | None       | `bool`  | Starts recording in background thread   |
| `stop_recording()`         | None       | `bytes` | Stops recording, returns raw audio data |
| `save_recording(filename)` | `str`      | `str`   | Saves to WAV file, returns path         |
| `save_recording(username)` | `str`      | `str`   | Saves to user's dated folder            |
| `get_audio_frames()`       | None       | `list`  | Returns recorded audio frames           |
| `is_recording`             | Property   | `bool`  | Check if currently recording            |

**Error Handling:**

- Detects missing microphones with descriptive error messages
- Handles `OSError` for device unavailability
- Thread-safe recording with mutex locks

**Recording Flow:**

```
start_recording() → Opens PyAudio stream → Starts recording thread
     ↓
Recording loop runs in background (non-blocking)
     ↓
stop_recording() → Stops thread → Closes stream → Returns audio data
     ↓
save_recording() → Writes WAV file to data/recordings/{user}/{date}/
```

---

#### `speech_analyzer.py` - Speech Recognition & Scoring

**Purpose:** Analyzes recorded audio for transcription and scoring.

**Class:** `SpeechAnalyzer`

**Key Methods:**

| Method                               | Parameters | Returns           | Description                       |
| ------------------------------------ | ---------- | ----------------- | --------------------------------- |
| `get_visual_data(file_path)`         | `str`      | `Dict`            | Extracts waveform & spectrogram   |
| `transcribe_audio(file_path)`        | `str`      | `Tuple[str, str]` | Speech-to-text using Google API   |
| `calculate_similarity(text1, text2)` | `str, str` | `float`           | Levenshtein similarity (0-100)    |
| `analyze_intensity(file_path)`       | `str`      | `float`           | RMS energy analysis               |
| `score_attempt(file_path, target)`   | `str, str` | `Dict`            | Complete scoring with method used |

**Scoring Algorithm:**

1. **Primary Method: Transcription**

   - Uses Google Speech Recognition API
   - Normalizes text (lowercase, remove punctuation)
   - Calculates Levenshtein similarity ratio
   - Score = similarity × 100

2. **Fallback Method: Intensity**
   - If transcription fails (no internet, unclear speech)
   - Analyzes RMS energy of audio
   - Maps intensity to 0-100 scale
   - Lower accuracy but always works

**Visual Data Output:**

```python
{
    'waveform': np.ndarray,      # 1D audio samples
    'spectrogram': np.ndarray,   # 2D mel-spectrogram in dB
    'times': np.ndarray,         # Time axis
    'sample_rate': int           # Usually 22050 Hz
}
```

**Scoring Output:**

```python
{
    'score': float,              # 0-100 percentage
    'transcribed': str,          # What was heard
    'target': str,               # What should have been said
    'method': str                # 'transcription' or 'intensity'
}
```

---

#### `database.py` - Database Operations

**Purpose:** Manages all SQLite database operations including authentication and progress tracking.

**Class:** `DatabaseManager`

**Initialization:**

- Creates `data/` directory if not exists
- Initializes tables on first run
- Uses context manager for connection handling

**Authentication Methods:**

| Method                                              | Parameters | Returns                | Description              |
| --------------------------------------------------- | ---------- | ---------------------- | ------------------------ |
| `register_user(username, password, age, condition)` | Various    | `Tuple[bool, str]`     | Creates new user account |
| `login_user(username, password)`                    | `str, str` | `Tuple[int/None, str]` | Validates credentials    |
| `update_password(user_id, new_password)`            | `int, str` | `Tuple[bool, str]`     | Changes password         |
| `get_user(user_id)`                                 | `int`      | `Dict/None`            | Gets user details        |
| `get_user_by_username(username)`                    | `str`      | `Dict/None`            | Finds user by name       |

**Password Security:**

- SHA-256 hashing using `hashlib`
- Passwords never stored in plain text
- Minimum length validation (4 characters)

**Progress Tracking Methods:**

| Method                                                    | Parameters | Returns      | Description            |
| --------------------------------------------------------- | ---------- | ------------ | ---------------------- |
| `save_session(user_id, score, audio_path, exercise_type)` | Various    | `int`        | Saves practice session |
| `get_user_progress(user_id, limit)`                       | `int, int` | `List[Dict]` | Gets session history   |
| `get_user_stats(user_id)`                                 | `int`      | `Dict`       | Basic statistics       |
| `get_all_attempts(user_id, limit)`                        | `int, int` | `List[Dict]` | Full attempt details   |

**Advanced Statistics Methods:**

| Method                                       | Parameters | Returns          | Description                  |
| -------------------------------------------- | ---------- | ---------------- | ---------------------------- |
| `get_category_breakdown(user_id)`            | `int`      | `Dict[str, int]` | Sessions per exercise type   |
| `get_total_practice_time(user_id)`           | `int`      | `int`            | Estimated seconds practiced  |
| `get_average_score_over_time(user_id, days)` | `int, int` | `List[Tuple]`    | Daily averages               |
| `get_overall_stats(user_id)`                 | `int`      | `Dict`           | Comprehensive dashboard data |

**Singleton Pattern:**

```python
_db_manager: Optional[DatabaseManager] = None

def get_database(db_path: str = "data/vocalcraft.db") -> DatabaseManager:
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
    return _db_manager
```

---

#### `exercises.py` - Exercise Management

**Purpose:** Loads and manages speech therapy exercises from JSON files.

**Class:** `ExerciseManager`

**Loading Priority:**

1. `assets/exercises.json` (primary)
2. `assets/default_exercises.json` (fallback)
3. Hardcoded minimal exercises (emergency fallback)

**Key Methods:**

| Method                          | Parameters | Returns      | Description                 |
| ------------------------------- | ---------- | ------------ | --------------------------- |
| `get_categories()`              | None       | `List[Dict]` | All exercise categories     |
| `get_category_names()`          | None       | `List[str]`  | Just category names         |
| `get_exercises_by_category(id)` | `str`      | `List[Dict]` | Exercises in category       |
| `get_exercise_by_id(id)`        | `str`      | `Dict/None`  | Find specific exercise      |
| `get_current_exercise()`        | None       | `Dict/None`  | Currently selected exercise |
| `get_next_exercise()`           | None       | `Dict/None`  | Navigate forward            |
| `get_previous_exercise()`       | None       | `Dict/None`  | Navigate backward           |
| `set_category(category_id)`     | `str`      | None         | Change current category     |

**Navigation State:**

```python
current_category_id: str    # Currently selected category
current_exercise_index: int # Index within category
_current_exercises: List    # Cached exercises for current category
```

**Singleton Pattern:**

```python
def get_exercise_manager() -> ExerciseManager:
    global _exercise_manager
    if _exercise_manager is None:
        _exercise_manager = ExerciseManager()
    return _exercise_manager
```

---

### 6.2 UI Module Files

---

#### `ui/__init__.py` - Package Initializer

**Purpose:** Makes `ui/` a Python package.

**Contents:** Empty file (required for Python imports)

---

#### `ui/login_window.py` - Login/Signup Window

**Purpose:** Handles user authentication interface.

**Class:** `LoginWindow(ctk.CTk)`

**Window Properties:**

- Size: 500×720 pixels
- Fixed size (not resizable)
- Centered on screen
- Dark mode theme

**Components:**

| Component      | Type       | Purpose                 |
| -------------- | ---------- | ----------------------- |
| Logo           | CTkLabel   | "VocalCraft" title      |
| TabView        | CTkTabview | Sign In / Sign Up tabs  |
| Username Entry | CTkEntry   | Username input          |
| Password Entry | CTkEntry   | Password input (masked) |
| Age Entry      | CTkEntry   | Age input (signup only) |
| Sign In Button | CTkButton  | Submit login            |
| Sign Up Button | CTkButton  | Submit registration     |
| Message Label  | CTkLabel   | Error/success messages  |

**Callback Pattern:**

```python
def __init__(self, on_login_success: Callable[[int, str], None]):
    self.on_login_success = on_login_success
    # When login succeeds:
    # self.on_login_success(user_id, username)
```

**Validation:**

- Username: minimum 3 characters
- Password: minimum 4 characters
- Duplicate username check on registration

---

#### `ui/main_window.py` - Main Application Window

**Purpose:** Primary application interface with sidebar navigation and dynamic views.

**Size:** 1300×850 pixels (minimum 1000×700)

**Classes:**

##### `BaseView(ctk.CTkFrame)` - Abstract Base

All views inherit from this class.

| Method      | Description                                  |
| ----------- | -------------------------------------------- |
| `on_show()` | Called when view becomes visible (load data) |
| `on_hide()` | Called when view is hidden (cleanup)         |

##### `PracticeView(BaseView)` - Main Practice Interface

**Layout:**

```
┌────────────────────────────────────────────────────┐
│  Exercise: "Say 'Hello World'"                      │
│  [Category Dropdown]                                │
├─────────────────────┬──────────────────────────────┤
│   Waveform Chart    │                              │
│   Spectrogram Chart │   [Record Button]            │
│                     │   [Rocket Feedback Widget]   │
├─────────────────────┴──────────────────────────────┤
│  Score: 85%   "You said: Hello World"              │
│  Status: Great job! Click 'Next >' to continue     │
├────────────────────────────────────────────────────┤
│  [< Previous]              [Next >]                 │
└────────────────────────────────────────────────────┘
```

**State Variables:**
| Variable | Type | Purpose |
|----------|------|---------|
| `is_recording` | bool | Currently recording? |
| `is_processing` | bool | Analyzing audio? |
| `has_completed_exercise` | bool | Exercise done? |
| `microphone_available` | bool | Mic detected? |
| `current_audio_file` | str | Path to recording |

**Recording Flow:**

1. Click "Record" → Button shows "Recording..." (disabled)
2. Click "Stop" → Button shows "Analyzing..." (disabled)
3. Analysis complete → Button shows "Record Again" (enabled)
4. Score persists until next action
5. Must complete exercise before "Next" works

##### `StatsView(BaseView)` - Statistics Dashboard

**Layout:**

```
┌────────────────────────────────────────────────────┐
│  📊 Statistics Dashboard                           │
├────────────┬────────────┬─────────────────────────┤
│ Total Time │ Avg Score  │ Total Exercises         │
│   45 min   │    72%     │      156                │
├────────────┴────────────┴─────────────────────────┤
│ ┌─────────────────┐  ┌───────────────────────────┐│
│ │ Practice by     │  │ Improvement Over Time     ││
│ │ Category        │  │                           ││
│ │ [Bar Chart]     │  │ [Line Chart with Trend]   ││
│ └─────────────────┘  └───────────────────────────┘│
└────────────────────────────────────────────────────┘
```

**Charts:**

- Category Breakdown: Horizontal bar chart (matplotlib)
- Progress Over Time: Line chart with polynomial trend line

##### `HistoryView(BaseView)` - Session History

**Layout:**

```
┌────────────────────────────────────────────────────┐
│  📜 Session History                    156 sessions│
├─────────────┬───────────┬──────────────┬──────────┤
│ Date & Time │ Category  │ Exercise     │ Score    │
├─────────────┼───────────┼──────────────┼──────────┤
│ Dec 28, 2025│ Breathing │ Take a deep..│ [85%]    │ ← Green
│ 10:30 AM    │           │              │          │
├─────────────┼───────────┼──────────────┼──────────┤
│ Dec 28, 2025│ Vowels    │ A-E-I-O-U    │ [62%]    │ ← Orange
│ 10:25 AM    │           │              │          │
└─────────────┴───────────┴──────────────┴──────────┘
```

**Score Color Coding:**

- ≥80%: Green (#27ae60)
- 50-79%: Orange (#f39c12)
- <50%: Red (#e74c3c)

##### `ProfileView(BaseView)` - Profile & Settings

**Sections:**

1. **Account Information** (read-only)

   - Username
   - Condition (Dysarthria)
   - Member Since date

2. **Change Password**

   - New Password field
   - Confirm Password field
   - Update button
   - Validation messages

3. **Quick Stats**
   - Total Sessions
   - Best Score
   - Current Streak

##### `VocalCraftMainWindow(ctk.CTk)` - Main Container

**Sidebar Navigation:**
| Button | Icon | View |
|--------|------|------|
| Home / Practice | 🏠 | PracticeView |
| Dashboard | 📊 | StatsView |
| History | 📜 | HistoryView |
| Profile | 👤 | ProfileView |
| Logout | - | Returns to LoginWindow |

**Appearance Options:**

- Dark (default)
- Light
- System

---

#### `ui/charts.py` - Audio Visualization

**Purpose:** Matplotlib-based audio visualization components.

**Class:** `AudioVisualizer`

**Features:**

- Dual-panel display (waveform + spectrogram)
- Dark theme styling
- Embedded in CTkFrame using FigureCanvasTkAgg

**Methods:**
| Method | Parameters | Description |
|--------|------------|-------------|
| `update_plot(waveform, sr)` | `ndarray, int` | Update waveform display |
| `update_spectrogram(spec, sr)` | `ndarray, int` | Update spectrogram |
| `update_full(waveform, spec, sr)` | Various | Update both at once |
| `clear()` | None | Reset to placeholder |

**Class:** `ProgressChart`

**Features:**

- Line chart with scatter points
- Trend line (linear regression)
- Green color scheme with fill

---

#### `ui/rocket_feedback.py` - Gamification Widget

**Purpose:** Animated rocket fuel tank showing score feedback.

**Class:** `RocketFeedback(ctk.CTkFrame)`

**Visual Elements:**

```
┌─────────────────┐
│     Power       │
├─────────────────┤
│                 │
│      🚀        │ ← Moves up with score
│   ┌───────┐     │
│   │███████│     │ ← Fuel level (progress bar)
│   │███████│     │
│   │       │     │
│   └───────┘     │
│                 │
│     85%         │
└─────────────────┘
```

**Color Thresholds:**
| Score Range | Color | Name |
|-------------|-------|------|
| 0-40% | #e74c3c | Red |
| 40-70% | #f39c12 | Yellow |
| 70-90% | #27ae60 | Green |
| >90% | #9b59b6 | Purple (Blast Off!) |

**Animation:**

- Score >90% triggers "Blast Off!" animation
- Rocket shakes and changes color
- Celebration message appears

**Methods:**
| Method | Parameters | Description |
|--------|------------|-------------|
| `update_fuel(score)` | `float` | Set fuel level (0-100) |
| `reset()` | None | Reset to empty state |
| `_animate_blast_off()` | None | Trigger celebration |

---

### 6.3 Asset Files

---

#### `assets/exercises.json` - Exercise Definitions

**Purpose:** Contains all speech therapy exercises organized by category.

**Structure:**

```json
{
  "categories": [
    {
      "id": "breathing",
      "name": "Breathing Exercises",
      "description": "...",
      "icon": "🌬️",
      "exercises": [
        {
          "id": "breath_001",
          "text": "Take a deep breath...",
          "difficulty": 1,
          "targetDuration": 10,
          "instructions": "Focus on slow breathing..."
        }
      ]
    }
  ]
}
```

**Categories Included:**
| ID | Name | Count | Difficulty Range |
|----|------|-------|-----------------|
| `breathing` | Breathing Exercises | 5 | 1-3 |
| `vowels` | Vowel Sounds | 6 | 1-3 |
| `short_sentences` | Short Sentences | 8 | 1-2 |
| `tongue_twisters` | Tongue Twisters | 6 | 2-4 |
| `functional_phrases` | Functional Phrases | 8 | 1-3 |
| `reading_passages` | Reading Passages | 4 | 3-4 |

**Exercise Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `text` | string | What patient should say |
| `difficulty` | int | 1 (easy) to 4 (hard) |
| `targetDuration` | int | Expected duration in seconds |
| `instructions` | string | Tips for the exercise |

---

#### `assets/default_exercises.json` - Fallback Exercises

**Purpose:** Backup exercises if main file is missing/corrupted.

Same structure as `exercises.json` but with minimal exercise set.

---

### 6.4 Data Files

---

#### `data/vocalcraft.db` - SQLite Database

**Purpose:** Stores all user data and progress.

See [Section 7: Database Schema](#7-database-schema) for details.

---

#### `data/schema.sql` - Database Schema

**Purpose:** SQL script to create database structure.

**Contents:**

- DROP TABLE statements (for clean reset)
- CREATE TABLE for `users`
- CREATE TABLE for `progress`
- CREATE INDEX for performance
- CREATE VIEW for statistics

---

#### `data/queries.sql` - SQL Query Reference

**Purpose:** Reference of all SQL queries used in the application.

**Sections:**

- User Management (INSERT, SELECT, UPDATE, DELETE)
- Progress/Session Queries
- Statistics Queries
- Data Cleanup Queries
- Maintenance Queries
- Reporting Queries

---

#### `data/reset_database.sql` - Database Reset

**Purpose:** Complete database reset script.

**Warning:** Deletes ALL data!

**Usage:**

```bash
sqlite3 data/vocalcraft.db < data/reset_database.sql
```

---

#### `data/clear_data.sql` - Data Clearing Options

**Purpose:** Various data deletion options.

**Options:**

1. Clear all data (keep tables)
2. Clear progress only (keep users)
3. Clear specific user data
4. Clear old data (30/90/365 days)
5. Clear by criteria (low scores, exercise type)

---

#### `data/recordings/` - Audio Storage

**Purpose:** Stores recorded audio files.

**Structure:**

```
recordings/
└── {username}/
    └── {YYYY-MM-DD}/
        ├── recording_001.wav
        ├── recording_002.wav
        └── ...
```

**File Format:** WAV (44.1kHz, 16-bit, Mono)

---

### 6.5 Configuration Files

---

#### `requirements.txt` - Python Dependencies

**Purpose:** Lists all required Python packages.

**Dependencies:**
| Package | Version | Purpose |
|---------|---------|---------|
| customtkinter | ≥5.2.0 | Modern GUI framework |
| pyaudio | ≥0.2.13 | Audio recording |
| librosa | ≥0.10.0 | Audio analysis |
| numpy | ≥1.24.0 | Numerical computing |
| SpeechRecognition | ≥3.10.0 | Speech-to-text |
| textdistance | ≥4.5.0 | Text similarity |
| matplotlib | ≥3.7.0 | Charts and visualization |

**Installation:**

```bash
pip install -r requirements.txt
```

---

## 7. Database Schema

### 7.1 Entity Relationship Diagram

```
┌─────────────────┐          ┌─────────────────────┐
│     USERS       │          │      PROGRESS       │
├─────────────────┤          ├─────────────────────┤
│ id (PK)         │──────────│ id (PK)             │
│ username        │     1:N  │ user_id (FK)        │
│ password_hash   │          │ date                │
│ age             │          │ exercise_type       │
│ condition       │          │ score               │
│ join_date       │          │ audio_path          │
└─────────────────┘          └─────────────────────┘
```

### 7.2 Table: users

| Column        | Type      | Constraints               | Description             |
| ------------- | --------- | ------------------------- | ----------------------- |
| id            | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique user ID          |
| username      | TEXT      | UNIQUE NOT NULL           | Login username          |
| password_hash | TEXT      | NOT NULL                  | SHA-256 hashed password |
| age           | INTEGER   | NULL                      | User's age              |
| condition     | TEXT      | DEFAULT 'Dysarthria'      | Speech condition        |
| join_date     | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration date       |

### 7.3 Table: progress

| Column        | Type      | Constraints               | Description          |
| ------------- | --------- | ------------------------- | -------------------- |
| id            | INTEGER   | PRIMARY KEY AUTOINCREMENT | Session ID           |
| user_id       | INTEGER   | FOREIGN KEY → users(id)   | Owner of session     |
| date          | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When recorded        |
| exercise_type | TEXT      | NULL                      | Category/exercise ID |
| score         | REAL      | NULL                      | Score (0-100)        |
| audio_path    | TEXT      | NULL                      | Path to WAV file     |

### 7.4 Indexes

| Index                 | Table    | Column(s)     | Purpose             |
| --------------------- | -------- | ------------- | ------------------- |
| idx_users_username    | users    | username      | Fast login lookup   |
| idx_progress_user     | progress | user_id       | Fast user queries   |
| idx_progress_date     | progress | date          | Date range queries  |
| idx_progress_exercise | progress | exercise_type | Category filtering  |
| idx_progress_score    | progress | score         | Score-based queries |

### 7.5 Foreign Key Behavior

```sql
FOREIGN KEY (user_id) REFERENCES users (id)
    ON DELETE CASCADE
```

When a user is deleted, all their progress records are automatically deleted.

---

## 8. User Interface Guide

### 8.1 Login Screen

**First Launch:**

1. Click "Sign Up" tab
2. Enter username (min 3 characters)
3. Enter password (min 4 characters)
4. Enter age (optional)
5. Click "Sign Up"
6. Account created → Automatically logged in

**Returning User:**

1. Enter username
2. Enter password
3. Click "Sign In"

### 8.2 Main Practice Screen

**Selecting an Exercise:**

1. Use category dropdown to choose exercise type
2. Current exercise displays at top
3. Use < Previous and Next > to navigate

**Recording:**

1. Click "Record" button
2. Speak the displayed sentence
3. Click "Stop" when finished
4. Wait for analysis
5. View score and feedback
6. Click "Next >" to continue (only available after recording)

**Understanding Feedback:**

- **Waveform:** Shows volume over time
- **Spectrogram:** Shows frequency content
- **Rocket Widget:** Visual score representation
- **Score:** Percentage match to target
- **"You said:"** What was transcribed

### 8.3 Statistics Dashboard

**Summary Cards:**

- Total Practice Time (estimated)
- Average Score (all sessions)
- Total Exercises (session count)

**Category Chart:**

- Shows which exercise types you practice most
- Horizontal bar chart
- Helps identify areas to focus on

**Progress Chart:**

- Daily average scores over last 30 days
- Dotted trend line shows improvement
- Upward trend = getting better!

### 8.4 History View

**Viewing History:**

- Most recent sessions at top
- Shows date, time, category, exercise, score
- Color-coded scores for quick assessment

**Score Colors:**

- 🟢 Green (≥80%): Excellent
- 🟠 Orange (50-79%): Good progress
- 🔴 Red (<50%): Needs practice

### 8.5 Profile & Settings

**Viewing Account:**

- Username (cannot be changed)
- Condition (Dysarthria)
- Member since date
- Quick statistics

**Changing Password:**

1. Enter new password
2. Confirm new password
3. Click "Update Password"
4. See success message

### 8.6 Appearance

**Changing Theme:**

1. Find "Appearance" dropdown in sidebar
2. Select: Dark, Light, or System
3. Theme changes immediately

---

## 9. How It Works

### 9.1 Recording Flow

```
[User clicks Record]
         ↓
    AudioRecorder.start_recording()
         ↓
    ┌─────────────────────────────┐
    │ Background Thread Running   │
    │ - Opens PyAudio stream      │
    │ - Reads audio chunks        │
    │ - Stores in memory          │
    └─────────────────────────────┘
         ↓
[User clicks Stop]
         ↓
    AudioRecorder.stop_recording()
         ↓
    AudioRecorder.save_recording(username)
         ↓
    File saved to: data/recordings/{user}/{date}/recording_{n}.wav
```

### 9.2 Scoring Flow

```
[Recording saved to file]
         ↓
    SpeechAnalyzer.get_visual_data(file)
    → Returns waveform + spectrogram
         ↓
    SpeechAnalyzer.score_attempt(file, target_text)
         ↓
    ┌─────────────────────────────────┐
    │  Try Google Speech Recognition  │
    │  transcribe_audio(file)         │
    └─────────────────┬───────────────┘
                      ↓
         ┌────────────┴────────────┐
         │                         │
    [Success]                 [Failed]
         ↓                         ↓
    calculate_similarity()    analyze_intensity()
    (Levenshtein ratio)      (RMS energy mapping)
         ↓                         ↓
    └────────────┬─────────────────┘
                 ↓
    Return: {score, transcribed, target, method}
```

### 9.3 Scoring Algorithm Details

**Levenshtein Similarity:**

```python
# Normalize both texts
text1 = text1.lower().strip()
text2 = text2.lower().strip()

# Remove punctuation
text1 = text1.translate(str.maketrans('', '', string.punctuation))
text2 = text2.translate(str.maketrans('', '', string.punctuation))

# Calculate similarity ratio (0.0 to 1.0)
ratio = textdistance.levenshtein.normalized_similarity(text1, text2)

# Convert to percentage
score = ratio * 100
```

**Example:**

- Target: "Hello World"
- Spoken: "Hello Word"
- Similarity: ~91%

### 9.4 Data Persistence

**Saving a Session:**

```python
database.save_session(
    user_id=1,
    score=85.5,
    exercise_type="breathing",
    audio_path="data/recordings/john/2025-01-01/recording_001.wav"
)
```

**Session Data Stored:**

- When recorded (timestamp)
- What exercise was practiced
- What score was achieved
- Where audio file is saved

---

## 10. Configuration

### 10.1 Audio Settings

In `audio_processor.py`:

```python
SAMPLE_RATE = 44100   # Change for different quality
CHANNELS = 1          # 1=mono, 2=stereo
FORMAT = paInt16      # Bit depth
CHUNK_SIZE = 1024     # Buffer size
```

### 10.2 Speech Recognition

In `speech_analyzer.py`:

```python
self._recognizer.energy_threshold = 300
self._recognizer.dynamic_energy_threshold = True
```

Adjust `energy_threshold` for noisy environments.

### 10.3 Appearance

In `main.py`:

```python
ctk.set_appearance_mode("dark")   # "dark", "light", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

### 10.4 Database Path

In `main.py`:

```python
db = get_database("data/vocalcraft.db")  # Change path here
```

### 10.5 Exercises

Edit `assets/exercises.json` to add/modify exercises:

```json
{
  "id": "custom_001",
  "text": "Your custom sentence here",
  "difficulty": 2,
  "targetDuration": 10,
  "instructions": "Tips for practicing"
}
```

---

## 11. Troubleshooting

### 11.1 No Microphone Detected

**Symptoms:**

- Error message: "No input audio devices found"
- Record button doesn't work

**Solutions:**

1. Check microphone is connected
2. Check Windows/OS audio settings
3. Grant microphone permissions to Python
4. Try a different USB port
5. Update audio drivers

### 11.2 Speech Recognition Fails

**Symptoms:**

- "Could not transcribe" message
- Scores based on intensity only

**Solutions:**

1. Check internet connection (Google API requires internet)
2. Speak more clearly and loudly
3. Reduce background noise
4. Try a higher quality microphone

### 11.3 Low Scores Despite Good Speech

**Solutions:**

1. Speak at normal pace (not too fast)
2. Pronounce words clearly
3. Match the exact text shown
4. Check for background noise
5. Position microphone closer

### 11.4 Application Won't Start

**Solutions:**

1. Check Python version (≥3.8)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check for error messages in terminal
4. Delete `data/vocalcraft.db` and restart

### 11.5 Database Errors

**Reset Database:**

```bash
python -c "import sqlite3; c=sqlite3.connect('data/vocalcraft.db'); c.execute('DELETE FROM progress'); c.execute('DELETE FROM users'); c.commit()"
```

Or delete `data/vocalcraft.db` and restart application.

---

## 12. API Reference

### 12.1 AudioRecorder

```python
from audio_processor import AudioRecorder

recorder = AudioRecorder()

# Start recording
success = recorder.start_recording()

# Check status
if recorder.is_recording:
    print("Recording...")

# Stop and save
recorder.stop_recording()
file_path = recorder.save_recording(username="john")
```

### 12.2 SpeechAnalyzer

```python
from speech_analyzer import SpeechAnalyzer

analyzer = SpeechAnalyzer()

# Get visualization data
visual = analyzer.get_visual_data("recording.wav")
waveform = visual['waveform']
spectrogram = visual['spectrogram']

# Score an attempt
result = analyzer.score_attempt("recording.wav", "Hello World")
print(f"Score: {result['score']}%")
print(f"You said: {result['transcribed']}")
```

### 12.3 DatabaseManager

```python
from database import get_database

db = get_database()

# Register user
success, message = db.register_user("john", "password123", age=25)

# Login
user_id, message = db.login_user("john", "password123")

# Save session
session_id = db.save_session(user_id, score=85.5, exercise_type="breathing")

# Get stats
stats = db.get_overall_stats(user_id)
print(f"Total sessions: {stats['total_sessions']}")
print(f"Average score: {stats['average_score']}%")
```

### 12.4 ExerciseManager

```python
from exercises import get_exercise_manager

manager = get_exercise_manager()

# Get categories
categories = manager.get_category_names()

# Set category
manager.set_category("breathing")

# Navigate
exercise = manager.get_current_exercise()
print(f"Say: {exercise['text']}")

next_exercise = manager.get_next_exercise()
```

---

## 13. Customization

### 13.1 Adding New Exercise Categories

1. Open `assets/exercises.json`
2. Add new category object:

```json
{
  "id": "my_category",
  "name": "My Custom Exercises",
  "description": "Description here",
  "icon": "🎯",
  "exercises": [
    {
      "id": "my_001",
      "text": "Practice sentence",
      "difficulty": 1,
      "targetDuration": 10,
      "instructions": "Tips here"
    }
  ]
}
```

### 13.2 Changing Colors

Edit in respective UI files:

```python
# Rocket widget colors
COLOR_LOW = "#e74c3c"     # Red
COLOR_MEDIUM = "#f39c12"  # Yellow
COLOR_HIGH = "#27ae60"    # Green

# Score badge colors (History view)
if score >= 80:
    color = "#27ae60"  # Green
elif score >= 50:
    color = "#f39c12"  # Orange
else:
    color = "#e74c3c"  # Red
```

### 13.3 Modifying Scoring Thresholds

In `ui/main_window.py`:

```python
# Change pass threshold
if score >= 70:  # Change this value
    self.status_label.configure(text="Great job!")
```

In `ui/rocket_feedback.py`:

```python
THRESHOLD_MEDIUM = 40    # Yellow starts here
THRESHOLD_HIGH = 70      # Green starts here
THRESHOLD_BLAST_OFF = 90 # Animation triggers here
```

### 13.4 Adding New Views

1. Create new class inheriting from `BaseView`:

```python
class MyCustomView(BaseView):
    def __init__(self, master, main_window, **kwargs):
        super().__init__(master, main_window, **kwargs)
        self._create_widgets()

    def _create_widgets(self):
        # Add your widgets here
        pass

    def on_show(self):
        # Load data when view opens
        pass
```

2. Add navigation in `VocalCraftMainWindow._create_sidebar()`:

```python
nav_items = [
    ("practice", "🏠 Home / Practice", self._show_practice_view),
    ("myview", "🔧 My View", self._show_my_view),  # Add this
]
```

3. Add show method:

```python
def _show_my_view(self):
    self._clear_content_area()
    self._update_nav_selection("myview")
    self.current_view = MyCustomView(self.content_area, self)
    self.current_view.grid(row=0, column=0, sticky="nsew")
    self.current_view.on_show()
```

---

## Appendix A: File Size Reference

| File                  | Lines  | Size  |
| --------------------- | ------ | ----- |
| main.py               | ~173   | 5 KB  |
| audio_processor.py    | ~356   | 12 KB |
| speech_analyzer.py    | ~345   | 11 KB |
| database.py           | ~800   | 28 KB |
| exercises.py          | ~371   | 11 KB |
| ui/main_window.py     | ~1,790 | 65 KB |
| ui/login_window.py    | ~307   | 10 KB |
| ui/charts.py          | ~302   | 9 KB  |
| ui/rocket_feedback.py | ~278   | 8 KB  |
| exercises.json        | ~259   | 10 KB |

---

## Appendix B: Version History

| Version | Date     | Changes         |
| ------- | -------- | --------------- |
| 1.0.0   | Jan 2026 | Initial release |

---

## Appendix C: License

VocalCraft is developed for speech therapy purposes.

---

**End of Manual**

_Last Updated: January 1, 2026_
