"""
Application configuration and color scheme.
Advanced Engineering Analysis Tool for Formula Student
ITU Racing | Lead Developer: Omer Rieber
"""

# Professional monochrome color scheme - v0.0.3
# High contrast, information-dense, suitable for prolonged technical use
COLORS = {
    # Background hierarchy
    'bg_dark': '#0a0a0a',       # Darkest - main background
    'bg_medium': '#141414',     # Medium - panels
    'bg_light': '#1e1e1e',      # Light - cards, inputs
    'bg_elevated': '#282828',   # Elevated elements

    # Text hierarchy
    'text_white': '#ffffff',    # Primary text
    'text_light': '#e0e0e0',    # Secondary text
    'text_gray': '#888888',     # Tertiary/disabled text
    'text_dark': '#555555',     # Subtle text

    # Accent colors - Minimal, purposeful use only
    'accent_primary': '#ffffff',    # Primary accent (white)
    'accent_secondary': '#cccccc',  # Secondary accent
    'accent_highlight': '#3d9970',  # Success/highlight (muted green)
    'accent_warning': '#ff8c00',    # Warning (orange)
    'accent_error': '#dc3545',      # Error (red)
    'accent_info': '#5bc0de',       # Info (blue)

    # Legacy color mappings for backward compatibility
    'accent_red': '#dc3545',
    'accent_green': '#3d9970',
    'accent_blue': '#2c5282',
    'accent_yellow': '#d69e2e',
    'accent_purple': '#805ad5',
    'accent_orange': '#dd6b20',

    # Borders and dividers
    'border_dark': '#2a2a2a',
    'border_light': '#3a3a3a',

    # Interactive states
    'hover': '#333333',
    'active': '#444444',
    'focus': '#4a5568',
}

# Application configuration - v0.0.3
APP_CONFIG = {
    'title': "Advanced Engineering Analysis Tool for Formula Student",
    'subtitle': "ITU Racing | Lead Developer: Omer Rieber",
    'version': "1.0.0",
    'geometry': "1700x980",
    'default_fs': 2000,  # Default sampling frequency (Hz)
    'default_calibration': 20.23,  # Default calibration (mV/g)
    'appearance_mode': 'dark',
    'color_theme': 'blue'
}

# Default filter settings
FILTER_DEFAULTS = {
    'cutoff': 50,
    'order': 4,
    'cutoff_high': 100,
    'type': 'lowpass',
    'design': 'butter'
}

# Plot settings - Professional dark theme
PLOT_CONFIG = {
    'height': 700,
    'template': 'plotly_dark',
    'freq_range_max': 200,
    'spectrogram_nperseg': 256,
    'spectrogram_noverlap': 128,
    'welch_nperseg': 1024,
    'paper_bgcolor': '#0a0a0a',
    'plot_bgcolor': '#141414',
    'grid_color': '#2a2a2a',
    'font_color': '#e0e0e0',
}

# Material properties - FSAE defaults
MATERIAL_DEFAULTS = {
    'steel': {
        'name': 'Steel (AISI 4130)',
        'E': 200e9,          # Young's modulus (Pa)
        'yield_nonwelded': 305e6,  # Yield strength non-welded (Pa)
        'yield_welded': 180e6,     # Yield strength welded (Pa)
        'ultimate_nonwelded': 365e6,
        'ultimate_welded': 300e6,
        'density': 7850,     # kg/m3
    },
    'aluminum': {
        'name': 'Aluminum (6061-T6)',
        'E': 69e9,
        'yield': 276e6,
        'ultimate': 310e6,
        'density': 2700,
    },
    'carbon_fiber': {
        'name': 'Carbon Fiber Composite',
        'E_fiber': 230e9,
        'E_matrix': 3.5e9,
        'density': 1600,
    }
}

# FSAE structural requirements
FSAE_REQUIREMENTS = {
    'main_front_hoops': {
        'min_thickness_mm': 2.0,
        'min_area_mm2': 173,
        'min_I_mm4': 11320,
        'min_EI_Nmm2': 2.264e9,
    },
    'side_impact': {
        'min_thickness_mm': 1.2,
        'min_area_mm2': 119,
        'min_I_mm4': 8509,
        'min_EI_Nmm2': 1.702e9,
    },
    'front_bulkhead': {
        'min_thickness_mm': 1.2,
        'min_area_mm2': 119,
        'min_I_mm4': 8509,
        'min_EI_Nmm2': 1.702e9,
    },
    'bulkhead_support': {
        'min_thickness_mm': 1.2,
        'min_area_mm2': 91,
        'min_I_mm4': 6695,
        'min_EI_Nmm2': 1.339e9,
    },
}

# Unit preferences
UNIT_PREFERENCES = {
    'length': 'mm',
    'force': 'N',
    'pressure': 'MPa',
    'moment_of_inertia': 'mm4',
    'energy': 'J',
    'power': 'kW',
    'voltage': 'V',
    'current': 'A',
    'capacitance': 'uF',
    'resistance': 'Ohm',
    'frequency': 'Hz',
    'velocity': 'm/s',
    'acceleration': 'g',
    'torque': 'Nm',
    'angle': 'deg',
}
