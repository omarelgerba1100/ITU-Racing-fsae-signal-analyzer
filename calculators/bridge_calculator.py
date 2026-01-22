"""
Bridge circuit calculators.
Supports Wheatstone, Wien, Maxwell, and other bridge types.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class BridgeType(Enum):
    """Types of bridge circuits."""
    WHEATSTONE = "Wheatstone Bridge"
    WIEN = "Wien Bridge"
    MAXWELL = "Maxwell Bridge"
    SCHERING = "Schering Bridge"
    ANDERSON = "Anderson Bridge"
    KELVIN = "Kelvin Double Bridge"


@dataclass
class BridgeResult:
    """Results from bridge calculation."""
    bridge_type: str
    is_balanced: bool
    unknown_value: float
    unknown_unit: str
    balance_condition: str
    sensitivity: float
    output_voltage: float


class BridgeCalculator:
    """
    Calculator for various bridge circuits.

    Supports:
    - Wheatstone Bridge (resistance measurement)
    - Wien Bridge (frequency/capacitance measurement)
    - Maxwell Bridge (inductance measurement)
    - Schering Bridge (capacitance measurement)
    """

    # ==================== WHEATSTONE BRIDGE ====================

    @staticmethod
    def wheatstone_resistance(
        r1: float,
        r2: float,
        r3: float
    ) -> float:
        """
        Calculate unknown resistance in Wheatstone bridge.

        At balance: R1/R2 = R3/Rx
        Therefore: Rx = R3 * R2 / R1

        Args:
            r1: Known resistance R1 (Ohms)
            r2: Known resistance R2 (Ohms)
            r3: Known resistance R3 (Ohms)

        Returns:
            Unknown resistance Rx (Ohms)
        """
        return r3 * r2 / r1

    @staticmethod
    def wheatstone_output_voltage(
        r1: float,
        r2: float,
        r3: float,
        rx: float,
        vs: float
    ) -> float:
        """
        Calculate Wheatstone bridge output voltage.

        Vout = Vs * (Rx/(R3+Rx) - R2/(R1+R2))

        Args:
            r1: Resistance R1 (Ohms)
            r2: Resistance R2 (Ohms)
            r3: Resistance R3 (Ohms)
            rx: Resistance Rx (Ohms)
            vs: Supply voltage (V)

        Returns:
            Output voltage (V)
        """
        return vs * (rx / (r3 + rx) - r2 / (r1 + r2))

    @staticmethod
    def wheatstone_sensitivity(
        r1: float,
        r2: float,
        r3: float,
        rx: float,
        vs: float
    ) -> float:
        """
        Calculate Wheatstone bridge sensitivity.

        S = dVout/dRx at balance point

        Args:
            r1, r2, r3, rx: Resistances (Ohms)
            vs: Supply voltage (V)

        Returns:
            Sensitivity (V/Ohm)
        """
        return vs * r3 / ((r3 + rx) ** 2)

    @staticmethod
    def wheatstone_balance_check(
        r1: float,
        r2: float,
        r3: float,
        rx: float,
        tolerance: float = 0.001
    ) -> bool:
        """
        Check if Wheatstone bridge is balanced.

        Args:
            r1, r2, r3, rx: Resistances (Ohms)
            tolerance: Balance tolerance

        Returns:
            True if balanced
        """
        ratio_diff = abs(r1 / r2 - r3 / rx)
        return ratio_diff < tolerance

    # ==================== WIEN BRIDGE ====================

    @staticmethod
    def wien_frequency(
        r: float,
        c: float
    ) -> float:
        """
        Calculate Wien bridge balance frequency.

        f = 1 / (2 * pi * R * C)

        Args:
            r: Resistance (Ohms)
            c: Capacitance (Farads)

        Returns:
            Frequency (Hz)
        """
        return 1 / (2 * np.pi * r * c)

    @staticmethod
    def wien_resistance(
        f: float,
        c: float
    ) -> float:
        """
        Calculate resistance for Wien bridge at given frequency.

        R = 1 / (2 * pi * f * C)

        Args:
            f: Frequency (Hz)
            c: Capacitance (Farads)

        Returns:
            Resistance (Ohms)
        """
        return 1 / (2 * np.pi * f * c)

    @staticmethod
    def wien_capacitance(
        f: float,
        r: float
    ) -> float:
        """
        Calculate capacitance for Wien bridge at given frequency.

        C = 1 / (2 * pi * f * R)

        Args:
            f: Frequency (Hz)
            r: Resistance (Ohms)

        Returns:
            Capacitance (Farads)
        """
        return 1 / (2 * np.pi * f * r)

    # ==================== MAXWELL BRIDGE ====================

    @staticmethod
    def maxwell_inductance(
        r1: float,
        r3: float,
        r4: float,
        c4: float
    ) -> Tuple[float, float]:
        """
        Calculate unknown inductance in Maxwell bridge.

        Lx = R1 * R3 * C4
        Rx = R1 * R3 / R4

        Args:
            r1: Resistance R1 (Ohms)
            r3: Resistance R3 (Ohms)
            r4: Resistance R4 (Ohms)
            c4: Capacitance C4 (Farads)

        Returns:
            Tuple of (Inductance Lx in Henries, Resistance Rx in Ohms)
        """
        lx = r1 * r3 * c4
        rx = r1 * r3 / r4
        return lx, rx

    @staticmethod
    def maxwell_q_factor(
        lx: float,
        rx: float,
        frequency: float
    ) -> float:
        """
        Calculate Q factor of inductor.

        Q = (2 * pi * f * L) / R

        Args:
            lx: Inductance (Henries)
            rx: Resistance (Ohms)
            frequency: Operating frequency (Hz)

        Returns:
            Q factor
        """
        return (2 * np.pi * frequency * lx) / rx

    # ==================== SCHERING BRIDGE ====================

    @staticmethod
    def schering_capacitance(
        r3: float,
        c2: float,
        r4: float
    ) -> float:
        """
        Calculate unknown capacitance in Schering bridge.

        Cx = C2 * R4 / R3

        Args:
            r3: Resistance R3 (Ohms)
            c2: Known capacitance C2 (Farads)
            r4: Resistance R4 (Ohms)

        Returns:
            Unknown capacitance Cx (Farads)
        """
        return c2 * r4 / r3

    @staticmethod
    def schering_dissipation_factor(
        c2: float,
        r3: float,
        c4: float,
        frequency: float
    ) -> float:
        """
        Calculate dissipation factor (tan delta) from Schering bridge.

        D = tan(delta) = 2 * pi * f * C4 * R3

        Args:
            c2: Capacitance C2 (Farads)
            r3: Resistance R3 (Ohms)
            c4: Capacitance C4 (Farads)
            frequency: Frequency (Hz)

        Returns:
            Dissipation factor
        """
        return 2 * np.pi * frequency * c4 * r3

    # ==================== KELVIN DOUBLE BRIDGE ====================

    @staticmethod
    def kelvin_low_resistance(
        r1: float,
        r2: float,
        r3: float,
        rs: float
    ) -> float:
        """
        Calculate unknown low resistance using Kelvin double bridge.
        Used for measuring very low resistances (milliohms).

        Rx = Rs * (R1 / R2)

        Args:
            r1: Ratio arm R1 (Ohms)
            r2: Ratio arm R2 (Ohms)
            r3: Ratio arm R3 (Ohms)
            rs: Standard resistance (Ohms)

        Returns:
            Unknown resistance Rx (Ohms)
        """
        return rs * (r1 / r2)

    # ==================== UTILITY FUNCTIONS ====================

    @staticmethod
    def calculate_bridge(
        bridge_type: BridgeType,
        **kwargs
    ) -> BridgeResult:
        """
        Universal bridge calculator.

        Args:
            bridge_type: Type of bridge circuit
            **kwargs: Parameters specific to bridge type

        Returns:
            BridgeResult with calculation results
        """
        calc = BridgeCalculator

        if bridge_type == BridgeType.WHEATSTONE:
            r1 = kwargs.get('r1', 1000)
            r2 = kwargs.get('r2', 1000)
            r3 = kwargs.get('r3', 1000)
            vs = kwargs.get('vs', 5)

            rx = calc.wheatstone_resistance(r1, r2, r3)
            vout = calc.wheatstone_output_voltage(r1, r2, r3, rx, vs)
            sens = calc.wheatstone_sensitivity(r1, r2, r3, rx, vs)

            return BridgeResult(
                bridge_type=bridge_type.value,
                is_balanced=True,
                unknown_value=rx,
                unknown_unit="Ohms",
                balance_condition=f"R1/R2 = R3/Rx ({r1/r2:.4f})",
                sensitivity=sens,
                output_voltage=vout
            )

        elif bridge_type == BridgeType.WIEN:
            r = kwargs.get('r', 1000)
            c = kwargs.get('c', 1e-6)
            solve_for = kwargs.get('solve_for', 'frequency')

            if solve_for == 'frequency':
                f = calc.wien_frequency(r, c)
                return BridgeResult(
                    bridge_type=bridge_type.value,
                    is_balanced=True,
                    unknown_value=f,
                    unknown_unit="Hz",
                    balance_condition=f"f = 1/(2*pi*R*C)",
                    sensitivity=0,
                    output_voltage=0
                )
            elif solve_for == 'resistance':
                f = kwargs.get('f', 1000)
                r_calc = calc.wien_resistance(f, c)
                return BridgeResult(
                    bridge_type=bridge_type.value,
                    is_balanced=True,
                    unknown_value=r_calc,
                    unknown_unit="Ohms",
                    balance_condition=f"R = 1/(2*pi*f*C)",
                    sensitivity=0,
                    output_voltage=0
                )
            else:  # capacitance
                f = kwargs.get('f', 1000)
                c_calc = calc.wien_capacitance(f, r)
                return BridgeResult(
                    bridge_type=bridge_type.value,
                    is_balanced=True,
                    unknown_value=c_calc,
                    unknown_unit="Farads",
                    balance_condition=f"C = 1/(2*pi*f*R)",
                    sensitivity=0,
                    output_voltage=0
                )

        elif bridge_type == BridgeType.MAXWELL:
            r1 = kwargs.get('r1', 1000)
            r3 = kwargs.get('r3', 1000)
            r4 = kwargs.get('r4', 1000)
            c4 = kwargs.get('c4', 1e-6)

            lx, rx = calc.maxwell_inductance(r1, r3, r4, c4)

            return BridgeResult(
                bridge_type=bridge_type.value,
                is_balanced=True,
                unknown_value=lx,
                unknown_unit="Henries",
                balance_condition=f"Lx = R1*R3*C4, Rx = {rx:.4f} Ohms",
                sensitivity=0,
                output_voltage=0
            )

        elif bridge_type == BridgeType.SCHERING:
            r3 = kwargs.get('r3', 1000)
            c2 = kwargs.get('c2', 1e-6)
            r4 = kwargs.get('r4', 1000)

            cx = calc.schering_capacitance(r3, c2, r4)

            return BridgeResult(
                bridge_type=bridge_type.value,
                is_balanced=True,
                unknown_value=cx,
                unknown_unit="Farads",
                balance_condition=f"Cx = C2*R4/R3",
                sensitivity=0,
                output_voltage=0
            )

        else:
            raise ValueError(f"Unsupported bridge type: {bridge_type}")

    @staticmethod
    def format_value_with_prefix(value: float, unit: str) -> str:
        """
        Format value with SI prefix.

        Args:
            value: Numerical value
            unit: Base unit string

        Returns:
            Formatted string with appropriate prefix
        """
        prefixes = [
            (1e12, 'T'),
            (1e9, 'G'),
            (1e6, 'M'),
            (1e3, 'k'),
            (1, ''),
            (1e-3, 'm'),
            (1e-6, 'u'),
            (1e-9, 'n'),
            (1e-12, 'p'),
        ]

        for threshold, prefix in prefixes:
            if abs(value) >= threshold:
                return f"{value / threshold:.4f} {prefix}{unit}"

        return f"{value:.6e} {unit}"

    @staticmethod
    def format_results(result: BridgeResult) -> str:
        """
        Format calculation results as string.

        Args:
            result: BridgeResult object

        Returns:
            Formatted string
        """
        formatted_value = BridgeCalculator.format_value_with_prefix(
            result.unknown_value, result.unknown_unit
        )

        lines = [
            f"BRIDGE CIRCUIT RESULTS",
            f"=" * 45,
            f"Bridge Type: {result.bridge_type}",
            f"",
            f"Calculated Value: {formatted_value}",
            f"Balance Condition: {result.balance_condition}",
            f"Balanced: {'Yes' if result.is_balanced else 'No'}",
        ]

        if result.sensitivity != 0:
            lines.append(f"Sensitivity: {result.sensitivity:.6e} V/Ohm")

        if result.output_voltage != 0:
            lines.append(f"Output Voltage: {result.output_voltage:.6f} V")

        return "\n".join(lines)
