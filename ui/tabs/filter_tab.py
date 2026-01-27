"""
Filter tab for digital filtering operations.
"""

import customtkinter as ctk
import numpy as np
import tempfile
import webbrowser

from core.config import COLORS, FILTER_DEFAULTS
from processing.signal_processing import SignalProcessor
from plotting.interactive_plotter import InteractivePlotter


class FilterTab:
    """Tab for digital filtering operations."""

    def __init__(self, parent, app):
        """
        Initialize the filter tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app
        self.filtered_data = None
        self.filter_plot_html = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        # Top controls
        control_frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_light'], corner_radius=10)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Filter type
        type_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            type_frame, text="Filter Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(0, 15))

        self.filter_type = ctk.StringVar(value=FILTER_DEFAULTS['type'])
        filter_types = [
            ("Low-Pass", "lowpass"),
            ("High-Pass", "highpass"),
            ("Band-Pass", "bandpass"),
            ("Notch", "bandstop")
        ]

        for text, value in filter_types:
            rb = ctk.CTkRadioButton(
                type_frame, text=text,
                variable=self.filter_type, value=value,
                fg_color=COLORS['accent_green'],
                hover_color=COLORS['accent_red']
            )
            rb.pack(side="left", padx=10)

        # Filter design
        design_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        design_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            design_frame, text="Design:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(0, 15))

        self.filter_design = ctk.StringVar(value=FILTER_DEFAULTS['design'])
        designs = [
            ("Butterworth", "butter"),
            ("Chebyshev I", "cheby1"),
            ("Bessel", "bessel")
        ]

        for text, value in designs:
            rb = ctk.CTkRadioButton(
                design_frame, text=text,
                variable=self.filter_design, value=value,
                fg_color=COLORS['accent_yellow'],
                hover_color=COLORS['accent_red']
            )
            rb.pack(side="left", padx=10)

        # Parameters
        param_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        param_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(param_frame, text="Cutoff (Hz):").pack(side="left", padx=(0, 5))
        self.cutoff_entry = ctk.CTkEntry(param_frame, width=80)
        self.cutoff_entry.insert(0, str(FILTER_DEFAULTS['cutoff']))
        self.cutoff_entry.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(param_frame, text="Order:").pack(side="left", padx=(0, 5))
        self.order_entry = ctk.CTkEntry(param_frame, width=60)
        self.order_entry.insert(0, str(FILTER_DEFAULTS['order']))
        self.order_entry.pack(side="left", padx=(0, 20))

        # For bandpass/bandstop
        ctk.CTkLabel(param_frame, text="High Cutoff (Hz):").pack(side="left", padx=(0, 5))
        self.cutoff_high_entry = ctk.CTkEntry(param_frame, width=80)
        self.cutoff_high_entry.insert(0, str(FILTER_DEFAULTS['cutoff_high']))
        self.cutoff_high_entry.pack(side="left", padx=(0, 20))

        apply_btn = ctk.CTkButton(
            param_frame, text="Apply Filter",
            command=self.apply_filter,
            fg_color=COLORS['accent_green'],
            hover_color="#7fff00",
            text_color=COLORS['bg_dark'],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        apply_btn.pack(side="left", padx=20)

        # Filter info
        self.filter_info_label = ctk.CTkLabel(
            control_frame,
            text="Configure filter and click 'Apply Filter'",
            font=ctk.CTkFont(size=13),
            text_color=COLORS['accent_green']
        )
        self.filter_info_label.pack(pady=10)

        # Plot area
        plot_frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_light'], corner_radius=10)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.filter_plot_btn = ctk.CTkButton(
            plot_frame, text="Open Filter Analysis in Browser",
            command=self.open_filter_plot_browser,
            fg_color=COLORS['accent_blue'],
            state="disabled"
        )
        self.filter_plot_btn.pack(pady=15)

        self.filter_plot_status = ctk.CTkLabel(
            plot_frame,
            text="Apply a filter to see comparison plots",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_gray']
        )
        self.filter_plot_status.pack(expand=True)

    def apply_filter(self):
        """Apply digital filter to data."""
        if self.app.data is None:
            self.app.show_warning("Please load data first!")
            return

        try:
            # Get parameters from analyze tab
            fs = self.app.analyze_tab.get_fs()
            cal = self.app.analyze_tab.get_calibration()
            fc = float(self.cutoff_entry.get())
            order = int(self.order_entry.get())
            ftype = self.filter_type.get()
            design = self.filter_design.get()

            data_g = self.app.data / cal
            nyq = fs / 2

            # Get high cutoff for bandpass/bandstop
            fc_high = float(self.cutoff_high_entry.get()) if ftype in ['bandpass', 'bandstop'] else None

            # Design filter
            b, a = SignalProcessor.design_filter(
                fs, fc, order, ftype, design, fc_high
            )

            # Apply filter
            self.filtered_data = SignalProcessor.apply_filter(data_g, b, a)
            self.app.filtered_data = self.filtered_data

            # Get frequency response
            freq_hz, freq_response, _ = SignalProcessor.get_filter_response(b, a, fs)

            # FFT comparison
            N = len(data_g)
            fft_orig = np.abs(np.fft.fft(data_g))[:N // 2]
            fft_filt = np.abs(np.fft.fft(self.filtered_data))[:N // 2]
            freqs_fft = np.fft.fftfreq(N, 1 / fs)[:N // 2]

            # Create plot
            time = np.arange(N) / fs
            filter_info = f"{design.upper()} {ftype.upper()} Order={order} Fc={fc}Hz"

            fig = InteractivePlotter.create_filter_comparison_plot(
                time, data_g, self.filtered_data,
                freq_response, freq_hz,
                freqs_fft, fft_orig, fft_filt,
                filter_info
            )

            # Save to temp file
            self.filter_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.filter_plot_html)

            self.filter_plot_btn.configure(state="normal")
            self.filter_info_label.configure(text=f"{filter_info} applied successfully!")
            self.filter_plot_status.configure(text="Filter applied! Click button above to view comparison.")

            self.app.update_status(f"Filter applied: {filter_info}")

        except Exception as e:
            self.app.show_error(f"Filtering failed:\n{str(e)}")

    def open_filter_plot_browser(self):
        """Open filter analysis plot in browser."""
        if self.filter_plot_html:
            webbrowser.open('file://' + self.filter_plot_html)
