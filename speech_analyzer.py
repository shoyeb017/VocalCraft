"""
Speech Analyzer Module for VocalCraft
Handles speech recognition, audio analysis, and scoring.
"""

import numpy as np
import librosa
import librosa.display
import speech_recognition as sr
import textdistance
from typing import Tuple, Optional, Dict
import string


class SpeechAnalyzer:
    """
    A class to analyze speech recordings.
    Provides visual data extraction and speech scoring functionality.
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize the SpeechAnalyzer.
        
        Args:
            sample_rate: Target sample rate for audio loading (default 22050 Hz).
        """
        self.sample_rate = sample_rate
        self._recognizer = sr.Recognizer()
        self._is_warmed_up = False
        
        # Recognizer settings for better accuracy
        self._recognizer.energy_threshold = 300
        self._recognizer.dynamic_energy_threshold = True

    def warm_up(self) -> None:
        """
        Pre-warm librosa and numpy to avoid first-run delay.
        
        Librosa uses Numba JIT compilation which causes significant delay
        on first use. This method runs a minimal computation to trigger
        the JIT compilation in the background.
        """
        if self._is_warmed_up:
            return
        
        try:
            # Create a small dummy audio signal (0.1 seconds of silence)
            dummy_signal = np.zeros(int(self.sample_rate * 0.1), dtype=np.float32)
            
            # Trigger librosa JIT compilation with minimal computation
            _ = librosa.feature.melspectrogram(
                y=dummy_signal, 
                sr=self.sample_rate, 
                n_mels=32,
                n_fft=512,
                hop_length=256
            )
            
            # Trigger RMS computation
            _ = librosa.feature.rms(y=dummy_signal)
            
            # Trigger zero crossing rate
            _ = librosa.feature.zero_crossing_rate(dummy_signal)
            
            self._is_warmed_up = True
            print("SpeechAnalyzer warmed up successfully")
            
        except Exception as e:
            print(f"Warm-up warning (non-critical): {e}")
            self._is_warmed_up = True  # Mark as done to avoid retries

    def get_visual_data(self, file_path: str) -> Dict[str, np.ndarray]:
        """
        Extract waveform and spectrogram data from an audio file.
        
        Args:
            file_path: Path to the audio file (WAV format).
            
        Returns:
            Dictionary containing:
                - 'waveform': 1D numpy array of audio samples
                - 'spectrogram': 2D numpy array (mel spectrogram in dB)
                - 'times': Time axis for waveform
                - 'sample_rate': Sample rate of loaded audio
        """
        try:
            # Load audio file
            y, sr_loaded = librosa.load(file_path, sr=self.sample_rate)
            
            # Generate time axis for waveform
            times = np.linspace(0, len(y) / sr_loaded, num=len(y))
            
            # Compute mel spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=y, 
                sr=sr_loaded, 
                n_mels=128,
                fmax=8000
            )
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            return {
                'waveform': y,
                'spectrogram': mel_spec_db,
                'times': times,
                'sample_rate': sr_loaded
            }
            
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return {
                'waveform': np.array([]),
                'spectrogram': np.array([[]]),
                'times': np.array([]),
                'sample_rate': self.sample_rate
            }

    def transcribe_audio(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Transcribe audio file to text using Google Speech Recognition.
        
        Args:
            file_path: Path to the audio file.
            
        Returns:
            Tuple of (transcribed_text, error_message).
            If successful, error_message is None.
            If failed, transcribed_text is None.
        """
        try:
            with sr.AudioFile(file_path) as source:
                # Adjust for ambient noise (shorter duration for speed)
                self._recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = self._recognizer.record(source)
            
            # Attempt transcription with Google (with timeout to prevent hanging)
            # Use a thread with timeout to prevent indefinite blocking
            import concurrent.futures
            
            def do_recognize():
                return self._recognizer.recognize_google(audio_data)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(do_recognize)
                try:
                    text = future.result(timeout=10)  # 10 second timeout
                    return text, None
                except concurrent.futures.TimeoutError:
                    return None, "Recognition timed out"
            
        except sr.UnknownValueError:
            return None, "Speech not recognized"
        except sr.RequestError as e:
            return None, f"API error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"

    def score_speech(self, file_path: str, target_text: str) -> Dict:
        """
        Score the speech by comparing transcription to target text.
        Falls back to intensity-based scoring if transcription fails.
        
        Args:
            file_path: Path to the audio file.
            target_text: The expected/target text.
            
        Returns:
            Dictionary containing:
                - 'score': Similarity score (0-100)
                - 'transcribed': Transcribed text (or None)
                - 'method': Scoring method used ('transcription' or 'intensity')
                - 'error': Error message if any
                - 'details': Additional scoring details
        """
        result = {
            'score': 0.0,
            'transcribed': None,
            'method': 'transcription',
            'error': None,
            'details': {}
        }
        
        # Attempt transcription
        transcribed, error = self.transcribe_audio(file_path)
        
        if transcribed:
            # Successful transcription - use Levenshtein distance
            result['transcribed'] = transcribed
            result['score'] = self._calculate_text_similarity(target_text, transcribed)
            result['details']['target_words'] = len(target_text.split())
            result['details']['transcribed_words'] = len(transcribed.split())
            
        else:
            # Transcription failed - fallback to intensity-based scoring
            result['method'] = 'intensity'
            result['error'] = error
            result['score'] = self._calculate_intensity_score(file_path)
            result['details']['fallback_reason'] = error
        
        return result

    def _calculate_text_similarity(self, target: str, transcribed: str) -> float:
        """
        Calculate similarity between target and transcribed text.
        Uses Levenshtein normalized similarity.
        
        Args:
            target: Target/expected text.
            transcribed: Transcribed text from speech.
            
        Returns:
            Similarity score from 0 to 100.
        """
        # Normalize texts
        target_clean = self._normalize_text(target)
        transcribed_clean = self._normalize_text(transcribed)
        
        # Calculate Levenshtein similarity (0 to 1)
        similarity = textdistance.levenshtein.normalized_similarity(
            target_clean,
            transcribed_clean
        )
        
        return similarity * 100

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison.
        Removes punctuation and converts to lowercase.
        
        Args:
            text: Input text.
            
        Returns:
            Normalized text.
        """
        # Convert to lowercase
        text = text.lower().strip()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Normalize whitespace
        text = ' '.join(text.split())
        return text

    def _calculate_intensity_score(self, file_path: str) -> float:
        """
        Calculate a score based on audio intensity/volume.
        Used as fallback when transcription fails (e.g., dysarthria).
        
        Args:
            file_path: Path to the audio file.
            
        Returns:
            Score from 0 to 100 based on audio characteristics.
        """
        try:
            # Load audio
            y, sr_loaded = librosa.load(file_path, sr=self.sample_rate)
            
            if len(y) == 0:
                return 0.0
            
            # Calculate RMS energy
            rms = librosa.feature.rms(y=y)[0]
            avg_rms = np.mean(rms)
            
            # Calculate zero crossing rate (voice activity indicator)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            avg_zcr = np.mean(zcr)
            
            # Calculate spectral centroid (voice quality indicator)
            spectral_cent = librosa.feature.spectral_centroid(y=y, sr=sr_loaded)[0]
            avg_centroid = np.mean(spectral_cent)
            
            # Scoring heuristics:
            # - RMS > 0.02 indicates sufficient volume
            # - ZCR between 0.02-0.15 typical for speech
            # - Spectral centroid 500-4000 Hz typical for speech
            
            score = 0.0
            
            # Volume score (0-40 points)
            if avg_rms > 0.01:
                volume_score = min(40, (avg_rms / 0.1) * 40)
                score += volume_score
            
            # Speech activity score (0-30 points)
            if 0.01 < avg_zcr < 0.2:
                zcr_score = 30 * (1 - abs(avg_zcr - 0.08) / 0.12)
                score += max(0, zcr_score)
            
            # Voice quality score (0-30 points)
            if 200 < avg_centroid < 6000:
                centroid_score = 30 * (1 - abs(avg_centroid - 2000) / 4000)
                score += max(0, centroid_score)
            
            return min(100, max(0, score))
            
        except Exception as e:
            print(f"Error calculating intensity score: {e}")
            return 0.0

    def get_audio_metrics(self, file_path: str) -> Dict:
        """
        Get detailed audio metrics for analysis.
        
        Args:
            file_path: Path to the audio file.
            
        Returns:
            Dictionary of audio metrics.
        """
        try:
            y, sr_loaded = librosa.load(file_path, sr=self.sample_rate)
            
            # Duration
            duration = librosa.get_duration(y=y, sr=sr_loaded)
            
            # RMS Energy
            rms = librosa.feature.rms(y=y)[0]
            
            # Pitch estimation
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr_loaded)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            avg_pitch = np.mean(pitch_values) if pitch_values else 0
            
            # Tempo estimation
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr_loaded)
            
            return {
                'duration': duration,
                'avg_volume': float(np.mean(rms)),
                'max_volume': float(np.max(rms)),
                'min_volume': float(np.min(rms)),
                'avg_pitch': float(avg_pitch),
                'tempo': float(tempo) if isinstance(tempo, (int, float)) else float(tempo[0]) if len(tempo) > 0 else 0.0,
                'sample_rate': sr_loaded
            }
            
        except Exception as e:
            print(f"Error getting audio metrics: {e}")
            return {
                'duration': 0,
                'avg_volume': 0,
                'max_volume': 0,
                'min_volume': 0,
                'avg_pitch': 0,
                'tempo': 0,
                'sample_rate': 0
            }


if __name__ == "__main__":
    # Test the SpeechAnalyzer
    import os
    
    analyzer = SpeechAnalyzer()
    
    test_file = "output.wav"
    target_text = "The quick brown fox jumps over the lazy dog."
    
    if os.path.exists(test_file):
        print("Testing SpeechAnalyzer...")
        
        # Test visual data extraction
        print("\n1. Getting visual data...")
        visual_data = analyzer.get_visual_data(test_file)
        print(f"   Waveform shape: {visual_data['waveform'].shape}")
        print(f"   Spectrogram shape: {visual_data['spectrogram'].shape}")
        
        # Test speech scoring
        print("\n2. Scoring speech...")
        score_result = analyzer.score_speech(test_file, target_text)
        print(f"   Score: {score_result['score']:.1f}%")
        print(f"   Method: {score_result['method']}")
        print(f"   Transcribed: {score_result['transcribed']}")
        
        # Test audio metrics
        print("\n3. Getting audio metrics...")
        metrics = analyzer.get_audio_metrics(test_file)
        print(f"   Duration: {metrics['duration']:.2f}s")
        print(f"   Avg Volume: {metrics['avg_volume']:.4f}")
        print(f"   Avg Pitch: {metrics['avg_pitch']:.1f} Hz")
    else:
        print(f"Test file '{test_file}' not found.")
        print("Record some audio first using the main application.")
