"""
Main application window for Advanced Engineering Analysis Tool.
Formula Student | ITU Racing
Version 1.0.0
"""

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import os

from core.config import COLORS, APP_CONFIG
from ui.tabs.analyze_tab import AnalyzeTab
from ui.tabs.filter_tab import FilterTab
from ui.tabs.advanced_tab import AdvancedTab
from ui.tabs.equations_tab import EquationsTab
from ui.tabs.fsae_tab import FSAETab
from ui.tabs.calculators_tab import CalculatorsTab
from ui.tabs.mechanical_tab import MechanicalTab


# Get the base directory for assets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')


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

        # Tabview - Professional monochrome styling
        self.tabview = ctk.CTkTabview(
            self.main_container,
            fg_color=COLORS['bg_medium'],
            segmented_button_fg_color=COLORS['bg_light'],
            segmented_button_selected_color=COLORS['accent_highlight'],
            segmented_button_unselected_color=COLORS['bg_light'],
            text_color=COLORS['text_white']
        )
        self.tabview.pack(fill="both", expand=True, pady=(10, 0))

        # Add tabs
        tab_analyze = self.tabview.add("Signal Analysis")
        tab_filter = self.tabview.add("Digital Filtering")
        tab_advanced = self.tabview.add("Advanced Analysis")
        tab_mechanical = self.tabview.add("Mechanical")
        tab_calculators = self.tabview.add("Electronics")
        tab_equations = self.tabview.add("Equations")
        tab_fsae = self.tabview.add("FSAE Guide")

        # Initialize tabs
        self.analyze_tab = AnalyzeTab(tab_analyze, self)
        self.filter_tab = FilterTab(tab_filter, self)
        self.advanced_tab = AdvancedTab(tab_advanced, self)
        self.mechanical_tab = MechanicalTab(tab_mechanical, self)
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
        """Create header section with logo and settings - v1.0.0."""
        header_frame = ctk.CTkFrame(self.main_container, fg_color=COLORS['bg_medium'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 10))

        # Configure header grid
        header_frame.grid_columnconfigure(0, weight=0)  # Logo
        header_frame.grid_columnconfigure(1, weight=1)  # Title (expandable)
        header_frame.grid_columnconfigure(2, weight=0)  # Settings

        # === LEFT: Logo in white rounded container ===
        logo_container = ctk.CTkFrame(
            header_frame,
            fg_color="#ffffff",  # White background
            corner_radius=8,
            width=60,
            height=60
        )
        logo_container.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        logo_container.grid_propagate(False)

        # Load and display logo
        try:
            logo_path = os.path.join(ASSETS_DIR, 'logo bw@4x.png')
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_ctk = ctk.CTkImage(
                    light_image=logo_image,
                    dark_image=logo_image,
                    size=(50, 50)
                )
                logo_label = ctk.CTkLabel(
                    logo_container,
                    image=logo_ctk,
                    text="",
                    fg_color="transparent"
                )
                logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            # Fallback text if logo fails to load
            ctk.CTkLabel(
                logo_container,
                text="ITU",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#000000"
            ).place(relx=0.5, rely=0.5, anchor="center")

        # === CENTER: Title and subtitle ===
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=1, pady=10)

        title = ctk.CTkLabel(
            title_frame,
            text=APP_CONFIG['title'],
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS['text_white']
        )
        title.pack(pady=(5, 2))

        subtitle = ctk.CTkLabel(
            title_frame,
            text=APP_CONFIG['subtitle'],
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray']
        )
        subtitle.pack(pady=(0, 2))

        version = ctk.CTkLabel(
            title_frame,
            text=f"v{APP_CONFIG['version']}",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['accent_highlight']
        )
        version.pack(pady=(0, 5))

        # === RIGHT: Settings button ===
        settings_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        settings_frame.grid(row=0, column=2, padx=15, pady=15, sticky="e")

        self.settings_btn = ctk.CTkButton(
            settings_frame,
            text="Settings",
            command=self.open_settings,
            width=100,
            height=32,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['hover'],
            border_width=1,
            border_color=COLORS['border_light'],
            font=ctk.CTkFont(size=12)
        )
        self.settings_btn.pack()

    def open_settings(self):
        """Open settings dialog."""
        SettingsDialog(self)

    def get_current_tab(self) -> str:
        """Get the name of the currently active tab."""
        return self.tabview.get()

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


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog window."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Settings")
        self.geometry("500x400")
        self.configure(fg_color=COLORS['bg_dark'])

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 400) // 2
        self.geometry(f"+{x}+{y}")

        self.create_ui()

    def create_ui(self):
        """Create settings UI."""
        # Title
        ctk.CTkLabel(
            self,
            text="Application Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['text_white']
        ).pack(pady=(20, 10))

        # Settings container
        settings_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_medium'],
            corner_radius=10
        )
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # === Appearance Section ===
        ctk.CTkLabel(
            settings_frame,
            text="Appearance",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_highlight']
        ).pack(anchor="w", padx=15, pady=(15, 5))

        # Theme selector
        theme_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light'],
            width=120,
            anchor="w"
        ).pack(side="left")

        self.theme_var = ctk.StringVar(value="dark")
        ctk.CTkSegmentedButton(
            theme_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self.change_theme,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=10)

        # === Units Section ===
        ctk.CTkLabel(
            settings_frame,
            text="Default Units",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_highlight']
        ).pack(anchor="w", padx=15, pady=(20, 5))

        # Length units
        self._create_unit_selector(settings_frame, "Length:", ["mm", "cm", "m", "in"])
        # Pressure units
        self._create_unit_selector(settings_frame, "Pressure:", ["MPa", "GPa", "Pa", "psi"])
        # Force units
        self._create_unit_selector(settings_frame, "Force:", ["N", "kN", "lbf"])

        # === Data Section ===
        ctk.CTkLabel(
            settings_frame,
            text="Signal Processing",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['accent_highlight']
        ).pack(anchor="w", padx=15, pady=(20, 5))

        # Default sampling frequency
        fs_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        fs_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            fs_frame,
            text="Default Fs:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light'],
            width=120,
            anchor="w"
        ).pack(side="left")

        self.fs_entry = ctk.CTkEntry(
            fs_frame,
            width=100,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light']
        )
        self.fs_entry.pack(side="left", padx=10)
        self.fs_entry.insert(0, str(APP_CONFIG['default_fs']))

        ctk.CTkLabel(
            fs_frame,
            text="Hz",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray']
        ).pack(side="left")

        # === Buttons ===
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(
            btn_frame,
            text="Save",
            command=self.save_settings,
            fg_color=COLORS['accent_highlight'],
            hover_color=COLORS['hover'],
            width=100
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['hover'],
            width=100
        ).pack(side="right", padx=5)

    def _create_unit_selector(self, parent, label: str, options: list):
        """Create a unit selector row."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light'],
            width=120,
            anchor="w"
        ).pack(side="left")

        ctk.CTkComboBox(
            frame,
            values=options,
            width=100,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            button_color=COLORS['accent_highlight'],
            dropdown_fg_color=COLORS['bg_medium'],
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=10)

    def change_theme(self, theme: str):
        """Change application theme."""
        ctk.set_appearance_mode(theme)

    def save_settings(self):
        """Save settings and close."""
        # TODO: Implement settings persistence
        self.destroy()
