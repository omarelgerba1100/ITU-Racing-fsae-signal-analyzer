"""
Vehicle Dynamics Calculators
Cornering, traction, transmission, and powertrain analysis for Formula Student
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


# Physical constants
G = 9.80665  # Standard gravity (m/s^2)


@dataclass
class SkidpadGeometry:
    """Skidpad geometry parameters."""
    inner_radius: float      # m
    outer_radius: float      # m
    center_distance: float   # m
    track_width: float       # m
    racing_line_radius: float  # m
    inner_circumference: float  # m
    outer_circumference: float  # m
    racing_line_circumference: float  # m


@dataclass
class TractionResult:
    """Result of traction analysis."""
    max_traction_force: float  # N
    max_traction_torque: float  # Nm
    motor_output_torque: float  # Nm
    traction_ratio: float      # <1 means traction limited
    is_traction_limited: bool
    available_acceleration: float  # m/s^2


@dataclass
class TransmissionResult:
    """Result of transmission analysis."""
    transmission_ratio: float
    wheel_rpm: float
    wheel_angular_velocity: float  # rad/s
    vehicle_velocity: float  # m/s
    output_torque: float  # Nm
    wheel_force: float  # N


def max_cornering_velocity_flat(
    friction_coefficient: float,
    turn_radius: float,
    gravity: float = G
) -> float:
    """
    Calculate maximum cornering velocity on flat surface.

    Args:
        friction_coefficient: Tire-road friction coefficient
        turn_radius: Corner radius (m)
        gravity: Gravitational acceleration (m/s^2)

    Returns:
        Maximum velocity (m/s)

    Equation:
        V_max = sqrt(mu * r * g)
    """
    return math.sqrt(friction_coefficient * turn_radius * gravity)


def max_cornering_velocity_banked(
    bank_angle: float,
    turn_radius: float,
    gravity: float = G,
    angle_in_degrees: bool = True
) -> float:
    """
    Calculate maximum cornering velocity on banked surface (no friction).

    Args:
        bank_angle: Banking angle
        turn_radius: Corner radius (m)
        gravity: Gravitational acceleration (m/s^2)
        angle_in_degrees: If True, angle is in degrees

    Returns:
        Maximum velocity (m/s)

    Equation:
        V_max = sqrt(tan(theta) * g * r)
    """
    if angle_in_degrees:
        bank_angle = math.radians(bank_angle)

    return math.sqrt(math.tan(bank_angle) * gravity * turn_radius)


def wall_of_death_velocity(
    turn_radius: float,
    friction_coefficient: float,
    gravity: float = G
) -> float:
    """
    Calculate minimum velocity to stay on vertical wall (cylinder).

    Args:
        turn_radius: Cylinder radius (m)
        friction_coefficient: Wall friction coefficient
        gravity: Gravitational acceleration (m/s^2)

    Returns:
        Minimum velocity (m/s)

    Equation:
        V_min = sqrt(r * g / mu)
    """
    return math.sqrt(turn_radius * gravity / friction_coefficient)


def skidpad_calculations(
    inner_radius: float = 7.625,
    outer_radius: float = 10.625,
    center_distance: float = 18.25,
    track_width: float = 3.0
) -> SkidpadGeometry:
    """
    Calculate FSAE skidpad geometry.

    Args:
        inner_radius: Inner cone radius (m) - default FSAE value
        outer_radius: Outer cone radius (m) - default FSAE value
        center_distance: Distance between circle centers (m)
        track_width: Track width (m)

    Returns:
        SkidpadGeometry dataclass with all dimensions
    """
    racing_line_radius = (inner_radius + outer_radius) / 2

    return SkidpadGeometry(
        inner_radius=inner_radius,
        outer_radius=outer_radius,
        center_distance=center_distance,
        track_width=track_width,
        racing_line_radius=racing_line_radius,
        inner_circumference=2 * math.pi * inner_radius,
        outer_circumference=2 * math.pi * outer_radius,
        racing_line_circumference=2 * math.pi * racing_line_radius
    )


def traction_limit(
    vehicle_mass: float,
    rear_weight_balance: float,
    friction_coefficient: float,
    tire_radius: float,
    gravity: float = G
) -> Tuple[float, float]:
    """
    Calculate traction-limited force and torque.

    Args:
        vehicle_mass: Total vehicle mass (kg)
        rear_weight_balance: Fraction of weight on driven wheels (0-1)
        friction_coefficient: Tire-road friction coefficient
        tire_radius: Driven tire radius (m)
        gravity: Gravitational acceleration (m/s^2)

    Returns:
        Tuple of (max_traction_force_N, max_traction_torque_Nm)

    Equations:
        F_rear = m * g * balance
        F_friction = F_rear * mu
        T_max = F_friction * r_tire
    """
    weight = vehicle_mass * gravity
    rear_normal_force = weight * rear_weight_balance
    max_friction_force = rear_normal_force * friction_coefficient
    max_torque = max_friction_force * tire_radius

    return max_friction_force, max_torque


def traction_ratio(
    motor_torque: float,
    gear_ratio: float,
    tire_radius: float,
    vehicle_mass: float,
    rear_weight_balance: float,
    friction_coefficient: float,
    efficiency: float = 1.0
) -> TractionResult:
    """
    Analyze traction vs motor torque capability.

    Args:
        motor_torque: Motor output torque (Nm)
        gear_ratio: Total gear ratio (motor to wheel)
        tire_radius: Tire radius (m)
        vehicle_mass: Vehicle mass (kg)
        rear_weight_balance: Rear weight fraction (0-1)
        friction_coefficient: Tire friction coefficient
        efficiency: Drivetrain efficiency (0-1)

    Returns:
        TractionResult with complete analysis
    """
    # Calculate traction limit
    max_traction_force, max_traction_torque = traction_limit(
        vehicle_mass, rear_weight_balance, friction_coefficient, tire_radius
    )

    # Calculate motor output at wheel
    wheel_torque = motor_torque * gear_ratio * efficiency
    wheel_force = wheel_torque / tire_radius

    # Traction ratio
    ratio = max_traction_torque / wheel_torque if wheel_torque > 0 else float('inf')

    # Available acceleration (limited by traction or motor)
    limiting_force = min(wheel_force, max_traction_force)
    acceleration = limiting_force / vehicle_mass

    return TractionResult(
        max_traction_force=max_traction_force,
        max_traction_torque=max_traction_torque,
        motor_output_torque=wheel_torque,
        traction_ratio=ratio,
        is_traction_limited=ratio < 1.0,
        available_acceleration=acceleration
    )


def transmission_ratio_from_speed(
    motor_max_rpm: float,
    max_vehicle_speed: float,
    tire_radius: float
) -> float:
    """
    Calculate required transmission ratio from max speed.

    Args:
        motor_max_rpm: Maximum motor RPM
        max_vehicle_speed: Desired maximum speed (m/s)
        tire_radius: Tire radius (m)

    Returns:
        Required transmission ratio

    Equations:
        omega_wheel = V / r
        n_wheel = omega_wheel * 60 / (2*pi)
        ratio = n_motor / n_wheel
    """
    wheel_angular_velocity = max_vehicle_speed / tire_radius  # rad/s
    wheel_rpm = (wheel_angular_velocity * 60) / (2 * math.pi)
    return motor_max_rpm / wheel_rpm


def wheel_force_from_torque(
    motor_torque: float,
    gear_ratio: float,
    tire_radius: float,
    efficiency: float = 1.0
) -> float:
    """
    Calculate wheel force from motor torque.

    Args:
        motor_torque: Motor torque (Nm)
        gear_ratio: Total gear ratio
        tire_radius: Tire radius (m)
        efficiency: Drivetrain efficiency

    Returns:
        Force at wheel contact patch (N)

    Equation:
        F = (T_motor * ratio * eta) / r_tire
    """
    return (motor_torque * gear_ratio * efficiency) / tire_radius


def rpm_to_velocity(
    rpm: float,
    gear_ratio: float,
    tire_radius: float
) -> Tuple[float, float]:
    """
    Convert motor RPM to vehicle velocity.

    Args:
        rpm: Motor RPM
        gear_ratio: Total gear ratio (motor to wheel)
        tire_radius: Tire radius (m)

    Returns:
        Tuple of (velocity_m_s, velocity_km_h)

    Equations:
        omega_motor = rpm * 2*pi / 60
        omega_wheel = omega_motor / ratio
        V = omega_wheel * r
    """
    omega_motor = rpm * 2 * math.pi / 60  # rad/s
    omega_wheel = omega_motor / gear_ratio
    velocity_ms = omega_wheel * tire_radius
    velocity_kmh = velocity_ms * 3.6

    return velocity_ms, velocity_kmh


def velocity_to_rpm(
    velocity: float,
    gear_ratio: float,
    tire_radius: float,
    velocity_in_kmh: bool = False
) -> float:
    """
    Convert vehicle velocity to motor RPM.

    Args:
        velocity: Vehicle velocity
        gear_ratio: Total gear ratio
        tire_radius: Tire radius (m)
        velocity_in_kmh: If True, velocity is in km/h

    Returns:
        Motor RPM

    Equations:
        omega_wheel = V / r
        omega_motor = omega_wheel * ratio
        rpm = omega_motor * 60 / (2*pi)
    """
    if velocity_in_kmh:
        velocity = velocity / 3.6  # Convert to m/s

    omega_wheel = velocity / tire_radius
    omega_motor = omega_wheel * gear_ratio
    rpm = (omega_motor * 60) / (2 * math.pi)

    return rpm


def analyze_transmission(
    motor_rpm: float,
    motor_torque: float,
    gear_ratio: float,
    tire_radius: float,
    efficiency: float = 1.0
) -> TransmissionResult:
    """
    Complete transmission analysis.

    Args:
        motor_rpm: Motor speed (RPM)
        motor_torque: Motor torque (Nm)
        gear_ratio: Total gear ratio
        tire_radius: Tire radius (m)
        efficiency: Drivetrain efficiency

    Returns:
        TransmissionResult with all calculated values
    """
    velocity_ms, _ = rpm_to_velocity(motor_rpm, gear_ratio, tire_radius)
    wheel_rpm = motor_rpm / gear_ratio
    wheel_omega = wheel_rpm * 2 * math.pi / 60
    output_torque = motor_torque * gear_ratio * efficiency
    wheel_force = output_torque / tire_radius

    return TransmissionResult(
        transmission_ratio=gear_ratio,
        wheel_rpm=wheel_rpm,
        wheel_angular_velocity=wheel_omega,
        vehicle_velocity=velocity_ms,
        output_torque=output_torque,
        wheel_force=wheel_force
    )


def lateral_load_transfer(
    vehicle_mass: float,
    cg_height: float,
    track_width: float,
    lateral_acceleration: float
) -> Tuple[float, float]:
    """
    Calculate lateral load transfer during cornering.

    Args:
        vehicle_mass: Total vehicle mass (kg)
        cg_height: Center of gravity height (m)
        track_width: Track width (m)
        lateral_acceleration: Lateral acceleration (m/s^2 or g's)

    Returns:
        Tuple of (load_transfer_N, percentage_of_weight)

    Equation:
        delta_F = (m * a_y * h) / t
    """
    weight = vehicle_mass * G
    load_transfer = (vehicle_mass * lateral_acceleration * cg_height) / track_width
    percentage = (load_transfer / (weight / 2)) * 100

    return load_transfer, percentage


def longitudinal_load_transfer(
    vehicle_mass: float,
    cg_height: float,
    wheelbase: float,
    longitudinal_acceleration: float
) -> Tuple[float, float]:
    """
    Calculate longitudinal load transfer during acceleration/braking.

    Args:
        vehicle_mass: Total vehicle mass (kg)
        cg_height: Center of gravity height (m)
        wheelbase: Wheelbase (m)
        longitudinal_acceleration: Longitudinal acceleration (m/s^2)

    Returns:
        Tuple of (load_transfer_N, percentage_change)

    Equation:
        delta_F = (m * a_x * h) / L
    """
    weight = vehicle_mass * G
    load_transfer = (vehicle_mass * longitudinal_acceleration * cg_height) / wheelbase
    percentage = (load_transfer / (weight / 2)) * 100

    return load_transfer, percentage
