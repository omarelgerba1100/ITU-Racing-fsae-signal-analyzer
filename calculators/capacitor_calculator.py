"""
Capacitor charging and discharging calculator.
Supports constant current and constant resistance modes.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CapacitorResult:
    """Results from capacitor calculation."""
    time: np.ndarray
    voltage: np.ndarray
    current: np.ndarray
    energy: np.ndarray
    tau: float  # Time constant
    charge_time_63: float  # Time to 63.2%
    charge_time_95: float  # Time to 95%
    charge_time_99: float  # Time to 99%


class CapacitorCalculator:
    """
    Calculator for capacitor charging and discharging.

    Supports:
    - Constant resistance (RC circuit) charging/discharging
    - Constant current charging/discharging
    """

    @staticmethod
    def rc_charging(
        capacitance: float,
        resistance: float,
        supply_voltage: float,
        initial_voltage: float = 0.0,
        duration_multiplier: float = 5.0,
        num_points: int = 1000
    ) -> CapacitorResult:
        """
        Calculate RC circuit charging.

        V(t) = Vs * (1 - e^(-t/tau)) + V0 * e^(-t/tau)
        I(t) = (Vs - V0) / R * e^(-t/tau)

        Args:
            capacitance: Capacitance in Farads
            resistance: Resistance in Ohms
            supply_voltage: Supply voltage in Volts
            initial_voltage: Initial capacitor voltage
            duration_multiplier: Simulate for this many time constants
            num_points: Number of time points

        Returns:
            CapacitorResult with time, voltage, current arrays
        """
        tau = resistance * capacitance
        duration = tau * duration_multiplier

        time = np.linspace(0, duration, num_points)

        # Voltage: V(t) = Vs - (Vs - V0) * e^(-t/tau)
        voltage = supply_voltage - (supply_voltage - initial_voltage) * np.exp(-time / tau)

        # Current: I(t) = (Vs - V0) / R * e^(-t/tau)
        current = (supply_voltage - initial_voltage) / resistance * np.exp(-time / tau)

        # Energy stored: E = 0.5 * C * V^2
        energy = 0.5 * capacitance * voltage ** 2

        return CapacitorResult(
            time=time,
            voltage=voltage,
            current=current,
            energy=energy,
            tau=tau,
            charge_time_63=tau,  # 63.2% at 1 tau
            charge_time_95=3 * tau,  # 95% at 3 tau
            charge_time_99=5 * tau  # 99% at 5 tau
        )

    @staticmethod
    def rc_discharging(
        capacitance: float,
        resistance: float,
        initial_voltage: float,
        duration_multiplier: float = 5.0,
        num_points: int = 1000
    ) -> CapacitorResult:
        """
        Calculate RC circuit discharging.

        V(t) = V0 * e^(-t/tau)
        I(t) = -V0 / R * e^(-t/tau)

        Args:
            capacitance: Capacitance in Farads
            resistance: Resistance in Ohms
            initial_voltage: Initial capacitor voltage
            duration_multiplier: Simulate for this many time constants
            num_points: Number of time points

        Returns:
            CapacitorResult with time, voltage, current arrays
        """
        tau = resistance * capacitance
        duration = tau * duration_multiplier

        time = np.linspace(0, duration, num_points)

        # Voltage: V(t) = V0 * e^(-t/tau)
        voltage = initial_voltage * np.exp(-time / tau)

        # Current: I(t) = -V0 / R * e^(-t/tau) (negative = discharging)
        current = -initial_voltage / resistance * np.exp(-time / tau)

        # Energy stored
        energy = 0.5 * capacitance * voltage ** 2

        return CapacitorResult(
            time=time,
            voltage=voltage,
            current=current,
            energy=energy,
            tau=tau,
            charge_time_63=tau,  # 36.8% remaining at 1 tau
            charge_time_95=3 * tau,  # 5% remaining at 3 tau
            charge_time_99=5 * tau  # 1% remaining at 5 tau
        )

    @staticmethod
    def constant_current_charging(
        capacitance: float,
        current: float,
        target_voltage: float,
        initial_voltage: float = 0.0,
        num_points: int = 1000
    ) -> CapacitorResult:
        """
        Calculate constant current charging.

        V(t) = V0 + (I * t) / C

        Args:
            capacitance: Capacitance in Farads
            current: Charging current in Amps
            target_voltage: Target voltage to stop charging
            initial_voltage: Initial capacitor voltage
            num_points: Number of time points

        Returns:
            CapacitorResult with time, voltage, current arrays
        """
        # Time to reach target voltage
        charge_time = (target_voltage - initial_voltage) * capacitance / current

        time = np.linspace(0, charge_time, num_points)

        # Voltage: V(t) = V0 + I*t/C
        voltage = initial_voltage + (current * time) / capacitance

        # Current is constant
        current_arr = np.full_like(time, current)

        # Energy stored
        energy = 0.5 * capacitance * voltage ** 2

        # Calculate equivalent RC time constant for comparison
        avg_resistance = (target_voltage - initial_voltage) / current / 2
        tau = avg_resistance * capacitance if current != 0 else 0

        return CapacitorResult(
            time=time,
            voltage=voltage,
            current=current_arr,
            energy=energy,
            tau=tau,
            charge_time_63=charge_time * 0.632,
            charge_time_95=charge_time * 0.95,
            charge_time_99=charge_time * 0.99
        )

    @staticmethod
    def constant_current_discharging(
        capacitance: float,
        current: float,
        initial_voltage: float,
        final_voltage: float = 0.0,
        num_points: int = 1000
    ) -> CapacitorResult:
        """
        Calculate constant current discharging.

        V(t) = V0 - (I * t) / C

        Args:
            capacitance: Capacitance in Farads
            current: Discharging current in Amps (positive value)
            initial_voltage: Initial capacitor voltage
            final_voltage: Final voltage (discharge stops here)
            num_points: Number of time points

        Returns:
            CapacitorResult with time, voltage, current arrays
        """
        # Time to reach final voltage
        discharge_time = (initial_voltage - final_voltage) * capacitance / current

        time = np.linspace(0, discharge_time, num_points)

        # Voltage: V(t) = V0 - I*t/C
        voltage = initial_voltage - (current * time) / capacitance

        # Current is constant (negative for discharge)
        current_arr = np.full_like(time, -current)

        # Energy stored
        energy = 0.5 * capacitance * voltage ** 2

        # Calculate equivalent time constant
        tau = discharge_time / 5

        return CapacitorResult(
            time=time,
            voltage=voltage,
            current=current_arr,
            energy=energy,
            tau=tau,
            charge_time_63=discharge_time * 0.632,
            charge_time_95=discharge_time * 0.95,
            charge_time_99=discharge_time
        )

    @staticmethod
    def calculate_time_constant(resistance: float, capacitance: float) -> float:
        """
        Calculate RC time constant.

        Args:
            resistance: Resistance in Ohms
            capacitance: Capacitance in Farads

        Returns:
            Time constant in seconds
        """
        return resistance * capacitance

    @staticmethod
    def calculate_charge_time(
        tau: float,
        percentage: float = 0.99
    ) -> float:
        """
        Calculate time to reach percentage of final voltage.

        t = -tau * ln(1 - percentage)

        Args:
            tau: Time constant
            percentage: Target percentage (0-1)

        Returns:
            Time in seconds
        """
        return -tau * np.log(1 - percentage)

    @staticmethod
    def calculate_energy(capacitance: float, voltage: float) -> float:
        """
        Calculate energy stored in capacitor.

        E = 0.5 * C * V^2

        Args:
            capacitance: Capacitance in Farads
            voltage: Voltage in Volts

        Returns:
            Energy in Joules
        """
        return 0.5 * capacitance * voltage ** 2

    @staticmethod
    def calculate_charge(capacitance: float, voltage: float) -> float:
        """
        Calculate charge stored in capacitor.

        Q = C * V

        Args:
            capacitance: Capacitance in Farads
            voltage: Voltage in Volts

        Returns:
            Charge in Coulombs
        """
        return capacitance * voltage

    @staticmethod
    def voltage_at_time(
        supply_voltage: float,
        initial_voltage: float,
        tau: float,
        time: float,
        charging: bool = True
    ) -> float:
        """
        Calculate voltage at specific time.

        Args:
            supply_voltage: Supply voltage (for charging)
            initial_voltage: Initial voltage
            tau: Time constant
            time: Time in seconds
            charging: True for charging, False for discharging

        Returns:
            Voltage at given time
        """
        if charging:
            return supply_voltage - (supply_voltage - initial_voltage) * np.exp(-time / tau)
        else:
            return initial_voltage * np.exp(-time / tau)

    @staticmethod
    def time_to_voltage(
        target_voltage: float,
        supply_voltage: float,
        initial_voltage: float,
        tau: float,
        charging: bool = True
    ) -> float:
        """
        Calculate time to reach specific voltage.

        Args:
            target_voltage: Target voltage
            supply_voltage: Supply voltage (for charging)
            initial_voltage: Initial voltage
            tau: Time constant
            charging: True for charging, False for discharging

        Returns:
            Time in seconds
        """
        if charging:
            ratio = (supply_voltage - target_voltage) / (supply_voltage - initial_voltage)
        else:
            ratio = target_voltage / initial_voltage

        if ratio <= 0:
            return float('inf')

        return -tau * np.log(ratio)

    @staticmethod
    def format_results(result: CapacitorResult) -> str:
        """
        Format calculation results as string.

        Args:
            result: CapacitorResult object

        Returns:
            Formatted string
        """
        lines = [
            "CAPACITOR CALCULATION RESULTS",
            "=" * 40,
            f"Time Constant (tau): {result.tau * 1000:.4f} ms",
            f"",
            f"Charging/Discharging Times:",
            f"  63.2%: {result.charge_time_63 * 1000:.4f} ms",
            f"  95.0%: {result.charge_time_95 * 1000:.4f} ms",
            f"  99.0%: {result.charge_time_99 * 1000:.4f} ms",
            f"",
            f"Voltage Range: {result.voltage[0]:.4f} V -> {result.voltage[-1]:.4f} V",
            f"Peak Current: {np.max(np.abs(result.current)):.6f} A",
            f"Final Energy: {result.energy[-1] * 1000:.4f} mJ",
        ]
        return "\n".join(lines)
