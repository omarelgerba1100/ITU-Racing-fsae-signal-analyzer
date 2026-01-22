# ITU Racing - FSAE Signal Analysis Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/FSAE-Formula%20Student-red.svg" alt="FSAE">
</p>

A professional signal processing and electronics design application for Formula Student teams. Features real-time interactive visualizations, digital filtering, and EV-specific calculators for design validation.

---

## Features

### Signal Analysis
- **Auto-detection** of file formats (CSV, TXT, Excel) with European/US decimal support
- **FFT Analysis** with resonance frequency detection
- **Interactive Plotly plots** with zoom, pan, and hover info
- **Digital Filtering**: Butterworth, Chebyshev, Bessel filters
- **Advanced Analysis**: Spectrogram, PSD (Welch), RMS, Peak Detection

### Live FSAE EV Calculation Suite
Real-time engineering dashboard with **zero-latency feedback** (no calculate buttons!):

| Module | Description |
|--------|-------------|
| **A: Pre-Charge/Discharge** | RC safety calculator with FSAE EV.5.5 compliance checking |
| **B: Battery Endurance** | Runtime & thermal simulation for endurance events |
| **C: Wheatstone Bridge** | Strain gauge/load cell signal conditioning design |
| **D: Filter Designer** | RC low-pass filter with Bode plot & noise simulation |

### Reference Guides
- Signal processing equations with LaTeX rendering
- FSAE sensor reference tables
- Filter selection guide
- Common quiz questions & answers

---

## Quick Start

### Option 1: PowerShell Installer (Windows - Recommended)

```powershell
# Run this in PowerShell as Administrator
.\install.ps1
```

### Option 2: Manual Installation

```powershell
# 1. Clone the repository
git clone https://github.com/ITU-Racing/fsae-signal-analyzer.git
cd fsae-signal-analyzer

# 2. Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run_analyzer.py
```

---

## Installation Guide (Detailed)

### Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** (optional) - [Download Git](https://git-scm.com/downloads)

### Step-by-Step Installation (Windows PowerShell)

```powershell
# Step 1: Check Python is installed
python --version
# Should show Python 3.8.x or higher

# Step 2: Navigate to where you want to install
cd C:\Users\YourName\Documents

# Step 3: Clone or download the repository
git clone https://github.com/ITU-Racing/fsae-signal-analyzer.git

# Step 4: Enter the directory
cd fsae-signal-analyzer

# Step 5: Create a virtual environment
python -m venv venv

# Step 6: Activate the virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Step 7: Upgrade pip
python -m pip install --upgrade pip

# Step 8: Install all dependencies
pip install -r requirements.txt

# Step 9: Run the application
python run_analyzer.py
```

### Troubleshooting Installation

| Problem | Solution |
|---------|----------|
| `python` not recognized | Add Python to PATH or use `py` instead |
| Execution policy error | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| pip install fails | Try `pip install --user -r requirements.txt` |
| Module not found | Make sure virtual environment is activated |
| GUI doesn't appear | Install Microsoft Visual C++ Redistributable |

---

## Usage Guide

### Running the Application

```powershell
# Make sure you're in the project directory with venv activated
python run_analyzer.py
```

### Tab Overview

#### 1. Load & Analyze
1. Click **Browse File** to select your data file
2. Set **Sampling Frequency** (Hz) and **Calibration** (mV/g)
3. Click **ANALYZE DATA**
4. Click **Open Interactive Plot in Browser** to view zoomable plots

**Supported File Formats:**
- `.txt`, `.csv`, `.dat` (auto-detects delimiter and decimal separator)
- `.xlsx`, `.xls` (Excel files)

#### 2. Digital Filtering
1. Select filter type: Low-Pass, High-Pass, Band-Pass, or Notch
2. Choose design: Butterworth, Chebyshev I, or Bessel
3. Set cutoff frequency and filter order
4. Click **Apply Filter** to see before/after comparison

#### 3. Advanced Analysis
- **Spectrogram**: Frequency content over time
- **PSD (Welch)**: Power spectral density
- **Statistics**: Mean, RMS, peak-to-peak, crest factor
- **Peak Detection**: Find dominant frequencies
- **RMS Analysis**: Vibration severity assessment

#### 4. Calculators (Live - No Calculate Button!)

**Module A: Pre-Charge/Discharge**
- Drag sliders to adjust bus voltage, resistors
- Watch charging/discharging curves update in real-time
- Safety status shows PASS/FAIL for FSAE EV.5.5 compliance

**Module B: Battery Endurance**
- Enter cell configuration (e.g., 96S4P)
- Adjust current and simulation time
- See runtime estimate and thermal analysis

**Module C: Wheatstone Bridge**
- Design strain gauge signal conditioning
- Adjust R2 slider to balance the bridge
- View linearity analysis

**Module D: Filter Designer**
- Set target cutoff frequency
- See Bode plot and filtered signal preview
- Snap to E24 standard component values

#### 5. Equations Reference
- Key signal processing formulas with explanations
- RC circuits, filters, FFT, sampling theory

#### 6. FSAE Guide
- Sensor reference tables
- Resonance frequency guidelines
- Filter selection guide
- Common quiz questions

---

## Project Structure

```
fsae_signal_analyzer/
├── __init__.py              # Package info
├── main.py                  # Application entry point
├── core/
│   ├── config.py           # Colors, settings
│   └── constants.py        # Equations, FSAE reference data
├── utils/
│   ├── data_loader.py      # File loading with auto-detection
│   └── latex_renderer.py   # Equation rendering
├── plotting/
│   └── interactive_plotter.py  # Plotly visualizations
├── processing/
│   └── signal_processing.py    # FFT, filtering, statistics
├── calculators/
│   ├── capacitor_calculator.py # RC charging/discharging
│   ├── battery_calculator.py   # Battery discharge
│   ├── bridge_calculator.py    # Wheatstone, Wien, Maxwell
│   └── filter_calculator.py    # RC/RL filter design
└── ui/
    ├── main_window.py      # Main application window
    └── tabs/
        ├── analyze_tab.py      # Signal analysis
        ├── filter_tab.py       # Digital filtering
        ├── advanced_tab.py     # Advanced analysis
        ├── calculators_tab.py  # Live EV calculators
        ├── equations_tab.py    # Equations reference
        └── fsae_tab.py         # FSAE guide
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| customtkinter | >=5.0.0 | Modern UI framework |
| CTkMessagebox | >=2.0 | Message dialogs |
| plotly | >=5.0.0 | Interactive plots |
| pandas | >=1.3.0 | Data handling |
| numpy | >=1.20.0 | Numerical computing |
| scipy | >=1.7.0 | Signal processing |
| matplotlib | >=3.4.0 | Equation rendering |
| pillow | >=8.0.0 | Image processing |

---

## For Developers

### Adding New Calculators

1. Create new calculator in `calculators/` folder
2. Add plotting methods to `plotting/interactive_plotter.py`
3. Create UI in `ui/tabs/calculators_tab.py`
4. Use `_create_slider_control()` for real-time updates

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters
- Add docstrings for all public methods

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-calculator`)
3. Commit your changes (`git commit -am 'Add new calculator'`)
4. Push to the branch (`git push origin feature/new-calculator`)
5. Open a Pull Request

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Team

**ITU Racing Electronics Subteam**

For questions or issues, contact the electronics team lead or open a GitHub issue.

---

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Interactive plots powered by [Plotly](https://plotly.com/python/)
- Signal processing with [SciPy](https://scipy.org/)
