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
from ui.tabs.calculator_browser_tab import CalculatorBrowserTab


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
        tab_calc_browser = self.tabview.add("Calculators")
        tab_equations = self.tabview.add("Equations")
        tab_fsae = self.tabview.add("FSAE Guide")

        # Initialize tabs
        self.analyze_tab = AnalyzeTab(tab_analyze, self)
        self.filter_tab = FilterTab(tab_filter, self)
        self.advanced_tab = AdvancedTab(tab_advanced, self)
        self.mechanical_tab = MechanicalTab(tab_mechanical, self)
        self.calculators_tab = CalculatorsTab(tab_calculators, self)
        self.calc_browser_tab = CalculatorBrowserTab(tab_calc_browser, self)
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

        # === RIGHT: Unit Calculator and Settings buttons ===
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, padx=15, pady=15, sticky="e")

        self.units_btn = ctk.CTkButton(
            buttons_frame,
            text="Units",
            command=self.open_unit_calculator,
            width=80,
            height=32,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['hover'],
            border_width=1,
            border_color=COLORS['border_light'],
            font=ctk.CTkFont(size=12)
        )
        self.units_btn.pack(side="left", padx=(0, 8))

        self.settings_btn = ctk.CTkButton(
            buttons_frame,
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
        self.settings_btn.pack(side="left")

    def open_settings(self):
        """Open settings dialog."""
        SettingsDialog(self)

    def open_unit_calculator(self):
        """Open adaptive unit calculator dialog."""
        current_tab = self.get_current_tab()
        UnitCalculatorDialog(self, current_tab)

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


class UnitCalculatorDialog(ctk.CTkToplevel):
    """Adaptive Unit Calculator dialog - context-aware with measurement system switching."""

    # Define unit categories relevant to each tab
    TAB_CATEGORIES = {
        'Signal Analysis': ['FREQUENCY', 'TIME', 'VOLTAGE'],
        'Digital Filtering': ['FREQUENCY', 'ANGLE', 'TIME'],
        'Advanced Analysis': ['FREQUENCY', 'POWER', 'TIME'],
        'Mechanical': ['LENGTH', 'FORCE', 'PRESSURE', 'MOMENT_OF_INERTIA', 'TORQUE', 'MASS'],
        'Electronics': ['VOLTAGE', 'CURRENT', 'RESISTANCE', 'CAPACITANCE', 'INDUCTANCE', 'POWER'],
        'Calculators': ['LENGTH', 'FORCE', 'PRESSURE', 'MASS', 'VELOCITY', 'POWER', 'ENERGY', 'TORQUE'],
        'Equations': ['LENGTH', 'FREQUENCY', 'ANGLE', 'TIME', 'ENERGY', 'POWER'],
        'FSAE Guide': ['LENGTH', 'FORCE', 'PRESSURE', 'MASS', 'VELOCITY', 'ACCELERATION', 'ANGLE'],
    }

    def __init__(self, parent, current_tab: str = 'Signal Analysis'):
        super().__init__(parent)
        self.parent = parent
        self.current_tab = current_tab

        self.title("Unit Calculator")
        self.geometry("500x650")
        self.configure(fg_color=COLORS['bg_dark'])

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 650) // 2
        self.geometry(f"+{x}+{y}")

        # Import unit converter
        from core.units import converter, UnitCategory, UNIT_DEFINITIONS, MeasurementSystem
        self.converter = converter
        self.unit_definitions = UNIT_DEFINITIONS
        self.UnitCategory = UnitCategory
        self.MeasurementSystem = MeasurementSystem

        # Current measurement system
        self.current_system = MeasurementSystem.METRIC

        self.create_ui()

    def create_ui(self):
        """Create the unit calculator UI."""
        # Title with context
        ctk.CTkLabel(
            self,
            text="Unit Calculator",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_white']
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self,
            text=f"Context: {self.current_tab}",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['accent_highlight']
        ).pack(pady=(0, 10))

        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # === Measurement System Selector ===
        system_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_light'], corner_radius=8)
        system_frame.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            system_frame,
            text="Measurement System:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_light']
        ).pack(side="left", padx=15, pady=10)

        self.system_var = ctk.StringVar(value="Metric")
        self.system_selector = ctk.CTkSegmentedButton(
            system_frame,
            values=["Metric", "Imperial", "All"],
            variable=self.system_var,
            command=self._on_system_change,
            font=ctk.CTkFont(size=11)
        )
        self.system_selector.pack(side="right", padx=15, pady=10)

        # === Category Selector ===
        cat_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cat_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            cat_frame,
            text="Category:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light']
        ).pack(anchor="w")

        # Get relevant categories for current tab
        relevant_cats = self.TAB_CATEGORIES.get(self.current_tab, ['LENGTH', 'MASS', 'FORCE'])
        self.category_var = ctk.StringVar(value=relevant_cats[0])

        self.category_combo = ctk.CTkComboBox(
            cat_frame,
            values=relevant_cats,
            variable=self.category_var,
            width=200,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            button_color=COLORS['accent_highlight'],
            dropdown_fg_color=COLORS['bg_medium'],
            command=self._on_category_change
        )
        self.category_combo.pack(fill="x", pady=(5, 10))

        # Input section
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            input_frame,
            text="Value:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light']
        ).pack(anchor="w")

        self.value_entry = ctk.CTkEntry(
            input_frame,
            width=200,
            height=35,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            font=ctk.CTkFont(size=14)
        )
        self.value_entry.pack(fill="x", pady=(5, 10))
        self.value_entry.insert(0, "1.0")
        self.value_entry.bind("<KeyRelease>", self._on_value_change)

        # From unit
        ctk.CTkLabel(
            input_frame,
            text="From:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light']
        ).pack(anchor="w")

        self.from_unit_var = ctk.StringVar(value="mm")

        self.from_combo = ctk.CTkComboBox(
            input_frame,
            values=["mm"],
            variable=self.from_unit_var,
            width=200,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            button_color=COLORS['accent_highlight'],
            dropdown_fg_color=COLORS['bg_medium'],
            command=self._on_from_unit_change
        )
        self.from_combo.pack(fill="x", pady=(5, 10))

        # To unit
        ctk.CTkLabel(
            input_frame,
            text="To:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_light']
        ).pack(anchor="w")

        self.to_unit_var = ctk.StringVar(value="m")

        self.to_combo = ctk.CTkComboBox(
            input_frame,
            values=["m"],
            variable=self.to_unit_var,
            width=200,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['border_light'],
            button_color=COLORS['accent_highlight'],
            dropdown_fg_color=COLORS['bg_medium'],
            command=self._on_to_unit_change
        )
        self.to_combo.pack(fill="x", pady=(5, 10))

        # Quick system convert button
        self.quick_convert_btn = ctk.CTkButton(
            input_frame,
            text="Quick: Metric <-> Imperial",
            command=self._quick_system_convert,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['hover'],
            border_width=1,
            border_color=COLORS['border_light'],
            height=30,
            font=ctk.CTkFont(size=11)
        )
        self.quick_convert_btn.pack(fill="x", pady=5)

        # Result section
        result_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_light'], corner_radius=8)
        result_frame.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            result_frame,
            text="Result:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_gray']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.result_label = ctk.CTkLabel(
            result_frame,
            text="1.0",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS['accent_highlight']
        )
        self.result_label.pack(padx=15, pady=(0, 5))

        self.system_label = ctk.CTkLabel(
            result_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_gray']
        )
        self.system_label.pack(padx=15, pady=(0, 10))

        # Quick conversions section
        quick_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        quick_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            quick_frame,
            text="Common Conversions:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(0, 5))

        self.quick_label = ctk.CTkLabel(
            quick_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_gray'],
            justify="left"
        )
        self.quick_label.pack(anchor="w")

        # Close button
        ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['hover'],
            width=100
        ).pack(pady=10)

        # Initialize units for selected category
        self._update_units_for_category()
        self._do_conversion()

    def _get_system_enum(self) -> 'MeasurementSystem':
        """Get the MeasurementSystem enum from the selector."""
        system_map = {
            "Metric": self.MeasurementSystem.METRIC,
            "Imperial": self.MeasurementSystem.IMPERIAL,
            "All": self.MeasurementSystem.BOTH
        }
        return system_map.get(self.system_var.get(), self.MeasurementSystem.METRIC)

    def _get_category_enum(self) -> 'UnitCategory':
        """Get the UnitCategory enum from the selector."""
        cat_name = self.category_var.get()
        return getattr(self.UnitCategory, cat_name, self.UnitCategory.LENGTH)

    def _on_system_change(self, value=None):
        """Handle measurement system change."""
        self._update_units_for_category()
        self._do_conversion()

    def _on_category_change(self, value=None):
        """Handle category change."""
        self._update_units_for_category()
        self._do_conversion()

    def _update_units_for_category(self):
        """Update unit dropdowns based on selected category and system."""
        category = self._get_category_enum()
        system = self._get_system_enum()

        # Get units for this category and system
        units = self.converter.get_units_by_category_and_system(category, system)
        unit_list = list(units.keys())

        if not unit_list:
            unit_list = ["N/A"]

        # Update from combo
        self.from_combo.configure(values=unit_list)
        if self.from_unit_var.get() not in unit_list:
            self.from_unit_var.set(unit_list[0])

        # Update to combo
        self.to_combo.configure(values=unit_list)
        if self.to_unit_var.get() not in unit_list:
            self.to_unit_var.set(unit_list[1] if len(unit_list) > 1 else unit_list[0])

        self._update_quick_reference()

    def _on_value_change(self, event=None):
        """Handle value change."""
        self._do_conversion()

    def _on_from_unit_change(self, value=None):
        """Handle from-unit change."""
        self._do_conversion()
        self._update_quick_reference()

    def _on_to_unit_change(self, value=None):
        """Handle to-unit change."""
        self._do_conversion()

    def _quick_system_convert(self):
        """Quick convert between Metric and Imperial."""
        from_unit = self.from_unit_var.get()
        if from_unit not in self.unit_definitions:
            return

        from_def = self.unit_definitions[from_unit]
        current_sys = from_def.system

        # Determine target system
        if current_sys == self.MeasurementSystem.METRIC or current_sys == self.MeasurementSystem.SI:
            target_sys = self.MeasurementSystem.IMPERIAL
        else:
            target_sys = self.MeasurementSystem.METRIC

        # Find equivalent unit
        equiv = self.converter.get_equivalent_unit(from_unit, target_sys)
        if equiv and equiv != from_unit:
            self.to_unit_var.set(equiv)
            self._do_conversion()

    def _do_conversion(self):
        """Perform the conversion."""
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()

            if from_unit == "N/A" or to_unit == "N/A":
                self.result_label.configure(text="Select valid units")
                return

            result = self.converter.convert(value, from_unit, to_unit)

            # Format result
            if abs(result) >= 10000 or (abs(result) < 0.001 and result != 0):
                result_str = f"{result:.4e} {to_unit}"
            else:
                result_str = f"{result:.6g} {to_unit}"

            self.result_label.configure(text=result_str)

            # Show system info
            from_sys = self.unit_definitions[from_unit].system.value
            to_sys = self.unit_definitions[to_unit].system.value
            if from_sys != to_sys:
                self.system_label.configure(text=f"({from_sys} -> {to_sys})")
            else:
                self.system_label.configure(text=f"(within {from_sys})")

        except ValueError as e:
            self.result_label.configure(text=str(e))
            self.system_label.configure(text="")
        except Exception:
            self.result_label.configure(text="Invalid input")
            self.system_label.configure(text="")

    def _update_quick_reference(self):
        """Update quick reference with common conversions."""
        from_unit = self.from_unit_var.get()
        if from_unit not in self.unit_definitions:
            self.quick_label.configure(text="")
            return

        from_def = self.unit_definitions[from_unit]
        category = from_def.category

        # Show conversions to both metric and imperial
        refs = []

        # Get metric equivalent
        metric_equiv = self.converter.get_equivalent_unit(from_unit, self.MeasurementSystem.METRIC)
        if metric_equiv and metric_equiv != from_unit:
            try:
                val = self.converter.convert(1.0, from_unit, metric_equiv)
                refs.append(f"1 {from_unit} = {val:.4g} {metric_equiv} (metric)")
            except Exception:
                pass

        # Get imperial equivalent
        imperial_equiv = self.converter.get_equivalent_unit(from_unit, self.MeasurementSystem.IMPERIAL)
        if imperial_equiv and imperial_equiv != from_unit:
            try:
                val = self.converter.convert(1.0, from_unit, imperial_equiv)
                refs.append(f"1 {from_unit} = {val:.4g} {imperial_equiv} (imperial)")
            except Exception:
                pass

        # Add a few more from same category
        all_units = self.converter.get_units_by_category(category)
        for unit in list(all_units.keys())[:4]:
            if unit != from_unit and len(refs) < 5:
                try:
                    val = self.converter.convert(1.0, from_unit, unit)
                    if f"{unit}" not in str(refs):
                        refs.append(f"1 {from_unit} = {val:.4g} {unit}")
                except Exception:
                    pass

        self.quick_label.configure(text="\n".join(refs[:5]))


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
