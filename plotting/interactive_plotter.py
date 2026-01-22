"""
Interactive plotting utilities using Plotly.
"""

import numpy as np
from scipy import signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, Optional

from ..core.config import COLORS, PLOT_CONFIG


class InteractivePlotter:
    """Create interactive Plotly plots."""

    @staticmethod
    def create_time_frequency_plot(
        time: np.ndarray,
        data: np.ndarray,
        frequencies: np.ndarray,
        psd: np.ndarray,
        resonance_freq: float,
        title: str = "Signal Analysis"
    ) -> go.Figure:
        """
        Create interactive time and frequency domain plots.

        Args:
            time: Time array
            data: Signal data
            frequencies: Frequency array
            psd: Power spectral density
            resonance_freq: Detected resonance frequency
            title: Plot title

        Returns:
            Plotly Figure object
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Time Domain Signal', 'Frequency Domain (FFT)'),
            vertical_spacing=0.12
        )

        # Time domain
        fig.add_trace(
            go.Scattergl(
                x=time, y=data,
                mode='lines',
                name='Signal',
                line=dict(color=COLORS['accent_green'], width=1),
                hovertemplate='Time: %{x:.4f}s<br>Amplitude: %{y:.4f}g<extra></extra>'
            ),
            row=1, col=1
        )

        # Frequency domain
        fig.add_trace(
            go.Scattergl(
                x=frequencies, y=psd,
                mode='lines',
                name='PSD',
                line=dict(color=COLORS['accent_red'], width=1),
                hovertemplate='Frequency: %{x:.2f}Hz<br>Power: %{y:.2e}<extra></extra>'
            ),
            row=2, col=1
        )

        # Add resonance line
        fig.add_vline(
            x=resonance_freq, row=2, col=1,
            line=dict(color=COLORS['accent_green'], width=2, dash='dash'),
            annotation_text=f"Peak: {resonance_freq:.2f} Hz",
            annotation_position="top"
        )

        # Update layout
        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            font=dict(color=COLORS['text_white'], size=12),
            title=dict(text=title, font=dict(size=18, color=COLORS['accent_red'])),
            showlegend=True,
            legend=dict(x=0.85, y=0.98),
            height=PLOT_CONFIG['height'],
            margin=dict(l=60, r=40, t=80, b=60),
            dragmode='zoom',
            hovermode='x unified'
        )

        # Update axes
        fig.update_xaxes(title_text="Time (s)", row=1, col=1, gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Acceleration (g)", row=1, col=1, gridcolor='#2a2a4a', showgrid=True)
        fig.update_xaxes(title_text="Frequency (Hz)", row=2, col=1, gridcolor='#2a2a4a', showgrid=True,
                        range=[0, PLOT_CONFIG['freq_range_max']])
        fig.update_yaxes(title_text="Power Spectral Density", row=2, col=1, gridcolor='#2a2a4a', showgrid=True)

        # Add modebar buttons for interaction
        fig.update_layout(
            modebar=dict(
                bgcolor=COLORS['bg_medium'],
                color=COLORS['text_gray'],
                activecolor=COLORS['accent_green']
            )
        )

        return fig

    @staticmethod
    def create_filter_comparison_plot(
        time: np.ndarray,
        original: np.ndarray,
        filtered: np.ndarray,
        freq_response: np.ndarray,
        freq_hz: np.ndarray,
        freqs_fft: np.ndarray,
        fft_orig: np.ndarray,
        fft_filt: np.ndarray,
        filter_info: str
    ) -> go.Figure:
        """
        Create interactive filter comparison plots.

        Args:
            time: Time array
            original: Original signal
            filtered: Filtered signal
            freq_response: Filter frequency response
            freq_hz: Frequency array for response
            freqs_fft: FFT frequency array
            fft_orig: Original FFT
            fft_filt: Filtered FFT
            filter_info: Filter description string

        Returns:
            Plotly Figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Original Signal', 'Filtered Signal',
                'Filter Frequency Response', 'FFT Comparison'
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )

        # Original signal
        fig.add_trace(
            go.Scattergl(x=time, y=original, mode='lines', name='Original',
                        line=dict(color=COLORS['accent_red'], width=1)),
            row=1, col=1
        )

        # Filtered signal
        fig.add_trace(
            go.Scattergl(x=time, y=filtered, mode='lines', name='Filtered',
                        line=dict(color=COLORS['accent_green'], width=1)),
            row=1, col=2
        )

        # Filter frequency response
        fig.add_trace(
            go.Scatter(x=freq_hz, y=freq_response, mode='lines', name='Response',
                      line=dict(color=COLORS['accent_yellow'], width=2)),
            row=2, col=1
        )

        # FFT comparison
        fig.add_trace(
            go.Scattergl(x=freqs_fft, y=fft_orig, mode='lines', name='Original FFT',
                        line=dict(color=COLORS['accent_red'], width=1), opacity=0.7),
            row=2, col=2
        )
        fig.add_trace(
            go.Scattergl(x=freqs_fft, y=fft_filt, mode='lines', name='Filtered FFT',
                        line=dict(color=COLORS['accent_green'], width=1)),
            row=2, col=2
        )

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            font=dict(color=COLORS['text_white'], size=11),
            title=dict(text=f"Digital Filter Analysis - {filter_info}",
                      font=dict(size=16, color=COLORS['accent_green'])),
            height=650,
            showlegend=True,
            dragmode='zoom'
        )

        # Update all axes
        fig.update_xaxes(gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(gridcolor='#2a2a4a', showgrid=True)

        fig.update_xaxes(title_text="Time (s)", row=1, col=1)
        fig.update_xaxes(title_text="Time (s)", row=1, col=2)
        fig.update_xaxes(title_text="Frequency (Hz)", row=2, col=1)
        fig.update_xaxes(title_text="Frequency (Hz)", row=2, col=2, range=[0, PLOT_CONFIG['freq_range_max']])

        fig.update_yaxes(title_text="Amplitude (g)", row=1, col=1)
        fig.update_yaxes(title_text="Amplitude (g)", row=1, col=2)
        fig.update_yaxes(title_text="Magnitude (dB)", row=2, col=1, range=[-60, 5])
        fig.update_yaxes(title_text="Magnitude", row=2, col=2)

        return fig

    @staticmethod
    def create_spectrogram(
        data: np.ndarray,
        fs: float,
        title: str = "Spectrogram"
    ) -> go.Figure:
        """
        Create interactive spectrogram.

        Args:
            data: Signal data
            fs: Sampling frequency
            title: Plot title

        Returns:
            Plotly Figure object
        """
        f, t, Sxx = signal.spectrogram(
            data, fs,
            nperseg=PLOT_CONFIG['spectrogram_nperseg'],
            noverlap=PLOT_CONFIG['spectrogram_noverlap']
        )

        fig = go.Figure(data=go.Heatmap(
            z=10 * np.log10(Sxx + 1e-10),
            x=t,
            y=f,
            colorscale='Plasma',
            colorbar=dict(title='Power (dB)')
        ))

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            font=dict(color=COLORS['text_white']),
            title=dict(text=title, font=dict(size=18, color=COLORS['accent_green'])),
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            height=500,
            yaxis=dict(range=[0, min(PLOT_CONFIG['freq_range_max'], fs / 2)])
        )

        return fig

    @staticmethod
    def create_psd_welch(
        data: np.ndarray,
        fs: float,
        title: str = "Power Spectral Density (Welch)"
    ) -> Tuple[go.Figure, float]:
        """
        Create PSD plot using Welch method.

        Args:
            data: Signal data
            fs: Sampling frequency
            title: Plot title

        Returns:
            Tuple of (Plotly Figure, peak frequency)
        """
        f, Pxx = signal.welch(data, fs, nperseg=PLOT_CONFIG['welch_nperseg'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=f, y=Pxx,
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(78, 204, 163, 0.3)',
            line=dict(color=COLORS['accent_green'], width=2),
            hovertemplate='Frequency: %{x:.2f}Hz<br>PSD: %{y:.2e} g2/Hz<extra></extra>'
        ))

        # Mark peak
        peak_idx = np.argmax(Pxx)
        fig.add_annotation(
            x=f[peak_idx], y=Pxx[peak_idx],
            text=f"Peak: {f[peak_idx]:.2f} Hz",
            showarrow=True,
            arrowhead=2,
            arrowcolor=COLORS['accent_red'],
            font=dict(color=COLORS['text_white'])
        )

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            font=dict(color=COLORS['text_white']),
            title=dict(text=title, font=dict(size=18, color=COLORS['accent_green'])),
            xaxis_title="Frequency (Hz)",
            yaxis_title="PSD (g2/Hz)",
            yaxis_type="log",
            height=500,
            xaxis=dict(range=[0, min(PLOT_CONFIG['freq_range_max'], fs / 2)], gridcolor='#2a2a4a'),
            yaxis=dict(gridcolor='#2a2a4a')
        )

        return fig, f[peak_idx]

    @staticmethod
    def create_histogram(
        data: np.ndarray,
        title: str = "Amplitude Distribution",
        nbins: int = 100
    ) -> go.Figure:
        """
        Create histogram plot.

        Args:
            data: Data array
            title: Plot title
            nbins: Number of bins

        Returns:
            Plotly Figure object
        """
        mean_val = np.mean(data)

        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data, nbinsx=nbins,
            marker_color=COLORS['accent_green'],
            opacity=0.7
        ))
        fig.add_vline(
            x=mean_val, line_dash="dash",
            line_color=COLORS['accent_red'],
            annotation_text=f"Mean: {mean_val:.4f}"
        )

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            title=title,
            xaxis_title="Amplitude (g)",
            yaxis_title="Count",
            height=500
        )

        return fig

    @staticmethod
    def create_peak_detection_plot(
        freqs: np.ndarray,
        fft_result: np.ndarray,
        peak_freqs: np.ndarray,
        peak_values: np.ndarray,
        fs: float,
        title: str = "Peak Detection"
    ) -> go.Figure:
        """
        Create peak detection plot.

        Args:
            freqs: Frequency array
            fft_result: FFT magnitude array
            peak_freqs: Detected peak frequencies
            peak_values: Detected peak values
            fs: Sampling frequency
            title: Plot title

        Returns:
            Plotly Figure object
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=freqs, y=fft_result,
            mode='lines',
            line=dict(color=COLORS['accent_green'], width=1),
            name='FFT'
        ))
        fig.add_trace(go.Scatter(
            x=peak_freqs, y=peak_values,
            mode='markers',
            marker=dict(color=COLORS['accent_red'], size=10, symbol='triangle-up'),
            name='Peaks'
        ))

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude",
            xaxis=dict(range=[0, min(PLOT_CONFIG['freq_range_max'], fs / 2)]),
            height=500
        )

        return fig

    @staticmethod
    def create_rms_plot(
        times: np.ndarray,
        rms_values: np.ndarray,
        overall_rms: float,
        title: str = "RMS vs Time"
    ) -> go.Figure:
        """
        Create RMS analysis plot.

        Args:
            times: Time array
            rms_values: Windowed RMS values
            overall_rms: Overall RMS value
            title: Plot title

        Returns:
            Plotly Figure object
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times, y=rms_values,
            mode='lines',
            line=dict(color=COLORS['accent_red'], width=2),
            name='RMS'
        ))
        fig.add_hline(
            y=overall_rms, line_dash="dash",
            line_color=COLORS['accent_green'],
            annotation_text=f"Overall: {overall_rms:.4f} g"
        )

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            title=title,
            xaxis_title="Time (s)",
            yaxis_title="RMS (g)",
            height=500
        )

        return fig

    @staticmethod
    def create_capacitor_plot(
        time: np.ndarray,
        voltage: np.ndarray,
        current: np.ndarray,
        title: str = "Capacitor Charging/Discharging"
    ) -> go.Figure:
        """
        Create capacitor charging/discharging plot.

        Args:
            time: Time array
            voltage: Voltage array
            current: Current array
            title: Plot title

        Returns:
            Plotly Figure object
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Voltage', 'Current'),
            vertical_spacing=0.15
        )

        fig.add_trace(
            go.Scatter(x=time, y=voltage, mode='lines', name='Voltage',
                      line=dict(color=COLORS['accent_green'], width=2)),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=time, y=current, mode='lines', name='Current',
                      line=dict(color=COLORS['accent_red'], width=2)),
            row=2, col=1
        )

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            title=dict(text=title, font=dict(size=18, color=COLORS['accent_green'])),
            height=550,
            showlegend=True
        )

        fig.update_xaxes(title_text="Time (s)", gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Voltage (V)", row=1, col=1, gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Current (A)", row=2, col=1, gridcolor='#2a2a4a', showgrid=True)

        return fig

    @staticmethod
    def create_battery_discharge_plot(
        time: np.ndarray,
        voltage: np.ndarray,
        capacity_remaining: np.ndarray,
        title: str = "Battery Discharge"
    ) -> go.Figure:
        """
        Create battery discharge plot.

        Args:
            time: Time array (hours)
            voltage: Voltage array
            capacity_remaining: Remaining capacity percentage
            title: Plot title

        Returns:
            Plotly Figure object
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Voltage vs Time', 'Capacity Remaining'),
            vertical_spacing=0.15
        )

        fig.add_trace(
            go.Scatter(x=time, y=voltage, mode='lines', name='Voltage',
                      line=dict(color=COLORS['accent_yellow'], width=2)),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=time, y=capacity_remaining, mode='lines', name='Capacity',
                      line=dict(color=COLORS['accent_green'], width=2),
                      fill='tozeroy', fillcolor='rgba(78, 204, 163, 0.2)'),
            row=2, col=1
        )

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            title=dict(text=title, font=dict(size=18, color=COLORS['accent_yellow'])),
            height=550,
            showlegend=True
        )

        fig.update_xaxes(title_text="Time (hours)", gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Voltage (V)", row=1, col=1, gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Capacity (%)", row=2, col=1, gridcolor='#2a2a4a', showgrid=True,
                        range=[0, 105])

        return fig

    @staticmethod
    def create_filter_response_plot(
        frequencies: np.ndarray,
        magnitude_db: np.ndarray,
        phase_deg: np.ndarray,
        cutoff_freq: float,
        title: str = "Filter Frequency Response"
    ) -> go.Figure:
        """
        Create filter frequency response plot (Bode plot style).

        Args:
            frequencies: Frequency array
            magnitude_db: Magnitude in dB
            phase_deg: Phase in degrees
            cutoff_freq: Cutoff frequency
            title: Plot title

        Returns:
            Plotly Figure object
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Magnitude Response', 'Phase Response'),
            vertical_spacing=0.15
        )

        fig.add_trace(
            go.Scatter(x=frequencies, y=magnitude_db, mode='lines', name='Magnitude',
                      line=dict(color=COLORS['accent_green'], width=2)),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=frequencies, y=phase_deg, mode='lines', name='Phase',
                      line=dict(color=COLORS['accent_yellow'], width=2)),
            row=2, col=1
        )

        # Add cutoff frequency marker
        fig.add_vline(x=cutoff_freq, line_dash="dash", line_color=COLORS['accent_red'],
                     annotation_text=f"fc = {cutoff_freq:.2f} Hz", row=1, col=1)
        fig.add_hline(y=-3, line_dash="dot", line_color=COLORS['text_gray'],
                     annotation_text="-3 dB", row=1, col=1)

        fig.update_layout(
            template=PLOT_CONFIG['template'],
            paper_bgcolor=COLORS['bg_dark'],
            plot_bgcolor=COLORS['bg_light'],
            title=dict(text=title, font=dict(size=18, color=COLORS['accent_green'])),
            height=550,
            showlegend=True
        )

        fig.update_xaxes(title_text="Frequency (Hz)", type="log", gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Magnitude (dB)", row=1, col=1, gridcolor='#2a2a4a', showgrid=True)
        fig.update_yaxes(title_text="Phase (degrees)", row=2, col=1, gridcolor='#2a2a4a', showgrid=True)

        return fig
