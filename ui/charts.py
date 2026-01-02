"""
Charts Module for VocalCraft
Provides audio visualization components using Matplotlib.
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from typing import Optional, Tuple
import librosa
import librosa.display


class AudioVisualizer:
    """
    A class to visualize audio data using Matplotlib.
    Designed to be embedded in CustomTkinter frames.
    """

    def __init__(
        self, 
        parent_frame, 
        figsize: Tuple[float, float] = (8, 4),
        dpi: int = 100,
        bg_color: str = '#2b2b2b'
    ):
        """
        Initialize the AudioVisualizer.
        
        Args:
            parent_frame: The CustomTkinter frame to embed the chart in.
            figsize: Figure size as (width, height) in inches.
            dpi: Dots per inch for the figure.
            bg_color: Background color for the plot.
        """
        self.parent_frame = parent_frame
        self.bg_color = bg_color
        self.figsize = figsize
        self.dpi = dpi
        
        # Set matplotlib style
        plt.style.use('dark_background')
        
        # Create the figure
        self.figure = Figure(figsize=figsize, dpi=dpi, facecolor=bg_color)
        
        # Create subplots
        self.ax_waveform = self.figure.add_subplot(2, 1, 1)
        self.ax_spectrogram = self.figure.add_subplot(2, 1, 2)
        
        # Style the axes
        self._style_axes()
        
        # Create canvas and embed in parent
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Show placeholder
        self._show_placeholder()

    def _style_axes(self):
        """Apply consistent styling to all axes."""
        for ax in [self.ax_waveform, self.ax_spectrogram]:
            ax.set_facecolor(self.bg_color)
            ax.tick_params(colors='gray')
            for spine in ax.spines.values():
                spine.set_color('gray')

    def _show_placeholder(self):
        """Show placeholder text when no audio is loaded."""
        self.ax_waveform.clear()
        self.ax_spectrogram.clear()
        
        self.ax_waveform.text(
            0.5, 0.5, '📊 Waveform will appear here',
            ha='center', va='center', fontsize=14,
            color='gray', transform=self.ax_waveform.transAxes
        )
        self.ax_waveform.set_facecolor(self.bg_color)
        self.ax_waveform.set_xticks([])
        self.ax_waveform.set_yticks([])
        
        self.ax_spectrogram.text(
            0.5, 0.5, '🎵 Spectrogram will appear here',
            ha='center', va='center', fontsize=14,
            color='gray', transform=self.ax_spectrogram.transAxes
        )
        self.ax_spectrogram.set_facecolor(self.bg_color)
        self.ax_spectrogram.set_xticks([])
        self.ax_spectrogram.set_yticks([])
        
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def update_plot(
        self, 
        waveform_data: np.ndarray, 
        sample_rate: int = 22050
    ):
        """
        Update the waveform plot with new audio data.
        
        Args:
            waveform_data: 1D numpy array of audio samples.
            sample_rate: Sample rate of the audio.
        """
        self.ax_waveform.clear()
        
        if len(waveform_data) == 0:
            self._show_placeholder()
            return
        
        # Create time axis
        times = np.linspace(0, len(waveform_data) / sample_rate, num=len(waveform_data))
        
        # Plot waveform
        self.ax_waveform.plot(times, waveform_data, color='#3498db', linewidth=0.5)
        
        # Style
        self.ax_waveform.set_title('Waveform', fontsize=12, color='white', fontweight='bold')
        self.ax_waveform.set_xlabel('Time (s)', fontsize=10, color='gray')
        self.ax_waveform.set_ylabel('Amplitude', fontsize=10, color='gray')
        self.ax_waveform.set_facecolor(self.bg_color)
        self.ax_waveform.tick_params(colors='gray')
        self.ax_waveform.set_xlim([0, times[-1] if len(times) > 0 else 1])
        
        for spine in self.ax_waveform.spines.values():
            spine.set_color('gray')
        
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def update_spectrogram(
        self, 
        spectrogram_data: np.ndarray,
        sample_rate: int = 22050
    ):
        """
        Update the spectrogram plot.
        
        Args:
            spectrogram_data: 2D numpy array (mel spectrogram in dB).
            sample_rate: Sample rate of the audio.
        """
        self.ax_spectrogram.clear()
        
        if spectrogram_data.size == 0:
            return
        
        # Display spectrogram
        img = librosa.display.specshow(
            spectrogram_data,
            sr=sample_rate,
            x_axis='time',
            y_axis='mel',
            ax=self.ax_spectrogram,
            cmap='magma'
        )
        
        # Style
        self.ax_spectrogram.set_title('Mel-Spectrogram', fontsize=12, color='white', fontweight='bold')
        self.ax_spectrogram.set_xlabel('Time (s)', fontsize=10, color='gray')
        self.ax_spectrogram.set_ylabel('Frequency (Hz)', fontsize=10, color='gray')
        self.ax_spectrogram.set_facecolor(self.bg_color)
        self.ax_spectrogram.tick_params(colors='gray')
        
        for spine in self.ax_spectrogram.spines.values():
            spine.set_color('gray')
        
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def update_full(
        self, 
        waveform_data: np.ndarray,
        spectrogram_data: np.ndarray,
        sample_rate: int = 22050
    ):
        """
        Update both waveform and spectrogram plots.
        
        Args:
            waveform_data: 1D numpy array of audio samples.
            spectrogram_data: 2D numpy array (mel spectrogram in dB).
            sample_rate: Sample rate of the audio.
        """
        self.update_plot(waveform_data, sample_rate)
        self.update_spectrogram(spectrogram_data, sample_rate)

    def clear(self):
        """Clear all plots and show placeholder."""
        self._show_placeholder()

    def destroy(self):
        """Clean up the visualizer."""
        self.canvas_widget.destroy()


class ProgressChart:
    """
    A class to visualize patient progress over time.
    Shows score trends and statistics.
    """

    def __init__(
        self, 
        parent_frame, 
        figsize: Tuple[float, float] = (6, 3),
        dpi: int = 100,
        bg_color: str = '#2b2b2b'
    ):
        """
        Initialize the ProgressChart.
        
        Args:
            parent_frame: The CustomTkinter frame to embed the chart in.
            figsize: Figure size as (width, height) in inches.
            dpi: Dots per inch for the figure.
            bg_color: Background color for the plot.
        """
        self.parent_frame = parent_frame
        self.bg_color = bg_color
        
        plt.style.use('dark_background')
        
        self.figure = Figure(figsize=figsize, dpi=dpi, facecolor=bg_color)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.set_facecolor(bg_color)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        self._show_placeholder()

    def _show_placeholder(self):
        """Show placeholder when no data is available."""
        self.ax.clear()
        self.ax.text(
            0.5, 0.5, '📈 Progress chart will appear here',
            ha='center', va='center', fontsize=12,
            color='gray', transform=self.ax.transAxes
        )
        self.ax.set_facecolor(self.bg_color)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def update_progress(self, dates: list, scores: list):
        """
        Update the progress chart with score history.
        
        Args:
            dates: List of date strings.
            scores: List of scores corresponding to dates.
        """
        self.ax.clear()
        
        if not dates or not scores:
            self._show_placeholder()
            return
        
        # Plot the progress line
        x = range(len(dates))
        self.ax.plot(x, scores, color='#2ecc71', linewidth=2, marker='o', markersize=6)
        self.ax.fill_between(x, scores, alpha=0.3, color='#2ecc71')
        
        # Add trend line
        if len(scores) > 1:
            z = np.polyfit(x, scores, 1)
            p = np.poly1d(z)
            self.ax.plot(x, p(x), '--', color='#3498db', linewidth=1, alpha=0.7)
        
        # Style
        self.ax.set_title('Progress Over Time', fontsize=12, color='white', fontweight='bold')
        self.ax.set_xlabel('Session', fontsize=10, color='gray')
        self.ax.set_ylabel('Score (%)', fontsize=10, color='gray')
        self.ax.set_ylim([0, 100])
        self.ax.set_facecolor(self.bg_color)
        self.ax.tick_params(colors='gray')
        
        # X-axis labels
        if len(dates) <= 10:
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)
        
        for spine in self.ax.spines.values():
            spine.set_color('gray')
        
        self.figure.tight_layout()
        self.canvas.draw()

    def clear(self):
        """Clear the chart."""
        self._show_placeholder()

    def destroy(self):
        """Clean up the chart."""
        self.canvas_widget.destroy()
