"""
Analyze tab for loading and analyzing signal data.
"""

import customtkinter as ctk
from tkinter import filedialog
import numpy as np
import tempfile
import os

from ...core.config import COLORS, APP_CONFIG
from ...utils.data_loader import DataLoader
from ...processing.signal_processing import SignalProcessor
from ...plotting.interactive_plotter import InteractivePlotter


class AnalyzeTab:
    """Tab for loading and analyzing signal data."""

    def __init__(self, parent, app):
        """
        Initialize the analyze tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app
        self.data = None
        self.current_plot_html = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        # Left panel - Controls
        left_panel = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_light'], corner_radius=10)
        left_panel.pack(side="left", fill="y", padx=(10, 5), pady=10)

        # File section
        file_label = ctk.CTkLabel(
            left_panel, text="Data Import",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_red']
        )
        file_label.pack(pady=(15, 10), padx=15)

        self.file_entry = ctk.CTkEntry(left_panel, width=250, placeholder_text="No file selected")
        self.file_entry.pack(pady=5, padx=15)

        browse_btn = ctk.CTkButton(
            left_panel, text="Browse File",
            command=self.browse_file,
            fg_color=COLORS['accent_red'],
            hover_color="#ff6b6b",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        browse_btn.pack(pady=10, padx=15, fill="x")

        # Detection info
        self.detect_info = ctk.CTkLabel(
            left_panel, text="Format: -\nDelimiter: -\nDecimal: -",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['accent_green'],
            justify="left"
        )
        self.detect_info.pack(pady=10, padx=15)

        # Separator
        sep1 = ctk.CTkFrame(left_panel, height=2, fg_color=COLORS['accent_blue'])
        sep1.pack(fill="x", padx=15, pady=10)

        # Parameters section
        param_label = ctk.CTkLabel(
            left_panel, text="Parameters",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_red']
        )
        param_label.pack(pady=(10, 10), padx=15)

        # Sampling frequency
        fs_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        fs_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(fs_frame, text="Sampling Freq (Hz):", font=ctk.CTkFont(size=13)).pack(side="left")
        self.fs_entry = ctk.CTkEntry(fs_frame, width=100)
        self.fs_entry.insert(0, str(APP_CONFIG['default_fs']))
        self.fs_entry.pack(side="right")

        # Calibration
        cal_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        cal_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(cal_frame, text="Calibration (mV/g):", font=ctk.CTkFont(size=13)).pack(side="left")
        self.cal_entry = ctk.CTkEntry(cal_frame, width=100)
        self.cal_entry.insert(0, str(APP_CONFIG['default_calibration']))
        self.cal_entry.pack(side="right")

        # Analyze button
        analyze_btn = ctk.CTkButton(
            left_panel, text="ANALYZE DATA",
            command=self.analyze_data,
            fg_color=COLORS['accent_green'],
            hover_color="#7fff00",
            text_color=COLORS['bg_dark'],
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
        analyze_btn.pack(pady=20, padx=15, fill="x")

        # Results section
        sep2 = ctk.CTkFrame(left_panel, height=2, fg_color=COLORS['accent_blue'])
        sep2.pack(fill="x", padx=15, pady=10)

        result_label = ctk.CTkLabel(
            left_panel, text="Results",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_red']
        )
        result_label.pack(pady=(10, 10), padx=15)

        self.result_text = ctk.CTkTextbox(
            left_panel, width=270, height=200,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=COLORS['bg_dark'],
            text_color=COLORS['accent_green']
        )
        self.result_text.pack(pady=10, padx=15)

        # Right panel - Plot
        right_panel = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_light'], corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        plot_label = ctk.CTkLabel(
            right_panel,
            text="Interactive Signal Visualization (Zoom with mouse wheel, Pan by dragging)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_green']
        )
        plot_label.pack(pady=(15, 10))

        # Plot buttons
        btn_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)

        self.open_plot_btn = ctk.CTkButton(
            btn_frame, text="Open Interactive Plot in Browser",
            command=self.open_plot_browser,
            fg_color=COLORS['accent_blue'],
            hover_color="#1a5490",
            state="disabled"
        )
        self.open_plot_btn.pack(side="left", padx=5)

        # Plot placeholder/info
        self.plot_info_frame = ctk.CTkFrame(right_panel, fg_color=COLORS['bg_dark'], corner_radius=10)
        self.plot_info_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.plot_status = ctk.CTkLabel(
            self.plot_info_frame,
            text="Load data and click 'Analyze' to generate interactive plots\n\n"
                 "Features:\n"
                 "- Zoom: Mouse wheel or box select\n"
                 "- Pan: Click and drag\n"
                 "- Reset: Double-click\n"
                 "- Save: Use toolbar in browser",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_gray'],
            justify="center"
        )
        self.plot_status.pack(expand=True)

    def browse_file(self):
        """Open file dialog and load data."""
        filepath = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[
                ("All Supported", "*.txt *.csv *.dat *.xlsx *.xls"),
                ("Text Files", "*.txt *.csv *.dat"),
                ("Excel Files", "*.xlsx *.xls"),
                ("All Files", "*.*")
            ]
        )

        if filepath:
            try:
                self.data, info = DataLoader.load(filepath)
                self.app.data = self.data  # Share with main app

                self.file_entry.delete(0, "end")
                self.file_entry.insert(0, os.path.basename(filepath))

                self.detect_info.configure(
                    text=f"Format: {info['type']}\nDelimiter: {info['delimiter']}\n"
                         f"Decimal: {info['decimal']}\nPoints: {len(self.data):,}"
                )

                self.app.update_status(f"Loaded {len(self.data):,} data points from {os.path.basename(filepath)}")

            except Exception as e:
                self.app.show_error(f"Failed to load file:\n{str(e)}")

    def get_fs(self) -> float:
        """Get sampling frequency from entry."""
        return float(self.fs_entry.get())

    def get_calibration(self) -> float:
        """Get calibration value from entry."""
        return float(self.cal_entry.get())

    def analyze_data(self):
        """Perform FFT analysis."""
        if self.data is None:
            self.app.show_warning("Please load a data file first!")
            return

        try:
            fs = self.get_fs()
            cal = self.get_calibration()

            data_g = self.data / cal
            N = len(data_g)
            dt = 1 / fs

            # FFT analysis
            freq_pos, magnitude, psd = SignalProcessor.perform_fft(data_g, fs)
            resonance_freq, resonance_rounded = SignalProcessor.find_resonance(freq_pos, psd)
            top_peaks = SignalProcessor.find_top_peaks(freq_pos, psd, 5)

            # Update results
            self.result_text.delete("1.0", "end")
            result = f"Data Points: {N:,}\n"
            result += f"Duration: {N/fs:.2f} s\n"
            result += f"Sampling: {fs:,.0f} Hz\n"
            result += f"{'=' * 30}\n"
            result += f"RESONANCE:\n"
            result += f"   {resonance_freq:.4f} Hz\n"
            result += f"   -> Rounded: {resonance_rounded} Hz\n"
            result += f"{'=' * 30}\n"
            result += f"Top 5 Peaks:\n"
            for i, (freq, power) in enumerate(top_peaks, 1):
                result += f"   {i}. {freq:.2f} Hz\n"

            self.result_text.insert("1.0", result)

            # Create interactive plot
            time = np.arange(N) * dt
            fig = InteractivePlotter.create_time_frequency_plot(
                time, data_g, freq_pos, psd, resonance_freq,
                f"Signal Analysis - Resonance: {resonance_freq:.2f} Hz"
            )

            # Save to temp file
            self.current_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.current_plot_html)

            # Enable plot button
            self.open_plot_btn.configure(state="normal")
            self.plot_status.configure(
                text=f"Analysis complete!\n\n"
                     f"Resonance: {resonance_freq:.4f} Hz -> {resonance_rounded} Hz\n\n"
                     f"Click 'Open Interactive Plot in Browser' to view and zoom"
            )

            self.app.update_status(f"Analysis complete! Resonance: {resonance_freq:.4f} Hz -> {resonance_rounded} Hz")

        except Exception as e:
            self.app.show_error(f"Analysis failed:\n{str(e)}")

    def open_plot_browser(self):
        """Open main analysis plot in browser."""
        import webbrowser
        if self.current_plot_html:
            webbrowser.open('file://' + self.current_plot_html)
