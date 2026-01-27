"""
Structural Engineering Calculators
Moment of Inertia, Flexural Rigidity, and FSAE Compliance
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TubeProperties:
    """Properties of a structural tube."""
    area: float              # Cross-sectional area (mm^2)
    moment_of_inertia: float # Second moment of area (mm^4)
    outer_dimension: float   # Outer diameter/width (mm)
    inner_dimension: float   # Inner diameter/width (mm)
    wall_thickness: float    # Wall thickness (mm)
    section_modulus: float   # Section modulus (mm^3)


def circular_tube_properties(
    outer_diameter: float,
    wall_thickness: float
) -> TubeProperties:
    """
    Calculate properties of a circular tube.

    Args:
        outer_diameter: Outer diameter in mm
        wall_thickness: Wall thickness in mm

    Returns:
        TubeProperties dataclass with calculated values

    Equations:
        A = (pi/4) * (D_o^2 - D_i^2)
        I = (pi/64) * (D_o^4 - D_i^4)
        S = I / (D_o/2)
    """
    inner_diameter = outer_diameter - 2 * wall_thickness

    if inner_diameter < 0:
        raise ValueError("Wall thickness too large for given outer diameter")

    # Cross-sectional area
    area = (math.pi / 4) * (outer_diameter**2 - inner_diameter**2)

    # Second moment of area (moment of inertia)
    I = (math.pi / 64) * (outer_diameter**4 - inner_diameter**4)

    # Section modulus
    S = I / (outer_diameter / 2)

    return TubeProperties(
        area=area,
        moment_of_inertia=I,
        outer_dimension=outer_diameter,
        inner_dimension=inner_diameter,
        wall_thickness=wall_thickness,
        section_modulus=S
    )


def rectangular_tube_properties(
    outer_width: float,
    outer_height: float,
    wall_thickness: float
) -> TubeProperties:
    """
    Calculate properties of a rectangular tube.

    Args:
        outer_width: Outer width in mm
        outer_height: Outer height in mm
        wall_thickness: Wall thickness in mm

    Returns:
        TubeProperties dataclass with calculated values

    Equations:
        A = W_o*H_o - W_i*H_i
        I = (1/12) * (W_o*H_o^3 - W_i*H_i^3)
    """
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - 2 * wall_thickness

    if inner_width < 0 or inner_height < 0:
        raise ValueError("Wall thickness too large for given dimensions")

    # Cross-sectional area
    area = outer_width * outer_height - inner_width * inner_height

    # Second moment of area about horizontal axis
    I = (1/12) * (outer_width * outer_height**3 - inner_width * inner_height**3)

    # Section modulus
    S = I / (outer_height / 2)

    return TubeProperties(
        area=area,
        moment_of_inertia=I,
        outer_dimension=outer_height,  # Using height as primary dimension
        inner_dimension=inner_height,
        wall_thickness=wall_thickness,
        section_modulus=S
    )


def sandwich_panel_moi(
    width: float,
    face_thickness: float,
    core_thickness: float
) -> float:
    """
    Calculate moment of inertia for sandwich panel.

    Args:
        width: Panel width (m or mm - consistent units)
        face_thickness: Face sheet thickness
        core_thickness: Core thickness

    Returns:
        Second moment of area (unit^4)

    Equation:
        M = (b * t * d^2) / 6

    Note: This is an approximation assuming thin face sheets
    relative to core thickness.
    """
    # Using parallel axis theorem approximation
    # I = 2 * (b*t^3/12 + b*t*(d/2)^2)
    # Simplified for thin faces: I ≈ b*t*d^2/2

    d = core_thickness + face_thickness  # Distance between face centroids
    I = (width * face_thickness * d**2) / 2

    return I


def flexural_rigidity(
    moment_of_inertia: float,
    elastic_modulus: float
) -> float:
    """
    Calculate flexural rigidity (EI).

    Args:
        moment_of_inertia: Second moment of area (mm^4)
        elastic_modulus: Young's modulus (GPa)

    Returns:
        Flexural rigidity (N*mm^2)

    Note: Elastic modulus is converted from GPa to MPa internally
    """
    E_mpa = elastic_modulus * 1000  # GPa to MPa
    return E_mpa * moment_of_inertia


def structural_equivalence(
    E_reference: float,
    I_reference: float,
    E_alternative: float,
    I_alternative: float
) -> Tuple[float, bool]:
    """
    Check structural equivalence between two materials/sections.

    Args:
        E_reference: Elastic modulus of reference material (GPa)
        I_reference: Moment of inertia of reference section (mm^4)
        E_alternative: Elastic modulus of alternative material (GPa)
        I_alternative: Moment of inertia of alternative section (mm^4)

    Returns:
        Tuple of (equivalence_ratio, passes_requirement)

    Equation:
        Ratio = (E_alt * I_alt) / (E_ref * I_ref)
        Passes if Ratio >= 1.0
    """
    EI_reference = E_reference * I_reference
    EI_alternative = E_alternative * I_alternative

    if EI_reference == 0:
        raise ValueError("Reference EI cannot be zero")

    ratio = EI_alternative / EI_reference
    passes = ratio >= 1.0

    return ratio, passes


@dataclass
class FSAEComplianceResult:
    """Result of FSAE compliance check."""
    component: str
    passes_thickness: bool
    passes_area: bool
    passes_inertia: bool
    passes_rigidity: bool
    passes_all: bool
    actual_thickness: float
    actual_area: float
    actual_inertia: float
    actual_rigidity: float
    required_thickness: float
    required_area: float
    required_inertia: float
    required_rigidity: float
    margin_thickness: float  # Percentage margin
    margin_area: float
    margin_inertia: float
    margin_rigidity: float


# FSAE minimum requirements
FSAE_MINIMUMS = {
    'main_front_hoops': {
        'min_thickness': 2.0,      # mm
        'min_area': 173.0,         # mm^2
        'min_inertia': 11320.0,    # mm^4
        'min_rigidity': 2.264e9,   # N*mm^2
    },
    'shoulder_harness_bar': {
        'min_thickness': 2.0,
        'min_area': 173.0,
        'min_inertia': 11320.0,
        'min_rigidity': 2.264e9,
    },
    'side_impact': {
        'min_thickness': 1.2,
        'min_area': 119.0,
        'min_inertia': 8509.0,
        'min_rigidity': 1.702e9,
    },
    'front_bulkhead': {
        'min_thickness': 1.2,
        'min_area': 119.0,
        'min_inertia': 8509.0,
        'min_rigidity': 1.702e9,
    },
    'hoop_bracing': {
        'min_thickness': 1.2,
        'min_area': 119.0,
        'min_inertia': 8509.0,
        'min_rigidity': 1.702e9,
    },
    'driver_restraint': {
        'min_thickness': 1.2,
        'min_area': 119.0,
        'min_inertia': 8509.0,
        'min_rigidity': 1.702e9,
    },
    'bulkhead_support': {
        'min_thickness': 1.2,
        'min_area': 91.0,
        'min_inertia': 6695.0,
        'min_rigidity': 1.339e9,
    },
    'bracing_supports': {
        'min_thickness': 1.2,
        'min_area': 91.0,
        'min_inertia': 6695.0,
        'min_rigidity': 1.339e9,
    },
}


def fsae_compliance_check(
    component: str,
    wall_thickness: float,
    area: float,
    moment_of_inertia: float,
    elastic_modulus: float = 200.0  # GPa, default steel
) -> FSAEComplianceResult:
    """
    Check if a tube section meets FSAE requirements.

    Args:
        component: Component type (see FSAE_MINIMUMS keys)
        wall_thickness: Actual wall thickness (mm)
        area: Actual cross-sectional area (mm^2)
        moment_of_inertia: Actual second moment of area (mm^4)
        elastic_modulus: Material elastic modulus (GPa)

    Returns:
        FSAEComplianceResult with detailed compliance information
    """
    if component not in FSAE_MINIMUMS:
        raise ValueError(f"Unknown component: {component}. Valid options: {list(FSAE_MINIMUMS.keys())}")

    req = FSAE_MINIMUMS[component]
    actual_rigidity = flexural_rigidity(moment_of_inertia, elastic_modulus)

    # Check each requirement
    passes_t = wall_thickness >= req['min_thickness']
    passes_a = area >= req['min_area']
    passes_i = moment_of_inertia >= req['min_inertia']
    passes_ei = actual_rigidity >= req['min_rigidity']

    # Calculate margins
    margin_t = ((wall_thickness - req['min_thickness']) / req['min_thickness']) * 100
    margin_a = ((area - req['min_area']) / req['min_area']) * 100
    margin_i = ((moment_of_inertia - req['min_inertia']) / req['min_inertia']) * 100
    margin_ei = ((actual_rigidity - req['min_rigidity']) / req['min_rigidity']) * 100

    return FSAEComplianceResult(
        component=component,
        passes_thickness=passes_t,
        passes_area=passes_a,
        passes_inertia=passes_i,
        passes_rigidity=passes_ei,
        passes_all=passes_t and passes_a and passes_i and passes_ei,
        actual_thickness=wall_thickness,
        actual_area=area,
        actual_inertia=moment_of_inertia,
        actual_rigidity=actual_rigidity,
        required_thickness=req['min_thickness'],
        required_area=req['min_area'],
        required_inertia=req['min_inertia'],
        required_rigidity=req['min_rigidity'],
        margin_thickness=margin_t,
        margin_area=margin_a,
        margin_inertia=margin_i,
        margin_rigidity=margin_ei,
    )
