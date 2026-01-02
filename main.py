"""
VocalCraft - Speech Therapy Tool
Main Entry Point

A modern desktop application for speech therapy using Python and CustomTkinter.
Designed to help patients with speech conditions practice and improve their
communication skills through guided exercises and real-time feedback.

Author: VocalCraft Team
Version: 1.0.0
"""

import sys
import os
import io

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from database import DatabaseManager, get_database
from ui.main_window import VocalCraftMainWindow
from ui.login_window import LoginWindow


def setup_appearance():
    """Configure the application appearance settings."""
    # Set the appearance mode (Dark, Light, or System)
    ctk.set_appearance_mode("dark")
    
    # Set the default color theme
    ctk.set_default_color_theme("blue")


def initialize_database() -> DatabaseManager:
    """
    Initialize the database on startup.
    Creates tables if they don't exist.
    
    Returns:
        DatabaseManager: The initialized database manager.
    """
    print("[DB] Initializing database...")
    db = get_database("data/vocalcraft.db")
    print("[OK] Database ready!")
    return db


def check_dependencies():
    """Check that all required dependencies are available."""
    missing = []
    
    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")
    
    try:
        import pyaudio
    except ImportError:
        missing.append("pyaudio")
    
    try:
        import librosa
    except ImportError:
        missing.append("librosa")
    
    try:
        import speech_recognition
    except ImportError:
        missing.append("SpeechRecognition")
    
    try:
        import textdistance
    except ImportError:
        missing.append("textdistance")
    
    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    if missing:
        print("[ERROR] Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False
    
    return True


def main():
    """
    Application entry point.
    Initializes all components and starts the main event loop.
    """
    print("=" * 50)
    print("  VocalCraft - Speech Therapy Tool")
    print("=" * 50)
    print()
    
    # Check dependencies
    print("[*] Checking dependencies...")
    if not check_dependencies():
        print("\n[!] Please install missing dependencies and try again.")
        sys.exit(1)
    print("[OK] All dependencies available!")
    print()
    
    # Initialize database
    db = initialize_database()
    print()
    
    # Setup appearance
    print("[*] Setting up appearance...")
    setup_appearance()
    print("[OK] Appearance configured!")
    print()
    
    # Create and run the application
    print("[*] Launching VocalCraft...")
    print("-" * 50)
    
    try:
        # Store user info for main window
        logged_in_user = {"user_id": None, "username": None}
        
        def on_login_success(user_id: int, username: str):
            """Callback when login is successful."""
            logged_in_user["user_id"] = user_id
            logged_in_user["username"] = username
            print(f"[OK] Logged in as: {username} (ID: {user_id})")
        
        # Show login window first
        print("[*] Showing login window...")
        login_window = LoginWindow(on_login_success=on_login_success)
        login_window.mainloop()
        
        # Only launch main window if login was successful
        if logged_in_user["user_id"] is not None:
            print("[*] Loading main application...")
            # Pass user info directly to constructor
            app = VocalCraftMainWindow(
                user_id=logged_in_user["user_id"],
                username=logged_in_user["username"]
            )
            app.mainloop()
        else:
            print("[!] Login cancelled or failed.")
            
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        raise
    finally:
        print("\n[OK] VocalCraft closed successfully.")


if __name__ == "__main__":
    main()
