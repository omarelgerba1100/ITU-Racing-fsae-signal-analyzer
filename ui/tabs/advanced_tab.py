"""
Advanced analysis tab for spectrogram, PSD, statistics, etc.
"""

import customtkinter as ctk
import numpy as np
import tempfile
import webbrowser

from core.config import COLORS
from processing.signal_processing import SignalProcessor
from plotting.interactive_plotter import InteractivePlotter


class AdvancedTab:
    """Tab for advanced signal analysis."""

    def __init__(self, parent, app):
        """
        Initialize the advanced tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app
        self.advanced_plot_html = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        # Buttons frame
        btn_frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_light'], corner_radius=10)
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            btn_frame, text="Select Analysis Type:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_red']
        ).pack(pady=10)

        buttons_row = ctk.CTkFrame(btn_frame, fg_color="transparent")
        buttons_row.pack(pady=10)

        analyses = [
            ("Spectrogram", self.show_spectrogram),
            ("PSD (Welch)", self.show_psd_welch),
            ("Statistics", self.show_statistics),
            ("Peak Detection", self.show_peaks),
            ("RMS Analysis", self.show_rms)
        ]

        for text, cmd in analyses:
            btn = ctk.CTkButton(
                buttons_row, text=text, command=cmd,
                fg_color=COLORS['accent_blue'],
                hover_color=COLORS['accent_red'],
                font=ctk.CTkFont(size=13, weight="bold"),
                width=150, height=40
            )
            btn.pack(side="left", padx=5)

        # Results area
        self.advanced_results = ctk.CTkTextbox(
            self.parent,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=COLORS['bg_light'],
            text_color=COLORS['accent_green'],
            height=150
        )
        self.advanced_results.pack(fill="x", padx=10, pady=5)
        self.advanced_results.insert("1.0", "Select an analysis method above...")

        # Plot button
        self.advanced_plot_btn = ctk.CTkButton(
            self.parent, text="Open Analysis in Browser",
            command=self.open_advanced_plot_browser,
            fg_color=COLORS['accent_blue'],
            state="disabled"
        )
        self.advanced_plot_btn.pack(pady=10)

    def get_data(self):
        """Get calibrated data."""
        if self.app.data is None:
            return None
        cal = self.app.analyze_tab.get_calibration()
        return self.app.data / cal

    def show_spectrogram(self):
        """Show spectrogram analysis."""
        data_g = self.get_data()
        if data_g is None:
            self.app.show_warning("Please load data first!")
            return

        try:
            fs = self.app.analyze_tab.get_fs()

            fig = InteractivePlotter.create_spectrogram(data_g, fs)

            self.advanced_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.advanced_plot_html)

            self.advanced_plot_btn.configure(state="normal")
            self.advanced_results.delete("1.0", "end")
            self.advanced_results.insert(
                "1.0",
                "Spectrogram: Shows how frequency content changes over time.\n"
                "Useful for identifying transient events and time-varying vibrations."
            )

        except Exception as e:
            self.app.show_error(f"Spectrogram failed:\n{str(e)}")

    def show_psd_welch(self):
        """Show PSD using Welch method."""
        data_g = self.get_data()
        if data_g is None:
            self.app.show_warning("Please load data first!")
            return

        try:
            fs = self.app.analyze_tab.get_fs()

            fig, peak_freq = InteractivePlotter.create_psd_welch(data_g, fs)

            self.advanced_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.advanced_plot_html)

            self.advanced_plot_btn.configure(state="normal")
            self.advanced_results.delete("1.0", "end")
            self.advanced_results.insert(
                "1.0",
                f"PSD (Welch Method)\nMore accurate than simple FFT periodogram.\n\n"
                f"Peak frequency: {peak_freq:.2f} Hz"
            )

        except Exception as e:
            self.app.show_error(f"PSD analysis failed:\n{str(e)}")

    def show_statistics(self):
        """Show signal statistics."""
        data_g = self.get_data()
        if data_g is None:
            self.app.show_warning("Please load data first!")
            return

        try:
            fs = self.app.analyze_tab.get_fs()

            stats = SignalProcessor.compute_statistics(data_g, fs)

            stats_text = f"""SIGNAL STATISTICS
{'=' * 40}
Points:     {stats['points']:,}
Duration:   {stats['duration']:.2f} s

Mean:       {stats['mean']:.6f} g
Std Dev:    {stats['std']:.6f} g
RMS:        {stats['rms']:.6f} g

Min:        {stats['min']:.6f} g
Max:        {stats['max']:.6f} g
Peak-Peak:  {stats['peak_to_peak']:.6f} g

Crest Factor: {stats['crest_factor']:.4f}
"""

            self.advanced_results.delete("1.0", "end")
            self.advanced_results.insert("1.0", stats_text)

            # Create histogram
            fig = InteractivePlotter.create_histogram(data_g)

            self.advanced_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.advanced_plot_html)
            self.advanced_plot_btn.configure(state="normal")

        except Exception as e:
            self.app.show_error(f"Statistics failed:\n{str(e)}")

    def show_peaks(self):
        """Detect and show frequency peaks."""
        data_g = self.get_data()
        if data_g is None:
            self.app.show_warning("Please load data first!")
            return

        try:
            fs = self.app.analyze_tab.get_fs()

            peak_freqs, peak_values = SignalProcessor.detect_peaks(data_g, fs)

            result = "TOP 10 FREQUENCY PEAKS\n" + "=" * 40 + "\n"
            for i, (freq, mag) in enumerate(zip(peak_freqs, peak_values), 1):
                result += f"{i:2d}. {freq:8.2f} Hz  |  Amp: {mag:.2e}\n"

            self.advanced_results.delete("1.0", "end")
            self.advanced_results.insert("1.0", result)

            # Create plot
            N = len(data_g)
            fft_result = np.abs(np.fft.fft(data_g))[:N // 2]
            freqs = np.fft.fftfreq(N, 1 / fs)[:N // 2]

            fig = InteractivePlotter.create_peak_detection_plot(
                freqs, fft_result, peak_freqs, peak_values, fs
            )

            self.advanced_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.advanced_plot_html)
            self.advanced_plot_btn.configure(state="normal")

        except Exception as e:
            self.app.show_error(f"Peak detection failed:\n{str(e)}")

    def show_rms(self):
        """RMS analysis with windowing."""
        data_g = self.get_data()
        if data_g is None:
            self.app.show_warning("Please load data first!")
            return

        try:
            fs = self.app.analyze_tab.get_fs()

            times, rms_values, overall_rms = SignalProcessor.compute_rms_windowed(data_g, fs)

            result = f"""RMS ANALYSIS (100ms windows)
{'=' * 40}
Overall RMS:    {overall_rms:.6f} g
Max RMS:        {np.max(rms_values):.6f} g
Min RMS:        {np.min(rms_values):.6f} g
Avg RMS:        {np.mean(rms_values):.6f} g

Vibration Severity (ISO 10816):
  - < 0.28 g: Good
  - 0.28-0.71 g: Acceptable
  - 0.71-1.8 g: Unsatisfactory
  - > 1.8 g: Unacceptable
"""

            self.advanced_results.delete("1.0", "end")
            self.advanced_results.insert("1.0", result)

            # Plot
            fig = InteractivePlotter.create_rms_plot(times, rms_values, overall_rms)

            self.advanced_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.advanced_plot_html)
            self.advanced_plot_btn.configure(state="normal")

        except Exception as e:
            self.app.show_error(f"RMS analysis failed:\n{str(e)}")

    def open_advanced_plot_browser(self):
        """Open advanced analysis plot in browser."""
        if self.advanced_plot_html:
            webbrowser.open('file://' + self.advanced_plot_html)
