"""
Main application window for FSAE Signal Analyzer.
"""

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from ..core.config import COLORS, APP_CONFIG
from .tabs.analyze_tab import AnalyzeTab
from .tabs.filter_tab import FilterTab
from .tabs.advanced_tab import AdvancedTab
from .tabs.equations_tab import EquationsTab
from .tabs.fsae_tab import FSAETab
from .tabs.calculators_tab import CalculatorsTab


class FSAESignalAnalyzer(ctk.CTk):
    """Main application class."""

    def __init__(self):
        super().__init__()

        # Configure appearance
        ctk.set_appearance_mode(APP_CONFIG['appearance_mode'])
        ctk.set_default_color_theme(APP_CONFIG['color_theme'])

        self.title(APP_CONFIG['title'])
        self.geometry(APP_CONFIG['geometry'])
        self.configure(fg_color=COLORS['bg_dark'])

        # Shared data
        self.data = None
        self.filtered_data = None

        # Create UI
        self.create_ui()

    def create_ui(self):
        """Create the main user interface."""
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.create_header()

        # Tabview
        self.tabview = ctk.CTkTabview(
            self.main_container,
            fg_color=COLORS['bg_medium'],
            segmented_button_fg_color=COLORS['bg_light'],
            segmented_button_selected_color=COLORS['accent_red'],
            segmented_button_unselected_color=COLORS['bg_light'],
            text_color=COLORS['text_white']
        )
        self.tabview.pack(fill="both", expand=True, pady=(10, 0))

        # Add tabs
        tab_analyze = self.tabview.add("Load & Analyze")
        tab_filter = self.tabview.add("Digital Filtering")
        tab_advanced = self.tabview.add("Advanced Analysis")
        tab_calculators = self.tabview.add("Calculators")
        tab_equations = self.tabview.add("Equations Reference")
        tab_fsae = self.tabview.add("FSAE Guide")

        # Initialize tabs
        self.analyze_tab = AnalyzeTab(tab_analyze, self)
        self.filter_tab = FilterTab(tab_filter, self)
        self.advanced_tab = AdvancedTab(tab_advanced, self)
        self.calculators_tab = CalculatorsTab(tab_calculators, self)
        self.equations_tab = EquationsTab(tab_equations, self)
        self.fsae_tab = FSAETab(tab_fsae, self)

        # Status bar
        self.status_var = ctk.StringVar(value="Ready - Load a data file to begin")
        self.status_bar = ctk.CTkLabel(
            self.main_container,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS['bg_light'],
            corner_radius=5,
            height=35
        )
        self.status_bar.pack(fill="x", pady=(10, 0))

    def create_header(self):
        """Create header section."""
        header_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS['bg_medium'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 10))

        # Title
        title = ctk.CTkLabel(
            header_frame,
            text="ITU Racing - Advanced Signal Analysis Tool",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['accent_red']
        )
        title.pack(pady=(15, 5))

        # Subtitle
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Formula Student FSA | Vibration Analysis | Digital Filtering | Electronics Calculators",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['accent_green']
        )
        subtitle.pack(pady=(0, 15))

    def update_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(f"{message}")

    def show_warning(self, message: str):
        """Show warning message."""
        CTkMessagebox(title="Warning", message=message, icon="warning")

    def show_error(self, message: str):
        """Show error message."""
        CTkMessagebox(title="Error", message=message, icon="cancel")

    def show_info(self, message: str):
        """Show info message."""
        CTkMessagebox(title="Info", message=message, icon="info")
