"""
Live FSAE EV Calculation Suite
Real-Time Engineering Dashboard for ITU Racing

Implements zero-latency feedback - all charts update instantly as sliders move.
No "Calculate" buttons - the system is always live.

Modules:
- A: Pre-Charge & Discharge Safety Calculator
- B: Battery Endurance & Discharge Simulator
- C: Wheatstone Bridge Balancer
- D: Filter Designer (Signal Processing)
"""

import customtkinter as ctk
import numpy as np
import tempfile
import webbrowser
from typing import Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ...core.config import COLORS


class CalculatorsTab:
    """Live FSAE EV Calculation Suite with real-time feedback."""

    def __init__(self, parent, app):
        """
        Initialize the calculators tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app
        self.calc_plot_html = None

        # Debounce timer for slider updates
        self._update_pending = False

        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        # Header
        header = ctk.CTkLabel(
            self.parent,
            text="Live FSAE EV Calculation Suite",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['accent_red']
        )
        header.pack(pady=(5, 0))

        subtitle = ctk.CTkLabel(
            self.parent,
            text="Real-Time Engineering Dashboard | Zero-Latency Feedback",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['accent_green']
        )
        subtitle.pack(pady=(0, 5))

        # Create sub-tabview for different calculators
        self.calc_tabview = ctk.CTkTabview(
            self.parent,
            fg_color=COLORS['bg_medium'],
            segmented_button_fg_color=COLORS['bg_light'],
            segmented_button_selected_color=COLORS['accent_red'],
            segmented_button_unselected_color=COLORS['bg_light'],
            text_color=COLORS['text_white']
        )
        self.calc_tabview.pack(fill="both", expand=True, padx=10, pady=5)

        # Add calculator tabs per spec
        self.precharge_tab = self.calc_tabview.add("A: Pre-Charge/Discharge")
        self.battery_tab = self.calc_tabview.add("B: Battery Endurance")
        self.bridge_tab = self.calc_tabview.add("C: Wheatstone Bridge")
        self.filter_tab = self.calc_tabview.add("D: Filter Designer")

        # Setup each calculator module
        self._setup_precharge_module()
        self._setup_battery_module()
        self._setup_bridge_module()
        self._setup_filter_module()

    # ==================== MODULE A: PRE-CHARGE & DISCHARGE ====================

    def _setup_precharge_module(self):
        """Setup Pre-Charge & Discharge Safety Calculator (Module A)."""
        main_frame = ctk.CTkFrame(self.precharge_tab, fg_color=COLORS['bg_light'], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10, width=350)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)

        ctk.CTkLabel(
            left_panel,
            text="Pre-Charge & Discharge Safety",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_green']
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            left_panel,
            text="FSAE EV.5.5 Compliance Check",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray']
        ).pack(pady=(0, 15))

        # Bus Voltage slider [0-600V]
        self._create_slider_control(
            left_panel, "Bus Voltage (Vbus)", "V",
            0, 600, 400, "precharge_vbus", self._update_precharge
        )

        # Total Capacitance input
        cap_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        cap_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(cap_frame, text="Total Capacitance (uF):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.precharge_cap = ctk.CTkEntry(cap_frame, width=80)
        self.precharge_cap.insert(0, "1000")
        self.precharge_cap.pack(side="right")
        self.precharge_cap.bind("<KeyRelease>", lambda e: self._update_precharge())

        # Pre-Charge Resistor slider [100-5000 Ohm]
        self._create_slider_control(
            left_panel, "Pre-Charge Resistor (Rpre)", "Ohm",
            100, 5000, 1000, "precharge_rpre", self._update_precharge
        )

        # Discharge Resistor slider [1000-50000 Ohm]
        self._create_slider_control(
            left_panel, "Discharge Resistor (Rdis)", "Ohm",
            1000, 50000, 10000, "precharge_rdis", self._update_precharge
        )

        # Resistor Power Rating
        pwr_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        pwr_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(pwr_frame, text="Resistor Power Rating (W):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.precharge_pwr = ctk.CTkEntry(pwr_frame, width=80)
        self.precharge_pwr.insert(0, "50")
        self.precharge_pwr.pack(side="right")
        self.precharge_pwr.bind("<KeyRelease>", lambda e: self._update_precharge())

        # Safety status display
        self.precharge_safety_frame = ctk.CTkFrame(left_panel, fg_color=COLORS['bg_dark'], corner_radius=10)
        self.precharge_safety_frame.pack(fill="x", padx=15, pady=15)

        self.precharge_status = ctk.CTkLabel(
            self.precharge_safety_frame,
            text="Safety Status: Calculating...",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS['accent_green']
        )
        self.precharge_status.pack(pady=10, padx=10)

        self.precharge_details = ctk.CTkLabel(
            self.precharge_safety_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray'],
            justify="left"
        )
        self.precharge_details.pack(pady=(0, 10), padx=10)

        # Right panel - Plot
        right_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.precharge_plot_btn = ctk.CTkButton(
            right_panel, text="Open Interactive Plot in Browser",
            command=lambda: self._open_plot("precharge"),
            fg_color=COLORS['accent_blue'],
            state="disabled"
        )
        self.precharge_plot_btn.pack(pady=10)

        self.precharge_info = ctk.CTkLabel(
            right_panel,
            text="Adjust sliders to see real-time updates",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray']
        )
        self.precharge_info.pack(pady=5)

        # Initial calculation
        self.parent.after(100, self._update_precharge)

    def _update_precharge(self, *args):
        """Update pre-charge/discharge calculations in real-time."""
        try:
            vbus = float(getattr(self, 'precharge_vbus_var', ctk.DoubleVar(value=400)).get())
            cap = float(self.precharge_cap.get()) * 1e-6  # uF to F
            rpre = float(getattr(self, 'precharge_rpre_var', ctk.DoubleVar(value=1000)).get())
            rdis = float(getattr(self, 'precharge_rdis_var', ctk.DoubleVar(value=10000)).get())
            pwr_rating = float(self.precharge_pwr.get())

            # Calculate time constants
            tau_pre = rpre * cap
            tau_dis = rdis * cap

            # Time arrays (5 tau for full charge/discharge)
            t_pre = np.linspace(0, 5 * tau_pre, 500)
            t_dis = np.linspace(0, 5 * tau_dis, 500)

            # Voltage curves
            v_charge = vbus * (1 - np.exp(-t_pre / tau_pre))
            v_discharge = vbus * np.exp(-t_dis / tau_dis)

            # Safety calculations
            time_to_95 = -tau_pre * np.log(0.05)  # Time to 95% charge
            time_to_60v = -tau_dis * np.log(60 / vbus) if vbus > 60 else 0  # Time to 60V

            # Peak power during pre-charge (at t=0, I = Vbus/R)
            peak_current = vbus / rpre
            peak_power = peak_current ** 2 * rpre

            # Energy stored
            energy = 0.5 * cap * vbus ** 2

            # Safety checks
            warnings = []
            status_color = COLORS['accent_green']
            status_text = "PASS"

            if time_to_60v > 5.0:
                warnings.append(f"FAIL: Discharge to 60V takes {time_to_60v:.2f}s (>5s per EV.5.5)")
                status_color = COLORS['accent_red']
                status_text = "FAIL"

            if peak_power > pwr_rating:
                warnings.append(f"WARNING: Peak power {peak_power:.1f}W exceeds {pwr_rating}W rating")
                if status_text != "FAIL":
                    status_color = COLORS['accent_yellow']
                    status_text = "WARNING"

            # Update status display
            self.precharge_status.configure(
                text=f"Safety Status: {status_text}",
                text_color=status_color
            )

            details = f"Tau (pre-charge): {tau_pre*1000:.2f} ms\n"
            details += f"Tau (discharge): {tau_dis*1000:.2f} ms\n"
            details += f"Time to 95%: {time_to_95*1000:.2f} ms\n"
            details += f"Time to 60V: {time_to_60v:.3f} s\n"
            details += f"Peak Current: {peak_current:.2f} A\n"
            details += f"Peak Power: {peak_power:.1f} W\n"
            details += f"Energy Stored: {energy:.2f} J\n"
            if warnings:
                details += "\n" + "\n".join(warnings)

            self.precharge_details.configure(text=details)

            # Create plot
            fig = make_subplots(rows=1, cols=1)

            # Charging curve (green)
            fig.add_trace(go.Scatter(
                x=t_pre * 1000, y=v_charge,
                mode='lines', name='Charging (Pre-charge)',
                line=dict(color='#4ecca3', width=2)
            ))

            # Discharging curve (red)
            fig.add_trace(go.Scatter(
                x=t_dis * 1000, y=v_discharge,
                mode='lines', name='Discharging',
                line=dict(color='#e94560', width=2)
            ))

            # 95% voltage line
            fig.add_hline(y=vbus * 0.95, line_dash="dash", line_color="#f39c12",
                         annotation_text=f"95% ({vbus*0.95:.0f}V)")

            # 60V safety threshold
            fig.add_hline(y=60, line_dash="dash", line_color="#e74c3c",
                         annotation_text="60V Safety Threshold")

            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor=COLORS['bg_dark'],
                plot_bgcolor=COLORS['bg_light'],
                title=dict(text="Pre-Charge & Discharge Curves", font=dict(size=18, color=COLORS['accent_green'])),
                xaxis_title="Time (ms)",
                yaxis_title="Voltage (V)",
                height=500,
                showlegend=True,
                legend=dict(x=0.7, y=0.95)
            )

            # Save plot
            self.precharge_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.precharge_plot_html)
            self.precharge_plot_btn.configure(state="normal")

        except Exception as e:
            self.precharge_details.configure(text=f"Error: {str(e)}")

    # ==================== MODULE B: BATTERY ENDURANCE ====================

    def _setup_battery_module(self):
        """Setup Battery Endurance & Discharge Simulator (Module B)."""
        main_frame = ctk.CTkFrame(self.battery_tab, fg_color=COLORS['bg_light'], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10, width=380)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)

        ctk.CTkLabel(
            left_panel,
            text="Battery Endurance Simulator",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_yellow']
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            left_panel,
            text="Endurance Event Runtime & Thermal Analysis",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray']
        ).pack(pady=(0, 15))

        # Cell Configuration
        config_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        config_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(config_frame, text="Series (S):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.battery_series = ctk.CTkEntry(config_frame, width=60)
        self.battery_series.insert(0, "96")
        self.battery_series.pack(side="left", padx=(5, 15))
        self.battery_series.bind("<KeyRelease>", lambda e: self._update_battery())

        ctk.CTkLabel(config_frame, text="Parallel (P):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.battery_parallel = ctk.CTkEntry(config_frame, width=60)
        self.battery_parallel.insert(0, "4")
        self.battery_parallel.pack(side="left", padx=5)
        self.battery_parallel.bind("<KeyRelease>", lambda e: self._update_battery())

        # Cell Parameters
        cell_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        cell_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(cell_frame, text="Cell Capacity (Ah):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.battery_cell_cap = ctk.CTkEntry(cell_frame, width=60)
        self.battery_cell_cap.insert(0, "3.0")
        self.battery_cell_cap.pack(side="left", padx=(5, 15))
        self.battery_cell_cap.bind("<KeyRelease>", lambda e: self._update_battery())

        ctk.CTkLabel(cell_frame, text="R_int (mOhm):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.battery_rint = ctk.CTkEntry(cell_frame, width=60)
        self.battery_rint.insert(0, "15")
        self.battery_rint.pack(side="left", padx=5)
        self.battery_rint.bind("<KeyRelease>", lambda e: self._update_battery())

        # Average Current slider
        self._create_slider_control(
            left_panel, "Average Current", "A",
            10, 200, 80, "battery_avg_current", self._update_battery
        )

        # Peak Current slider
        self._create_slider_control(
            left_panel, "Peak Current", "A",
            50, 400, 200, "battery_peak_current", self._update_battery
        )

        # Simulation Time slider
        self._create_slider_control(
            left_panel, "Simulation Time", "min",
            5, 60, 30, "battery_sim_time", self._update_battery
        )

        # SoC Range
        soc_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        soc_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(soc_frame, text="SoC Start (%):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.battery_soc_start = ctk.CTkEntry(soc_frame, width=50)
        self.battery_soc_start.insert(0, "100")
        self.battery_soc_start.pack(side="left", padx=(5, 10))
        self.battery_soc_start.bind("<KeyRelease>", lambda e: self._update_battery())

        ctk.CTkLabel(soc_frame, text="SoC End (%):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.battery_soc_end = ctk.CTkEntry(soc_frame, width=50)
        self.battery_soc_end.insert(0, "20")
        self.battery_soc_end.pack(side="left", padx=5)
        self.battery_soc_end.bind("<KeyRelease>", lambda e: self._update_battery())

        # KPI Cards
        kpi_frame = ctk.CTkFrame(left_panel, fg_color=COLORS['bg_dark'], corner_radius=10)
        kpi_frame.pack(fill="x", padx=15, pady=15)

        self.battery_runtime_label = ctk.CTkLabel(
            kpi_frame,
            text="Time to Empty: -- min",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_green']
        )
        self.battery_runtime_label.pack(pady=(10, 5))

        self.battery_heat_label = ctk.CTkLabel(
            kpi_frame,
            text="Total Heat Waste: -- kW",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_yellow']
        )
        self.battery_heat_label.pack(pady=(5, 10))

        self.battery_details = ctk.CTkLabel(
            kpi_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray'],
            justify="left"
        )
        self.battery_details.pack(pady=(0, 10), padx=10)

        # Right panel - Plot
        right_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.battery_plot_btn = ctk.CTkButton(
            right_panel, text="Open Interactive Plot in Browser",
            command=lambda: self._open_plot("battery"),
            fg_color=COLORS['accent_blue'],
            state="disabled"
        )
        self.battery_plot_btn.pack(pady=10)

        # Initial calculation
        self.parent.after(200, self._update_battery)

    def _update_battery(self, *args):
        """Update battery simulation in real-time."""
        try:
            series = int(self.battery_series.get())
            parallel = int(self.battery_parallel.get())
            cell_cap = float(self.battery_cell_cap.get())
            r_int = float(self.battery_rint.get()) * 1e-3  # mOhm to Ohm
            avg_current = float(getattr(self, 'battery_avg_current_var', ctk.DoubleVar(value=80)).get())
            peak_current = float(getattr(self, 'battery_peak_current_var', ctk.DoubleVar(value=200)).get())
            sim_time = float(getattr(self, 'battery_sim_time_var', ctk.DoubleVar(value=30)).get())
            soc_start = float(self.battery_soc_start.get()) / 100
            soc_end = float(self.battery_soc_end.get()) / 100

            # Pack calculations
            pack_capacity = cell_cap * parallel  # Ah
            total_cells = series * parallel
            nominal_cell_v = 3.7  # Typical Li-ion
            pack_voltage_nom = series * nominal_cell_v

            # Runtime calculation
            usable_capacity = pack_capacity * (soc_start - soc_end)
            runtime_hours = usable_capacity / avg_current
            runtime_mins = runtime_hours * 60

            # Heat generation (Joule heating)
            # P_heat = I_rms^2 * R_internal * N_cells
            # Approximate I_rms from avg and peak
            i_rms = np.sqrt((avg_current ** 2 + peak_current ** 2) / 2)
            heat_power = i_rms ** 2 * r_int * total_cells / 1000  # kW

            # Simulation arrays
            time_array = np.linspace(0, sim_time, 500)

            # Voltage drop over time (simplified model)
            soc_array = soc_start - (avg_current / pack_capacity) * (time_array / 60)
            soc_array = np.maximum(soc_array, soc_end)

            # Voltage curve (simplified: V = V_full - drop * (1-SoC))
            v_full = 4.2 * series
            v_empty = 3.0 * series
            voltage_array = v_full - (v_full - v_empty) * (1 - soc_array)
            voltage_array = voltage_array - avg_current * r_int * series  # IR drop

            # Temperature rise (simplified thermal model)
            # Assume thermal mass and cooling
            thermal_mass = 0.5  # kJ/K per cell approx
            cooling_rate = 0.01  # kW/K
            ambient = 25  # C

            temp_array = np.zeros_like(time_array)
            temp_array[0] = ambient
            dt = time_array[1] - time_array[0]
            for i in range(1, len(time_array)):
                heat_in = heat_power * dt * 60  # kJ
                heat_out = cooling_rate * (temp_array[i-1] - ambient) * dt * 60
                delta_t = (heat_in - heat_out) / (thermal_mass * total_cells)
                temp_array[i] = temp_array[i-1] + delta_t

            # Update KPI cards
            runtime_color = COLORS['accent_red'] if runtime_mins < 22 else COLORS['accent_green']
            self.battery_runtime_label.configure(
                text=f"Time to Empty: {runtime_mins:.1f} min",
                text_color=runtime_color
            )
            self.battery_heat_label.configure(
                text=f"Total Heat Waste: {heat_power:.2f} kW"
            )

            details = f"Pack: {series}S{parallel}P = {total_cells} cells\n"
            details += f"Pack Capacity: {pack_capacity:.1f} Ah\n"
            details += f"Nominal Voltage: {pack_voltage_nom:.0f} V\n"
            details += f"Total Energy: {pack_capacity * pack_voltage_nom / 1000:.2f} kWh\n"
            details += f"I_rms estimate: {i_rms:.1f} A"
            self.battery_details.configure(text=details)

            # Create dual-axis plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Voltage trace (left axis)
            fig.add_trace(
                go.Scatter(x=time_array, y=voltage_array, name="Pack Voltage",
                          line=dict(color=COLORS['accent_yellow'], width=2)),
                secondary_y=False
            )

            # Temperature trace (right axis)
            fig.add_trace(
                go.Scatter(x=time_array, y=temp_array, name="Pack Temperature",
                          line=dict(color=COLORS['accent_red'], width=2)),
                secondary_y=True
            )

            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor=COLORS['bg_dark'],
                plot_bgcolor=COLORS['bg_light'],
                title=dict(text=f"Battery Endurance Simulation ({series}S{parallel}P)",
                          font=dict(size=18, color=COLORS['accent_yellow'])),
                xaxis_title="Time (minutes)",
                height=500,
                legend=dict(x=0.7, y=0.95)
            )

            fig.update_yaxes(title_text="Pack Voltage (V)", secondary_y=False,
                           color=COLORS['accent_yellow'])
            fig.update_yaxes(title_text="Temperature (C)", secondary_y=True,
                           color=COLORS['accent_red'])

            # Save plot
            self.battery_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.battery_plot_html)
            self.battery_plot_btn.configure(state="normal")

        except Exception as e:
            self.battery_details.configure(text=f"Error: {str(e)}")

    # ==================== MODULE C: WHEATSTONE BRIDGE ====================

    def _setup_bridge_module(self):
        """Setup Wheatstone Bridge Balancer (Module C)."""
        main_frame = ctk.CTkFrame(self.bridge_tab, fg_color=COLORS['bg_light'], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10, width=380)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)

        ctk.CTkLabel(
            left_panel,
            text="Wheatstone Bridge Balancer",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_purple']
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            left_panel,
            text="Strain Gauge / Load Cell Signal Conditioning",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray']
        ).pack(pady=(0, 15))

        # Source Voltage
        vsrc_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        vsrc_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(vsrc_frame, text="Source Voltage:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.bridge_vsource = ctk.StringVar(value="5.0")
        ctk.CTkOptionMenu(
            vsrc_frame, values=["3.3", "5.0", "10.0"],
            variable=self.bridge_vsource,
            fg_color=COLORS['accent_purple'],
            command=lambda v: self._update_bridge()
        ).pack(side="right")

        # Known Resistors R1, R3
        r1_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        r1_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(r1_frame, text="R1 (Ohm):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.bridge_r1 = ctk.CTkEntry(r1_frame, width=80)
        self.bridge_r1.insert(0, "1000")
        self.bridge_r1.pack(side="right")
        self.bridge_r1.bind("<KeyRelease>", lambda e: self._update_bridge())

        r3_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        r3_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(r3_frame, text="R3 (Ohm):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.bridge_r3 = ctk.CTkEntry(r3_frame, width=80)
        self.bridge_r3.insert(0, "1000")
        self.bridge_r3.pack(side="right")
        self.bridge_r3.bind("<KeyRelease>", lambda e: self._update_bridge())

        # Balancing Resistor R2 (Fine-tune slider)
        self._create_slider_control(
            left_panel, "Balancing Resistor R2", "Ohm",
            100, 10000, 1000, "bridge_r2", self._update_bridge
        )

        # Sensor Range Rx
        rx_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        rx_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(rx_frame, text="Rx Min (Ohm):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.bridge_rx_min = ctk.CTkEntry(rx_frame, width=70)
        self.bridge_rx_min.insert(0, "900")
        self.bridge_rx_min.pack(side="left", padx=5)
        self.bridge_rx_min.bind("<KeyRelease>", lambda e: self._update_bridge())

        ctk.CTkLabel(rx_frame, text="Max:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.bridge_rx_max = ctk.CTkEntry(rx_frame, width=70)
        self.bridge_rx_max.insert(0, "1100")
        self.bridge_rx_max.pack(side="left", padx=5)
        self.bridge_rx_max.bind("<KeyRelease>", lambda e: self._update_bridge())

        # Needle Gauge Display
        gauge_frame = ctk.CTkFrame(left_panel, fg_color=COLORS['bg_dark'], corner_radius=10)
        gauge_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            gauge_frame, text="Bridge Output (Vg)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_gray']
        ).pack(pady=(10, 5))

        self.bridge_vg_label = ctk.CTkLabel(
            gauge_frame,
            text="Vg = 0.000 mV",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['accent_green']
        )
        self.bridge_vg_label.pack(pady=5)

        self.bridge_balance_label = ctk.CTkLabel(
            gauge_frame,
            text="BALANCED",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_green']
        )
        self.bridge_balance_label.pack(pady=(5, 10))

        self.bridge_details = ctk.CTkLabel(
            gauge_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray'],
            justify="left"
        )
        self.bridge_details.pack(pady=(0, 10), padx=10)

        # Right panel - Plot
        right_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.bridge_plot_btn = ctk.CTkButton(
            right_panel, text="Open Linearity Plot in Browser",
            command=lambda: self._open_plot("bridge"),
            fg_color=COLORS['accent_blue'],
            state="disabled"
        )
        self.bridge_plot_btn.pack(pady=10)

        # Initial calculation
        self.parent.after(300, self._update_bridge)

    def _update_bridge(self, *args):
        """Update Wheatstone bridge calculations in real-time."""
        try:
            vsource = float(self.bridge_vsource.get())
            r1 = float(self.bridge_r1.get())
            r3 = float(self.bridge_r3.get())
            r2 = float(getattr(self, 'bridge_r2_var', ctk.DoubleVar(value=1000)).get())
            rx_min = float(self.bridge_rx_min.get())
            rx_max = float(self.bridge_rx_max.get())

            # Calculate Vg for current R2 (with Rx at midpoint)
            rx_mid = (rx_min + rx_max) / 2
            vg = vsource * (rx_mid / (r3 + rx_mid) - r2 / (r1 + r2))
            vg_mv = vg * 1000

            # Balance condition: R1/R2 = R3/Rx => Rx_balance = R3 * R2 / R1
            rx_balance = r3 * r2 / r1

            # Update gauge display
            if abs(vg_mv) < 1:
                balance_text = "BALANCED"
                balance_color = COLORS['accent_green']
            elif abs(vg_mv) < 10:
                balance_text = "NEAR BALANCE"
                balance_color = COLORS['accent_yellow']
            else:
                balance_text = "UNBALANCED"
                balance_color = COLORS['accent_red']

            self.bridge_vg_label.configure(
                text=f"Vg = {vg_mv:.3f} mV",
                text_color=balance_color
            )
            self.bridge_balance_label.configure(
                text=balance_text,
                text_color=balance_color
            )

            details = f"R2 for balance at Rx={rx_mid:.0f}: {r1*rx_mid/r3:.1f} Ohm\n"
            details += f"Rx at balance with R2={r2:.0f}: {rx_balance:.1f} Ohm\n"
            details += f"Sensitivity: {vsource*r3/((r3+rx_mid)**2)*1000:.4f} mV/Ohm"
            self.bridge_details.configure(text=details)

            # Linearity plot
            rx_array = np.linspace(rx_min, rx_max, 200)
            vout_array = vsource * (rx_array / (r3 + rx_array) - r2 / (r1 + r2))

            # Linear fit for linearity analysis
            delta_r = rx_array - rx_mid
            coeffs = np.polyfit(delta_r, vout_array, 1)
            linear_fit = np.polyval(coeffs, delta_r)
            linearity_error = (vout_array - linear_fit) * 1000  # mV

            fig = make_subplots(rows=2, cols=1, subplot_titles=(
                "Vout vs Rx", "Linearity Error"
            ), vertical_spacing=0.15)

            # Vout vs Rx
            fig.add_trace(
                go.Scatter(x=rx_array, y=vout_array * 1000, name="Vout",
                          line=dict(color=COLORS['accent_purple'], width=2)),
                row=1, col=1
            )

            # Linear range highlight (within 1% linearity)
            linear_mask = np.abs(linearity_error) < np.max(np.abs(vout_array)) * 10  # 1% of range
            fig.add_trace(
                go.Scatter(x=rx_array[linear_mask], y=vout_array[linear_mask] * 1000,
                          mode='lines', name="Linear Range",
                          line=dict(color=COLORS['accent_green'], width=4),
                          opacity=0.5),
                row=1, col=1
            )

            # Linearity error
            fig.add_trace(
                go.Scatter(x=delta_r, y=linearity_error, name="Error",
                          line=dict(color=COLORS['accent_red'], width=2)),
                row=2, col=1
            )

            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor=COLORS['bg_dark'],
                plot_bgcolor=COLORS['bg_light'],
                title=dict(text="Wheatstone Bridge Linearity Analysis",
                          font=dict(size=18, color=COLORS['accent_purple'])),
                height=550,
                showlegend=True
            )

            fig.update_xaxes(title_text="Rx (Ohm)", row=1, col=1)
            fig.update_yaxes(title_text="Vout (mV)", row=1, col=1)
            fig.update_xaxes(title_text="Delta R (Ohm)", row=2, col=1)
            fig.update_yaxes(title_text="Error (mV)", row=2, col=1)

            # Save plot
            self.bridge_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.bridge_plot_html)
            self.bridge_plot_btn.configure(state="normal")

        except Exception as e:
            self.bridge_details.configure(text=f"Error: {str(e)}")

    # ==================== MODULE D: FILTER DESIGNER ====================

    def _setup_filter_module(self):
        """Setup Filter Designer (Module D)."""
        main_frame = ctk.CTkFrame(self.filter_tab, fg_color=COLORS['bg_light'], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10, width=380)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)

        ctk.CTkLabel(
            left_panel,
            text="RC Filter Designer",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_orange']
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            left_panel,
            text="Low-Pass Filter for Sensor Signal Conditioning",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray']
        ).pack(pady=(0, 15))

        # Target Cutoff Frequency slider [1 Hz - 20 kHz]
        self._create_slider_control(
            left_panel, "Target Cutoff Freq (fc)", "Hz",
            1, 20000, 1000, "filter_fc", self._update_filter, log_scale=True
        )

        # Noise Frequency slider
        self._create_slider_control(
            left_panel, "Noise Frequency", "Hz",
            50, 50000, 10000, "filter_noise", self._update_filter, log_scale=True
        )

        # Signal Frequency slider
        self._create_slider_control(
            left_panel, "Signal Frequency", "Hz",
            1, 1000, 50, "filter_signal", self._update_filter
        )

        # Snap to E24 values
        self.filter_snap_e24 = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            left_panel, text="Snap to Standard E24 Values",
            variable=self.filter_snap_e24,
            fg_color=COLORS['accent_orange'],
            command=self._update_filter
        ).pack(pady=10, padx=15, anchor="w")

        # Component display
        comp_frame = ctk.CTkFrame(left_panel, fg_color=COLORS['bg_dark'], corner_radius=10)
        comp_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            comp_frame, text="Calculated Components",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_gray']
        ).pack(pady=(10, 5))

        self.filter_r_label = ctk.CTkLabel(
            comp_frame,
            text="R = -- Ohm",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_orange']
        )
        self.filter_r_label.pack(pady=2)

        self.filter_c_label = ctk.CTkLabel(
            comp_frame,
            text="C = -- nF",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_orange']
        )
        self.filter_c_label.pack(pady=2)

        self.filter_actual_fc = ctk.CTkLabel(
            comp_frame,
            text="Actual fc = -- Hz",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['accent_green']
        )
        self.filter_actual_fc.pack(pady=(5, 10))

        self.filter_attenuation = ctk.CTkLabel(
            comp_frame,
            text="Noise Attenuation: -- dB",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray']
        )
        self.filter_attenuation.pack(pady=(0, 10))

        # Right panel - Plot
        right_panel = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.filter_plot_btn = ctk.CTkButton(
            right_panel, text="Open Bode Plot & Signal Preview in Browser",
            command=lambda: self._open_plot("filter"),
            fg_color=COLORS['accent_blue'],
            state="disabled"
        )
        self.filter_plot_btn.pack(pady=10)

        # Initial calculation
        self.parent.after(400, self._update_filter)

    def _update_filter(self, *args):
        """Update filter design in real-time."""
        try:
            fc_target = float(getattr(self, 'filter_fc_var', ctk.DoubleVar(value=1000)).get())
            noise_freq = float(getattr(self, 'filter_noise_var', ctk.DoubleVar(value=10000)).get())
            signal_freq = float(getattr(self, 'filter_signal_var', ctk.DoubleVar(value=50)).get())
            snap_e24 = self.filter_snap_e24.get()

            # E24 standard values
            e24_mult = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

            def find_nearest_e24(value):
                """Find nearest E24 standard value."""
                if value <= 0:
                    return 1.0
                decade = 10 ** np.floor(np.log10(value))
                normalized = value / decade
                nearest = min(e24_mult, key=lambda x: abs(x - normalized))
                return nearest * decade

            # Design for fc = 1/(2*pi*R*C)
            # Start with R = 10k, solve for C
            r_ideal = 10000  # 10k default
            c_ideal = 1 / (2 * np.pi * fc_target * r_ideal)

            if snap_e24:
                r = find_nearest_e24(r_ideal)
                c = find_nearest_e24(c_ideal * 1e9) * 1e-9  # Work in nF for E24
            else:
                r = r_ideal
                c = c_ideal

            # Actual cutoff
            fc_actual = 1 / (2 * np.pi * r * c)

            # Format component values
            if c < 1e-9:
                c_str = f"{c*1e12:.1f} pF"
            elif c < 1e-6:
                c_str = f"{c*1e9:.1f} nF"
            else:
                c_str = f"{c*1e6:.2f} uF"

            if r >= 1e6:
                r_str = f"{r/1e6:.2f} MOhm"
            elif r >= 1e3:
                r_str = f"{r/1e3:.2f} kOhm"
            else:
                r_str = f"{r:.1f} Ohm"

            self.filter_r_label.configure(text=f"R = {r_str}")
            self.filter_c_label.configure(text=f"C = {c_str}")
            self.filter_actual_fc.configure(text=f"Actual fc = {fc_actual:.1f} Hz")

            # Calculate attenuation at noise frequency
            h_noise = 1 / np.sqrt(1 + (noise_freq / fc_actual) ** 2)
            attenuation_db = 20 * np.log10(h_noise)
            self.filter_attenuation.configure(text=f"Noise Attenuation: {attenuation_db:.1f} dB")

            # Create Bode plot and signal preview
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=("Magnitude Response", "Phase Response", "Signal Preview"),
                vertical_spacing=0.1,
                row_heights=[0.3, 0.3, 0.4]
            )

            # Frequency array (log scale)
            freq = np.logspace(0, 5, 500)  # 1 Hz to 100 kHz

            # Transfer function: H(f) = 1 / (1 + j*f/fc)
            h = 1 / (1 + 1j * freq / fc_actual)
            magnitude_db = 20 * np.log10(np.abs(h))
            phase_deg = np.angle(h, deg=True)

            # Magnitude plot
            fig.add_trace(
                go.Scatter(x=freq, y=magnitude_db, name="Magnitude",
                          line=dict(color=COLORS['accent_orange'], width=2)),
                row=1, col=1
            )
            fig.add_vline(x=fc_actual, line_dash="dash", line_color=COLORS['accent_green'],
                         annotation_text=f"fc={fc_actual:.0f}Hz", row=1, col=1)
            fig.add_vline(x=noise_freq, line_dash="dot", line_color=COLORS['accent_red'],
                         annotation_text=f"Noise", row=1, col=1)
            fig.add_hline(y=-3, line_dash="dot", line_color=COLORS['text_gray'],
                         annotation_text="-3dB", row=1, col=1)

            # Phase plot
            fig.add_trace(
                go.Scatter(x=freq, y=phase_deg, name="Phase",
                          line=dict(color=COLORS['accent_yellow'], width=2)),
                row=2, col=1
            )

            # Signal preview (time domain)
            t = np.linspace(0, 5 / signal_freq, 1000)  # 5 periods

            # Input: signal + noise
            signal_in = np.sin(2 * np.pi * signal_freq * t)
            noise_in = 0.3 * np.sin(2 * np.pi * noise_freq * t)
            input_signal = signal_in + noise_in

            # Output: apply filter transfer function
            h_signal = 1 / np.sqrt(1 + (signal_freq / fc_actual) ** 2)
            h_noise_out = 1 / np.sqrt(1 + (noise_freq / fc_actual) ** 2)
            phase_signal = -np.arctan(signal_freq / fc_actual)
            phase_noise = -np.arctan(noise_freq / fc_actual)

            output_signal = (h_signal * np.sin(2 * np.pi * signal_freq * t + phase_signal) +
                           0.3 * h_noise_out * np.sin(2 * np.pi * noise_freq * t + phase_noise))

            fig.add_trace(
                go.Scatter(x=t * 1000, y=input_signal, name="Input (Noisy)",
                          line=dict(color=COLORS['accent_red'], width=1), opacity=0.7),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=t * 1000, y=output_signal, name="Output (Filtered)",
                          line=dict(color=COLORS['accent_green'], width=2)),
                row=3, col=1
            )

            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor=COLORS['bg_dark'],
                plot_bgcolor=COLORS['bg_light'],
                title=dict(text="RC Low-Pass Filter Design",
                          font=dict(size=18, color=COLORS['accent_orange'])),
                height=700,
                showlegend=True
            )

            fig.update_xaxes(type="log", title_text="Frequency (Hz)", row=1, col=1)
            fig.update_xaxes(type="log", title_text="Frequency (Hz)", row=2, col=1)
            fig.update_xaxes(title_text="Time (ms)", row=3, col=1)

            fig.update_yaxes(title_text="Magnitude (dB)", row=1, col=1, range=[-60, 5])
            fig.update_yaxes(title_text="Phase (deg)", row=2, col=1)
            fig.update_yaxes(title_text="Amplitude", row=3, col=1)

            # Save plot
            self.filter_plot_html = tempfile.NamedTemporaryFile(
                mode='w', suffix='.html', delete=False
            ).name
            fig.write_html(self.filter_plot_html)
            self.filter_plot_btn.configure(state="normal")

        except Exception as e:
            self.filter_c_label.configure(text=f"Error: {str(e)}")

    # ==================== UTILITY METHODS ====================

    def _create_slider_control(self, parent, label, unit, min_val, max_val, default,
                               var_name, callback, log_scale=False):
        """Create a labeled slider with real-time value display."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=8)

        # Label with current value
        value_var = ctk.DoubleVar(value=default)
        setattr(self, f"{var_name}_var", value_var)

        label_text = ctk.StringVar(value=f"{label}: {default:.0f} {unit}")
        setattr(self, f"{var_name}_label", label_text)

        ctk.CTkLabel(
            frame, textvariable=label_text,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        # Slider
        def on_slider_change(value):
            if log_scale:
                # Convert linear slider to log scale
                actual_value = min_val * (max_val / min_val) ** (float(value) / 100)
            else:
                actual_value = float(value)

            value_var.set(actual_value)
            label_text.set(f"{label}: {actual_value:.0f} {unit}")
            callback()

        if log_scale:
            # For log scale, slider goes 0-100 and we convert
            default_slider = 100 * np.log(default / min_val) / np.log(max_val / min_val)
            slider = ctk.CTkSlider(
                frame, from_=0, to=100,
                command=on_slider_change,
                fg_color=COLORS['bg_dark'],
                progress_color=COLORS['accent_green']
            )
            slider.set(default_slider)
        else:
            slider = ctk.CTkSlider(
                frame, from_=min_val, to=max_val,
                command=on_slider_change,
                fg_color=COLORS['bg_dark'],
                progress_color=COLORS['accent_green']
            )
            slider.set(default)

        slider.pack(fill="x", pady=(5, 0))
        setattr(self, f"{var_name}_slider", slider)

    def _open_plot(self, module):
        """Open plot in browser for specified module."""
        html_attr = f"{module}_plot_html"
        if hasattr(self, html_attr):
            html_path = getattr(self, html_attr)
            if html_path:
                webbrowser.open('file://' + html_path)
