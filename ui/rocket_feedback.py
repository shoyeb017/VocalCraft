"""
Rocket Feedback Widget for VocalCraft
A gamified visual feedback component with animated rocket and fuel tank.
"""

import customtkinter as ctk
from typing import Optional
import threading


class RocketFeedback(ctk.CTkFrame):
    """
    A custom widget displaying a rocket with a vertical fuel tank progress bar.
    Provides animated visual feedback based on user performance score.
    
    Features:
    - Vertical progress bar ("Fuel Tank") that fills based on score
    - Rocket icon that moves up as score increases
    - Color-coded feedback (Red/Yellow/Green)
    - "Blast Off!" animation when score exceeds 90%
    """

    # Color thresholds
    COLOR_LOW = "#e74c3c"       # Red (0-40%)
    COLOR_MEDIUM = "#f39c12"    # Yellow (40-70%)
    COLOR_HIGH = "#27ae60"      # Green (70-100%)
    COLOR_BLAST_OFF = "#9b59b6" # Purple for blast off effect
    
    # Score thresholds
    THRESHOLD_MEDIUM = 40
    THRESHOLD_HIGH = 70
    THRESHOLD_BLAST_OFF = 90

    def __init__(
        self,
        master,
        width: int = 120,
        height: int = 300,
        **kwargs
    ):
        """
        Initialize the RocketFeedback widget.
        
        Args:
            master: Parent widget.
            width: Widget width in pixels.
            height: Widget height in pixels.
        """
        super().__init__(master, width=width, height=height, **kwargs)
        
        self.widget_width = width
        self.widget_height = height
        self.current_score = 0
        self._is_animating = False
        
        # Configure layout
        self.configure(fg_color=("gray90", "gray17"))
        self.grid_propagate(False)
        
        # Build the widget
        self._create_widgets()
        
        # Initial state
        self.update_fuel(0)

    def _create_widgets(self):
        """Create the fuel tank and rocket display."""
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Power",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(pady=(10, 5))
        
        # Container for fuel tank and rocket
        self.tank_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            width=self.widget_width - 20,
            height=self.widget_height - 80
        )
        self.tank_frame.pack(expand=True, fill="both", padx=10, pady=5)
        self.tank_frame.pack_propagate(False)
        
        # Fuel tank (vertical progress bar)
        self.fuel_tank = ctk.CTkProgressBar(
            self.tank_frame,
            orientation="vertical",
            width=30,
            height=self.widget_height - 120,
            progress_color=self.COLOR_LOW,
            fg_color=("gray80", "gray25")
        )
        self.fuel_tank.place(relx=0.3, rely=0.5, anchor="center")
        self.fuel_tank.set(0)
        
        # Rocket icon (using text emoji as placeholder - can be replaced with image)
        self.rocket_label = ctk.CTkLabel(
            self.tank_frame,
            text="🚀",
            font=ctk.CTkFont(size=32)
        )
        # Initial position at bottom
        self._rocket_base_y = 0.85
        self.rocket_label.place(relx=0.7, rely=self._rocket_base_y, anchor="center")
        
        # Score label
        self.score_label = ctk.CTkLabel(
            self,
            text="0%",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.score_label.pack(pady=(5, 5))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        self.status_label.pack(pady=(0, 10))

    def update_fuel(self, score: float):
        """
        Update the fuel tank and rocket position based on score.
        
        Args:
            score: Score value from 0 to 100.
        """
        # Clamp score to valid range
        score = max(0, min(100, score))
        self.current_score = score
        
        # Update progress bar
        self.fuel_tank.set(score / 100)
        
        # Update score label
        self.score_label.configure(text=f"{int(score)}%")
        
        # Determine color based on score
        if score < self.THRESHOLD_MEDIUM:
            color = self.COLOR_LOW
            status = "Keep trying!"
        elif score < self.THRESHOLD_HIGH:
            color = self.COLOR_MEDIUM
            status = "Getting better!"
        else:
            color = self.COLOR_HIGH
            status = "Great job!"
        
        # Apply color
        self.fuel_tank.configure(progress_color=color)
        self.status_label.configure(text=status)
        
        # Move rocket based on score (0% = bottom, 100% = top)
        # Map score to y position: 0.85 (bottom) to 0.15 (top)
        rocket_y = self._rocket_base_y - (score / 100) * 0.7
        self.rocket_label.place(relx=0.7, rely=rocket_y, anchor="center")
        
        # Trigger blast off animation if score > 90
        if score > self.THRESHOLD_BLAST_OFF:
            self._trigger_blast_off()

    def _trigger_blast_off(self):
        """Trigger the blast off animation effect."""
        if self._is_animating:
            return
        
        self._is_animating = True
        self.status_label.configure(text="BLAST OFF!", text_color=self.COLOR_BLAST_OFF)
        
        # Flash animation sequence
        def flash_sequence():
            colors = [
                self.COLOR_BLAST_OFF,
                self.COLOR_HIGH,
                self.COLOR_BLAST_OFF,
                self.COLOR_HIGH,
                self.COLOR_BLAST_OFF,
            ]
            
            for i, color in enumerate(colors):
                self.after(i * 150, lambda c=color: self._flash_color(c))
            
            # Reset after animation
            self.after(len(colors) * 150 + 200, self._reset_after_blast_off)
        
        flash_sequence()

    def _flash_color(self, color: str):
        """Flash the widget with a color."""
        try:
            self.configure(fg_color=color)
            self.fuel_tank.configure(progress_color=color)
        except Exception:
            pass  # Widget might be destroyed

    def _reset_after_blast_off(self):
        """Reset widget appearance after blast off animation."""
        try:
            self.configure(fg_color=("gray90", "gray17"))
            self.fuel_tank.configure(progress_color=self.COLOR_HIGH)
            self.status_label.configure(
                text="Excellent!",
                text_color=self.COLOR_HIGH
            )
            self._is_animating = False
        except Exception:
            pass  # Widget might be destroyed

    def reset(self):
        """Reset the widget to initial state."""
        self._is_animating = False
        self.current_score = 0
        self.fuel_tank.set(0)
        self.fuel_tank.configure(progress_color=self.COLOR_LOW)
        self.score_label.configure(text="0%")
        self.status_label.configure(text="Ready", text_color=("gray50", "gray60"))
        self.rocket_label.place(relx=0.7, rely=self._rocket_base_y, anchor="center")
        self.configure(fg_color=("gray90", "gray17"))

    def get_score(self) -> float:
        """Get the current score value."""
        return self.current_score

    def set_rocket_image(self, image_path: str):
        """
        Set a custom rocket image (optional enhancement).
        
        Args:
            image_path: Path to the rocket image file.
        """
        try:
            from PIL import Image
            image = Image.open(image_path)
            image = image.resize((40, 40))
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(40, 40))
            self.rocket_label.configure(image=ctk_image, text="")
        except Exception as e:
            print(f"[WARN] Could not load rocket image: {e}")
            # Keep the emoji fallback


if __name__ == "__main__":
    # Test the RocketFeedback widget
    import time
    
    root = ctk.CTk()
    root.title("RocketFeedback Test")
    root.geometry("300x400")
    
    ctk.set_appearance_mode("dark")
    
    rocket = RocketFeedback(root, width=150, height=320)
    rocket.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Score slider for testing
    def on_slider_change(value):
        rocket.update_fuel(value)
    
    slider = ctk.CTkSlider(
        root,
        from_=0,
        to=100,
        command=on_slider_change
    )
    slider.pack(padx=20, pady=10, fill="x")
    slider.set(0)
    
    # Reset button
    reset_btn = ctk.CTkButton(root, text="Reset", command=rocket.reset)
    reset_btn.pack(pady=10)
    
    root.mainloop()
