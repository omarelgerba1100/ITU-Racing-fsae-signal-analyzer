"""
Application configuration and color scheme.
"""

# Color scheme for the application
COLORS = {
    'bg_dark': '#0f0f1a',
    'bg_medium': '#1a1a2e',
    'bg_light': '#16213e',
    'accent_red': '#e94560',
    'accent_green': '#4ecca3',
    'accent_blue': '#0f3460',
    'accent_yellow': '#f39c12',
    'accent_purple': '#9b59b6',
    'accent_orange': '#e67e22',
    'text_white': '#ffffff',
    'text_gray': '#a0a0a0'
}

# Application configuration
APP_CONFIG = {
    'title': "ITU Racing - FSAE Signal Analysis Tool",
    'geometry': "1600x950",
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

# Plot settings
PLOT_CONFIG = {
    'height': 700,
    'template': 'plotly_dark',
    'freq_range_max': 200,
    'spectrogram_nperseg': 256,
    'spectrogram_noverlap': 128,
    'welch_nperseg': 1024
}
