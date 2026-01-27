"""
FSAE reference guide tab.
"""

import customtkinter as ctk

from core.config import COLORS
from core.constants import FSAE_REFERENCE


class FSAETab:
    """Tab for FSAE reference guide."""

    def __init__(self, parent, app):
        """
        Initialize the FSAE tab.

        Args:
            parent: Parent widget (tab frame)
            app: Main application reference
        """
        self.parent = parent
        self.app = app

        self.setup_ui()

    def setup_ui(self):
        """Setup the tab user interface."""
        scroll_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=10
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Content sections
        sections = [
            ("FSAE SIGNAL PROCESSING REFERENCE GUIDE", COLORS['accent_red'],
             "This comprehensive guide covers essential signal processing concepts for Formula Student teams."),

            ("1. Common FSAE Sensors & Signals", COLORS['accent_green'],
             FSAE_REFERENCE['sensors']),

            ("2. Typical Resonance Frequencies", COLORS['accent_yellow'],
             FSAE_REFERENCE['resonance']),

            ("3. Filter Selection Guide", COLORS['accent_green'],
             FSAE_REFERENCE['filters']),

            ("4. Common FSAE Quiz Questions", COLORS['accent_red'],
             FSAE_REFERENCE['quiz']),

            ("5. Practical Tips", COLORS['accent_green'],
             FSAE_REFERENCE['tips']),
        ]

        for title, color, content in sections:
            # Section title
            ctk.CTkLabel(
                scroll_frame,
                text=title,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=color
            ).pack(anchor="w", padx=20, pady=(20, 10))

            # Content
            content_frame = ctk.CTkFrame(scroll_frame, fg_color=COLORS['bg_light'], corner_radius=10)
            content_frame.pack(fill="x", padx=20, pady=(0, 10))

            ctk.CTkLabel(
                content_frame,
                text=content.strip(),
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=COLORS['text_white'],
                justify="left",
                anchor="w"
            ).pack(padx=15, pady=15, anchor="w")
