"""
Audio Processor Module for VocalCraft
Handles audio recording functionality using PyAudio.
"""

import pyaudio
import wave
import threading
import os
from datetime import datetime
from typing import Optional
import numpy as np


class AudioRecorder:
    """
    A class to handle audio recording from the microphone.
    Records in a separate thread to prevent UI freezing.
    """

    # Audio configuration constants
    SAMPLE_RATE = 44100  # 44.1 kHz standard sample rate
    CHANNELS = 1  # Mono audio
    FORMAT = pyaudio.paInt16  # 16-bit audio
    CHUNK_SIZE = 1024  # Buffer size

    def __init__(self):
        """Initialize the AudioRecorder with default settings."""
        self._pyaudio: Optional[pyaudio.PyAudio] = None
        self._stream: Optional[pyaudio.Stream] = None
        self._frames: list = []
        self._is_recording: bool = False
        self._record_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    @property
    def is_recording(self) -> bool:
        """Check if recording is currently in progress."""
        with self._lock:
            return self._is_recording

    def start_recording(self) -> bool:
        """
        Start recording audio from the microphone.
        
        Initializes PyAudio, opens an input stream, and starts the recording
        thread. Includes comprehensive error handling for microphone issues.
        
        Returns:
            bool: True if recording started successfully, False otherwise.
            
        Raises:
            OSError: If no microphone is detected or audio device is unavailable.
            Exception: For other unexpected audio initialization errors.
        """
        if self.is_recording:
            return False

        try:
            # Initialize PyAudio instance
            self._pyaudio = pyaudio.PyAudio()
            
            # Check if any input devices are available
            input_device_count = 0
            for i in range(self._pyaudio.get_device_count()):
                device_info = self._pyaudio.get_device_info_by_index(i)
                if device_info.get('maxInputChannels', 0) > 0:
                    input_device_count += 1
            
            if input_device_count == 0:
                # No input devices found - raise descriptive error
                self._cleanup()
                raise OSError("No input audio devices found. Please connect a microphone.")
            
            # Attempt to open audio stream with the default input device
            self._stream = self._pyaudio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.SAMPLE_RATE,
                input=True,
                frames_per_buffer=self.CHUNK_SIZE
            )
            
            # Clear previous frames
            self._frames = []
            
            # Set recording flag
            with self._lock:
                self._is_recording = True
            
            # Start recording thread (daemon so it exits when main thread exits)
            self._record_thread = threading.Thread(
                target=self._recording_loop,
                daemon=True
            )
            self._record_thread.start()
            
            return True
            
        except OSError as e:
            # Re-raise OSError for the caller to handle (microphone not found)
            print(f"[ERROR] Audio device error: {e}")
            self._cleanup()
            raise
            
        except Exception as e:
            # Log and return False for other errors
            print(f"[ERROR] Failed to start recording: {e}")
            self._cleanup()
            return False

    def _recording_loop(self) -> None:
        """
        Internal method that runs in a separate thread.
        
        Continuously reads audio data from the input stream while
        recording is active. Uses non-blocking reads to prevent
        buffer overflow issues.
        """
        while self.is_recording:
            try:
                if self._stream and self._stream.is_active():
                    # Read audio chunk from the stream
                    # exception_on_overflow=False prevents crashes on slow systems
                    data = self._stream.read(
                        self.CHUNK_SIZE,
                        exception_on_overflow=False
                    )
                    self._frames.append(data)
            except Exception as e:
                print(f"[ERROR] Recording loop error: {e}")
                break

    def stop_recording(self) -> bool:
        """
        Stop the current recording.
        
        Returns:
            bool: True if recording was stopped successfully, False otherwise.
        """
        if not self.is_recording:
            return False

        # Set flag to stop recording
        with self._lock:
            self._is_recording = False

        # Wait for recording thread to finish
        if self._record_thread and self._record_thread.is_alive():
            self._record_thread.join(timeout=2.0)

        # Stop and close the stream
        if self._stream:
            try:
                self._stream.stop_stream()
                self._stream.close()
            except Exception as e:
                print(f"Error stopping stream: {e}")
            self._stream = None

        # Terminate PyAudio
        if self._pyaudio:
            self._pyaudio.terminate()
            self._pyaudio = None

        return True

    def save_wav(self, filename: str) -> bool:
        """
        Save the recorded audio to a WAV file.
        
        Args:
            filename: The path/name of the output WAV file.
            
        Returns:
            bool: True if file was saved successfully, False otherwise.
        """
        if not self._frames:
            print("No audio data to save.")
            return False

        try:
            # Ensure directory exists
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(b''.join(self._frames))
            return True
        except Exception as e:
            print(f"Error saving WAV file: {e}")
            return False

    def save_recording(self, username: str, base_dir: str = "data") -> Optional[str]:
        """
        Save the recorded audio to a user-specific folder with timestamp.
        
        Creates folder structure: data/recordings/{username}/{YYYY-MM-DD}/
        Filename format: {HH-MM-SS}.wav
        
        Args:
            username: The username to create folder for.
            base_dir: Base directory for data storage (default: "data").
            
        Returns:
            str: Full path to saved file, or None if save failed.
        """
        if not self._frames:
            print("No audio data to save.")
            return None

        if not username:
            print("Username is required for saving.")
            return None

        try:
            # Get current date and time
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d")
            time_string = now.strftime("%H-%M-%S")
            
            # Construct the save path: data/recordings/username/date/
            save_dir = os.path.join(base_dir, "recordings", username, date_string)
            
            # Create directory if it doesn't exist
            if not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
                print(f"Created directory: {save_dir}")
            
            # Full file path with timestamp
            filename = f"{time_string}.wav"
            full_path = os.path.join(save_dir, filename)
            
            # Save the WAV file
            with wave.open(full_path, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(b''.join(self._frames))
            
            print(f"Recording saved: {full_path}")
            return full_path
            
        except Exception as e:
            print(f"Error saving recording: {e}")
            return None

    def get_audio_data(self) -> Optional[np.ndarray]:
        """
        Get the recorded audio as a numpy array.
        
        Returns:
            numpy.ndarray or None: Audio data as float32 array, or None if no data.
        """
        if not self._frames:
            return None

        # Convert bytes to numpy array
        audio_bytes = b''.join(self._frames)
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
        
        # Normalize to float32 in range [-1, 1]
        audio_float = audio_array.astype(np.float32) / 32768.0
        
        return audio_float

    def get_duration(self) -> float:
        """
        Get the duration of the recorded audio in seconds.
        
        Returns:
            float: Duration in seconds.
        """
        if not self._frames:
            return 0.0
        
        total_samples = len(self._frames) * self.CHUNK_SIZE
        return total_samples / self.SAMPLE_RATE

    def clear(self):
        """Clear the recorded audio frames."""
        self._frames = []

    def _cleanup(self):
        """Clean up PyAudio resources."""
        with self._lock:
            self._is_recording = False
            
        if self._stream:
            try:
                self._stream.stop_stream()
                self._stream.close()
            except:
                pass
            self._stream = None
            
        if self._pyaudio:
            try:
                self._pyaudio.terminate()
            except:
                pass
            self._pyaudio = None

    def __del__(self):
        """Destructor to ensure resources are cleaned up."""
        self._cleanup()


# Convenience function for quick recording
def record_audio(duration: float, filename: str) -> bool:
    """
    Record audio for a specified duration and save to file.
    
    Args:
        duration: Recording duration in seconds.
        filename: Output WAV filename.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    import time
    
    recorder = AudioRecorder()
    
    if not recorder.start_recording():
        return False
    
    time.sleep(duration)
    recorder.stop_recording()
    
    return recorder.save_wav(filename)


if __name__ == "__main__":
    # Test the AudioRecorder
    import time
    
    print("Testing AudioRecorder...")
    recorder = AudioRecorder()
    
    print("Starting recording for 3 seconds...")
    recorder.start_recording()
    time.sleep(3)
    recorder.stop_recording()
    
    print(f"Recording duration: {recorder.get_duration():.2f} seconds")
    
    if recorder.save_wav("test_recording.wav"):
        print("Saved to test_recording.wav")
    else:
        print("Failed to save recording")
