"""
Battery discharge calculator.
Supports various battery chemistries and discharge profiles.
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum


class BatteryChemistry(Enum):
    """Battery chemistry types with typical parameters."""
    LIPO = "LiPo"
    LIION = "Li-Ion"
    LIFE = "LiFePO4"
    NIMH = "NiMH"
    LEAD_ACID = "Lead Acid"
    CUSTOM = "Custom"


# Typical voltage curves for different chemistries (per cell)
CHEMISTRY_PARAMS = {
    BatteryChemistry.LIPO: {
        'nominal_voltage': 3.7,
        'full_voltage': 4.2,
        'empty_voltage': 3.0,
        'cutoff_voltage': 3.0,
    },
    BatteryChemistry.LIION: {
        'nominal_voltage': 3.6,
        'full_voltage': 4.2,
        'empty_voltage': 2.8,
        'cutoff_voltage': 2.8,
    },
    BatteryChemistry.LIFE: {
        'nominal_voltage': 3.2,
        'full_voltage': 3.65,
        'empty_voltage': 2.5,
        'cutoff_voltage': 2.5,
    },
    BatteryChemistry.NIMH: {
        'nominal_voltage': 1.2,
        'full_voltage': 1.4,
        'empty_voltage': 1.0,
        'cutoff_voltage': 1.0,
    },
    BatteryChemistry.LEAD_ACID: {
        'nominal_voltage': 2.0,
        'full_voltage': 2.4,
        'empty_voltage': 1.75,
        'cutoff_voltage': 1.75,
    },
}


@dataclass
class BatteryResult:
    """Results from battery discharge calculation."""
    time_hours: np.ndarray
    voltage: np.ndarray
    current: np.ndarray
    capacity_remaining_ah: np.ndarray
    capacity_remaining_percent: np.ndarray
    energy_remaining_wh: np.ndarray
    runtime_hours: float
    total_energy_wh: float
    average_power_w: float


class BatteryCalculator:
    """
    Calculator for battery discharge characteristics.

    Features:
    - Multiple battery chemistries
    - Constant current discharge
    - Constant power discharge
    - Peukert effect for lead acid
    - Temperature compensation (simplified)
    """

    @staticmethod
    def constant_current_discharge(
        capacity_ah: float,
        current_a: float,
        num_cells: int = 1,
        chemistry: BatteryChemistry = BatteryChemistry.LIPO,
        internal_resistance: float = 0.02,
        num_points: int = 500
    ) -> BatteryResult:
        """
        Calculate constant current discharge profile.

        Args:
            capacity_ah: Battery capacity in Amp-hours
            current_a: Discharge current in Amps
            num_cells: Number of cells in series
            chemistry: Battery chemistry type
            internal_resistance: Internal resistance per cell (Ohms)
            num_points: Number of data points

        Returns:
            BatteryResult with discharge profile
        """
        params = CHEMISTRY_PARAMS.get(chemistry, CHEMISTRY_PARAMS[BatteryChemistry.LIPO])

        # Calculate runtime (ideal)
        runtime_hours = capacity_ah / current_a

        # Time array
        time_hours = np.linspace(0, runtime_hours, num_points)

        # Remaining capacity
        capacity_remaining_ah = capacity_ah - current_a * time_hours
        capacity_remaining_ah = np.maximum(capacity_remaining_ah, 0)
        capacity_remaining_percent = (capacity_remaining_ah / capacity_ah) * 100

        # Voltage curve (simplified model)
        # V = V_full - (V_full - V_empty) * (1 - SOC) - I * R_internal
        soc = capacity_remaining_ah / capacity_ah

        # Non-linear voltage curve approximation
        v_full = params['full_voltage'] * num_cells
        v_empty = params['empty_voltage'] * num_cells
        v_nominal = params['nominal_voltage'] * num_cells

        # Simplified Shepherd model
        voltage = v_full - (v_full - v_empty) * (1 - soc) ** 0.8
        voltage = voltage - current_a * internal_resistance * num_cells

        # Ensure voltage stays above cutoff
        cutoff = params['cutoff_voltage'] * num_cells
        voltage = np.maximum(voltage, cutoff)

        # Recalculate runtime based on cutoff
        cutoff_idx = np.argmax(voltage <= cutoff)
        if cutoff_idx > 0:
            runtime_hours = time_hours[cutoff_idx]

        # Current array (constant)
        current = np.full_like(time_hours, current_a)

        # Energy remaining
        energy_remaining_wh = capacity_remaining_ah * voltage

        # Total energy
        total_energy_wh = capacity_ah * v_nominal

        # Average power
        average_power_w = np.mean(voltage * current)

        return BatteryResult(
            time_hours=time_hours,
            voltage=voltage,
            current=current,
            capacity_remaining_ah=capacity_remaining_ah,
            capacity_remaining_percent=capacity_remaining_percent,
            energy_remaining_wh=energy_remaining_wh,
            runtime_hours=runtime_hours,
            total_energy_wh=total_energy_wh,
            average_power_w=average_power_w
        )

    @staticmethod
    def constant_power_discharge(
        capacity_ah: float,
        power_w: float,
        num_cells: int = 1,
        chemistry: BatteryChemistry = BatteryChemistry.LIPO,
        internal_resistance: float = 0.02,
        num_points: int = 500
    ) -> BatteryResult:
        """
        Calculate constant power discharge profile.

        Args:
            capacity_ah: Battery capacity in Amp-hours
            power_w: Constant power draw in Watts
            num_cells: Number of cells in series
            chemistry: Battery chemistry type
            internal_resistance: Internal resistance per cell (Ohms)
            num_points: Number of data points

        Returns:
            BatteryResult with discharge profile
        """
        params = CHEMISTRY_PARAMS.get(chemistry, CHEMISTRY_PARAMS[BatteryChemistry.LIPO])

        v_full = params['full_voltage'] * num_cells
        v_empty = params['empty_voltage'] * num_cells
        v_nominal = params['nominal_voltage'] * num_cells
        cutoff = params['cutoff_voltage'] * num_cells

        # Estimate runtime based on energy
        total_energy_wh = capacity_ah * v_nominal
        estimated_runtime = total_energy_wh / power_w

        # Time array
        time_hours = np.linspace(0, estimated_runtime * 1.2, num_points)
        dt = time_hours[1] - time_hours[0]

        # Initialize arrays
        voltage = np.zeros(num_points)
        current = np.zeros(num_points)
        capacity_remaining_ah = np.zeros(num_points)

        # Initial conditions
        capacity_remaining_ah[0] = capacity_ah
        soc = 1.0
        voltage[0] = v_full

        # Simulate discharge
        actual_runtime = estimated_runtime
        for i in range(1, num_points):
            # Calculate current needed for constant power
            # P = V * I, so I = P / V
            current[i - 1] = power_w / voltage[i - 1]

            # Update remaining capacity
            capacity_used = current[i - 1] * dt
            capacity_remaining_ah[i] = capacity_remaining_ah[i - 1] - capacity_used
            capacity_remaining_ah[i] = max(capacity_remaining_ah[i], 0)

            # Update SOC
            soc = capacity_remaining_ah[i] / capacity_ah

            # Update voltage
            voltage[i] = v_full - (v_full - v_empty) * (1 - soc) ** 0.8
            voltage[i] = voltage[i] - current[i - 1] * internal_resistance * num_cells
            voltage[i] = max(voltage[i], cutoff)

            # Check cutoff
            if voltage[i] <= cutoff or capacity_remaining_ah[i] <= 0:
                actual_runtime = time_hours[i]
                # Fill remaining with final values
                voltage[i:] = cutoff
                current[i:] = 0
                capacity_remaining_ah[i:] = 0
                break

        current[-1] = current[-2] if len(current) > 1 else 0

        capacity_remaining_percent = (capacity_remaining_ah / capacity_ah) * 100
        energy_remaining_wh = capacity_remaining_ah * voltage

        return BatteryResult(
            time_hours=time_hours,
            voltage=voltage,
            current=current,
            capacity_remaining_ah=capacity_remaining_ah,
            capacity_remaining_percent=capacity_remaining_percent,
            energy_remaining_wh=energy_remaining_wh,
            runtime_hours=actual_runtime,
            total_energy_wh=total_energy_wh,
            average_power_w=power_w
        )

    @staticmethod
    def calculate_c_rate(current_a: float, capacity_ah: float) -> float:
        """
        Calculate C-rate.

        C-rate = I / C

        Args:
            current_a: Current in Amps
            capacity_ah: Capacity in Amp-hours

        Returns:
            C-rate
        """
        return current_a / capacity_ah

    @staticmethod
    def calculate_runtime(
        capacity_ah: float,
        current_a: float,
        efficiency: float = 1.0
    ) -> float:
        """
        Calculate simple runtime estimate.

        Runtime = Capacity / Current * Efficiency

        Args:
            capacity_ah: Capacity in Amp-hours
            current_a: Discharge current in Amps
            efficiency: Discharge efficiency (0-1)

        Returns:
            Runtime in hours
        """
        return (capacity_ah / current_a) * efficiency

    @staticmethod
    def calculate_energy(
        capacity_ah: float,
        voltage: float
    ) -> float:
        """
        Calculate battery energy.

        E = C * V

        Args:
            capacity_ah: Capacity in Amp-hours
            voltage: Nominal voltage

        Returns:
            Energy in Watt-hours
        """
        return capacity_ah * voltage

    @staticmethod
    def peukert_capacity(
        rated_capacity_ah: float,
        rated_hours: float,
        discharge_current: float,
        peukert_exponent: float = 1.2
    ) -> float:
        """
        Calculate effective capacity using Peukert's Law.
        Primarily applicable to lead-acid batteries.

        C_effective = C_rated * (I_rated / I_actual)^(n-1)

        Args:
            rated_capacity_ah: Rated capacity at rated discharge
            rated_hours: Hours for rated capacity (e.g., 20 for C20)
            discharge_current: Actual discharge current
            peukert_exponent: Peukert exponent (1.1-1.4 typical)

        Returns:
            Effective capacity in Amp-hours
        """
        rated_current = rated_capacity_ah / rated_hours
        effective_capacity = rated_capacity_ah * (rated_current / discharge_current) ** (peukert_exponent - 1)
        return effective_capacity

    @staticmethod
    def state_of_charge(
        remaining_ah: float,
        total_ah: float
    ) -> float:
        """
        Calculate state of charge percentage.

        Args:
            remaining_ah: Remaining capacity in Ah
            total_ah: Total capacity in Ah

        Returns:
            SOC percentage (0-100)
        """
        return (remaining_ah / total_ah) * 100

    @staticmethod
    def depth_of_discharge(
        remaining_ah: float,
        total_ah: float
    ) -> float:
        """
        Calculate depth of discharge percentage.

        Args:
            remaining_ah: Remaining capacity in Ah
            total_ah: Total capacity in Ah

        Returns:
            DOD percentage (0-100)
        """
        return ((total_ah - remaining_ah) / total_ah) * 100

    @staticmethod
    def series_parallel_config(
        cell_voltage: float,
        cell_capacity_ah: float,
        target_voltage: float,
        target_capacity_ah: float
    ) -> Tuple[int, int]:
        """
        Calculate series/parallel cell configuration.

        Args:
            cell_voltage: Single cell voltage
            cell_capacity_ah: Single cell capacity
            target_voltage: Desired pack voltage
            target_capacity_ah: Desired pack capacity

        Returns:
            Tuple of (series cells, parallel cells)
        """
        series = int(np.ceil(target_voltage / cell_voltage))
        parallel = int(np.ceil(target_capacity_ah / cell_capacity_ah))
        return series, parallel

    @staticmethod
    def format_results(result: BatteryResult, chemistry: str = "LiPo") -> str:
        """
        Format calculation results as string.

        Args:
            result: BatteryResult object
            chemistry: Battery chemistry name

        Returns:
            Formatted string
        """
        lines = [
            f"BATTERY DISCHARGE RESULTS ({chemistry})",
            "=" * 45,
            f"Runtime: {result.runtime_hours:.2f} hours ({result.runtime_hours * 60:.1f} min)",
            f"",
            f"Voltage Range:",
            f"  Start: {result.voltage[0]:.2f} V",
            f"  End:   {result.voltage[-1]:.2f} V",
            f"",
            f"Energy:",
            f"  Total:   {result.total_energy_wh:.2f} Wh",
            f"  Average Power: {result.average_power_w:.2f} W",
            f"",
            f"Capacity:",
            f"  Start: {result.capacity_remaining_ah[0]:.2f} Ah (100%)",
            f"  End:   {result.capacity_remaining_ah[-1]:.2f} Ah ({result.capacity_remaining_percent[-1]:.1f}%)",
        ]
        return "\n".join(lines)
