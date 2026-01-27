"""
Fastener and Connection Calculators
Bolt stress, shear force, and joint analysis
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class BoltStressResult:
    """Result of bolt stress calculation."""
    tensile_stress: float    # MPa
    shear_stress: float      # MPa
    von_mises_stress: float  # MPa
    factor_of_safety: float
    passes: bool


def bolt_stress(
    force: float,
    stress_area: float,
    num_bolts: int = 1
) -> float:
    """
    Calculate tensile stress in bolts.

    Args:
        force: Applied force (N)
        stress_area: Tensile stress area per bolt (mm^2)
        num_bolts: Number of bolts sharing the load

    Returns:
        Stress in bolt (MPa)

    Equation:
        sigma = F / (A * n)
    """
    if stress_area <= 0:
        raise ValueError("Stress area must be positive")
    if num_bolts <= 0:
        raise ValueError("Number of bolts must be positive")

    return force / (stress_area * num_bolts)


def bolt_shear_stress(
    shear_force: float,
    shank_area: float,
    num_bolts: int = 1,
    num_shear_planes: int = 1
) -> float:
    """
    Calculate shear stress in bolts.

    Args:
        shear_force: Applied shear force (N)
        shank_area: Bolt shank cross-sectional area (mm^2)
        num_bolts: Number of bolts sharing the load
        num_shear_planes: Number of shear planes per bolt

    Returns:
        Shear stress (MPa)

    Equation:
        tau = V / (A * n * m)
    """
    if shank_area <= 0:
        raise ValueError("Shank area must be positive")

    return shear_force / (shank_area * num_bolts * num_shear_planes)


def bolt_combined_stress(
    tensile_force: float,
    shear_force: float,
    stress_area: float,
    shank_area: float,
    num_bolts: int = 1,
    yield_strength: float = 640  # MPa, Grade 8.8 default
) -> BoltStressResult:
    """
    Calculate combined stress in bolts using von Mises criterion.

    Args:
        tensile_force: Applied tensile force (N)
        shear_force: Applied shear force (N)
        stress_area: Tensile stress area (mm^2)
        shank_area: Shank cross-sectional area (mm^2)
        num_bolts: Number of bolts
        yield_strength: Bolt yield strength (MPa)

    Returns:
        BoltStressResult with all stress values and factor of safety
    """
    sigma = bolt_stress(tensile_force, stress_area, num_bolts)
    tau = bolt_shear_stress(shear_force, shank_area, num_bolts)

    # Von Mises equivalent stress
    von_mises = math.sqrt(sigma**2 + 3 * tau**2)

    # Factor of safety
    fos = yield_strength / von_mises if von_mises > 0 else float('inf')

    return BoltStressResult(
        tensile_stress=sigma,
        shear_stress=tau,
        von_mises_stress=von_mises,
        factor_of_safety=fos,
        passes=fos >= 1.0
    )


def shear_force_plate(
    applicator_diameter: float,
    plate_thickness: float,
    shear_strength: float
) -> Tuple[float, float]:
    """
    Calculate shear force capacity for plate punching.

    Args:
        applicator_diameter: Diameter of load applicator (mm)
        plate_thickness: Plate thickness (mm)
        shear_strength: Material shear yield strength (MPa)

    Returns:
        Tuple of (shear_area_mm2, max_shear_force_N)

    Equation:
        A_shear = pi * D * t
        F_shear = A_shear * tau_yield

    This calculates the force required to punch through a plate.
    """
    # Shear area is the cylindrical surface around the applicator
    shear_area = math.pi * applicator_diameter * plate_thickness

    # Maximum shear force
    max_force = shear_area * shear_strength

    return shear_area, max_force


def bolt_shear_strength(
    diameter: float,
    grade: str = '8.8',
    num_shear_planes: int = 1
) -> float:
    """
    Calculate shear strength of a bolt.

    Args:
        diameter: Nominal bolt diameter (mm)
        grade: Bolt grade (e.g., '8.8', '10.9', '12.9')
        num_shear_planes: Number of shear planes

    Returns:
        Shear strength (N)

    Common bolt grades and approximate shear strengths:
        8.8: 400 MPa shear
        10.9: 500 MPa shear
        12.9: 600 MPa shear
    """
    # Shear strength lookup (approximate values)
    shear_strengths = {
        '4.6': 240,
        '4.8': 320,
        '5.8': 320,
        '8.8': 400,
        '10.9': 500,
        '12.9': 600,
    }

    if grade not in shear_strengths:
        raise ValueError(f"Unknown bolt grade: {grade}. Valid: {list(shear_strengths.keys())}")

    tau = shear_strengths[grade]
    area = math.pi * (diameter / 2)**2

    return tau * area * num_shear_planes


def bearing_stress(
    force: float,
    diameter: float,
    thickness: float,
    num_bolts: int = 1
) -> float:
    """
    Calculate bearing stress on plate at bolt hole.

    Args:
        force: Applied force (N)
        diameter: Bolt diameter (mm)
        thickness: Plate thickness (mm)
        num_bolts: Number of bolts

    Returns:
        Bearing stress (MPa)

    Equation:
        sigma_b = F / (d * t * n)
    """
    bearing_area = diameter * thickness * num_bolts
    return force / bearing_area


def tearout_strength(
    edge_distance: float,
    thickness: float,
    ultimate_strength: float,
    num_bolts: int = 1
) -> float:
    """
    Calculate tearout strength of bolted connection.

    Args:
        edge_distance: Distance from bolt center to edge (mm)
        thickness: Plate thickness (mm)
        ultimate_strength: Material ultimate strength (MPa)
        num_bolts: Number of bolts in a row

    Returns:
        Tearout strength (N)

    Equation:
        F_tearout = 2 * e * t * sigma_u * n
    """
    return 2 * edge_distance * thickness * ultimate_strength * num_bolts


# Standard metric bolt tensile stress areas (mm^2)
BOLT_STRESS_AREAS = {
    'M3': 5.03,
    'M4': 8.78,
    'M5': 14.2,
    'M6': 20.1,
    'M8': 36.6,
    'M10': 58.0,
    'M12': 84.3,
    'M14': 115,
    'M16': 157,
    'M18': 192,
    'M20': 245,
    'M22': 303,
    'M24': 353,
    'M27': 459,
    'M30': 561,
}

# Standard metric bolt shank areas (mm^2)
BOLT_SHANK_AREAS = {
    'M3': 7.07,
    'M4': 12.57,
    'M5': 19.63,
    'M6': 28.27,
    'M8': 50.27,
    'M10': 78.54,
    'M12': 113.1,
    'M14': 153.9,
    'M16': 201.1,
    'M18': 254.5,
    'M20': 314.2,
    'M22': 380.1,
    'M24': 452.4,
    'M27': 572.6,
    'M30': 706.9,
}


def get_bolt_areas(bolt_size: str) -> Tuple[float, float]:
    """
    Get stress area and shank area for a standard metric bolt.

    Args:
        bolt_size: Bolt designation (e.g., 'M8', 'M10')

    Returns:
        Tuple of (stress_area_mm2, shank_area_mm2)
    """
    if bolt_size not in BOLT_STRESS_AREAS:
        raise ValueError(f"Unknown bolt size: {bolt_size}")

    return BOLT_STRESS_AREAS[bolt_size], BOLT_SHANK_AREAS[bolt_size]
