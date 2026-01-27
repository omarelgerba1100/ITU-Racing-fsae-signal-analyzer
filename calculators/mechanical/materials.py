"""
Material Property Calculators
Composite laminates, rule of mixtures, and material property estimation
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LaminateProperties:
    """Properties of a composite laminate."""
    E_longitudinal: float   # Elastic modulus in fiber direction (GPa)
    E_transverse: float     # Elastic modulus transverse to fibers (GPa)
    density: float          # Density (kg/m^3)
    fiber_volume_fraction: float
    matrix_volume_fraction: float


def laminate_elastic_modulus(
    E_fiber: float,
    E_matrix: float,
    V_fiber: float,
    V_matrix: Optional[float] = None
) -> float:
    """
    Calculate elastic modulus of a laminate using rule of mixtures.

    Args:
        E_fiber: Elastic modulus of fiber (GPa)
        E_matrix: Elastic modulus of matrix (GPa)
        V_fiber: Volume fraction of fiber (0-1 or as ratio)
        V_matrix: Volume fraction of matrix (optional, calculated if not provided)

    Returns:
        Elastic modulus of laminate (GPa)

    Equation (Voigt - upper bound, longitudinal):
        E_laminate = E_fiber * V_fiber + E_matrix * V_matrix
    """
    if V_matrix is None:
        V_matrix = 1.0 - V_fiber if V_fiber <= 1.0 else (V_fiber + 1) - V_fiber

    # Handle case where fractions are given as ratios (e.g., 5:15)
    total = V_fiber + V_matrix
    if total != 1.0 and total > 1.0:
        V_fiber = V_fiber / total
        V_matrix = V_matrix / total

    E_laminate = E_fiber * V_fiber + E_matrix * V_matrix
    return E_laminate


def rule_of_mixtures(
    property_fiber: float,
    property_matrix: float,
    V_fiber: float,
    model: str = 'voigt'
) -> float:
    """
    Calculate composite property using rule of mixtures.

    Args:
        property_fiber: Property value for fiber
        property_matrix: Property value for matrix
        V_fiber: Volume fraction of fiber (0-1)
        model: 'voigt' (parallel/upper bound) or 'reuss' (series/lower bound)

    Returns:
        Effective property of composite

    Equations:
        Voigt (parallel): P_c = P_f * V_f + P_m * V_m
        Reuss (series): 1/P_c = V_f/P_f + V_m/P_m
    """
    V_matrix = 1.0 - V_fiber

    if model.lower() == 'voigt':
        # Upper bound - parallel model
        return property_fiber * V_fiber + property_matrix * V_matrix
    elif model.lower() == 'reuss':
        # Lower bound - series model
        if property_fiber == 0 or property_matrix == 0:
            raise ValueError("Properties cannot be zero for Reuss model")
        return 1.0 / (V_fiber / property_fiber + V_matrix / property_matrix)
    else:
        raise ValueError(f"Unknown model: {model}. Use 'voigt' or 'reuss'")


def laminate_density(
    rho_fiber: float,
    rho_matrix: float,
    V_fiber: float
) -> float:
    """
    Calculate laminate density using rule of mixtures.

    Args:
        rho_fiber: Fiber density (kg/m^3)
        rho_matrix: Matrix density (kg/m^3)
        V_fiber: Volume fraction of fiber (0-1)

    Returns:
        Laminate density (kg/m^3)
    """
    V_matrix = 1.0 - V_fiber
    return rho_fiber * V_fiber + rho_matrix * V_matrix


def laminate_transverse_modulus(
    E_fiber: float,
    E_matrix: float,
    V_fiber: float
) -> float:
    """
    Calculate transverse elastic modulus of unidirectional laminate.

    Args:
        E_fiber: Fiber elastic modulus (GPa)
        E_matrix: Matrix elastic modulus (GPa)
        V_fiber: Volume fraction of fiber (0-1)

    Returns:
        Transverse elastic modulus (GPa)

    Uses Reuss (series) model as approximation for transverse loading.
    """
    return rule_of_mixtures(E_fiber, E_matrix, V_fiber, model='reuss')


def calculate_laminate_properties(
    E_fiber: float,
    E_matrix: float,
    rho_fiber: float,
    rho_matrix: float,
    V_fiber: float
) -> LaminateProperties:
    """
    Calculate complete set of laminate properties.

    Args:
        E_fiber: Fiber elastic modulus (GPa)
        E_matrix: Matrix elastic modulus (GPa)
        rho_fiber: Fiber density (kg/m^3)
        rho_matrix: Matrix density (kg/m^3)
        V_fiber: Volume fraction of fiber (0-1)

    Returns:
        LaminateProperties dataclass
    """
    V_matrix = 1.0 - V_fiber

    return LaminateProperties(
        E_longitudinal=laminate_elastic_modulus(E_fiber, E_matrix, V_fiber),
        E_transverse=laminate_transverse_modulus(E_fiber, E_matrix, V_fiber),
        density=laminate_density(rho_fiber, rho_matrix, V_fiber),
        fiber_volume_fraction=V_fiber,
        matrix_volume_fraction=V_matrix
    )


# Common material property database
MATERIAL_DATABASE = {
    'carbon_fiber_t300': {
        'E': 230,           # GPa
        'density': 1760,    # kg/m^3
        'tensile_strength': 3530,  # MPa
    },
    'carbon_fiber_t700': {
        'E': 230,
        'density': 1800,
        'tensile_strength': 4900,
    },
    'e_glass': {
        'E': 72,
        'density': 2540,
        'tensile_strength': 3450,
    },
    's_glass': {
        'E': 87,
        'density': 2490,
        'tensile_strength': 4890,
    },
    'kevlar_49': {
        'E': 112,
        'density': 1440,
        'tensile_strength': 3000,
    },
    'epoxy_resin': {
        'E': 3.5,
        'density': 1200,
        'tensile_strength': 85,
    },
    'polyester_resin': {
        'E': 3.2,
        'density': 1100,
        'tensile_strength': 50,
    },
    'steel_4130': {
        'E': 200,
        'density': 7850,
        'yield_strength': 435,
        'ultimate_strength': 670,
    },
    'aluminum_6061_t6': {
        'E': 69,
        'density': 2700,
        'yield_strength': 276,
        'ultimate_strength': 310,
    },
    'titanium_6al4v': {
        'E': 114,
        'density': 4430,
        'yield_strength': 880,
        'ultimate_strength': 950,
    },
}


def get_material_property(material: str, property_name: str) -> float:
    """
    Get a material property from the database.

    Args:
        material: Material name (key in MATERIAL_DATABASE)
        property_name: Property to retrieve

    Returns:
        Property value
    """
    if material not in MATERIAL_DATABASE:
        raise ValueError(f"Unknown material: {material}")

    mat_props = MATERIAL_DATABASE[material]
    if property_name not in mat_props:
        raise ValueError(f"Property '{property_name}' not found for {material}")

    return mat_props[property_name]
