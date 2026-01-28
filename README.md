# Advanced Engineering Analysis Tool for Formula Student

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange.svg" alt="Version">
</p>

**ITU Racing Team | Version 1.0.0**

A comprehensive engineering analysis tool designed for Formula Student teams. Features signal processing, mechanical calculations, electronics analysis, and FSAE compliance checking.

---

## Features

### Signal Analysis
- **Auto-detection** of file formats (CSV, TXT, Excel) with European/US decimal support
- **FFT Analysis** with resonance frequency detection
- **Interactive Plotly plots** with zoom, pan, and hover info
- **Digital Filtering**: Butterworth, Chebyshev, Bessel filters
- **Advanced Analysis**: Spectrogram, PSD (Welch), RMS, Peak Detection

### Mechanical Engineering Module
- **Tube Properties**: Moment of inertia, flexural rigidity
- **FSAE Compliance**: Structural requirement checking per FSAE rules
- **Sandwich Panels**: Composite panel MOI calculations
- **Laminate Analysis**: Rule of mixtures for elastic modulus
- **Fastener Analysis**: Bolt tensile/shear stress
- **Beam Bending**: 3-point bending stress and deflection
- **Vehicle Dynamics**: Cornering, lateral load transfer, skidpad
- **Transmission**: Gear ratios, torque multiplication

### Electronics Calculators
- **Pre-Charge/Discharge**: RC safety with FSAE EV.5.5 compliance
- **Battery Endurance**: Runtime & thermal simulation
- **Wheatstone Bridge**: Strain gauge signal conditioning
- **Filter Designer**: RC low-pass with Bode plot

### Dynamic Formula Engine
- External formula definitions for easy updates
- No recompilation needed for calculation changes
- Excel-style formula syntax support

---

## Installation

### Prerequisites
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)

### Windows (One-Click)

1. Download or clone this repository
2. Double-click `install_windows.bat`
3. Wait for installation to complete
4. Double-click `run_app.bat` to start the application

### macOS / Linux

1. Download or clone this repository
2. Open terminal in the project folder
3. Run:
   ```bash
   chmod +x install_mac_linux.sh
   ./install_mac_linux.sh
   ```
4. Start the application:
   ```bash
   ./run_app.sh
   ```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/omarelgerba1100/ITU-Racing-fsae-signal-analyzer.git
cd ITU-Racing-fsae-signal-analyzer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## Usage

### Tab Overview

| Tab | Description |
|-----|-------------|
| Signal Analysis | Load and analyze sensor data with FFT and statistics |
| Digital Filtering | Apply filters with real-time preview |
| Advanced Analysis | Spectrogram, PSD, peak detection |
| Mechanical | 8 engineering calculators for structural analysis |
| Electronics | EV-specific circuit calculators |
| Equations | Reference formulas with LaTeX rendering |
| FSAE Guide | Sensor tables and compliance guidelines |

### Settings
Click the **Settings** button to customize:
- Theme (dark/light/system)
- Default units (mm/m/in, N/kN/lbf, etc.)
- Default sampling frequency

---

## Project Structure

```
fsae-signal-analyzer/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
├── install_windows.bat     # Windows installer
├── run_app.bat             # Windows launcher
├── install_mac_linux.sh    # macOS/Linux installer
├── core/
│   ├── config.py          # Configuration and colors
│   ├── units.py           # Unit conversion engine
│   └── formula_engine.py  # Dynamic formula parser
├── ui/
│   ├── main_window.py     # Main application window
│   └── tabs/              # Tab implementations
├── calculators/
│   └── mechanical/        # Mechanical calculators
├── plotting/              # Visualization modules
├── utils/                 # Utility functions
├── assets/                # Images and resources
└── Updates/Feed/          # External formula definitions
```

---

## Extending Formulas

Add formulas to `Updates/Feed/` directory:
- `01_formulas.txt` - Formula definitions
- `02_named_ranges.txt` - Named constants
- `03_dependencies.txt` - Calculation dependencies

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Credits

Developed by **ITU Racing Team**

Lead Developer: Omer Rieber

---

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Interactive plots powered by [Plotly](https://plotly.com/python/)
- Signal processing with [SciPy](https://scipy.org/)
