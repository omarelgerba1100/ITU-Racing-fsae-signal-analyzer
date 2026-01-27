"""
Mechanical Engineering Calculators Module
Advanced Engineering Analysis Tool for Formula Student

Contains calculators for:
- Moment of Inertia & Flexural Rigidity
- Sandwich Panel Analysis
- Shear Force Calculations
- Laminate Elastic Modulus (Rule of Mixtures)
- Bolt Strength Analysis
- Beam Bending (3-Point)
- Structural Equivalence
- Skidpad/Cornering Dynamics
- Traction Control
- Transmission Ratio
"""

from .structural import (
    circular_tube_properties,
    rectangular_tube_properties,
    sandwich_panel_moi,
    flexural_rigidity,
    structural_equivalence,
    fsae_compliance_check,
)

from .materials import (
    laminate_elastic_modulus,
    rule_of_mixtures,
)

from .fasteners import (
    bolt_stress,
    shear_force_plate,
    bolt_shear_strength,
)

from .beam_analysis import (
    three_point_bending_deflection,
    three_point_bending_stress,
    cantilever_deflection,
    beam_end_slope,
)

from .vehicle_dynamics import (
    max_cornering_velocity_flat,
    max_cornering_velocity_banked,
    skidpad_calculations,
    traction_limit,
    traction_ratio,
    transmission_ratio_from_speed,
    wheel_force_from_torque,
    rpm_to_velocity,
    velocity_to_rpm,
)
