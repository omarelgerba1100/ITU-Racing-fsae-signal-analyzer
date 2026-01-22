"""
Constants, equations, and reference data for FSAE signal processing.
"""

# LaTeX equations with descriptions
EQUATIONS = [
    ("Nyquist Theorem", r"f_{max} = \frac{f_s}{2}",
     "Maximum frequency that can be captured = Sampling rate / 2\nExample: 2000 Hz sampling -> max 1000 Hz signal"),

    ("FFT Frequency Resolution", r"\Delta f = \frac{f_s}{N}",
     "Frequency bin width = Sampling rate / Number of samples\nExample: 2000 Hz, 2000 samples -> 1 Hz resolution"),

    ("RMS (Root Mean Square)", r"RMS = \sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2}",
     "Represents the 'effective' value of an AC signal\nUsed for vibration severity assessment"),

    ("Decibel (Voltage)", r"dB = 20 \cdot \log_{10}\left(\frac{V_{out}}{V_{in}}\right)",
     "Logarithmic ratio for voltage/amplitude signals"),

    ("Decibel (Power)", r"dB = 10 \cdot \log_{10}\left(\frac{P_{out}}{P_{in}}\right)",
     "Logarithmic ratio for power signals"),

    ("Butterworth Filter", r"|H(j\omega)|^2 = \frac{1}{1 + \left(\frac{\omega}{\omega_c}\right)^{2n}}",
     "Maximally flat magnitude response\nn = filter order, wc = cutoff frequency"),

    ("DFT (Discrete Fourier Transform)", r"X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j\frac{2\pi kn}{N}}",
     "Converts time-domain signal to frequency-domain"),

    ("Wheel Speed Calculation", r"v = \frac{f \cdot \pi \cdot D}{n}",
     "f = pulse frequency, D = tire diameter, n = pulses/revolution"),

    ("Natural Frequency", r"f_n = \frac{1}{2\pi}\sqrt{\frac{k}{m}}",
     "k = stiffness (N/m), m = mass (kg)\nUsed for suspension resonance calculation"),

    ("Damping Ratio", r"\zeta = \frac{c}{2\sqrt{km}}",
     "c = damping coefficient, k = stiffness, m = mass\nz < 1: underdamped, z = 1: critically damped"),

    ("Power Spectral Density", r"S_{xx}(f) = \lim_{T\to\infty} \frac{1}{T}|X(f)|^2",
     "Shows power distribution across frequencies"),

    ("ADC Resolution", r"Resolution = \frac{V_{ref}}{2^n}",
     "n = ADC bits\n10-bit, 5V ref -> 4.88 mV\n12-bit, 5V ref -> 1.22 mV"),

    ("RC Time Constant", r"\tau = R \cdot C",
     "Time for capacitor to charge to 63.2% or discharge to 36.8%"),

    ("Capacitor Voltage (Charging)", r"V(t) = V_s \cdot \left(1 - e^{-t/\tau}\right)",
     "Vs = supply voltage, tau = RC time constant"),

    ("Capacitor Voltage (Discharging)", r"V(t) = V_0 \cdot e^{-t/\tau}",
     "V0 = initial voltage, tau = RC time constant"),

    ("RC Filter Cutoff Frequency", r"f_c = \frac{1}{2\pi RC}",
     "R = resistance (Ohms), C = capacitance (Farads)"),

    ("Wheatstone Bridge Balance", r"\frac{R_1}{R_2} = \frac{R_3}{R_4}",
     "Bridge is balanced when no current flows through galvanometer"),

    ("Wien Bridge Frequency", r"f = \frac{1}{2\pi RC}",
     "Frequency at which bridge is balanced"),

    ("Battery Capacity", r"C = I \cdot t",
     "C = capacity (Ah), I = current (A), t = time (hours)"),
]

# FSAE Reference guide sections
FSAE_REFERENCE = {
    'sensors': """
Common FSAE Sensors & Signals:
+---------------------+------------------+-----------------+-----------------------------------------+
| Sensor              | Signal Type      | Typical Fs      | Key Processing                          |
+---------------------+------------------+-----------------+-----------------------------------------+
| Wheel Speed (ABS)   | Digital/Pulse    | 1-10 kHz        | Frequency counting, edge detection      |
| Accelerometer       | Analog           | 1-5 kHz         | FFT, filtering, integration             |
| Gyroscope (IMU)     | Analog/Digital   | 100-1000 Hz     | Integration, complementary filter       |
| Strain Gauge        | Analog           | 1-10 kHz        | Amplification, Wheatstone bridge        |
| Thermocouple        | Analog           | 1-100 Hz        | Cold junction compensation, filtering   |
| Pressure Sensor     | Analog           | 100-1000 Hz     | Low-pass filtering, calibration         |
| LVDT/Potentiometer  | Analog           | 100-500 Hz      | Low-pass filtering                      |
| Lambda Sensor       | Analog           | 10-100 Hz       | Averaging, lookup tables                |
+---------------------+------------------+-----------------+-----------------------------------------+
""",

    'resonance': """
Typical Resonance Frequencies:
+-------------------------+-----------------+--------------------------------------------------------+
| Component               | Frequency Range | Notes                                                  |
+-------------------------+-----------------+--------------------------------------------------------+
| Sprung mass (body)      | 1-2 Hz          | Ride frequency, affects comfort                        |
| Unsprung mass (wheel)   | 10-15 Hz        | Wheel hop frequency                                    |
| Tire                    | 30-80 Hz        | Depends on pressure, temperature                       |
| Drivetrain              | 50-200 Hz       | Gear mesh, CV joints                                   |
| Engine harmonics        | RPM/60 x n      | n = 0.5, 1, 1.5, 2... for 4-cylinder                   |
| Aerodynamic flutter     | 10-50 Hz        | Wings, undertray                                       |
+-------------------------+-----------------+--------------------------------------------------------+
""",

    'filters': """
Filter Selection Guide:

LOW-PASS FILTER:
  - Use: Remove high-frequency noise from sensor signals
  - FSAE Example: Smoothing accelerometer data, tire temperature
  - Typical cutoff: 10-50 Hz for vehicle dynamics

HIGH-PASS FILTER:
  - Use: Remove DC offset and low-frequency drift
  - FSAE Example: AC-coupling accelerometer, removing bias
  - Typical cutoff: 0.1-1 Hz

BAND-PASS FILTER:
  - Use: Isolate specific frequency range of interest
  - FSAE Example: Extracting engine harmonics, wheel speed signal
  - Example: 40-60 Hz to isolate tire resonance

BAND-STOP (NOTCH) FILTER:
  - Use: Remove specific unwanted frequency
  - FSAE Example: Removing 50/60 Hz electrical noise
  - Also used to remove known mechanical resonances

+-------------+---------------------+---------------------+------------------------------------------+
| Filter Type | Frequency Response  | Phase Response      | Best For                                 |
+-------------+---------------------+---------------------+------------------------------------------+
| Butterworth | Maximally flat      | Non-linear          | General purpose, good all-rounder        |
| Chebyshev   | Sharper rolloff     | More non-linear     | When sharp cutoff needed                 |
| Bessel      | Gradual rolloff     | Linear (minimal)    | When signal shape must be preserved      |
+-------------+---------------------+---------------------+------------------------------------------+
""",

    'quiz': """
Common FSAE Quiz Questions:

Q1: What is the minimum sampling frequency to capture a 50 Hz vibration?
A1: 100 Hz minimum (Nyquist), but 250-500 Hz recommended for accuracy

Q2: How do you remove 50 Hz electrical noise from a sensor signal?
A2: Use a notch (band-stop) filter centered at 50 Hz

Q3: Why use a low-pass filter on accelerometer data?
A3: To remove high-frequency noise and aliasing, typically cutoff at 50-100 Hz

Q4: What causes aliasing and how to prevent it?
A4: Sampling below Nyquist rate. Prevent with anti-aliasing filter before ADC

Q5: How to calculate vehicle speed from wheel speed sensor pulses?
A5: Count pulses/second x tire circumference / pulses per revolution

Q6: What is the purpose of a complementary filter in IMU?
A6: Combines gyro (good short-term) and accelerometer (good long-term) data

Q7: How to identify resonance frequency from FFT?
A7: Look for the peak in the frequency spectrum (highest amplitude)

Q8: What filter type preserves signal shape best?
A8: Bessel filter (linear phase response)

Q9: What is the -3dB point of a filter?
A9: The cutoff frequency where power is reduced by half (amplitude by sqrt(2))

Q10: How does filter order affect performance?
A10: Higher order = sharper cutoff, but more phase distortion and computation
""",

    'tips': """
Practical Tips:

DATA ACQUISITION:
  - Always use hardware anti-aliasing filter before ADC
  - Sample at 5-10x your maximum frequency of interest
  - Use shielded cables for analog sensors
  - Implement proper grounding (star ground)
  - Calibrate sensors before each test session
  - Log raw data - filter in post-processing when possible
  - Use differential inputs for noise rejection
  - Consider CAN bus for digital sensor communication

SIGNAL PROCESSING:
  - Remove DC offset before FFT analysis
  - Use windowing (Hanning, Hamming) to reduce spectral leakage
  - Zero-pad for better frequency resolution
  - Use Welch method for more stable PSD estimates
  - Check for saturation/clipping in raw data
  - Document all calibration factors and units

NOISE REDUCTION:
  - Hardware: Shielding, twisted pairs, proper grounding
  - Software: Averaging, filtering, oversampling
  - Always filter AFTER saving raw data
"""
}
