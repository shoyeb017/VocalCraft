# VocalCraft - Speech Therapy Tool

A modern desktop application for speech therapy using Python and CustomTkinter. Designed to help patients with speech conditions practice and improve their communication skills through guided exercises and real-time feedback.

## Features

- **Guided Exercises**: 29 exercises across 5 categories (Breathing, Vowels, Sentences, Consonants, Functional)
- **Real-time Recording**: Record speech with visual feedback
- **Audio Visualization**: Waveform and Mel-Spectrogram display
- **Speech Scoring**: Automatic transcription and similarity scoring using Levenshtein distance
- **Fallback Scoring**: Intensity-based scoring for patients with severe dysarthria
- **Progress Tracking**: SQLite database to track patient attempts and progress
- **Gamification**: Power meter, score display, and auto-progression

## Installation

### Prerequisites

- Python 3.8 or higher
- Microphone for audio recording

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

## Project Structure

```
VocalCraft/
├── main.py                 # Application entry point
├── audio_processor.py      # Audio recording (PyAudio)
├── speech_analyzer.py      # Speech analysis (librosa, SpeechRecognition)
├── exercises.py            # Exercise manager
├── database.py             # SQLite database handler
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── assets/
│   └── exercises.json      # Exercise data (29 exercises)
│
├── data/
│   └── vocalcraft.db       # SQLite database (created on first run)
│
└── ui/
    ├── __init__.py         # Package init
    ├── charts.py           # Audio visualization (matplotlib)
    └── main_window.py      # Main GUI (CustomTkinter)
```

## Usage

1. **Start the app**: Run `python main.py`
2. **Select a category**: Use the sidebar dropdown to choose exercise type
3. **Read the target sentence**: Displayed at the top of the screen
4. **Click Record**: Speak the sentence clearly into your microphone
5. **Click Stop**: The app will analyze your speech
6. **View results**: See your score and the transcribed text
7. **Progress**: Score above 70% auto-advances to the next exercise

## Exercise Categories

| Category        | Description                   | Exercises |
| --------------- | ----------------------------- | --------- |
| Breathing       | Breath control exercises      | 5         |
| Vowels          | Vowel pronunciation           | 6         |
| Short Sentences | Sentences and tongue twisters | 8         |
| Consonants      | Consonant drills              | 5         |
| Functional      | Everyday phrases              | 5         |

## Scoring

- **Transcription-based** (default): Uses Google Speech API to transcribe, then calculates Levenshtein similarity
- **Intensity-based** (fallback): If transcription fails, scores based on voice volume, activity, and quality

### Score Feedback

| Score  | Power Meter | Message           |
| ------ | ----------- | ----------------- |
| 80%+   | Green       | Rocket Launched!  |
| 50-79% | Orange      | Building Power... |
| <50%   | Red         | Try Again!        |

## Dependencies

- `customtkinter` - Modern GUI framework
- `pyaudio` - Audio recording
- `librosa` - Audio analysis
- `SpeechRecognition` - Speech-to-text
- `textdistance` - Text similarity
- `matplotlib` - Visualization
- `numpy` - Numerical operations

## Database

Patient data and attempts are stored in `data/vocalcraft.db`:

- **patients**: id, name, age, condition, notes
- **attempts**: id, patient_id, exercise_text, audio_path, score, timestamp

## License

This project is for educational purposes.

## Authors

VocalCraft Team - 2025
