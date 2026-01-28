"""
Calculator definitions for the browser-based calculator system.
Organized by category following Omni Calculator structure.
"""

CALCULATORS = {
    "Kinematics": {
        "icon": "🚀",
        "description": "Motion, velocity, projectiles",
        "calculators": {
            "velocity": {
                "name": "Velocity Calculator",
                "description": "Calculate velocity from distance and time",
                "inputs": [
                    {"id": "distance", "label": "Distance", "unit": "m", "default": 100},
                    {"id": "time", "label": "Time", "unit": "s", "default": 10}
                ],
                "outputs": [
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "formula": "distance / time"},
                    {"id": "velocity_kmh", "label": "Velocity", "unit": "km/h", "formula": "(distance / time) * 3.6"}
                ]
            },
            "acceleration": {
                "name": "Acceleration Calculator",
                "description": "Calculate acceleration from velocity change",
                "inputs": [
                    {"id": "v_initial", "label": "Initial Velocity", "unit": "m/s", "default": 0},
                    {"id": "v_final", "label": "Final Velocity", "unit": "m/s", "default": 30},
                    {"id": "time", "label": "Time", "unit": "s", "default": 5}
                ],
                "outputs": [
                    {"id": "acceleration", "label": "Acceleration", "unit": "m/s²", "formula": "(v_final - v_initial) / time"},
                    {"id": "accel_g", "label": "Acceleration", "unit": "g", "formula": "((v_final - v_initial) / time) / 9.81"}
                ]
            },
            "projectile_motion": {
                "name": "Projectile Motion",
                "description": "Calculate projectile trajectory",
                "inputs": [
                    {"id": "v0", "label": "Initial Velocity", "unit": "m/s", "default": 20},
                    {"id": "angle", "label": "Launch Angle", "unit": "°", "default": 45},
                    {"id": "h0", "label": "Initial Height", "unit": "m", "default": 0}
                ],
                "outputs": [
                    {"id": "max_height", "label": "Max Height", "unit": "m", "formula": "h0 + (v0 * Math.sin(angle * Math.PI/180))**2 / (2 * 9.81)"},
                    {"id": "range", "label": "Range", "unit": "m", "formula": "(v0**2 * Math.sin(2 * angle * Math.PI/180)) / 9.81"},
                    {"id": "flight_time", "label": "Flight Time", "unit": "s", "formula": "(2 * v0 * Math.sin(angle * Math.PI/180)) / 9.81"}
                ]
            },
            "free_fall": {
                "name": "Free Fall Calculator",
                "description": "Calculate free fall motion",
                "inputs": [
                    {"id": "height", "label": "Drop Height", "unit": "m", "default": 10},
                    {"id": "g", "label": "Gravity", "unit": "m/s²", "default": 9.81}
                ],
                "outputs": [
                    {"id": "fall_time", "label": "Fall Time", "unit": "s", "formula": "Math.sqrt(2 * height / g)"},
                    {"id": "impact_vel", "label": "Impact Velocity", "unit": "m/s", "formula": "Math.sqrt(2 * g * height)"}
                ]
            },
            "stopping_distance": {
                "name": "Stopping Distance",
                "description": "Calculate braking distance",
                "inputs": [
                    {"id": "velocity", "label": "Initial Speed", "unit": "km/h", "default": 100},
                    {"id": "friction", "label": "Friction Coefficient", "unit": "", "default": 0.7},
                    {"id": "reaction_time", "label": "Reaction Time", "unit": "s", "default": 1.5}
                ],
                "outputs": [
                    {"id": "reaction_dist", "label": "Reaction Distance", "unit": "m", "formula": "(velocity / 3.6) * reaction_time"},
                    {"id": "braking_dist", "label": "Braking Distance", "unit": "m", "formula": "(velocity / 3.6)**2 / (2 * friction * 9.81)"},
                    {"id": "total_dist", "label": "Total Distance", "unit": "m", "formula": "(velocity / 3.6) * reaction_time + (velocity / 3.6)**2 / (2 * friction * 9.81)"}
                ]
            }
        }
    },
    "Dynamics": {
        "icon": "⚡",
        "description": "Forces, Newton's laws",
        "calculators": {
            "force": {
                "name": "Force Calculator (F=ma)",
                "description": "Newton's second law",
                "inputs": [
                    {"id": "mass", "label": "Mass", "unit": "kg", "default": 100},
                    {"id": "acceleration", "label": "Acceleration", "unit": "m/s²", "default": 5}
                ],
                "outputs": [
                    {"id": "force", "label": "Force", "unit": "N", "formula": "mass * acceleration"},
                    {"id": "force_kn", "label": "Force", "unit": "kN", "formula": "mass * acceleration / 1000"}
                ]
            },
            "friction": {
                "name": "Friction Calculator",
                "description": "Calculate friction force",
                "inputs": [
                    {"id": "normal_force", "label": "Normal Force", "unit": "N", "default": 1000},
                    {"id": "mu", "label": "Friction Coefficient", "unit": "", "default": 0.5}
                ],
                "outputs": [
                    {"id": "friction_force", "label": "Friction Force", "unit": "N", "formula": "mu * normal_force"}
                ]
            },
            "centripetal": {
                "name": "Centripetal Force",
                "description": "Circular motion force",
                "inputs": [
                    {"id": "mass", "label": "Mass", "unit": "kg", "default": 300},
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "default": 15},
                    {"id": "radius", "label": "Radius", "unit": "m", "default": 10}
                ],
                "outputs": [
                    {"id": "force", "label": "Centripetal Force", "unit": "N", "formula": "mass * velocity**2 / radius"},
                    {"id": "accel", "label": "Centripetal Accel", "unit": "g", "formula": "(velocity**2 / radius) / 9.81"}
                ]
            },
            "momentum": {
                "name": "Momentum Calculator",
                "description": "Linear momentum p=mv",
                "inputs": [
                    {"id": "mass", "label": "Mass", "unit": "kg", "default": 1500},
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "default": 20}
                ],
                "outputs": [
                    {"id": "momentum", "label": "Momentum", "unit": "kg·m/s", "formula": "mass * velocity"}
                ]
            },
            "impulse": {
                "name": "Impulse Calculator",
                "description": "Impulse and momentum change",
                "inputs": [
                    {"id": "force", "label": "Force", "unit": "N", "default": 5000},
                    {"id": "time", "label": "Time", "unit": "s", "default": 0.1}
                ],
                "outputs": [
                    {"id": "impulse", "label": "Impulse", "unit": "N·s", "formula": "force * time"}
                ]
            }
        }
    },
    "Energy & Power": {
        "icon": "🔋",
        "description": "Work, energy, power",
        "calculators": {
            "kinetic_energy": {
                "name": "Kinetic Energy",
                "description": "Energy of motion",
                "inputs": [
                    {"id": "mass", "label": "Mass", "unit": "kg", "default": 300},
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "default": 30}
                ],
                "outputs": [
                    {"id": "energy", "label": "Kinetic Energy", "unit": "J", "formula": "0.5 * mass * velocity**2"},
                    {"id": "energy_kj", "label": "Kinetic Energy", "unit": "kJ", "formula": "0.5 * mass * velocity**2 / 1000"}
                ]
            },
            "potential_energy": {
                "name": "Potential Energy",
                "description": "Gravitational potential energy",
                "inputs": [
                    {"id": "mass", "label": "Mass", "unit": "kg", "default": 300},
                    {"id": "height", "label": "Height", "unit": "m", "default": 5}
                ],
                "outputs": [
                    {"id": "energy", "label": "Potential Energy", "unit": "J", "formula": "mass * 9.81 * height"}
                ]
            },
            "work": {
                "name": "Work Calculator",
                "description": "Work done by force",
                "inputs": [
                    {"id": "force", "label": "Force", "unit": "N", "default": 500},
                    {"id": "distance", "label": "Distance", "unit": "m", "default": 10},
                    {"id": "angle", "label": "Angle", "unit": "°", "default": 0}
                ],
                "outputs": [
                    {"id": "work", "label": "Work", "unit": "J", "formula": "force * distance * Math.cos(angle * Math.PI/180)"}
                ]
            },
            "power": {
                "name": "Power Calculator",
                "description": "Power from work and time",
                "inputs": [
                    {"id": "work", "label": "Work/Energy", "unit": "J", "default": 10000},
                    {"id": "time", "label": "Time", "unit": "s", "default": 5}
                ],
                "outputs": [
                    {"id": "power_w", "label": "Power", "unit": "W", "formula": "work / time"},
                    {"id": "power_kw", "label": "Power", "unit": "kW", "formula": "work / time / 1000"},
                    {"id": "power_hp", "label": "Power", "unit": "hp", "formula": "work / time / 745.7"}
                ]
            },
            "power_velocity": {
                "name": "Power from Velocity",
                "description": "P = F × v",
                "inputs": [
                    {"id": "force", "label": "Force", "unit": "N", "default": 2000},
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "default": 20}
                ],
                "outputs": [
                    {"id": "power_w", "label": "Power", "unit": "W", "formula": "force * velocity"},
                    {"id": "power_kw", "label": "Power", "unit": "kW", "formula": "force * velocity / 1000"},
                    {"id": "power_hp", "label": "Power", "unit": "hp", "formula": "force * velocity / 745.7"}
                ]
            }
        }
    },
    "Rotational Motion": {
        "icon": "🔄",
        "description": "Angular motion, torque",
        "calculators": {
            "angular_velocity": {
                "name": "Angular Velocity",
                "description": "RPM to rad/s conversion",
                "inputs": [
                    {"id": "rpm", "label": "RPM", "unit": "rpm", "default": 6000}
                ],
                "outputs": [
                    {"id": "omega", "label": "Angular Velocity", "unit": "rad/s", "formula": "rpm * 2 * Math.PI / 60"},
                    {"id": "frequency", "label": "Frequency", "unit": "Hz", "formula": "rpm / 60"}
                ]
            },
            "torque": {
                "name": "Torque Calculator",
                "description": "Rotational force",
                "inputs": [
                    {"id": "force", "label": "Force", "unit": "N", "default": 100},
                    {"id": "radius", "label": "Lever Arm", "unit": "m", "default": 0.5},
                    {"id": "angle", "label": "Angle", "unit": "°", "default": 90}
                ],
                "outputs": [
                    {"id": "torque", "label": "Torque", "unit": "N·m", "formula": "force * radius * Math.sin(angle * Math.PI/180)"}
                ]
            },
            "rotational_ke": {
                "name": "Rotational Kinetic Energy",
                "description": "Energy of rotating body",
                "inputs": [
                    {"id": "inertia", "label": "Moment of Inertia", "unit": "kg·m²", "default": 0.5},
                    {"id": "omega", "label": "Angular Velocity", "unit": "rad/s", "default": 100}
                ],
                "outputs": [
                    {"id": "energy", "label": "Rotational KE", "unit": "J", "formula": "0.5 * inertia * omega**2"}
                ]
            },
            "gear_ratio": {
                "name": "Gear Ratio",
                "description": "Gear train calculations",
                "inputs": [
                    {"id": "teeth_driven", "label": "Driven Gear Teeth", "unit": "", "default": 60},
                    {"id": "teeth_driver", "label": "Driver Gear Teeth", "unit": "", "default": 15},
                    {"id": "input_rpm", "label": "Input RPM", "unit": "rpm", "default": 6000},
                    {"id": "input_torque", "label": "Input Torque", "unit": "N·m", "default": 50}
                ],
                "outputs": [
                    {"id": "ratio", "label": "Gear Ratio", "unit": ":1", "formula": "teeth_driven / teeth_driver"},
                    {"id": "output_rpm", "label": "Output RPM", "unit": "rpm", "formula": "input_rpm * teeth_driver / teeth_driven"},
                    {"id": "output_torque", "label": "Output Torque", "unit": "N·m", "formula": "input_torque * teeth_driven / teeth_driver"}
                ]
            }
        }
    },
    "Materials & Stress": {
        "icon": "🔩",
        "description": "Stress, strain, material properties",
        "calculators": {
            "stress": {
                "name": "Stress Calculator",
                "description": "σ = F/A",
                "inputs": [
                    {"id": "force", "label": "Force", "unit": "N", "default": 10000},
                    {"id": "area", "label": "Cross-section Area", "unit": "mm²", "default": 100}
                ],
                "outputs": [
                    {"id": "stress_mpa", "label": "Stress", "unit": "MPa", "formula": "force / area"},
                    {"id": "stress_psi", "label": "Stress", "unit": "psi", "formula": "force / area * 145.038"}
                ]
            },
            "strain": {
                "name": "Strain Calculator",
                "description": "ε = ΔL/L",
                "inputs": [
                    {"id": "delta_l", "label": "Change in Length", "unit": "mm", "default": 0.5},
                    {"id": "original_l", "label": "Original Length", "unit": "mm", "default": 100}
                ],
                "outputs": [
                    {"id": "strain", "label": "Strain", "unit": "", "formula": "delta_l / original_l"},
                    {"id": "strain_pct", "label": "Strain", "unit": "%", "formula": "(delta_l / original_l) * 100"}
                ]
            },
            "youngs_modulus": {
                "name": "Young's Modulus",
                "description": "E = σ/ε",
                "inputs": [
                    {"id": "stress", "label": "Stress", "unit": "MPa", "default": 200},
                    {"id": "strain", "label": "Strain", "unit": "", "default": 0.001}
                ],
                "outputs": [
                    {"id": "modulus", "label": "Young's Modulus", "unit": "GPa", "formula": "stress / strain / 1000"}
                ]
            },
            "shear_stress": {
                "name": "Shear Stress",
                "description": "τ = F/A",
                "inputs": [
                    {"id": "force", "label": "Shear Force", "unit": "N", "default": 5000},
                    {"id": "area", "label": "Shear Area", "unit": "mm²", "default": 50}
                ],
                "outputs": [
                    {"id": "shear", "label": "Shear Stress", "unit": "MPa", "formula": "force / area"}
                ]
            },
            "factor_of_safety": {
                "name": "Factor of Safety",
                "description": "FoS = Yield/Applied",
                "inputs": [
                    {"id": "yield_stress", "label": "Yield Strength", "unit": "MPa", "default": 250},
                    {"id": "applied_stress", "label": "Applied Stress", "unit": "MPa", "default": 100}
                ],
                "outputs": [
                    {"id": "fos", "label": "Factor of Safety", "unit": "", "formula": "yield_stress / applied_stress"}
                ]
            },
            "beam_bending": {
                "name": "Beam Bending Stress",
                "description": "σ = My/I",
                "inputs": [
                    {"id": "moment", "label": "Bending Moment", "unit": "N·m", "default": 1000},
                    {"id": "y", "label": "Distance from NA", "unit": "mm", "default": 25},
                    {"id": "I", "label": "Moment of Inertia", "unit": "mm⁴", "default": 50000}
                ],
                "outputs": [
                    {"id": "stress", "label": "Bending Stress", "unit": "MPa", "formula": "(moment * 1000 * y) / I"}
                ]
            }
        }
    },
    "Structural": {
        "icon": "🏗️",
        "description": "Beams, tubes, sections",
        "calculators": {
            "tube_moi": {
                "name": "Tube Moment of Inertia",
                "description": "Hollow circular section",
                "inputs": [
                    {"id": "od", "label": "Outer Diameter", "unit": "mm", "default": 25.4},
                    {"id": "wall", "label": "Wall Thickness", "unit": "mm", "default": 1.6}
                ],
                "outputs": [
                    {"id": "id", "label": "Inner Diameter", "unit": "mm", "formula": "od - 2*wall"},
                    {"id": "area", "label": "Cross-section Area", "unit": "mm²", "formula": "Math.PI/4 * (od**2 - (od-2*wall)**2)"},
                    {"id": "I", "label": "Moment of Inertia", "unit": "mm⁴", "formula": "Math.PI/64 * (od**4 - (od-2*wall)**4)"},
                    {"id": "EI", "label": "Flexural Rigidity (Steel)", "unit": "N·mm²", "formula": "200000 * Math.PI/64 * (od**4 - (od-2*wall)**4)"}
                ]
            },
            "rectangular_section": {
                "name": "Rectangular Section",
                "description": "Rectangular beam properties",
                "inputs": [
                    {"id": "width", "label": "Width", "unit": "mm", "default": 50},
                    {"id": "height", "label": "Height", "unit": "mm", "default": 100}
                ],
                "outputs": [
                    {"id": "area", "label": "Area", "unit": "mm²", "formula": "width * height"},
                    {"id": "Ix", "label": "Ix (about x)", "unit": "mm⁴", "formula": "width * height**3 / 12"},
                    {"id": "Iy", "label": "Iy (about y)", "unit": "mm⁴", "formula": "height * width**3 / 12"}
                ]
            },
            "three_point_bend": {
                "name": "3-Point Bending",
                "description": "Simply supported beam",
                "inputs": [
                    {"id": "force", "label": "Central Force", "unit": "N", "default": 1000},
                    {"id": "length", "label": "Span Length", "unit": "mm", "default": 500},
                    {"id": "E", "label": "Young's Modulus", "unit": "GPa", "default": 200},
                    {"id": "I", "label": "Moment of Inertia", "unit": "mm⁴", "default": 10000}
                ],
                "outputs": [
                    {"id": "max_moment", "label": "Max Moment", "unit": "N·mm", "formula": "force * length / 4"},
                    {"id": "deflection", "label": "Max Deflection", "unit": "mm", "formula": "(force * length**3) / (48 * E * 1000 * I)"}
                ]
            },
            "cantilever": {
                "name": "Cantilever Beam",
                "description": "Fixed-free beam",
                "inputs": [
                    {"id": "force", "label": "End Force", "unit": "N", "default": 500},
                    {"id": "length", "label": "Length", "unit": "mm", "default": 300},
                    {"id": "E", "label": "Young's Modulus", "unit": "GPa", "default": 200},
                    {"id": "I", "label": "Moment of Inertia", "unit": "mm⁴", "default": 5000}
                ],
                "outputs": [
                    {"id": "max_moment", "label": "Max Moment (at fix)", "unit": "N·mm", "formula": "force * length"},
                    {"id": "deflection", "label": "End Deflection", "unit": "mm", "formula": "(force * length**3) / (3 * E * 1000 * I)"}
                ]
            }
        }
    },
    "Vehicle Dynamics": {
        "icon": "🏎️",
        "description": "FSAE vehicle calculations",
        "calculators": {
            "weight_transfer_accel": {
                "name": "Weight Transfer (Accel)",
                "description": "Longitudinal weight transfer",
                "inputs": [
                    {"id": "mass", "label": "Vehicle Mass", "unit": "kg", "default": 300},
                    {"id": "accel", "label": "Acceleration", "unit": "g", "default": 0.8},
                    {"id": "cg_height", "label": "CG Height", "unit": "mm", "default": 300},
                    {"id": "wheelbase", "label": "Wheelbase", "unit": "mm", "default": 1550}
                ],
                "outputs": [
                    {"id": "transfer", "label": "Weight Transfer", "unit": "N", "formula": "(mass * 9.81 * accel * cg_height) / wheelbase"}
                ]
            },
            "weight_transfer_corner": {
                "name": "Weight Transfer (Corner)",
                "description": "Lateral weight transfer",
                "inputs": [
                    {"id": "mass", "label": "Vehicle Mass", "unit": "kg", "default": 300},
                    {"id": "lateral_g", "label": "Lateral G", "unit": "g", "default": 1.5},
                    {"id": "cg_height", "label": "CG Height", "unit": "mm", "default": 300},
                    {"id": "track_width", "label": "Track Width", "unit": "mm", "default": 1200}
                ],
                "outputs": [
                    {"id": "transfer", "label": "Weight Transfer", "unit": "N", "formula": "(mass * 9.81 * lateral_g * cg_height) / track_width"}
                ]
            },
            "skidpad": {
                "name": "Skidpad Calculator",
                "description": "Skidpad time and speed",
                "inputs": [
                    {"id": "radius", "label": "Radius", "unit": "m", "default": 7.625},
                    {"id": "lateral_g", "label": "Lateral G", "unit": "g", "default": 1.4}
                ],
                "outputs": [
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "formula": "Math.sqrt(lateral_g * 9.81 * radius)"},
                    {"id": "velocity_kmh", "label": "Velocity", "unit": "km/h", "formula": "Math.sqrt(lateral_g * 9.81 * radius) * 3.6"},
                    {"id": "lap_time", "label": "Lap Time", "unit": "s", "formula": "(2 * Math.PI * radius) / Math.sqrt(lateral_g * 9.81 * radius)"}
                ]
            },
            "tire_load": {
                "name": "Tire Load Calculator",
                "description": "Individual tire loads",
                "inputs": [
                    {"id": "mass", "label": "Vehicle Mass", "unit": "kg", "default": 300},
                    {"id": "front_weight_pct", "label": "Front Weight %", "unit": "%", "default": 45},
                    {"id": "lateral_g", "label": "Lateral G", "unit": "g", "default": 1.2},
                    {"id": "cg_height", "label": "CG Height", "unit": "mm", "default": 280},
                    {"id": "track_width", "label": "Track Width", "unit": "mm", "default": 1200}
                ],
                "outputs": [
                    {"id": "front_static", "label": "Front Axle Load", "unit": "N", "formula": "mass * 9.81 * front_weight_pct / 100"},
                    {"id": "rear_static", "label": "Rear Axle Load", "unit": "N", "formula": "mass * 9.81 * (100 - front_weight_pct) / 100"},
                    {"id": "transfer", "label": "Lateral Transfer", "unit": "N", "formula": "(mass * 9.81 * lateral_g * cg_height) / track_width"}
                ]
            },
            "traction_limit": {
                "name": "Traction Limit",
                "description": "Maximum tire force",
                "inputs": [
                    {"id": "normal_load", "label": "Normal Load", "unit": "N", "default": 1000},
                    {"id": "friction_coef", "label": "Friction Coefficient", "unit": "", "default": 1.5}
                ],
                "outputs": [
                    {"id": "max_force", "label": "Max Tire Force", "unit": "N", "formula": "normal_load * friction_coef"}
                ]
            }
        }
    },
    "Powertrain": {
        "icon": "⚙️",
        "description": "Engine, transmission, drivetrain",
        "calculators": {
            "engine_power": {
                "name": "Engine Power",
                "description": "Power from torque and RPM",
                "inputs": [
                    {"id": "torque", "label": "Torque", "unit": "N·m", "default": 50},
                    {"id": "rpm", "label": "Engine RPM", "unit": "rpm", "default": 8000}
                ],
                "outputs": [
                    {"id": "power_kw", "label": "Power", "unit": "kW", "formula": "(torque * rpm * 2 * Math.PI) / 60000"},
                    {"id": "power_hp", "label": "Power", "unit": "hp", "formula": "(torque * rpm * 2 * Math.PI) / 60000 / 0.7457"}
                ]
            },
            "transmission_ratio": {
                "name": "Transmission Calculator",
                "description": "Overall drive ratio",
                "inputs": [
                    {"id": "primary", "label": "Primary Ratio", "unit": ":1", "default": 2.5},
                    {"id": "gear", "label": "Gear Ratio", "unit": ":1", "default": 2.0},
                    {"id": "final", "label": "Final Drive Ratio", "unit": ":1", "default": 3.5},
                    {"id": "tire_radius", "label": "Tire Radius", "unit": "m", "default": 0.26}
                ],
                "outputs": [
                    {"id": "overall", "label": "Overall Ratio", "unit": ":1", "formula": "primary * gear * final"},
                    {"id": "rpm_per_kmh", "label": "RPM per km/h", "unit": "rpm/(km/h)", "formula": "(primary * gear * final) / (tire_radius * 2 * Math.PI) * 1000 / 60"}
                ]
            },
            "wheel_torque": {
                "name": "Wheel Torque",
                "description": "Torque at wheels",
                "inputs": [
                    {"id": "engine_torque", "label": "Engine Torque", "unit": "N·m", "default": 50},
                    {"id": "overall_ratio", "label": "Overall Ratio", "unit": ":1", "default": 12},
                    {"id": "efficiency", "label": "Drivetrain Efficiency", "unit": "%", "default": 85}
                ],
                "outputs": [
                    {"id": "wheel_torque", "label": "Wheel Torque", "unit": "N·m", "formula": "engine_torque * overall_ratio * efficiency / 100"}
                ]
            },
            "tractive_force": {
                "name": "Tractive Force",
                "description": "Force at tire contact",
                "inputs": [
                    {"id": "wheel_torque", "label": "Wheel Torque", "unit": "N·m", "default": 500},
                    {"id": "tire_radius", "label": "Tire Radius", "unit": "m", "default": 0.26}
                ],
                "outputs": [
                    {"id": "force", "label": "Tractive Force", "unit": "N", "formula": "wheel_torque / tire_radius"}
                ]
            },
            "top_speed": {
                "name": "Top Speed Calculator",
                "description": "Maximum velocity",
                "inputs": [
                    {"id": "max_rpm", "label": "Max Engine RPM", "unit": "rpm", "default": 10000},
                    {"id": "overall_ratio", "label": "Overall Ratio", "unit": ":1", "default": 8},
                    {"id": "tire_radius", "label": "Tire Radius", "unit": "m", "default": 0.26}
                ],
                "outputs": [
                    {"id": "wheel_rpm", "label": "Wheel RPM", "unit": "rpm", "formula": "max_rpm / overall_ratio"},
                    {"id": "speed_ms", "label": "Speed", "unit": "m/s", "formula": "(max_rpm / overall_ratio) * (2 * Math.PI * tire_radius) / 60"},
                    {"id": "speed_kmh", "label": "Speed", "unit": "km/h", "formula": "(max_rpm / overall_ratio) * (2 * Math.PI * tire_radius) / 60 * 3.6"}
                ]
            }
        }
    },
    "Electrical": {
        "icon": "⚡",
        "description": "Circuits, components",
        "calculators": {
            "ohms_law": {
                "name": "Ohm's Law",
                "description": "V = IR",
                "inputs": [
                    {"id": "voltage", "label": "Voltage", "unit": "V", "default": 12},
                    {"id": "resistance", "label": "Resistance", "unit": "Ω", "default": 100}
                ],
                "outputs": [
                    {"id": "current", "label": "Current", "unit": "A", "formula": "voltage / resistance"},
                    {"id": "current_ma", "label": "Current", "unit": "mA", "formula": "voltage / resistance * 1000"},
                    {"id": "power", "label": "Power", "unit": "W", "formula": "voltage**2 / resistance"}
                ]
            },
            "voltage_divider": {
                "name": "Voltage Divider",
                "description": "Resistor voltage divider",
                "inputs": [
                    {"id": "vin", "label": "Input Voltage", "unit": "V", "default": 12},
                    {"id": "r1", "label": "R1 (top)", "unit": "Ω", "default": 10000},
                    {"id": "r2", "label": "R2 (bottom)", "unit": "Ω", "default": 10000}
                ],
                "outputs": [
                    {"id": "vout", "label": "Output Voltage", "unit": "V", "formula": "vin * r2 / (r1 + r2)"},
                    {"id": "ratio", "label": "Division Ratio", "unit": "", "formula": "r2 / (r1 + r2)"}
                ]
            },
            "rc_time_constant": {
                "name": "RC Time Constant",
                "description": "Capacitor charge/discharge",
                "inputs": [
                    {"id": "resistance", "label": "Resistance", "unit": "Ω", "default": 10000},
                    {"id": "capacitance", "label": "Capacitance", "unit": "µF", "default": 100}
                ],
                "outputs": [
                    {"id": "tau", "label": "Time Constant τ", "unit": "s", "formula": "resistance * capacitance / 1000000"},
                    {"id": "t_95", "label": "95% Charge Time", "unit": "s", "formula": "3 * resistance * capacitance / 1000000"},
                    {"id": "t_99", "label": "99% Charge Time", "unit": "s", "formula": "5 * resistance * capacitance / 1000000"}
                ]
            },
            "led_resistor": {
                "name": "LED Resistor",
                "description": "Current limiting resistor",
                "inputs": [
                    {"id": "v_supply", "label": "Supply Voltage", "unit": "V", "default": 12},
                    {"id": "v_led", "label": "LED Forward Voltage", "unit": "V", "default": 2.0},
                    {"id": "i_led", "label": "LED Current", "unit": "mA", "default": 20}
                ],
                "outputs": [
                    {"id": "resistance", "label": "Resistor Value", "unit": "Ω", "formula": "(v_supply - v_led) / (i_led / 1000)"},
                    {"id": "power", "label": "Resistor Power", "unit": "W", "formula": "(v_supply - v_led) * (i_led / 1000)"}
                ]
            },
            "power_dissipation": {
                "name": "Power Dissipation",
                "description": "Component power loss",
                "inputs": [
                    {"id": "voltage", "label": "Voltage Drop", "unit": "V", "default": 5},
                    {"id": "current", "label": "Current", "unit": "A", "default": 2}
                ],
                "outputs": [
                    {"id": "power", "label": "Power", "unit": "W", "formula": "voltage * current"}
                ]
            },
            "wire_resistance": {
                "name": "Wire Resistance",
                "description": "Copper wire resistance",
                "inputs": [
                    {"id": "length", "label": "Wire Length", "unit": "m", "default": 5},
                    {"id": "diameter", "label": "Wire Diameter", "unit": "mm", "default": 1.0}
                ],
                "outputs": [
                    {"id": "area", "label": "Cross-section", "unit": "mm²", "formula": "Math.PI * (diameter/2)**2"},
                    {"id": "resistance", "label": "Resistance", "unit": "Ω", "formula": "0.0172 * length / (Math.PI * (diameter/2)**2)"}
                ]
            }
        }
    },
    "Fluid Mechanics": {
        "icon": "💧",
        "description": "Pressure, flow, drag",
        "calculators": {
            "pressure": {
                "name": "Pressure Calculator",
                "description": "P = F/A",
                "inputs": [
                    {"id": "force", "label": "Force", "unit": "N", "default": 1000},
                    {"id": "area", "label": "Area", "unit": "cm²", "default": 10}
                ],
                "outputs": [
                    {"id": "pressure_pa", "label": "Pressure", "unit": "Pa", "formula": "force / (area / 10000)"},
                    {"id": "pressure_bar", "label": "Pressure", "unit": "bar", "formula": "force / (area / 10000) / 100000"},
                    {"id": "pressure_psi", "label": "Pressure", "unit": "psi", "formula": "force / (area / 10000) / 6894.76"}
                ]
            },
            "hydraulic_pressure": {
                "name": "Hydraulic System",
                "description": "Pascal's principle",
                "inputs": [
                    {"id": "f1", "label": "Input Force", "unit": "N", "default": 100},
                    {"id": "a1", "label": "Input Piston Area", "unit": "cm²", "default": 2},
                    {"id": "a2", "label": "Output Piston Area", "unit": "cm²", "default": 20}
                ],
                "outputs": [
                    {"id": "pressure", "label": "System Pressure", "unit": "bar", "formula": "(f1 / (a1/10000)) / 100000"},
                    {"id": "f2", "label": "Output Force", "unit": "N", "formula": "f1 * a2 / a1"},
                    {"id": "ratio", "label": "Force Ratio", "unit": ":1", "formula": "a2 / a1"}
                ]
            },
            "flow_rate": {
                "name": "Flow Rate",
                "description": "Volume flow Q = Av",
                "inputs": [
                    {"id": "diameter", "label": "Pipe Diameter", "unit": "mm", "default": 25},
                    {"id": "velocity", "label": "Flow Velocity", "unit": "m/s", "default": 2}
                ],
                "outputs": [
                    {"id": "area", "label": "Cross-section", "unit": "mm²", "formula": "Math.PI * (diameter/2)**2"},
                    {"id": "flow_m3s", "label": "Flow Rate", "unit": "m³/s", "formula": "Math.PI * (diameter/2000)**2 * velocity"},
                    {"id": "flow_lpm", "label": "Flow Rate", "unit": "L/min", "formula": "Math.PI * (diameter/2000)**2 * velocity * 60000"}
                ]
            },
            "drag_force": {
                "name": "Aerodynamic Drag",
                "description": "Drag force calculation",
                "inputs": [
                    {"id": "cd", "label": "Drag Coefficient", "unit": "", "default": 0.35},
                    {"id": "area", "label": "Frontal Area", "unit": "m²", "default": 1.0},
                    {"id": "velocity", "label": "Velocity", "unit": "km/h", "default": 100},
                    {"id": "rho", "label": "Air Density", "unit": "kg/m³", "default": 1.225}
                ],
                "outputs": [
                    {"id": "drag", "label": "Drag Force", "unit": "N", "formula": "0.5 * rho * cd * area * (velocity/3.6)**2"},
                    {"id": "power", "label": "Power to Overcome", "unit": "kW", "formula": "0.5 * rho * cd * area * (velocity/3.6)**3 / 1000"}
                ]
            },
            "reynolds": {
                "name": "Reynolds Number",
                "description": "Flow regime indicator",
                "inputs": [
                    {"id": "velocity", "label": "Velocity", "unit": "m/s", "default": 10},
                    {"id": "length", "label": "Characteristic Length", "unit": "m", "default": 0.5},
                    {"id": "viscosity", "label": "Kinematic Viscosity", "unit": "m²/s", "default": 0.0000151}
                ],
                "outputs": [
                    {"id": "re", "label": "Reynolds Number", "unit": "", "formula": "velocity * length / viscosity"}
                ]
            }
        }
    },
    "Thermodynamics": {
        "icon": "🌡️",
        "description": "Heat, temperature, energy",
        "calculators": {
            "heat_transfer": {
                "name": "Heat Transfer",
                "description": "Q = mcΔT",
                "inputs": [
                    {"id": "mass", "label": "Mass", "unit": "kg", "default": 1},
                    {"id": "specific_heat", "label": "Specific Heat", "unit": "J/(kg·K)", "default": 4186},
                    {"id": "delta_t", "label": "Temperature Change", "unit": "°C", "default": 10}
                ],
                "outputs": [
                    {"id": "heat", "label": "Heat Energy", "unit": "J", "formula": "mass * specific_heat * delta_t"},
                    {"id": "heat_kj", "label": "Heat Energy", "unit": "kJ", "formula": "mass * specific_heat * delta_t / 1000"}
                ]
            },
            "thermal_resistance": {
                "name": "Thermal Resistance",
                "description": "Conduction through wall",
                "inputs": [
                    {"id": "thickness", "label": "Thickness", "unit": "mm", "default": 10},
                    {"id": "area", "label": "Area", "unit": "m²", "default": 0.01},
                    {"id": "k", "label": "Thermal Conductivity", "unit": "W/(m·K)", "default": 50}
                ],
                "outputs": [
                    {"id": "resistance", "label": "Thermal Resistance", "unit": "K/W", "formula": "(thickness/1000) / (k * area)"}
                ]
            },
            "heat_flux": {
                "name": "Heat Flux",
                "description": "Heat flow rate",
                "inputs": [
                    {"id": "delta_t", "label": "Temperature Difference", "unit": "°C", "default": 50},
                    {"id": "resistance", "label": "Thermal Resistance", "unit": "K/W", "default": 0.5}
                ],
                "outputs": [
                    {"id": "heat_rate", "label": "Heat Flow Rate", "unit": "W", "formula": "delta_t / resistance"}
                ]
            }
        }
    },
    "Math & Geometry": {
        "icon": "📐",
        "description": "Trigonometry, geometry",
        "calculators": {
            "circle": {
                "name": "Circle Calculator",
                "description": "Circle properties",
                "inputs": [
                    {"id": "radius", "label": "Radius", "unit": "mm", "default": 50}
                ],
                "outputs": [
                    {"id": "diameter", "label": "Diameter", "unit": "mm", "formula": "2 * radius"},
                    {"id": "circumference", "label": "Circumference", "unit": "mm", "formula": "2 * Math.PI * radius"},
                    {"id": "area", "label": "Area", "unit": "mm²", "formula": "Math.PI * radius**2"}
                ]
            },
            "triangle": {
                "name": "Triangle Area",
                "description": "Area from base and height",
                "inputs": [
                    {"id": "base", "label": "Base", "unit": "mm", "default": 100},
                    {"id": "height", "label": "Height", "unit": "mm", "default": 50}
                ],
                "outputs": [
                    {"id": "area", "label": "Area", "unit": "mm²", "formula": "0.5 * base * height"}
                ]
            },
            "pythagorean": {
                "name": "Pythagorean Theorem",
                "description": "Right triangle sides",
                "inputs": [
                    {"id": "a", "label": "Side a", "unit": "mm", "default": 30},
                    {"id": "b", "label": "Side b", "unit": "mm", "default": 40}
                ],
                "outputs": [
                    {"id": "c", "label": "Hypotenuse c", "unit": "mm", "formula": "Math.sqrt(a**2 + b**2)"}
                ]
            },
            "angle_trig": {
                "name": "Trigonometry",
                "description": "Sin, Cos, Tan",
                "inputs": [
                    {"id": "angle", "label": "Angle", "unit": "°", "default": 45}
                ],
                "outputs": [
                    {"id": "sin", "label": "Sine", "unit": "", "formula": "Math.sin(angle * Math.PI / 180)"},
                    {"id": "cos", "label": "Cosine", "unit": "", "formula": "Math.cos(angle * Math.PI / 180)"},
                    {"id": "tan", "label": "Tangent", "unit": "", "formula": "Math.tan(angle * Math.PI / 180)"}
                ]
            },
            "quadratic": {
                "name": "Quadratic Formula",
                "description": "ax² + bx + c = 0",
                "inputs": [
                    {"id": "a", "label": "a coefficient", "unit": "", "default": 1},
                    {"id": "b", "label": "b coefficient", "unit": "", "default": -5},
                    {"id": "c", "label": "c coefficient", "unit": "", "default": 6}
                ],
                "outputs": [
                    {"id": "discriminant", "label": "Discriminant", "unit": "", "formula": "b**2 - 4*a*c"},
                    {"id": "x1", "label": "x₁", "unit": "", "formula": "(-b + Math.sqrt(b**2 - 4*a*c)) / (2*a)"},
                    {"id": "x2", "label": "x₂", "unit": "", "formula": "(-b - Math.sqrt(b**2 - 4*a*c)) / (2*a)"}
                ]
            }
        }
    },
    "Statistics": {
        "icon": "📊",
        "description": "Statistical calculations",
        "calculators": {
            "mean_std": {
                "name": "Mean (Simple)",
                "description": "Average of values",
                "inputs": [
                    {"id": "v1", "label": "Value 1", "unit": "", "default": 10},
                    {"id": "v2", "label": "Value 2", "unit": "", "default": 20},
                    {"id": "v3", "label": "Value 3", "unit": "", "default": 30},
                    {"id": "v4", "label": "Value 4", "unit": "", "default": 40}
                ],
                "outputs": [
                    {"id": "mean", "label": "Mean", "unit": "", "formula": "(v1 + v2 + v3 + v4) / 4"},
                    {"id": "sum", "label": "Sum", "unit": "", "formula": "v1 + v2 + v3 + v4"}
                ]
            },
            "percentage": {
                "name": "Percentage",
                "description": "Percentage calculations",
                "inputs": [
                    {"id": "part", "label": "Part", "unit": "", "default": 25},
                    {"id": "whole", "label": "Whole", "unit": "", "default": 100}
                ],
                "outputs": [
                    {"id": "percentage", "label": "Percentage", "unit": "%", "formula": "(part / whole) * 100"}
                ]
            },
            "percent_change": {
                "name": "Percentage Change",
                "description": "Change between values",
                "inputs": [
                    {"id": "old_val", "label": "Old Value", "unit": "", "default": 100},
                    {"id": "new_val", "label": "New Value", "unit": "", "default": 120}
                ],
                "outputs": [
                    {"id": "change", "label": "Absolute Change", "unit": "", "formula": "new_val - old_val"},
                    {"id": "pct_change", "label": "Percentage Change", "unit": "%", "formula": "((new_val - old_val) / old_val) * 100"}
                ]
            }
        }
    },
    "Unit Conversion": {
        "icon": "🔄",
        "description": "Common unit conversions",
        "calculators": {
            "length": {
                "name": "Length Conversion",
                "description": "mm, cm, m, in, ft",
                "inputs": [
                    {"id": "mm", "label": "Millimeters", "unit": "mm", "default": 1000}
                ],
                "outputs": [
                    {"id": "cm", "label": "Centimeters", "unit": "cm", "formula": "mm / 10"},
                    {"id": "m", "label": "Meters", "unit": "m", "formula": "mm / 1000"},
                    {"id": "inch", "label": "Inches", "unit": "in", "formula": "mm / 25.4"},
                    {"id": "ft", "label": "Feet", "unit": "ft", "formula": "mm / 304.8"}
                ]
            },
            "speed": {
                "name": "Speed Conversion",
                "description": "m/s, km/h, mph",
                "inputs": [
                    {"id": "ms", "label": "Meters/second", "unit": "m/s", "default": 10}
                ],
                "outputs": [
                    {"id": "kmh", "label": "km/h", "unit": "km/h", "formula": "ms * 3.6"},
                    {"id": "mph", "label": "mph", "unit": "mph", "formula": "ms * 2.237"}
                ]
            },
            "pressure": {
                "name": "Pressure Conversion",
                "description": "Pa, bar, psi, atm",
                "inputs": [
                    {"id": "mpa", "label": "Megapascals", "unit": "MPa", "default": 1}
                ],
                "outputs": [
                    {"id": "pa", "label": "Pascals", "unit": "Pa", "formula": "mpa * 1000000"},
                    {"id": "bar", "label": "Bar", "unit": "bar", "formula": "mpa * 10"},
                    {"id": "psi", "label": "PSI", "unit": "psi", "formula": "mpa * 145.038"},
                    {"id": "atm", "label": "Atmospheres", "unit": "atm", "formula": "mpa / 0.101325"}
                ]
            },
            "temperature": {
                "name": "Temperature Conversion",
                "description": "°C, °F, K",
                "inputs": [
                    {"id": "celsius", "label": "Celsius", "unit": "°C", "default": 25}
                ],
                "outputs": [
                    {"id": "fahrenheit", "label": "Fahrenheit", "unit": "°F", "formula": "celsius * 9/5 + 32"},
                    {"id": "kelvin", "label": "Kelvin", "unit": "K", "formula": "celsius + 273.15"}
                ]
            },
            "torque": {
                "name": "Torque Conversion",
                "description": "N·m, lb·ft",
                "inputs": [
                    {"id": "nm", "label": "Newton-meters", "unit": "N·m", "default": 100}
                ],
                "outputs": [
                    {"id": "lbft", "label": "Pound-feet", "unit": "lb·ft", "formula": "nm * 0.7376"}
                ]
            }
        }
    }
}
