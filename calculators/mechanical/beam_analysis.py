"""
Beam Bending Analysis Calculators
Three-point bending, cantilever, and general beam deflection
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class LoadCase(Enum):
    """Standard beam loading cases."""
    SIMPLY_SUPPORTED_CENTER = 1      # Simply supported, center point load
    SIMPLY_SUPPORTED_UNIFORM = 2     # Simply supported, uniform load
    CANTILEVER_END = 3               # Cantilever, end point load
    CANTILEVER_UNIFORM = 4           # Cantilever, uniform load
    FIXED_FIXED_CENTER = 5           # Fixed-fixed, center point load
    FIXED_FIXED_UNIFORM = 6          # Fixed-fixed, uniform load


@dataclass
class BeamDeflectionResult:
    """Result of beam deflection analysis."""
    max_deflection: float      # mm
    max_slope: float           # radians
    max_bending_moment: float  # N*mm
    max_bending_stress: float  # MPa
    location_max_deflection: str
    location_max_moment: str


def three_point_bending_deflection(
    force: float,
    span_length: float,
    elastic_modulus: float,
    moment_of_inertia: float
) -> float:
    """
    Calculate maximum deflection for three-point bending (center load).

    Args:
        force: Applied point load at center (N)
        span_length: Distance between supports (mm)
        elastic_modulus: Material elastic modulus (MPa or N/mm^2)
        moment_of_inertia: Second moment of area (mm^4)

    Returns:
        Maximum deflection at center (mm)

    Equation:
        delta_max = (F * L^3) / (48 * E * I)
    """
    if elastic_modulus <= 0 or moment_of_inertia <= 0:
        raise ValueError("E and I must be positive")

    return (force * span_length**3) / (48 * elastic_modulus * moment_of_inertia)


def three_point_bending_stress(
    force: float,
    span_length: float,
    moment_of_inertia: float,
    distance_from_neutral: float
) -> float:
    """
    Calculate maximum bending stress for three-point bending.

    Args:
        force: Applied point load at center (N)
        span_length: Distance between supports (mm)
        moment_of_inertia: Second moment of area (mm^4)
        distance_from_neutral: Distance from neutral axis to outer fiber (mm)

    Returns:
        Maximum bending stress (MPa)

    Equations:
        M_max = (F * L) / 4  (at center for center point load)
        sigma = (M * c) / I
    """
    max_moment = (force * span_length) / 4
    return (max_moment * distance_from_neutral) / moment_of_inertia


def beam_end_slope(
    force: float,
    span_length: float,
    elastic_modulus: float,
    moment_of_inertia: float
) -> float:
    """
    Calculate end slope for simply supported beam with center load.

    Args:
        force: Applied point load at center (N)
        span_length: Distance between supports (mm)
        elastic_modulus: Material elastic modulus (MPa)
        moment_of_inertia: Second moment of area (mm^4)

    Returns:
        Slope at supports (radians)

    Equation:
        theta = (F * L^2) / (16 * E * I)
    """
    return (force * span_length**2) / (16 * elastic_modulus * moment_of_inertia)


def cantilever_deflection(
    force: float,
    length: float,
    elastic_modulus: float,
    moment_of_inertia: float
) -> float:
    """
    Calculate maximum deflection for cantilever with end load.

    Args:
        force: Applied point load at free end (N)
        length: Cantilever length (mm)
        elastic_modulus: Material elastic modulus (MPa)
        moment_of_inertia: Second moment of area (mm^4)

    Returns:
        Maximum deflection at free end (mm)

    Equation:
        delta_max = (F * L^3) / (3 * E * I)
    """
    return (force * length**3) / (3 * elastic_modulus * moment_of_inertia)


def cantilever_slope(
    force: float,
    length: float,
    elastic_modulus: float,
    moment_of_inertia: float
) -> float:
    """
    Calculate slope at free end for cantilever with end load.

    Args:
        force: Applied point load at free end (N)
        length: Cantilever length (mm)
        elastic_modulus: Material elastic modulus (MPa)
        moment_of_inertia: Second moment of area (mm^4)

    Returns:
        Slope at free end (radians)

    Equation:
        theta = (F * L^2) / (2 * E * I)
    """
    return (force * length**2) / (2 * elastic_modulus * moment_of_inertia)


def uniform_load_deflection(
    load_per_length: float,
    span_length: float,
    elastic_modulus: float,
    moment_of_inertia: float,
    support_type: str = 'simply_supported'
) -> float:
    """
    Calculate maximum deflection for uniformly distributed load.

    Args:
        load_per_length: Distributed load (N/mm)
        span_length: Span length (mm)
        elastic_modulus: Material elastic modulus (MPa)
        moment_of_inertia: Second moment of area (mm^4)
        support_type: 'simply_supported', 'cantilever', or 'fixed_fixed'

    Returns:
        Maximum deflection (mm)

    Equations:
        Simply supported: delta = (5 * w * L^4) / (384 * E * I)
        Cantilever: delta = (w * L^4) / (8 * E * I)
        Fixed-fixed: delta = (w * L^4) / (384 * E * I)
    """
    L = span_length
    w = load_per_length
    EI = elastic_modulus * moment_of_inertia

    if support_type == 'simply_supported':
        return (5 * w * L**4) / (384 * EI)
    elif support_type == 'cantilever':
        return (w * L**4) / (8 * EI)
    elif support_type == 'fixed_fixed':
        return (w * L**4) / (384 * EI)
    else:
        raise ValueError(f"Unknown support type: {support_type}")


def analyze_beam(
    load_case: LoadCase,
    force_or_load: float,
    length: float,
    elastic_modulus: float,
    moment_of_inertia: float,
    distance_from_neutral: float
) -> BeamDeflectionResult:
    """
    Complete beam analysis for standard load cases.

    Args:
        load_case: Type of loading condition
        force_or_load: Point force (N) or distributed load (N/mm)
        length: Span or cantilever length (mm)
        elastic_modulus: Material elastic modulus (MPa)
        moment_of_inertia: Second moment of area (mm^4)
        distance_from_neutral: Distance to outer fiber (mm)

    Returns:
        BeamDeflectionResult with all calculated values
    """
    F = force_or_load
    L = length
    E = elastic_modulus
    I = moment_of_inertia
    c = distance_from_neutral
    EI = E * I

    if load_case == LoadCase.SIMPLY_SUPPORTED_CENTER:
        delta = (F * L**3) / (48 * EI)
        theta = (F * L**2) / (16 * EI)
        M_max = (F * L) / 4
        loc_delta = "center"
        loc_moment = "center"

    elif load_case == LoadCase.SIMPLY_SUPPORTED_UNIFORM:
        w = F  # F is load per unit length
        delta = (5 * w * L**4) / (384 * EI)
        theta = (w * L**3) / (24 * EI)
        M_max = (w * L**2) / 8
        loc_delta = "center"
        loc_moment = "center"

    elif load_case == LoadCase.CANTILEVER_END:
        delta = (F * L**3) / (3 * EI)
        theta = (F * L**2) / (2 * EI)
        M_max = F * L
        loc_delta = "free end"
        loc_moment = "fixed end"

    elif load_case == LoadCase.CANTILEVER_UNIFORM:
        w = F
        delta = (w * L**4) / (8 * EI)
        theta = (w * L**3) / (6 * EI)
        M_max = (w * L**2) / 2
        loc_delta = "free end"
        loc_moment = "fixed end"

    elif load_case == LoadCase.FIXED_FIXED_CENTER:
        delta = (F * L**3) / (192 * EI)
        theta = 0  # Zero slope at supports for fixed-fixed
        M_max = (F * L) / 8
        loc_delta = "center"
        loc_moment = "supports and center"

    elif load_case == LoadCase.FIXED_FIXED_UNIFORM:
        w = F
        delta = (w * L**4) / (384 * EI)
        theta = 0
        M_max = (w * L**2) / 12
        loc_delta = "center"
        loc_moment = "supports"

    else:
        raise ValueError(f"Unknown load case: {load_case}")

    sigma_max = (M_max * c) / I

    return BeamDeflectionResult(
        max_deflection=delta,
        max_slope=theta,
        max_bending_moment=M_max,
        max_bending_stress=sigma_max,
        location_max_deflection=loc_delta,
        location_max_moment=loc_moment
    )


def required_moment_of_inertia(
    force: float,
    span_length: float,
    elastic_modulus: float,
    max_deflection: float,
    load_case: LoadCase = LoadCase.SIMPLY_SUPPORTED_CENTER
) -> float:
    """
    Calculate required moment of inertia for given deflection limit.

    Args:
        force: Applied load (N or N/mm)
        span_length: Span length (mm)
        elastic_modulus: Material elastic modulus (MPa)
        max_deflection: Maximum allowable deflection (mm)
        load_case: Type of loading

    Returns:
        Required moment of inertia (mm^4)
    """
    F = force
    L = span_length
    E = elastic_modulus
    delta = max_deflection

    if load_case == LoadCase.SIMPLY_SUPPORTED_CENTER:
        return (F * L**3) / (48 * E * delta)
    elif load_case == LoadCase.CANTILEVER_END:
        return (F * L**3) / (3 * E * delta)
    elif load_case == LoadCase.FIXED_FIXED_CENTER:
        return (F * L**3) / (192 * E * delta)
    else:
        raise ValueError(f"Calculation not implemented for: {load_case}")
