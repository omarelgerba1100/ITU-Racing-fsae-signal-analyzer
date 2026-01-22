"""
Signal processing utilities for FSAE analysis.
"""

import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftfreq
from typing import Tuple, Dict, List, Optional


class SignalProcessor:
    """Signal processing utilities."""

    @staticmethod
    def perform_fft(
        data: np.ndarray,
        fs: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform FFT analysis on signal.

        Args:
            data: Signal data
            fs: Sampling frequency

        Returns:
            Tuple of (positive frequencies, FFT magnitude, PSD)
        """
        N = len(data)
        dt = 1 / fs

        fft_result = np.fft.fft(data)
        frequencies = np.fft.fftfreq(N, dt)

        pos_idx = frequencies > 0
        freq_pos = frequencies[pos_idx]
        magnitude = np.abs(fft_result[pos_idx])
        psd = magnitude ** 2

        return freq_pos, magnitude, psd

    @staticmethod
    def find_resonance(
        frequencies: np.ndarray,
        psd: np.ndarray,
        round_to: int = 5
    ) -> Tuple[float, float]:
        """
        Find resonance frequency from PSD.

        Args:
            frequencies: Frequency array
            psd: Power spectral density
            round_to: Round frequency to nearest value

        Returns:
            Tuple of (exact resonance frequency, rounded resonance frequency)
        """
        peak_idx = np.argmax(psd)
        resonance_freq = frequencies[peak_idx]
        resonance_rounded = round(resonance_freq / round_to) * round_to
        return resonance_freq, resonance_rounded

    @staticmethod
    def find_top_peaks(
        frequencies: np.ndarray,
        psd: np.ndarray,
        n_peaks: int = 5
    ) -> List[Tuple[float, float]]:
        """
        Find top N frequency peaks.

        Args:
            frequencies: Frequency array
            psd: Power spectral density
            n_peaks: Number of peaks to find

        Returns:
            List of (frequency, power) tuples
        """
        top_idx = np.argsort(psd)[-n_peaks:][::-1]
        return [(frequencies[idx], psd[idx]) for idx in top_idx]

    @staticmethod
    def design_filter(
        fs: float,
        fc: float,
        order: int,
        filter_type: str = 'lowpass',
        design: str = 'butter',
        fc_high: Optional[float] = None,
        ripple: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Design a digital filter.

        Args:
            fs: Sampling frequency
            fc: Cutoff frequency (low)
            order: Filter order
            filter_type: 'lowpass', 'highpass', 'bandpass', 'bandstop'
            design: 'butter', 'cheby1', 'bessel'
            fc_high: High cutoff for bandpass/bandstop
            ripple: Ripple for Chebyshev filter

        Returns:
            Tuple of (b, a) filter coefficients
        """
        nyq = fs / 2

        if filter_type in ['bandpass', 'bandstop']:
            if fc_high is None:
                fc_high = fc * 2
            Wn = [fc / nyq, fc_high / nyq]
        else:
            Wn = fc / nyq

        if design == 'butter':
            b, a = signal.butter(order, Wn, btype=filter_type)
        elif design == 'cheby1':
            b, a = signal.cheby1(order, ripple, Wn, btype=filter_type)
        elif design == 'bessel':
            b, a = signal.bessel(order, Wn, btype=filter_type)
        else:
            raise ValueError(f"Unknown filter design: {design}")

        return b, a

    @staticmethod
    def apply_filter(
        data: np.ndarray,
        b: np.ndarray,
        a: np.ndarray
    ) -> np.ndarray:
        """
        Apply filter to signal using filtfilt (zero-phase).

        Args:
            data: Signal data
            b: Filter numerator coefficients
            a: Filter denominator coefficients

        Returns:
            Filtered signal
        """
        return signal.filtfilt(b, a, data)

    @staticmethod
    def get_filter_response(
        b: np.ndarray,
        a: np.ndarray,
        fs: float,
        worN: int = 2000
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get filter frequency response.

        Args:
            b: Filter numerator coefficients
            a: Filter denominator coefficients
            fs: Sampling frequency
            worN: Number of frequency points

        Returns:
            Tuple of (frequency Hz, magnitude dB, phase degrees)
        """
        nyq = fs / 2
        w, h = signal.freqz(b, a, worN=worN)
        freq_hz = (w / np.pi) * nyq
        magnitude_db = 20 * np.log10(np.abs(h) + 1e-10)
        phase_deg = np.angle(h, deg=True)
        return freq_hz, magnitude_db, phase_deg

    @staticmethod
    def compute_statistics(data: np.ndarray, fs: float) -> Dict[str, float]:
        """
        Compute signal statistics.

        Args:
            data: Signal data
            fs: Sampling frequency

        Returns:
            Dictionary of statistics
        """
        return {
            'points': len(data),
            'duration': len(data) / fs,
            'mean': np.mean(data),
            'std': np.std(data),
            'rms': np.sqrt(np.mean(data ** 2)),
            'min': np.min(data),
            'max': np.max(data),
            'peak_to_peak': np.ptp(data),
            'crest_factor': np.max(np.abs(data)) / np.sqrt(np.mean(data ** 2))
        }

    @staticmethod
    def detect_peaks(
        data: np.ndarray,
        fs: float,
        height_ratio: float = 0.05,
        distance: int = 10,
        n_peaks: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect frequency peaks in signal.

        Args:
            data: Signal data
            fs: Sampling frequency
            height_ratio: Minimum height as ratio of max
            distance: Minimum distance between peaks
            n_peaks: Number of top peaks to return

        Returns:
            Tuple of (peak frequencies, peak magnitudes)
        """
        N = len(data)
        fft_result = np.abs(np.fft.fft(data))[:N // 2]
        freqs = np.fft.fftfreq(N, 1 / fs)[:N // 2]

        peaks, properties = signal.find_peaks(
            fft_result,
            height=np.max(fft_result) * height_ratio,
            distance=distance
        )

        sorted_idx = np.argsort(properties['peak_heights'])[::-1]
        top_peaks = peaks[sorted_idx[:n_peaks]]

        return freqs[top_peaks], fft_result[top_peaks]

    @staticmethod
    def compute_rms_windowed(
        data: np.ndarray,
        fs: float,
        window_seconds: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Compute windowed RMS values.

        Args:
            data: Signal data
            fs: Sampling frequency
            window_seconds: Window size in seconds

        Returns:
            Tuple of (time array, RMS values, overall RMS)
        """
        window_size = int(fs * window_seconds)
        n_windows = len(data) // window_size

        rms_values = []
        times = []

        for i in range(n_windows):
            window = data[i * window_size:(i + 1) * window_size]
            rms_values.append(np.sqrt(np.mean(window ** 2)))
            times.append((i + 0.5) * window_size / fs)

        overall_rms = np.sqrt(np.mean(data ** 2))

        return np.array(times), np.array(rms_values), overall_rms

    @staticmethod
    def compute_spectrogram(
        data: np.ndarray,
        fs: float,
        nperseg: int = 256,
        noverlap: int = 128
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute spectrogram.

        Args:
            data: Signal data
            fs: Sampling frequency
            nperseg: Samples per segment
            noverlap: Overlap samples

        Returns:
            Tuple of (frequencies, times, Sxx power)
        """
        f, t, Sxx = signal.spectrogram(data, fs, nperseg=nperseg, noverlap=noverlap)
        return f, t, Sxx

    @staticmethod
    def compute_psd_welch(
        data: np.ndarray,
        fs: float,
        nperseg: int = 1024
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute PSD using Welch method.

        Args:
            data: Signal data
            fs: Sampling frequency
            nperseg: Samples per segment

        Returns:
            Tuple of (frequencies, PSD)
        """
        return signal.welch(data, fs, nperseg=nperseg)
