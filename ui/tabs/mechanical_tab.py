"""
Mechanical Engineering Tab
Interactive calculators for structural analysis, materials, and vehicle dynamics.
"""

import customtkinter as ctk
from typing import Optional, Callable
import math

from core.config import COLORS, FSAE_REQUIREMENTS, MATERIAL_DEFAULTS
from calculators.mechanical.structural import (
    circular_tube_properties,
    rectangular_tube_properties,
    flexural_rigidity,
    structural_equivalence,
    fsae_compliance_check,
    FSAE_MINIMUMS,
)
from calculators.mechanical.materials import (
    laminate_elastic_modulus,
    MATERIAL_DATABASE,
)
from calculators.mechanical.fasteners import (
    bolt_stress,
    shear_force_plate,
    get_bolt_areas,
    BOLT_STRESS_AREAS,
)
from calculators.mechanical.beam_analysis import (
    three_point_bending_deflection,
    three_point_bending_stress,
    beam_end_slope,
)
from calculators.mechanical.vehicle_dynamics import (
    max_cornering_velocity_flat,
    max_cornering_velocity_banked,
    skidpad_calculations,
    traction_limit,
    transmission_ratio_from_speed,
    rpm_to_velocity,
    velocity_to_rpm,
)


class MechanicalTab:
    """Tab for mechanical engineering calculators."""

    def __init__(self, parent, app):
        """
        Initialize the mechanical engineering tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color=COLORS['bg_dark'],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)

        # Title
        title_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_medium'], corner_radius=8)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            title_frame,
            text="MECHANICAL ENGINEERING",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['text_white']
        ).pack(pady=10)

        ctk.CTkLabel(
            title_frame,
            text="Structural Analysis | Materials | Vehicle Dynamics",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray']
        ).pack(pady=(0, 10))

        # Create calculator sections in a 2-column layout
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Configure grid
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # Row 0: Tube Properties | FSAE Compliance
        self._create_tube_properties_section(0, 0)
        self._create_fsae_compliance_section(0, 1)

        # Row 1: Laminate Calculator | Beam Bending
        self._create_laminate_section(1, 0)
        self._create_beam_bending_section(1, 1)

        # Row 2: Bolt/Shear Calculator | Skidpad/Cornering
        self._create_fastener_section(2, 0)
        self._create_vehicle_dynamics_section(2, 1)

        # Row 3: Transmission Calculator | Structural Equivalence
        self._create_transmission_section(3, 0)
        self._create_equivalence_section(3, 1)

    def _create_section_frame(self, title: str, row: int, col: int) -> ctk.CTkFrame:
        """Create a standard calculator section frame."""
        frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=8
        )
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Title
        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_highlight']
        ).pack(pady=(10, 5), padx=10, anchor="w")

        return frame

    def _create_input_row(self, parent, label: str, default: str, unit: str = "") -> ctk.CTkEntry:
        """Create a labeled input row."""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(
            row_frame,
            text=label,
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_light'],
            width=180,
            anchor="w"
        ).pack(side="left")

        entry = ctk.CTkEntry(
            row_frame,
            width=100,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            text_color=COLORS['text_white']
        )
        entry.pack(side="left", padx=5)
        entry.insert(0, default)

        if unit:
            ctk.CTkLabel(
                row_frame,
                text=unit,
                font=ctk.CTkFont(size=11),
                text_color=COLORS['text_gray'],
                width=50,
                anchor="w"
            ).pack(side="left")

        return entry

    def _create_output_row(self, parent, label: str, unit: str = "") -> ctk.CTkLabel:
        """Create a labeled output row."""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(
            row_frame,
            text=label,
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray'],
            width=180,
            anchor="w"
        ).pack(side="left")

        value_label = ctk.CTkLabel(
            row_frame,
            text="--",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS['text_white'],
            width=100,
            anchor="w"
        )
        value_label.pack(side="left", padx=5)

        if unit:
            ctk.CTkLabel(
                row_frame,
                text=unit,
                font=ctk.CTkFont(size=11),
                text_color=COLORS['text_gray'],
                width=50,
                anchor="w"
            ).pack(side="left")

        return value_label

    # ========== TUBE PROPERTIES CALCULATOR ==========
    def _create_tube_properties_section(self, row: int, col: int):
        """Create tube properties calculator section."""
        frame = self._create_section_frame("Tube Properties Calculator", row, col)

        # Profile type selector
        type_frame = ctk.CTkFrame(frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            type_frame,
            text="Profile Type:",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_light']
        ).pack(side="left")

        self.tube_type_var = ctk.StringVar(value="circular")
        ctk.CTkSegmentedButton(
            type_frame,
            values=["circular", "rectangular"],
            variable=self.tube_type_var,
            font=ctk.CTkFont(size=10),
            fg_color=COLORS['bg_light'],
            selected_color=COLORS['accent_highlight'],
            selected_hover_color=COLORS['hover']
        ).pack(side="left", padx=10)

        # Inputs
        self.tube_outer = self._create_input_row(frame, "Outer Diameter/Width:", "25", "mm")
        self.tube_thickness = self._create_input_row(frame, "Wall Thickness:", "2.5", "mm")
        self.tube_modulus = self._create_input_row(frame, "Elastic Modulus:", "200", "GPa")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Calculate",
            command=self._calculate_tube_properties,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Outputs
        ctk.CTkLabel(
            frame,
            text="Results:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS['text_light']
        ).pack(anchor="w", padx=10)

        self.tube_area_out = self._create_output_row(frame, "Cross-sectional Area:", "mm2")
        self.tube_inertia_out = self._create_output_row(frame, "Moment of Inertia:", "mm4")
        self.tube_rigidity_out = self._create_output_row(frame, "Flexural Rigidity:", "N.mm2")

    def _calculate_tube_properties(self):
        """Calculate tube section properties."""
        try:
            outer = float(self.tube_outer.get())
            thickness = float(self.tube_thickness.get())
            E = float(self.tube_modulus.get())

            if self.tube_type_var.get() == "circular":
                props = circular_tube_properties(outer, thickness)
            else:
                props = rectangular_tube_properties(outer, outer, thickness)

            EI = flexural_rigidity(props.moment_of_inertia, E)

            self.tube_area_out.configure(text=f"{props.area:.2f}")
            self.tube_inertia_out.configure(text=f"{props.moment_of_inertia:.2f}")
            self.tube_rigidity_out.configure(text=f"{EI:.2e}")

        except Exception as e:
            self.tube_area_out.configure(text="Error")
            self.tube_inertia_out.configure(text=str(e)[:20])

    # ========== FSAE COMPLIANCE CHECKER ==========
    def _create_fsae_compliance_section(self, row: int, col: int):
        """Create FSAE compliance checker section."""
        frame = self._create_section_frame("FSAE Compliance Checker", row, col)

        # Component selector
        comp_frame = ctk.CTkFrame(frame, fg_color="transparent")
        comp_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            comp_frame,
            text="Component:",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_light']
        ).pack(side="left")

        self.fsae_component = ctk.CTkComboBox(
            comp_frame,
            values=list(FSAE_MINIMUMS.keys()),
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            button_color=COLORS['accent_highlight'],
            dropdown_fg_color=COLORS['bg_medium'],
            font=ctk.CTkFont(size=10),
            width=180
        )
        self.fsae_component.pack(side="left", padx=10)
        self.fsae_component.set("main_front_hoops")

        # Inputs
        self.fsae_thickness = self._create_input_row(frame, "Wall Thickness:", "2.5", "mm")
        self.fsae_area = self._create_input_row(frame, "Cross-sectional Area:", "176.7", "mm2")
        self.fsae_inertia = self._create_input_row(frame, "Moment of Inertia:", "11320", "mm4")

        # Check button
        ctk.CTkButton(
            frame,
            text="Check Compliance",
            command=self._check_fsae_compliance,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Result
        self.fsae_result = ctk.CTkLabel(
            frame,
            text="Enter values and click Check",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_gray']
        )
        self.fsae_result.pack(pady=5)

        self.fsae_margin = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_gray']
        )
        self.fsae_margin.pack(pady=(0, 10))

    def _check_fsae_compliance(self):
        """Check FSAE compliance."""
        try:
            component = self.fsae_component.get()
            thickness = float(self.fsae_thickness.get())
            area = float(self.fsae_area.get())
            inertia = float(self.fsae_inertia.get())

            result = fsae_compliance_check(component, thickness, area, inertia)

            if result.passes_all:
                self.fsae_result.configure(
                    text="COMPLIANT",
                    text_color=COLORS['accent_highlight']
                )
            else:
                self.fsae_result.configure(
                    text="NON-COMPLIANT",
                    text_color=COLORS['accent_error']
                )

            margin_text = f"Margins: t={result.margin_thickness:+.1f}% | A={result.margin_area:+.1f}% | I={result.margin_inertia:+.1f}%"
            self.fsae_margin.configure(text=margin_text)

        except Exception as e:
            self.fsae_result.configure(text=f"Error: {str(e)[:30]}", text_color=COLORS['accent_error'])

    # ========== LAMINATE CALCULATOR ==========
    def _create_laminate_section(self, row: int, col: int):
        """Create laminate modulus calculator section."""
        frame = self._create_section_frame("Laminate Elastic Modulus", row, col)

        ctk.CTkLabel(
            frame,
            text="Rule of Mixtures (Voigt Model)",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_gray']
        ).pack(anchor="w", padx=10)

        # Inputs
        self.lam_e_fiber = self._create_input_row(frame, "Fiber Elastic Modulus:", "230", "GPa")
        self.lam_e_matrix = self._create_input_row(frame, "Matrix Elastic Modulus:", "3.5", "GPa")
        self.lam_vf = self._create_input_row(frame, "Fiber Volume Fraction:", "0.6", "")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Calculate",
            command=self._calculate_laminate,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Output
        self.lam_result = self._create_output_row(frame, "Laminate Modulus:", "GPa")

        # Formula display
        ctk.CTkLabel(
            frame,
            text="E = Ef*Vf + Em*Vm",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=COLORS['text_gray']
        ).pack(pady=(5, 10))

    def _calculate_laminate(self):
        """Calculate laminate elastic modulus."""
        try:
            E_f = float(self.lam_e_fiber.get())
            E_m = float(self.lam_e_matrix.get())
            V_f = float(self.lam_vf.get())

            E_lam = laminate_elastic_modulus(E_f, E_m, V_f)
            self.lam_result.configure(text=f"{E_lam:.2f}")

        except Exception as e:
            self.lam_result.configure(text="Error")

    # ========== BEAM BENDING CALCULATOR ==========
    def _create_beam_bending_section(self, row: int, col: int):
        """Create beam bending calculator section."""
        frame = self._create_section_frame("3-Point Bending Analysis", row, col)

        # Inputs
        self.beam_force = self._create_input_row(frame, "Applied Force:", "2500", "N")
        self.beam_span = self._create_input_row(frame, "Span Length:", "500", "mm")
        self.beam_E = self._create_input_row(frame, "Elastic Modulus:", "200000", "MPa")
        self.beam_I = self._create_input_row(frame, "Moment of Inertia:", "16491", "mm4")
        self.beam_c = self._create_input_row(frame, "Outer Fiber Distance:", "12.5", "mm")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Calculate",
            command=self._calculate_beam,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Outputs
        self.beam_deflection = self._create_output_row(frame, "Max Deflection:", "mm")
        self.beam_stress = self._create_output_row(frame, "Max Bending Stress:", "MPa")
        self.beam_slope = self._create_output_row(frame, "End Slope:", "rad")

    def _calculate_beam(self):
        """Calculate beam bending results."""
        try:
            F = float(self.beam_force.get())
            L = float(self.beam_span.get())
            E = float(self.beam_E.get())
            I = float(self.beam_I.get())
            c = float(self.beam_c.get())

            delta = three_point_bending_deflection(F, L, E, I)
            sigma = three_point_bending_stress(F, L, I, c)
            theta = beam_end_slope(F, L, E, I)

            self.beam_deflection.configure(text=f"{delta:.4f}")
            self.beam_stress.configure(text=f"{sigma:.2f}")
            self.beam_slope.configure(text=f"{theta:.6f}")

        except Exception as e:
            self.beam_deflection.configure(text="Error")

    # ========== FASTENER CALCULATOR ==========
    def _create_fastener_section(self, row: int, col: int):
        """Create fastener/shear calculator section."""
        frame = self._create_section_frame("Plate Shear Force Calculator", row, col)

        # Inputs
        self.shear_dia = self._create_input_row(frame, "Applicator Diameter:", "25", "mm")
        self.shear_thick = self._create_input_row(frame, "Plate Thickness:", "1.5", "mm")
        self.shear_strength = self._create_input_row(frame, "Shear Strength:", "280", "MPa")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Calculate",
            command=self._calculate_shear,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Outputs
        self.shear_area = self._create_output_row(frame, "Shear Area:", "mm2")
        self.shear_force = self._create_output_row(frame, "Max Shear Force:", "N")

        # Formula
        ctk.CTkLabel(
            frame,
            text="A = pi*D*t | F = A*tau",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=COLORS['text_gray']
        ).pack(pady=(5, 10))

    def _calculate_shear(self):
        """Calculate shear force."""
        try:
            D = float(self.shear_dia.get())
            t = float(self.shear_thick.get())
            tau = float(self.shear_strength.get())

            area, force = shear_force_plate(D, t, tau)

            self.shear_area.configure(text=f"{area:.2f}")
            self.shear_force.configure(text=f"{force:.2f}")

        except Exception as e:
            self.shear_area.configure(text="Error")

    # ========== VEHICLE DYNAMICS CALCULATOR ==========
    def _create_vehicle_dynamics_section(self, row: int, col: int):
        """Create vehicle dynamics calculator section."""
        frame = self._create_section_frame("Cornering / Skidpad Calculator", row, col)

        # Inputs
        self.corner_mu = self._create_input_row(frame, "Friction Coefficient:", "1.5", "")
        self.corner_radius = self._create_input_row(frame, "Turn Radius:", "9.125", "m")
        self.corner_angle = self._create_input_row(frame, "Bank Angle (if any):", "0", "deg")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Calculate",
            command=self._calculate_cornering,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Outputs
        self.corner_vmax = self._create_output_row(frame, "Max Velocity (flat):", "m/s")
        self.corner_vmax_kmh = self._create_output_row(frame, "Max Velocity (flat):", "km/h")
        self.corner_vbanked = self._create_output_row(frame, "Max Velocity (banked):", "m/s")

    def _calculate_cornering(self):
        """Calculate cornering velocities."""
        try:
            mu = float(self.corner_mu.get())
            r = float(self.corner_radius.get())
            theta = float(self.corner_angle.get())

            v_flat = max_cornering_velocity_flat(mu, r)
            v_flat_kmh = v_flat * 3.6

            self.corner_vmax.configure(text=f"{v_flat:.2f}")
            self.corner_vmax_kmh.configure(text=f"{v_flat_kmh:.2f}")

            if theta > 0:
                v_banked = max_cornering_velocity_banked(theta, r)
                self.corner_vbanked.configure(text=f"{v_banked:.2f}")
            else:
                self.corner_vbanked.configure(text="N/A")

        except Exception as e:
            self.corner_vmax.configure(text="Error")

    # ========== TRANSMISSION CALCULATOR ==========
    def _create_transmission_section(self, row: int, col: int):
        """Create transmission calculator section."""
        frame = self._create_section_frame("Transmission Ratio Calculator", row, col)

        # Inputs
        self.trans_motor_rpm = self._create_input_row(frame, "Motor Max RPM:", "6500", "rpm")
        self.trans_max_speed = self._create_input_row(frame, "Target Max Speed:", "120", "km/h")
        self.trans_tire_radius = self._create_input_row(frame, "Tire Radius:", "0.2057", "m")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Calculate",
            command=self._calculate_transmission,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Outputs
        self.trans_ratio = self._create_output_row(frame, "Required Gear Ratio:", "")
        self.trans_wheel_rpm = self._create_output_row(frame, "Wheel RPM at Max:", "rpm")

    def _calculate_transmission(self):
        """Calculate transmission ratio."""
        try:
            motor_rpm = float(self.trans_motor_rpm.get())
            max_speed_kmh = float(self.trans_max_speed.get())
            tire_r = float(self.trans_tire_radius.get())

            max_speed_ms = max_speed_kmh / 3.6
            ratio = transmission_ratio_from_speed(motor_rpm, max_speed_ms, tire_r)
            wheel_rpm = motor_rpm / ratio

            self.trans_ratio.configure(text=f"{ratio:.2f}")
            self.trans_wheel_rpm.configure(text=f"{wheel_rpm:.1f}")

        except Exception as e:
            self.trans_ratio.configure(text="Error")

    # ========== STRUCTURAL EQUIVALENCE CALCULATOR ==========
    def _create_equivalence_section(self, row: int, col: int):
        """Create structural equivalence calculator section."""
        frame = self._create_section_frame("Structural Equivalence", row, col)

        ctk.CTkLabel(
            frame,
            text="Compare alternative material to steel baseline",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_gray']
        ).pack(anchor="w", padx=10)

        # Reference (Steel)
        ctk.CTkLabel(
            frame,
            text="Reference (Steel):",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS['text_light']
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.eq_e_steel = self._create_input_row(frame, "Elastic Modulus:", "200", "GPa")
        self.eq_i_steel = self._create_input_row(frame, "Moment of Inertia:", "11320", "mm4")

        # Alternative
        ctk.CTkLabel(
            frame,
            text="Alternative Material:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS['text_light']
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.eq_e_alt = self._create_input_row(frame, "Elastic Modulus:", "69", "GPa")
        self.eq_i_alt = self._create_input_row(frame, "Moment of Inertia:", "33666", "mm4")

        # Calculate button
        ctk.CTkButton(
            frame,
            text="Check Equivalence",
            command=self._calculate_equivalence,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28
        ).pack(pady=10)

        # Result
        self.eq_result = ctk.CTkLabel(
            frame,
            text="Enter values and check",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_gray']
        )
        self.eq_result.pack(pady=5)

        self.eq_ratio = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_gray']
        )
        self.eq_ratio.pack(pady=(0, 10))

    def _calculate_equivalence(self):
        """Calculate structural equivalence."""
        try:
            E_steel = float(self.eq_e_steel.get())
            I_steel = float(self.eq_i_steel.get())
            E_alt = float(self.eq_e_alt.get())
            I_alt = float(self.eq_i_alt.get())

            ratio, passes = structural_equivalence(E_steel, I_steel, E_alt, I_alt)

            if passes:
                self.eq_result.configure(
                    text="EQUIVALENT - PASSES",
                    text_color=COLORS['accent_highlight']
                )
            else:
                self.eq_result.configure(
                    text="NOT EQUIVALENT - FAILS",
                    text_color=COLORS['accent_error']
                )

            self.eq_ratio.configure(text=f"Equivalence Ratio: {ratio:.4f} (must be >= 1.0)")

        except Exception as e:
            self.eq_result.configure(text=f"Error: {str(e)[:30]}", text_color=COLORS['accent_error'])
