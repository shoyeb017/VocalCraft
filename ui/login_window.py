"""
Login Window for VocalCraft
Handles user authentication with Sign In and Sign Up tabs.
"""

import customtkinter as ctk
from typing import Optional, Callable
from database import DatabaseManager, get_database


class LoginWindow(ctk.CTk):
    """
    Login/Signup window using CustomTkinter.
    Features tabbed interface for Sign In and Sign Up.
    """

    def __init__(self, on_login_success: Optional[Callable[[int, str], None]] = None):
        """
        Initialize the login window.
        
        Args:
            on_login_success: Callback function called with (user_id, username) on successful login.
        """
        super().__init__()

        # Callback for successful login
        self.on_login_success = on_login_success
        
        # Database connection
        self.db = get_database()
        
        # Logged in user info
        self.logged_in_user_id: Optional[int] = None
        self.logged_in_username: Optional[str] = None

        # Window configuration
        self.title("VocalCraft - Login")
        self.geometry("500x720")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 720) // 2
        self.geometry(f"500x720+{x}+{y}")

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Build UI
        self._create_widgets()

    def _create_widgets(self):
        """Create all UI widgets."""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.main_frame,
            text="VocalCraft",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.logo_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Speech Therapy Tool",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray60")
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Tab View for Sign In / Sign Up
        self.tabview = ctk.CTkTabview(self.main_frame, width=400, height=500)
        self.tabview.pack(pady=10, fill="both", expand=True)

        self.tabview.add("Sign In")
        self.tabview.add("Sign Up")
        self.tabview.set("Sign In")

        # ========== Sign In Tab ==========
        self._create_signin_tab()

        # ========== Sign Up Tab ==========
        self._create_signup_tab()

    def _create_signin_tab(self):
        """Create the Sign In tab content."""
        tab = self.tabview.tab("Sign In")

        # Username
        self.signin_username_label = ctk.CTkLabel(
            tab, text="Username", font=ctk.CTkFont(size=14)
        )
        self.signin_username_label.pack(pady=(30, 5), anchor="w", padx=30)

        self.signin_username_entry = ctk.CTkEntry(
            tab, width=340, height=42, placeholder_text="Enter your username"
        )
        self.signin_username_entry.pack(pady=(0, 15), padx=30)

        # Password
        self.signin_password_label = ctk.CTkLabel(
            tab, text="Password", font=ctk.CTkFont(size=14)
        )
        self.signin_password_label.pack(pady=(5, 5), anchor="w", padx=30)

        self.signin_password_entry = ctk.CTkEntry(
            tab, width=340, height=42, placeholder_text="Enter your password", show="*"
        )
        self.signin_password_entry.pack(pady=(0, 20), padx=30)

        # Error label (hidden initially)
        self.signin_error_label = ctk.CTkLabel(
            tab, text="", font=ctk.CTkFont(size=12),
            text_color=("#e74c3c", "#e74c3c")
        )
        self.signin_error_label.pack(pady=(0, 10))

        # Login button
        self.signin_button = ctk.CTkButton(
            tab, text="Login", width=340, height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._on_signin_click
        )
        self.signin_button.pack(pady=(10, 20))

        # Bind Enter key
        self.signin_password_entry.bind("<Return>", lambda e: self._on_signin_click())

    def _create_signup_tab(self):
        """Create the Sign Up tab content."""
        tab = self.tabview.tab("Sign Up")

        # Username
        self.signup_username_label = ctk.CTkLabel(
            tab, text="Username", font=ctk.CTkFont(size=14)
        )
        self.signup_username_label.pack(pady=(20, 5), anchor="w", padx=30)

        self.signup_username_entry = ctk.CTkEntry(
            tab, width=340, height=40, placeholder_text="Choose a username (min 3 chars)"
        )
        self.signup_username_entry.pack(pady=(0, 10), padx=30)

        # Password
        self.signup_password_label = ctk.CTkLabel(
            tab, text="Password", font=ctk.CTkFont(size=14)
        )
        self.signup_password_label.pack(pady=(5, 5), anchor="w", padx=30)

        self.signup_password_entry = ctk.CTkEntry(
            tab, width=340, height=40, placeholder_text="Choose a password (min 4 chars)", show="*"
        )
        self.signup_password_entry.pack(pady=(0, 10), padx=30)

        # Age
        self.signup_age_label = ctk.CTkLabel(
            tab, text="Age", font=ctk.CTkFont(size=14)
        )
        self.signup_age_label.pack(pady=(5, 5), anchor="w", padx=30)

        self.signup_age_entry = ctk.CTkEntry(
            tab, width=340, height=40, placeholder_text="Your age (optional)"
        )
        self.signup_age_entry.pack(pady=(0, 20), padx=30)

        # Error/Success label
        self.signup_message_label = ctk.CTkLabel(
            tab, text="", font=ctk.CTkFont(size=12)
        )
        self.signup_message_label.pack(pady=(0, 10))

        # Sign Up button
        self.signup_button = ctk.CTkButton(
            tab, text="Create Account", width=340, height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._on_signup_click
        )
        self.signup_button.pack(pady=(5, 20))

    def _on_signin_click(self):
        """Handle Sign In button click."""
        username = self.signin_username_entry.get().strip()
        password = self.signin_password_entry.get()

        if not username or not password:
            self._show_signin_error("Please enter username and password.")
            return

        # Attempt login
        user_id, message = self.db.login_user(username, password)

        if user_id:
            # Success
            self.logged_in_user_id = user_id
            self.logged_in_username = username
            self.signin_error_label.configure(text="")
            
            # Call success callback or launch main window
            if self.on_login_success:
                self.on_login_success(user_id, username)
            
            self.destroy()
        else:
            # Failed
            self._show_signin_error(message)

    def _show_signin_error(self, message: str):
        """Display error message on Sign In tab."""
        self.signin_error_label.configure(
            text=message,
            text_color=("#e74c3c", "#e74c3c")
        )

    def _on_signup_click(self):
        """Handle Sign Up button click."""
        username = self.signup_username_entry.get().strip()
        password = self.signup_password_entry.get()
        age_str = self.signup_age_entry.get().strip()

        # Validate
        if not username or not password:
            self._show_signup_message("Username and password are required.", error=True)
            return

        # Parse age
        age = None
        if age_str:
            try:
                age = int(age_str)
                if age < 1 or age > 120:
                    self._show_signup_message("Please enter a valid age.", error=True)
                    return
            except ValueError:
                self._show_signup_message("Age must be a number.", error=True)
                return

        # Condition is always Dysarthria for this application
        condition = "Dysarthria"

        # Attempt registration
        success, message = self.db.register_user(username, password, age, condition)

        if success:
            self._show_signup_message(message, error=False)
            # Clear fields
            self.signup_username_entry.delete(0, "end")
            self.signup_password_entry.delete(0, "end")
            self.signup_age_entry.delete(0, "end")
            # Switch to Sign In tab
            self.after(1500, lambda: self.tabview.set("Sign In"))
        else:
            self._show_signup_message(message, error=True)

    def _show_signup_message(self, message: str, error: bool = True):
        """Display message on Sign Up tab."""
        color = ("#e74c3c", "#e74c3c") if error else ("#2ecc71", "#27ae60")
        self.signup_message_label.configure(text=message, text_color=color)

    def get_logged_in_user(self) -> Optional[tuple]:
        """
        Get the logged in user info.
        
        Returns:
            Tuple of (user_id, username) or None if not logged in.
        """
        if self.logged_in_user_id:
            return (self.logged_in_user_id, self.logged_in_username)
        return None


def launch_app_with_login():
    """
    Launch the application with login flow.
    Shows login window first, then main window on success.
    """
    from ui.main_window import VocalCraftMainWindow
    
    main_window = None
    
    def on_login_success(user_id: int, username: str):
        nonlocal main_window
        print(f"[OK] Logged in as {username} (ID: {user_id})")
        # Launch main window
        main_window = VocalCraftMainWindow()
        main_window.current_user_id = user_id
        main_window.current_username = username
        main_window.mainloop()
    
    # Show login window
    login = LoginWindow(on_login_success=on_login_success)
    login.mainloop()


if __name__ == "__main__":
    # Test the login window standalone
    def test_callback(user_id, username):
        print(f"Login successful! User: {username} (ID: {user_id})")
    
    app = LoginWindow(on_login_success=test_callback)
    app.mainloop()
