"""
Global Unit Conversion Engine for Advanced Engineering Analysis Tool.
Provides SI base units, engineering units, automatic scaling, and dimensional validation.
"""

from typing import Dict, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math


class UnitCategory(Enum):
    """Categories of physical quantities."""
    LENGTH = "length"
    MASS = "mass"
    TIME = "time"
    FORCE = "force"
    PRESSURE = "pressure"
    ENERGY = "energy"
    POWER = "power"
    VOLTAGE = "voltage"
    CURRENT = "current"
    RESISTANCE = "resistance"
    CAPACITANCE = "capacitance"
    INDUCTANCE = "inductance"
    FREQUENCY = "frequency"
    ANGLE = "angle"
    AREA = "area"
    VOLUME = "volume"
    VELOCITY = "velocity"
    ACCELERATION = "acceleration"
    TORQUE = "torque"
    MOMENT_OF_INERTIA = "moment_of_inertia"
    DENSITY = "density"
    TEMPERATURE = "temperature"


@dataclass
class UnitDefinition:
    """Definition of a unit with conversion factor to SI base."""
    name: str
    symbol: str
    category: UnitCategory
    to_si_factor: float  # Multiply by this to convert to SI base
    to_si_offset: float = 0.0  # Add this after multiplication (for temperature)


# SI Prefixes
SI_PREFIXES = {
    'Y': 1e24,   # yotta
    'Z': 1e21,   # zetta
    'E': 1e18,   # exa
    'P': 1e15,   # peta
    'T': 1e12,   # tera
    'G': 1e9,    # giga
    'M': 1e6,    # mega
    'k': 1e3,    # kilo
    'h': 1e2,    # hecto
    'da': 1e1,   # deca
    '': 1,       # base
    'd': 1e-1,   # deci
    'c': 1e-2,   # centi
    'm': 1e-3,   # milli
    'u': 1e-6,   # micro (using 'u' instead of Greek mu)
    'n': 1e-9,   # nano
    'p': 1e-12,  # pico
    'f': 1e-15,  # femto
    'a': 1e-18,  # atto
}


# Unit Definitions - All relative to SI base units
UNIT_DEFINITIONS: Dict[str, UnitDefinition] = {
    # Length (base: meter)
    'm': UnitDefinition('meter', 'm', UnitCategory.LENGTH, 1.0),
    'km': UnitDefinition('kilometer', 'km', UnitCategory.LENGTH, 1e3),
    'cm': UnitDefinition('centimeter', 'cm', UnitCategory.LENGTH, 1e-2),
    'mm': UnitDefinition('millimeter', 'mm', UnitCategory.LENGTH, 1e-3),
    'um': UnitDefinition('micrometer', 'um', UnitCategory.LENGTH, 1e-6),
    'nm': UnitDefinition('nanometer', 'nm', UnitCategory.LENGTH, 1e-9),
    'in': UnitDefinition('inch', 'in', UnitCategory.LENGTH, 0.0254),
    'ft': UnitDefinition('foot', 'ft', UnitCategory.LENGTH, 0.3048),
    'yd': UnitDefinition('yard', 'yd', UnitCategory.LENGTH, 0.9144),
    'mi': UnitDefinition('mile', 'mi', UnitCategory.LENGTH, 1609.344),

    # Mass (base: kilogram)
    'kg': UnitDefinition('kilogram', 'kg', UnitCategory.MASS, 1.0),
    'g': UnitDefinition('gram', 'g', UnitCategory.MASS, 1e-3),
    'mg': UnitDefinition('milligram', 'mg', UnitCategory.MASS, 1e-6),
    'lb': UnitDefinition('pound', 'lb', UnitCategory.MASS, 0.453592),
    'oz': UnitDefinition('ounce', 'oz', UnitCategory.MASS, 0.0283495),
    't': UnitDefinition('tonne', 't', UnitCategory.MASS, 1e3),

    # Time (base: second)
    's': UnitDefinition('second', 's', UnitCategory.TIME, 1.0),
    'ms': UnitDefinition('millisecond', 'ms', UnitCategory.TIME, 1e-3),
    'us': UnitDefinition('microsecond', 'us', UnitCategory.TIME, 1e-6),
    'ns': UnitDefinition('nanosecond', 'ns', UnitCategory.TIME, 1e-9),
    'min': UnitDefinition('minute', 'min', UnitCategory.TIME, 60.0),
    'h': UnitDefinition('hour', 'h', UnitCategory.TIME, 3600.0),

    # Force (base: Newton)
    'N': UnitDefinition('newton', 'N', UnitCategory.FORCE, 1.0),
    'kN': UnitDefinition('kilonewton', 'kN', UnitCategory.FORCE, 1e3),
    'mN': UnitDefinition('millinewton', 'mN', UnitCategory.FORCE, 1e-3),
    'lbf': UnitDefinition('pound-force', 'lbf', UnitCategory.FORCE, 4.44822),
    'kgf': UnitDefinition('kilogram-force', 'kgf', UnitCategory.FORCE, 9.80665),

    # Pressure (base: Pascal)
    'Pa': UnitDefinition('pascal', 'Pa', UnitCategory.PRESSURE, 1.0),
    'kPa': UnitDefinition('kilopascal', 'kPa', UnitCategory.PRESSURE, 1e3),
    'MPa': UnitDefinition('megapascal', 'MPa', UnitCategory.PRESSURE, 1e6),
    'GPa': UnitDefinition('gigapascal', 'GPa', UnitCategory.PRESSURE, 1e9),
    'bar': UnitDefinition('bar', 'bar', UnitCategory.PRESSURE, 1e5),
    'mbar': UnitDefinition('millibar', 'mbar', UnitCategory.PRESSURE, 1e2),
    'psi': UnitDefinition('psi', 'psi', UnitCategory.PRESSURE, 6894.76),
    'atm': UnitDefinition('atmosphere', 'atm', UnitCategory.PRESSURE, 101325.0),

    # Energy (base: Joule)
    'J': UnitDefinition('joule', 'J', UnitCategory.ENERGY, 1.0),
    'kJ': UnitDefinition('kilojoule', 'kJ', UnitCategory.ENERGY, 1e3),
    'MJ': UnitDefinition('megajoule', 'MJ', UnitCategory.ENERGY, 1e6),
    'mJ': UnitDefinition('millijoule', 'mJ', UnitCategory.ENERGY, 1e-3),
    'Wh': UnitDefinition('watt-hour', 'Wh', UnitCategory.ENERGY, 3600.0),
    'kWh': UnitDefinition('kilowatt-hour', 'kWh', UnitCategory.ENERGY, 3.6e6),
    'cal': UnitDefinition('calorie', 'cal', UnitCategory.ENERGY, 4.184),
    'kcal': UnitDefinition('kilocalorie', 'kcal', UnitCategory.ENERGY, 4184.0),
    'eV': UnitDefinition('electronvolt', 'eV', UnitCategory.ENERGY, 1.602e-19),

    # Power (base: Watt)
    'W': UnitDefinition('watt', 'W', UnitCategory.POWER, 1.0),
    'kW': UnitDefinition('kilowatt', 'kW', UnitCategory.POWER, 1e3),
    'MW': UnitDefinition('megawatt', 'MW', UnitCategory.POWER, 1e6),
    'mW': UnitDefinition('milliwatt', 'mW', UnitCategory.POWER, 1e-3),
    'hp': UnitDefinition('horsepower', 'hp', UnitCategory.POWER, 745.7),

    # Electrical - Voltage (base: Volt)
    'V': UnitDefinition('volt', 'V', UnitCategory.VOLTAGE, 1.0),
    'kV': UnitDefinition('kilovolt', 'kV', UnitCategory.VOLTAGE, 1e3),
    'mV': UnitDefinition('millivolt', 'mV', UnitCategory.VOLTAGE, 1e-3),
    'uV': UnitDefinition('microvolt', 'uV', UnitCategory.VOLTAGE, 1e-6),

    # Electrical - Current (base: Ampere)
    'A': UnitDefinition('ampere', 'A', UnitCategory.CURRENT, 1.0),
    'kA': UnitDefinition('kiloampere', 'kA', UnitCategory.CURRENT, 1e3),
    'mA': UnitDefinition('milliampere', 'mA', UnitCategory.CURRENT, 1e-3),
    'uA': UnitDefinition('microampere', 'uA', UnitCategory.CURRENT, 1e-6),
    'nA': UnitDefinition('nanoampere', 'nA', UnitCategory.CURRENT, 1e-9),

    # Electrical - Resistance (base: Ohm)
    'Ohm': UnitDefinition('ohm', 'Ohm', UnitCategory.RESISTANCE, 1.0),
    'kOhm': UnitDefinition('kiloohm', 'kOhm', UnitCategory.RESISTANCE, 1e3),
    'MOhm': UnitDefinition('megaohm', 'MOhm', UnitCategory.RESISTANCE, 1e6),
    'mOhm': UnitDefinition('milliohm', 'mOhm', UnitCategory.RESISTANCE, 1e-3),

    # Electrical - Capacitance (base: Farad)
    'F': UnitDefinition('farad', 'F', UnitCategory.CAPACITANCE, 1.0),
    'mF': UnitDefinition('millifarad', 'mF', UnitCategory.CAPACITANCE, 1e-3),
    'uF': UnitDefinition('microfarad', 'uF', UnitCategory.CAPACITANCE, 1e-6),
    'nF': UnitDefinition('nanofarad', 'nF', UnitCategory.CAPACITANCE, 1e-9),
    'pF': UnitDefinition('picofarad', 'pF', UnitCategory.CAPACITANCE, 1e-12),

    # Electrical - Inductance (base: Henry)
    'H': UnitDefinition('henry', 'H', UnitCategory.INDUCTANCE, 1.0),
    'mH': UnitDefinition('millihenry', 'mH', UnitCategory.INDUCTANCE, 1e-3),
    'uH': UnitDefinition('microhenry', 'uH', UnitCategory.INDUCTANCE, 1e-6),
    'nH': UnitDefinition('nanohenry', 'nH', UnitCategory.INDUCTANCE, 1e-9),

    # Frequency (base: Hertz)
    'Hz': UnitDefinition('hertz', 'Hz', UnitCategory.FREQUENCY, 1.0),
    'kHz': UnitDefinition('kilohertz', 'kHz', UnitCategory.FREQUENCY, 1e3),
    'MHz': UnitDefinition('megahertz', 'MHz', UnitCategory.FREQUENCY, 1e6),
    'GHz': UnitDefinition('gigahertz', 'GHz', UnitCategory.FREQUENCY, 1e9),
    'rpm': UnitDefinition('revolutions per minute', 'rpm', UnitCategory.FREQUENCY, 1/60),

    # Angle (base: radian)
    'rad': UnitDefinition('radian', 'rad', UnitCategory.ANGLE, 1.0),
    'mrad': UnitDefinition('milliradian', 'mrad', UnitCategory.ANGLE, 1e-3),
    'deg': UnitDefinition('degree', 'deg', UnitCategory.ANGLE, math.pi/180),
    'arcmin': UnitDefinition('arcminute', 'arcmin', UnitCategory.ANGLE, math.pi/10800),
    'arcsec': UnitDefinition('arcsecond', 'arcsec', UnitCategory.ANGLE, math.pi/648000),

    # Area (base: square meter)
    'm2': UnitDefinition('square meter', 'm2', UnitCategory.AREA, 1.0),
    'cm2': UnitDefinition('square centimeter', 'cm2', UnitCategory.AREA, 1e-4),
    'mm2': UnitDefinition('square millimeter', 'mm2', UnitCategory.AREA, 1e-6),
    'km2': UnitDefinition('square kilometer', 'km2', UnitCategory.AREA, 1e6),
    'in2': UnitDefinition('square inch', 'in2', UnitCategory.AREA, 6.4516e-4),
    'ft2': UnitDefinition('square foot', 'ft2', UnitCategory.AREA, 0.092903),

    # Volume (base: cubic meter)
    'm3': UnitDefinition('cubic meter', 'm3', UnitCategory.VOLUME, 1.0),
    'cm3': UnitDefinition('cubic centimeter', 'cm3', UnitCategory.VOLUME, 1e-6),
    'mm3': UnitDefinition('cubic millimeter', 'mm3', UnitCategory.VOLUME, 1e-9),
    'L': UnitDefinition('liter', 'L', UnitCategory.VOLUME, 1e-3),
    'mL': UnitDefinition('milliliter', 'mL', UnitCategory.VOLUME, 1e-6),
    'gal': UnitDefinition('gallon (US)', 'gal', UnitCategory.VOLUME, 3.78541e-3),

    # Velocity (base: m/s)
    'm/s': UnitDefinition('meter per second', 'm/s', UnitCategory.VELOCITY, 1.0),
    'km/h': UnitDefinition('kilometer per hour', 'km/h', UnitCategory.VELOCITY, 1/3.6),
    'mph': UnitDefinition('miles per hour', 'mph', UnitCategory.VELOCITY, 0.44704),
    'ft/s': UnitDefinition('feet per second', 'ft/s', UnitCategory.VELOCITY, 0.3048),
    'knot': UnitDefinition('knot', 'knot', UnitCategory.VELOCITY, 0.514444),

    # Acceleration (base: m/s2)
    'm/s2': UnitDefinition('meter per second squared', 'm/s2', UnitCategory.ACCELERATION, 1.0),
    'g': UnitDefinition('standard gravity', 'g', UnitCategory.ACCELERATION, 9.80665),
    'ft/s2': UnitDefinition('feet per second squared', 'ft/s2', UnitCategory.ACCELERATION, 0.3048),

    # Torque (base: N*m)
    'Nm': UnitDefinition('newton-meter', 'Nm', UnitCategory.TORQUE, 1.0),
    'kNm': UnitDefinition('kilonewton-meter', 'kNm', UnitCategory.TORQUE, 1e3),
    'mNm': UnitDefinition('millinewton-meter', 'mNm', UnitCategory.TORQUE, 1e-3),
    'lbf_ft': UnitDefinition('pound-foot', 'lbf_ft', UnitCategory.TORQUE, 1.35582),
    'lbf_in': UnitDefinition('pound-inch', 'lbf_in', UnitCategory.TORQUE, 0.112985),

    # Moment of Inertia - Area (base: m^4)
    'm4': UnitDefinition('meter to fourth', 'm4', UnitCategory.MOMENT_OF_INERTIA, 1.0),
    'cm4': UnitDefinition('centimeter to fourth', 'cm4', UnitCategory.MOMENT_OF_INERTIA, 1e-8),
    'mm4': UnitDefinition('millimeter to fourth', 'mm4', UnitCategory.MOMENT_OF_INERTIA, 1e-12),
    'in4': UnitDefinition('inch to fourth', 'in4', UnitCategory.MOMENT_OF_INERTIA, 4.162314e-7),

    # Density (base: kg/m3)
    'kg/m3': UnitDefinition('kilogram per cubic meter', 'kg/m3', UnitCategory.DENSITY, 1.0),
    'g/cm3': UnitDefinition('gram per cubic centimeter', 'g/cm3', UnitCategory.DENSITY, 1e3),
    'kg/L': UnitDefinition('kilogram per liter', 'kg/L', UnitCategory.DENSITY, 1e3),
    'lb/ft3': UnitDefinition('pound per cubic foot', 'lb/ft3', UnitCategory.DENSITY, 16.0185),
}


class UnitConverter:
    """Main unit conversion engine."""

    def __init__(self):
        self.units = UNIT_DEFINITIONS
        self.prefixes = SI_PREFIXES

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one unit to another.

        Args:
            value: The numerical value to convert
            from_unit: Source unit symbol
            to_unit: Target unit symbol

        Returns:
            Converted value

        Raises:
            ValueError: If units are incompatible or not found
        """
        if from_unit not in self.units:
            raise ValueError(f"Unknown unit: {from_unit}")
        if to_unit not in self.units:
            raise ValueError(f"Unknown unit: {to_unit}")

        from_def = self.units[from_unit]
        to_def = self.units[to_unit]

        if from_def.category != to_def.category:
            raise ValueError(
                f"Cannot convert between {from_def.category.value} and {to_def.category.value}"
            )

        # Convert to SI base, then to target unit
        si_value = (value * from_def.to_si_factor) + from_def.to_si_offset
        result = (si_value - to_def.to_si_offset) / to_def.to_si_factor

        return result

    def to_si(self, value: float, from_unit: str) -> float:
        """Convert a value to SI base unit."""
        if from_unit not in self.units:
            raise ValueError(f"Unknown unit: {from_unit}")

        unit_def = self.units[from_unit]
        return (value * unit_def.to_si_factor) + unit_def.to_si_offset

    def from_si(self, value: float, to_unit: str) -> float:
        """Convert a value from SI base unit."""
        if to_unit not in self.units:
            raise ValueError(f"Unknown unit: {to_unit}")

        unit_def = self.units[to_unit]
        return (value - unit_def.to_si_offset) / unit_def.to_si_factor

    def get_si_unit(self, unit: str) -> str:
        """Get the SI base unit for a given unit."""
        if unit not in self.units:
            raise ValueError(f"Unknown unit: {unit}")

        category = self.units[unit].category
        si_units = {
            UnitCategory.LENGTH: 'm',
            UnitCategory.MASS: 'kg',
            UnitCategory.TIME: 's',
            UnitCategory.FORCE: 'N',
            UnitCategory.PRESSURE: 'Pa',
            UnitCategory.ENERGY: 'J',
            UnitCategory.POWER: 'W',
            UnitCategory.VOLTAGE: 'V',
            UnitCategory.CURRENT: 'A',
            UnitCategory.RESISTANCE: 'Ohm',
            UnitCategory.CAPACITANCE: 'F',
            UnitCategory.INDUCTANCE: 'H',
            UnitCategory.FREQUENCY: 'Hz',
            UnitCategory.ANGLE: 'rad',
            UnitCategory.AREA: 'm2',
            UnitCategory.VOLUME: 'm3',
            UnitCategory.VELOCITY: 'm/s',
            UnitCategory.ACCELERATION: 'm/s2',
            UnitCategory.TORQUE: 'Nm',
            UnitCategory.MOMENT_OF_INERTIA: 'm4',
            UnitCategory.DENSITY: 'kg/m3',
        }
        return si_units.get(category, unit)

    def get_units_by_category(self, category: UnitCategory) -> Dict[str, UnitDefinition]:
        """Get all units in a specific category."""
        return {
            symbol: unit_def
            for symbol, unit_def in self.units.items()
            if unit_def.category == category
        }

    def format_with_prefix(self, value: float, unit: str, precision: int = 3) -> Tuple[float, str]:
        """
        Format a value with appropriate SI prefix.

        Args:
            value: The value to format
            unit: The base unit symbol
            precision: Number of significant digits

        Returns:
            Tuple of (scaled_value, prefixed_unit_symbol)
        """
        if value == 0:
            return 0.0, unit

        # Find the appropriate prefix
        abs_value = abs(value)
        exponent = math.floor(math.log10(abs_value))

        # Round to nearest multiple of 3 for engineering notation
        eng_exponent = (exponent // 3) * 3

        prefix_map = {
            24: 'Y', 21: 'Z', 18: 'E', 15: 'P', 12: 'T',
            9: 'G', 6: 'M', 3: 'k', 0: '',
            -3: 'm', -6: 'u', -9: 'n', -12: 'p', -15: 'f', -18: 'a'
        }

        if eng_exponent in prefix_map:
            prefix = prefix_map[eng_exponent]
            scaled_value = value / (10 ** eng_exponent)
            return round(scaled_value, precision), f"{prefix}{unit}"
        else:
            return value, unit

    def auto_scale(self, value: float, unit: str) -> Tuple[float, str]:
        """
        Automatically scale a value to a human-readable range.

        Args:
            value: The value to scale
            unit: The unit symbol

        Returns:
            Tuple of (scaled_value, new_unit)
        """
        if unit not in self.units:
            return value, unit

        category = self.units[unit].category
        available_units = self.get_units_by_category(category)

        # Convert to SI first
        si_value = self.to_si(value, unit)

        # Find the unit that gives a value closest to 1-1000 range
        best_unit = unit
        best_value = value
        best_score = abs(math.log10(abs(value)) if value != 0 else 0)

        for sym, unit_def in available_units.items():
            converted = self.from_si(si_value, sym)
            if converted != 0:
                score = abs(math.log10(abs(converted)))
                # Prefer values in 1-1000 range
                if 0 <= math.log10(abs(converted)) < 3:
                    score -= 1  # Bonus for being in nice range
                if score < best_score:
                    best_score = score
                    best_unit = sym
                    best_value = converted

        return best_value, best_unit


# Global converter instance
converter = UnitConverter()


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convenience function for unit conversion."""
    return converter.convert(value, from_unit, to_unit)


def to_si(value: float, from_unit: str) -> float:
    """Convenience function to convert to SI."""
    return converter.to_si(value, from_unit)


def from_si(value: float, to_unit: str) -> float:
    """Convenience function to convert from SI."""
    return converter.from_si(value, to_unit)


def auto_scale(value: float, unit: str) -> Tuple[float, str]:
    """Convenience function for auto-scaling."""
    return converter.auto_scale(value, unit)


def format_value(value: float, unit: str, precision: int = 3) -> str:
    """Format a value with unit for display."""
    scaled_val, scaled_unit = converter.format_with_prefix(value, unit, precision)
    return f"{scaled_val:.{precision}g} {scaled_unit}"
