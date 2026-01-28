"""
Calculator Browser Tab - Opens comprehensive calculator suite in browser.
Similar to Omni Calculator with all physics, math, and engineering calculations.
"""

import customtkinter as ctk
from core.config import COLORS


class CalculatorBrowserTab:
    """Tab for launching the browser-based calculator suite."""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_ui()

    def create_ui(self):
        """Create the calculator browser tab UI."""
        # Main container
        main_frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header_frame,
            text="Engineering Calculator Suite",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['text_white']
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            header_frame,
            text="Comprehensive calculator collection for Formula Student engineering",
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_gray']
        ).pack(pady=(0, 20))

        # Content area with categories preview
        content_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_medium'], corner_radius=10)
        content_frame.pack(fill="both", expand=True)

        # Categories grid
        ctk.CTkLabel(
            content_frame,
            text="Available Categories",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_highlight']
        ).pack(pady=(20, 15))

        # Grid of category cards
        grid_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=30, pady=10)

        categories = [
            ("🚀", "Kinematics", "Motion, velocity, projectiles"),
            ("⚡", "Dynamics", "Forces, Newton's laws"),
            ("🔋", "Energy & Power", "Work, energy, power"),
            ("🔄", "Rotational Motion", "Angular motion, torque"),
            ("🔩", "Materials & Stress", "Stress, strain, materials"),
            ("🏗️", "Structural", "Beams, tubes, sections"),
            ("🏎️", "Vehicle Dynamics", "FSAE vehicle calculations"),
            ("⚙️", "Powertrain", "Engine, transmission"),
            ("⚡", "Electrical", "Circuits, components"),
            ("💧", "Fluid Mechanics", "Pressure, flow, drag"),
            ("🌡️", "Thermodynamics", "Heat, temperature"),
            ("📐", "Math & Geometry", "Trigonometry, geometry"),
            ("📊", "Statistics", "Statistical calculations"),
            ("🔄", "Unit Conversion", "Common conversions"),
        ]

        # Create 3-column grid
        for i, (icon, name, desc) in enumerate(categories):
            row = i // 3
            col = i % 3

            # Configure grid
            grid_frame.grid_columnconfigure(col, weight=1)

            card = ctk.CTkFrame(
                grid_frame,
                fg_color=COLORS['bg_light'],
                corner_radius=8
            )
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            ctk.CTkLabel(
                card,
                text=f"{icon} {name}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS['text_white']
            ).pack(anchor="w", padx=15, pady=(12, 2))

            ctk.CTkLabel(
                card,
                text=desc,
                font=ctk.CTkFont(size=11),
                text_color=COLORS['text_gray']
            ).pack(anchor="w", padx=15, pady=(0, 12))

        # Launch button
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=30)

        launch_btn = ctk.CTkButton(
            button_frame,
            text="Open Calculator Suite in Browser",
            command=self.open_calculator,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            corner_radius=10
        )
        launch_btn.pack()

        ctk.CTkLabel(
            button_frame,
            text="Opens in your default web browser with 70+ interactive calculators",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_gray']
        ).pack(pady=(10, 0))

        # Stats
        stats_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['bg_light'], corner_radius=8)
        stats_frame.pack(fill="x", padx=30, pady=(0, 20))

        stats_inner = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_inner.pack(pady=15)

        # Stats row
        for stat, label in [("70+", "Calculators"), ("14", "Categories"), ("Live", "Updates")]:
            stat_box = ctk.CTkFrame(stats_inner, fg_color="transparent")
            stat_box.pack(side="left", padx=40)

            ctk.CTkLabel(
                stat_box,
                text=stat,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=COLORS['accent_highlight']
            ).pack()

            ctk.CTkLabel(
                stat_box,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color=COLORS['text_gray']
            ).pack()

    def open_calculator(self):
        """Open the calculator suite in browser."""
        try:
            from calculators.browser import open_calculator_in_browser
            filepath = open_calculator_in_browser()
            self.app.update_status(f"Calculator suite opened in browser")
        except Exception as e:
            self.app.show_error(f"Failed to open calculator: {str(e)}")
