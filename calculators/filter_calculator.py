"""
Filter calculator for RC, RL, and RLC circuits.
Calculate cutoff frequencies, component values, and frequency responses.
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum


class FilterType(Enum):
    """Filter topology types."""
    RC_LOWPASS = "RC Low-Pass"
    RC_HIGHPASS = "RC High-Pass"
    RL_LOWPASS = "RL Low-Pass"
    RL_HIGHPASS = "RL High-Pass"
    RLC_LOWPASS = "RLC Low-Pass"
    RLC_HIGHPASS = "RLC High-Pass"
    RLC_BANDPASS = "RLC Band-Pass"
    SALLEN_KEY_LOWPASS = "Sallen-Key Low-Pass"
    TWIN_T_NOTCH = "Twin-T Notch"


@dataclass
class FilterResult:
    """Results from filter calculation."""
    filter_type: str
    cutoff_frequency: float
    resistance: float
    capacitance: Optional[float]
    inductance: Optional[float]
    time_constant: float
    q_factor: Optional[float]
    bandwidth: Optional[float]
    rolloff_db_decade: float


class FilterCalculator:
    """
    Calculator for analog filter circuits.

    Supports:
    - RC low-pass and high-pass filters
    - RL low-pass and high-pass filters
    - RLC filters (low-pass, high-pass, band-pass)
    - Active filters (Sallen-Key)
    - Notch filters (Twin-T)
    """

    # ==================== RC FILTERS ====================

    @staticmethod
    def rc_cutoff_frequency(r: float, c: float) -> float:
        """
        Calculate RC filter cutoff frequency.

        fc = 1 / (2 * pi * R * C)

        Args:
            r: Resistance in Ohms
            c: Capacitance in Farads

        Returns:
            Cutoff frequency in Hz
        """
        return 1 / (2 * np.pi * r * c)

    @staticmethod
    def rc_resistance(fc: float, c: float) -> float:
        """
        Calculate resistance for desired cutoff frequency.

        R = 1 / (2 * pi * fc * C)

        Args:
            fc: Cutoff frequency in Hz
            c: Capacitance in Farads

        Returns:
            Resistance in Ohms
        """
        return 1 / (2 * np.pi * fc * c)

    @staticmethod
    def rc_capacitance(fc: float, r: float) -> float:
        """
        Calculate capacitance for desired cutoff frequency.

        C = 1 / (2 * pi * fc * R)

        Args:
            fc: Cutoff frequency in Hz
            r: Resistance in Ohms

        Returns:
            Capacitance in Farads
        """
        return 1 / (2 * np.pi * fc * r)

    @staticmethod
    def rc_time_constant(r: float, c: float) -> float:
        """
        Calculate RC time constant.

        tau = R * C

        Args:
            r: Resistance in Ohms
            c: Capacitance in Farads

        Returns:
            Time constant in seconds
        """
        return r * c

    @staticmethod
    def rc_frequency_response(
        r: float,
        c: float,
        frequencies: np.ndarray,
        filter_type: str = 'lowpass'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate RC filter frequency response.

        Args:
            r: Resistance in Ohms
            c: Capacitance in Farads
            frequencies: Frequency array in Hz
            filter_type: 'lowpass' or 'highpass'

        Returns:
            Tuple of (magnitude in dB, phase in degrees)
        """
        omega = 2 * np.pi * frequencies
        tau = r * c

        if filter_type == 'lowpass':
            # H(jw) = 1 / (1 + jw*tau)
            h = 1 / (1 + 1j * omega * tau)
        else:  # highpass
            # H(jw) = jw*tau / (1 + jw*tau)
            h = (1j * omega * tau) / (1 + 1j * omega * tau)

        magnitude_db = 20 * np.log10(np.abs(h))
        phase_deg = np.angle(h, deg=True)

        return magnitude_db, phase_deg

    # ==================== RL FILTERS ====================

    @staticmethod
    def rl_cutoff_frequency(r: float, l: float) -> float:
        """
        Calculate RL filter cutoff frequency.

        fc = R / (2 * pi * L)

        Args:
            r: Resistance in Ohms
            l: Inductance in Henries

        Returns:
            Cutoff frequency in Hz
        """
        return r / (2 * np.pi * l)

    @staticmethod
    def rl_resistance(fc: float, l: float) -> float:
        """
        Calculate resistance for desired cutoff frequency.

        R = 2 * pi * fc * L

        Args:
            fc: Cutoff frequency in Hz
            l: Inductance in Henries

        Returns:
            Resistance in Ohms
        """
        return 2 * np.pi * fc * l

    @staticmethod
    def rl_inductance(fc: float, r: float) -> float:
        """
        Calculate inductance for desired cutoff frequency.

        L = R / (2 * pi * fc)

        Args:
            fc: Cutoff frequency in Hz
            r: Resistance in Ohms

        Returns:
            Inductance in Henries
        """
        return r / (2 * np.pi * fc)

    @staticmethod
    def rl_time_constant(r: float, l: float) -> float:
        """
        Calculate RL time constant.

        tau = L / R

        Args:
            r: Resistance in Ohms
            l: Inductance in Henries

        Returns:
            Time constant in seconds
        """
        return l / r

    # ==================== RLC FILTERS ====================

    @staticmethod
    def rlc_resonant_frequency(l: float, c: float) -> float:
        """
        Calculate RLC resonant frequency.

        f0 = 1 / (2 * pi * sqrt(L * C))

        Args:
            l: Inductance in Henries
            c: Capacitance in Farads

        Returns:
            Resonant frequency in Hz
        """
        return 1 / (2 * np.pi * np.sqrt(l * c))

    @staticmethod
    def rlc_q_factor(r: float, l: float, c: float) -> float:
        """
        Calculate RLC Q factor (quality factor).

        Q = (1/R) * sqrt(L/C)

        Args:
            r: Resistance in Ohms
            l: Inductance in Henries
            c: Capacitance in Farads

        Returns:
            Q factor
        """
        return (1 / r) * np.sqrt(l / c)

    @staticmethod
    def rlc_bandwidth(f0: float, q: float) -> float:
        """
        Calculate RLC bandwidth.

        BW = f0 / Q

        Args:
            f0: Resonant frequency in Hz
            q: Q factor

        Returns:
            Bandwidth in Hz
        """
        return f0 / q

    @staticmethod
    def rlc_damping_ratio(r: float, l: float, c: float) -> float:
        """
        Calculate RLC damping ratio.

        zeta = R * sqrt(C / L) / 2

        Args:
            r: Resistance in Ohms
            l: Inductance in Henries
            c: Capacitance in Farads

        Returns:
            Damping ratio
        """
        return r * np.sqrt(c / l) / 2

    @staticmethod
    def rlc_components_for_frequency(
        f0: float,
        q: float,
        r: float
    ) -> Tuple[float, float]:
        """
        Calculate L and C for desired frequency and Q with given R.

        Args:
            f0: Desired resonant frequency in Hz
            q: Desired Q factor
            r: Resistance in Ohms

        Returns:
            Tuple of (Inductance in H, Capacitance in F)
        """
        # From Q = (1/R) * sqrt(L/C) and f0 = 1/(2*pi*sqrt(LC))
        omega0 = 2 * np.pi * f0
        l = (q * r) / omega0
        c = 1 / (omega0 ** 2 * l)
        return l, c

    # ==================== SALLEN-KEY FILTER ====================

    @staticmethod
    def sallen_key_lowpass(
        fc: float,
        q: float = 0.707,
        c1: Optional[float] = None
    ) -> Tuple[float, float, float, float]:
        """
        Calculate Sallen-Key low-pass filter components.
        Assumes equal resistors (R1 = R2).

        Args:
            fc: Cutoff frequency in Hz
            q: Q factor (0.707 for Butterworth)
            c1: Capacitor C1 value (if None, use standard value)

        Returns:
            Tuple of (R1, R2, C1, C2)
        """
        if c1 is None:
            c1 = 10e-9  # 10nF default

        omega = 2 * np.pi * fc

        # For equal R design:
        # C2 = C1 / (4 * Q^2)
        c2 = c1 / (4 * q ** 2)

        # R = 1 / (omega * sqrt(C1 * C2))
        r = 1 / (omega * np.sqrt(c1 * c2))

        return r, r, c1, c2

    @staticmethod
    def sallen_key_q(c1: float, c2: float) -> float:
        """
        Calculate Q factor from Sallen-Key capacitor ratio.

        Q = 0.5 * sqrt(C1/C2)

        Args:
            c1: Capacitor C1 in Farads
            c2: Capacitor C2 in Farads

        Returns:
            Q factor
        """
        return 0.5 * np.sqrt(c1 / c2)

    # ==================== TWIN-T NOTCH FILTER ====================

    @staticmethod
    def twin_t_notch_frequency(r: float, c: float) -> float:
        """
        Calculate Twin-T notch filter frequency.

        fn = 1 / (2 * pi * R * C)

        Args:
            r: Resistance in Ohms
            c: Capacitance in Farads

        Returns:
            Notch frequency in Hz
        """
        return 1 / (2 * np.pi * r * c)

    @staticmethod
    def twin_t_components(fn: float, r: Optional[float] = None, c: Optional[float] = None) -> Tuple[float, float]:
        """
        Calculate Twin-T components for desired notch frequency.

        Args:
            fn: Notch frequency in Hz
            r: Resistance (if specified)
            c: Capacitance (if specified)

        Returns:
            Tuple of (R, C) - R/2 and 2C used in T networks
        """
        if r is not None:
            c = 1 / (2 * np.pi * fn * r)
        elif c is not None:
            r = 1 / (2 * np.pi * fn * c)
        else:
            # Default to 10k resistor
            r = 10000
            c = 1 / (2 * np.pi * fn * r)

        return r, c

    # ==================== UTILITY FUNCTIONS ====================

    @staticmethod
    def calculate_filter(
        filter_type: FilterType,
        **kwargs
    ) -> FilterResult:
        """
        Universal filter calculator.

        Args:
            filter_type: Type of filter
            **kwargs: Filter-specific parameters

        Returns:
            FilterResult with calculation results
        """
        calc = FilterCalculator

        if filter_type in [FilterType.RC_LOWPASS, FilterType.RC_HIGHPASS]:
            r = kwargs.get('r')
            c = kwargs.get('c')
            fc = kwargs.get('fc')

            # Solve for missing parameter
            if fc is None:
                fc = calc.rc_cutoff_frequency(r, c)
            elif r is None:
                r = calc.rc_resistance(fc, c)
            elif c is None:
                c = calc.rc_capacitance(fc, r)

            tau = calc.rc_time_constant(r, c)

            return FilterResult(
                filter_type=filter_type.value,
                cutoff_frequency=fc,
                resistance=r,
                capacitance=c,
                inductance=None,
                time_constant=tau,
                q_factor=None,
                bandwidth=None,
                rolloff_db_decade=-20 if 'LOWPASS' in filter_type.value else 20
            )

        elif filter_type in [FilterType.RL_LOWPASS, FilterType.RL_HIGHPASS]:
            r = kwargs.get('r')
            l = kwargs.get('l')
            fc = kwargs.get('fc')

            if fc is None:
                fc = calc.rl_cutoff_frequency(r, l)
            elif r is None:
                r = calc.rl_resistance(fc, l)
            elif l is None:
                l = calc.rl_inductance(fc, r)

            tau = calc.rl_time_constant(r, l)

            return FilterResult(
                filter_type=filter_type.value,
                cutoff_frequency=fc,
                resistance=r,
                capacitance=None,
                inductance=l,
                time_constant=tau,
                q_factor=None,
                bandwidth=None,
                rolloff_db_decade=-20 if 'LOWPASS' in filter_type.value else 20
            )

        elif filter_type in [FilterType.RLC_LOWPASS, FilterType.RLC_HIGHPASS, FilterType.RLC_BANDPASS]:
            r = kwargs.get('r')
            l = kwargs.get('l')
            c = kwargs.get('c')

            f0 = calc.rlc_resonant_frequency(l, c)
            q = calc.rlc_q_factor(r, l, c)
            bw = calc.rlc_bandwidth(f0, q)
            zeta = calc.rlc_damping_ratio(r, l, c)

            return FilterResult(
                filter_type=filter_type.value,
                cutoff_frequency=f0,
                resistance=r,
                capacitance=c,
                inductance=l,
                time_constant=l / r,
                q_factor=q,
                bandwidth=bw,
                rolloff_db_decade=-40 if 'LOWPASS' in filter_type.value else 40
            )

        else:
            raise ValueError(f"Unsupported filter type: {filter_type}")

    @staticmethod
    def standard_capacitor_values() -> List[float]:
        """
        Return list of standard E12 capacitor values (in Farads).

        Returns:
            List of capacitor values
        """
        e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
        values = []
        for exp in range(-12, -5):  # pF to uF range
            for val in e12:
                values.append(val * 10 ** exp)
        return values

    @staticmethod
    def standard_resistor_values() -> List[float]:
        """
        Return list of standard E24 resistor values (in Ohms).

        Returns:
            List of resistor values
        """
        e24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
               3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
        values = []
        for exp in range(0, 7):  # 1 Ohm to 10M range
            for val in e24:
                values.append(val * 10 ** exp)
        return values

    @staticmethod
    def find_nearest_standard(value: float, standard_values: List[float]) -> float:
        """
        Find nearest standard value.

        Args:
            value: Desired value
            standard_values: List of standard values

        Returns:
            Nearest standard value
        """
        return min(standard_values, key=lambda x: abs(x - value))

    @staticmethod
    def format_value_with_prefix(value: float, unit: str) -> str:
        """
        Format value with SI prefix.

        Args:
            value: Numerical value
            unit: Base unit string

        Returns:
            Formatted string
        """
        prefixes = [
            (1e12, 'T'), (1e9, 'G'), (1e6, 'M'), (1e3, 'k'),
            (1, ''), (1e-3, 'm'), (1e-6, 'u'), (1e-9, 'n'), (1e-12, 'p'),
        ]

        for threshold, prefix in prefixes:
            if abs(value) >= threshold:
                return f"{value / threshold:.4f} {prefix}{unit}"

        return f"{value:.6e} {unit}"

    @staticmethod
    def format_results(result: FilterResult) -> str:
        """
        Format calculation results as string.

        Args:
            result: FilterResult object

        Returns:
            Formatted string
        """
        fmt = FilterCalculator.format_value_with_prefix

        lines = [
            f"FILTER CALCULATION RESULTS",
            f"=" * 45,
            f"Filter Type: {result.filter_type}",
            f"",
            f"Cutoff Frequency: {fmt(result.cutoff_frequency, 'Hz')}",
            f"Resistance: {fmt(result.resistance, 'Ohms')}",
        ]

        if result.capacitance is not None:
            lines.append(f"Capacitance: {fmt(result.capacitance, 'F')}")

        if result.inductance is not None:
            lines.append(f"Inductance: {fmt(result.inductance, 'H')}")

        lines.append(f"")
        lines.append(f"Time Constant: {fmt(result.time_constant, 's')}")

        if result.q_factor is not None:
            lines.append(f"Q Factor: {result.q_factor:.4f}")

        if result.bandwidth is not None:
            lines.append(f"Bandwidth: {fmt(result.bandwidth, 'Hz')}")

        lines.append(f"Rolloff: {result.rolloff_db_decade} dB/decade")

        return "\n".join(lines)
