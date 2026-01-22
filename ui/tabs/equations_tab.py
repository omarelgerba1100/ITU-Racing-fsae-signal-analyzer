"""
Equations reference tab with LaTeX rendering.
"""

import customtkinter as ctk

from ...core.config import COLORS
from ...core.constants import EQUATIONS
from ...utils.latex_renderer import LatexRenderer


class EquationsTab:
    """Tab for equations reference with LaTeX rendering."""

    def __init__(self, parent, app):
        """
        Initialize the equations tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app

        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=10
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        ctk.CTkLabel(
            scroll_frame,
            text="Key Signal Processing Equations",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['accent_red']
        ).pack(pady=(20, 30))

        # Render each equation
        for title, equation, description in EQUATIONS:
            self._create_equation_frame(scroll_frame, title, equation, description)

    def _create_equation_frame(self, parent, title, equation, description):
        """Create a frame for a single equation."""
        eq_frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_light'], corner_radius=10)
        eq_frame.pack(fill="x", padx=20, pady=10)

        # Title
        ctk.CTkLabel(
            eq_frame,
            text=f"{title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['accent_green']
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Render equation
        try:
            eq_img = LatexRenderer.render_equation(equation, fontsize=16)
            eq_ctk_img = ctk.CTkImage(
                light_image=eq_img,
                dark_image=eq_img,
                size=(eq_img.width, eq_img.height)
            )
            ctk.CTkLabel(eq_frame, image=eq_ctk_img, text="").pack(pady=10)
        except Exception:
            # Fallback to text
            ctk.CTkLabel(
                eq_frame,
                text=equation,
                font=ctk.CTkFont(family="Consolas", size=14),
                text_color=COLORS['text_white']
            ).pack(pady=10)

        # Description
        ctk.CTkLabel(
            eq_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray'],
            justify="left"
        ).pack(anchor="w", padx=15, pady=(5, 15))
