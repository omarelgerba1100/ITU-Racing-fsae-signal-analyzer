"""
Dynamic Formula Engine
Parses and executes formulas from external configuration files.
Allows updating calculations without code recompilation.
"""

import os
import re
import math
from typing import Dict, List, Tuple, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path


# Get the base directory
BASE_DIR = Path(__file__).parent.parent
FEED_DIR = BASE_DIR / 'Updates' / 'Feed'


@dataclass
class Formula:
    """Represents a parsed formula."""
    cell_ref: str           # e.g., "Sheet!A1"
    sheet: str              # Sheet name
    cell: str               # Cell reference (e.g., "A1")
    expression: str         # The formula expression
    python_expr: str        # Converted Python expression
    dependencies: List[str] = field(default_factory=list)


@dataclass
class CalculatorDefinition:
    """Definition of a calculator from parsed formulas."""
    name: str
    description: str
    inputs: Dict[str, Dict[str, Any]]   # {var_name: {label, unit, default}}
    outputs: Dict[str, Dict[str, Any]]  # {var_name: {label, unit, formula}}
    formulas: Dict[str, str]            # {var_name: python_expression}


class FormulaParser:
    """Parses Excel-style formulas into Python expressions."""

    # Excel to Python function mappings
    FUNCTION_MAP = {
        'PI': 'math.pi',
        'SIN': 'math.sin',
        'COS': 'math.cos',
        'TAN': 'math.tan',
        'ATAN': 'math.atan',
        'SQRT': 'math.sqrt',
        'ABS': 'abs',
        'DEGREES': 'math.degrees',
        'RADIANS': 'math.radians',
        'EXP': 'math.exp',
        'LOG': 'math.log',
        'LOG10': 'math.log10',
        'POWER': 'pow',
        'IFERROR': '_iferror',
    }

    @staticmethod
    def parse_cell_ref(cell_ref: str) -> Tuple[str, str]:
        """Parse a cell reference into sheet and cell parts."""
        if '!' in cell_ref:
            sheet, cell = cell_ref.split('!', 1)
            return sheet, cell
        return '', cell_ref

    @staticmethod
    def cell_to_var(cell_ref: str) -> str:
        """Convert cell reference to a valid Python variable name."""
        # Replace special characters
        var = cell_ref.replace('!', '_').replace(' ', '_').replace('-', '_')
        var = re.sub(r'[^a-zA-Z0-9_]', '', var)
        return f"cell_{var}"

    @classmethod
    def excel_to_python(cls, formula: str, sheet_context: str = '') -> str:
        """
        Convert Excel formula to Python expression.

        Args:
            formula: Excel formula string (without leading =)
            sheet_context: Current sheet name for relative references

        Returns:
            Python expression string
        """
        if formula.startswith('='):
            formula = formula[1:]

        expr = formula

        # Replace Excel functions with Python equivalents
        for excel_func, python_func in cls.FUNCTION_MAP.items():
            # Handle PI() specifically
            if excel_func == 'PI':
                expr = re.sub(r'\bPI\(\)', python_func, expr, flags=re.IGNORECASE)
            else:
                expr = re.sub(
                    rf'\b{excel_func}\s*\(',
                    f'{python_func}(',
                    expr,
                    flags=re.IGNORECASE
                )

        # Replace cell references with variable names
        # Pattern matches references like A1, Sheet!A1, 'Sheet Name'!A1
        cell_pattern = r"([A-Za-z_][A-Za-z0-9_ -]*!)?([A-Z]+[0-9]+)"

        def replace_cell(match):
            full_match = match.group(0)
            sheet_part = match.group(1) or ''
            cell_part = match.group(2)

            if sheet_part:
                # Has sheet reference
                sheet_name = sheet_part.rstrip('!')
            else:
                # Use context sheet
                sheet_name = sheet_context

            full_ref = f"{sheet_name}!{cell_part}" if sheet_name else cell_part
            return cls.cell_to_var(full_ref)

        expr = re.sub(cell_pattern, replace_cell, expr)

        # Replace ^ with ** for exponentiation
        expr = expr.replace('^', '**')

        return expr

    @classmethod
    def extract_dependencies(cls, formula: str, sheet_context: str = '') -> List[str]:
        """Extract cell references from a formula."""
        if formula.startswith('='):
            formula = formula[1:]

        dependencies = []
        cell_pattern = r"([A-Za-z_][A-Za-z0-9_ -]*!)?([A-Z]+[0-9]+)"

        for match in re.finditer(cell_pattern, formula):
            sheet_part = match.group(1) or ''
            cell_part = match.group(2)

            if sheet_part:
                sheet_name = sheet_part.rstrip('!')
            else:
                sheet_name = sheet_context

            full_ref = f"{sheet_name}!{cell_part}" if sheet_name else cell_part
            dependencies.append(full_ref)

        return dependencies


class FormulaEngine:
    """
    Dynamic formula execution engine.
    Loads formulas from external files and executes them.
    """

    def __init__(self, feed_dir: Path = FEED_DIR):
        self.feed_dir = feed_dir
        self.formulas: Dict[str, Formula] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.named_ranges: Dict[str, str] = {}
        self.calculators: Dict[str, CalculatorDefinition] = {}

        # Load formulas on initialization
        self.load_all()

    def load_all(self):
        """Load all formula files."""
        self.load_formulas()
        self.load_dependencies()
        self.load_named_ranges()
        self._build_calculators()

    def load_formulas(self):
        """Load formulas from 01_formulas.txt."""
        formula_file = self.feed_dir / '01_formulas.txt'
        if not formula_file.exists():
            return

        current_sheet = ''

        with open(formula_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Check for sheet header
                if line.startswith('=== Sheet:'):
                    match = re.match(r'=== Sheet: (.+) ===', line)
                    if match:
                        current_sheet = match.group(1)
                    continue

                # Parse formula line: "Sheet!Cell = =formula"
                if ' = =' in line:
                    parts = line.split(' = =', 1)
                    if len(parts) == 2:
                        cell_ref = parts[0].strip()
                        formula_expr = '=' + parts[1].strip()

                        sheet, cell = FormulaParser.parse_cell_ref(cell_ref)
                        if not sheet:
                            sheet = current_sheet

                        python_expr = FormulaParser.excel_to_python(formula_expr, sheet)
                        deps = FormulaParser.extract_dependencies(formula_expr, sheet)

                        self.formulas[cell_ref] = Formula(
                            cell_ref=cell_ref,
                            sheet=sheet,
                            cell=cell,
                            expression=formula_expr,
                            python_expr=python_expr,
                            dependencies=deps
                        )

    def load_dependencies(self):
        """Load dependencies from 03_dependencies.txt."""
        dep_file = self.feed_dir / '03_dependencies.txt'
        if not dep_file.exists():
            return

        with open(dep_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '->' not in line:
                    continue

                parts = line.split(' -> ')
                if len(parts) == 2:
                    source = parts[0].strip()
                    target = parts[1].strip()

                    if target not in self.dependencies:
                        self.dependencies[target] = []
                    self.dependencies[target].append(source)

    def load_named_ranges(self):
        """Load named ranges from 02_named_ranges.txt."""
        nr_file = self.feed_dir / '02_named_ranges.txt'
        if not nr_file.exists():
            return

        with open(nr_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue

                parts = line.split('=', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    ref = parts[1].strip()
                    self.named_ranges[name] = ref

    def _build_calculators(self):
        """Build calculator definitions from parsed formulas."""
        # Group formulas by sheet
        sheets: Dict[str, List[Formula]] = {}
        for formula in self.formulas.values():
            if formula.sheet not in sheets:
                sheets[formula.sheet] = []
            sheets[formula.sheet].append(formula)

        # Create calculator for each sheet with formulas
        for sheet_name, formulas in sheets.items():
            if not formulas:
                continue

            # Determine inputs (cells referenced but not defined)
            all_deps = set()
            all_outputs = set()

            for formula in formulas:
                all_outputs.add(formula.cell_ref)
                for dep in formula.dependencies:
                    all_deps.add(dep)

            inputs = all_deps - all_outputs

            calc = CalculatorDefinition(
                name=sheet_name,
                description=f"Calculator from {sheet_name}",
                inputs={FormulaParser.cell_to_var(inp): {'ref': inp} for inp in inputs},
                outputs={FormulaParser.cell_to_var(f.cell_ref): {'ref': f.cell_ref, 'formula': f.python_expr} for f in formulas},
                formulas={FormulaParser.cell_to_var(f.cell_ref): f.python_expr for f in formulas}
            )
            self.calculators[sheet_name] = calc

    def calculate(self, sheet: str, inputs: Dict[str, float]) -> Dict[str, float]:
        """
        Execute calculations for a sheet.

        Args:
            sheet: Sheet name
            inputs: Dictionary of input values {cell_ref: value}

        Returns:
            Dictionary of calculated values {cell_ref: value}
        """
        if sheet not in self.calculators:
            return {}

        calc = self.calculators[sheet]

        # Build namespace with inputs
        namespace = {
            'math': math,
            '_iferror': lambda expr, default: default if expr is None else expr,
        }

        # Add input values
        for cell_ref, value in inputs.items():
            var_name = FormulaParser.cell_to_var(cell_ref)
            namespace[var_name] = value

        # Sort formulas by dependencies and execute
        results = {}
        executed = set()

        def execute_formula(var_name: str, formula: str):
            if var_name in executed:
                return

            # Execute dependencies first
            for dep_var in self._extract_vars(formula):
                if dep_var in calc.formulas and dep_var not in executed:
                    execute_formula(dep_var, calc.formulas[dep_var])

            try:
                result = eval(formula, namespace)
                namespace[var_name] = result
                results[var_name] = result
                executed.add(var_name)
            except Exception as e:
                results[var_name] = None
                executed.add(var_name)

        for var_name, formula in calc.formulas.items():
            execute_formula(var_name, formula)

        return results

    def _extract_vars(self, formula: str) -> List[str]:
        """Extract variable names from a formula."""
        return re.findall(r'cell_[A-Za-z0-9_]+', formula)

    def get_calculator_info(self, sheet: str) -> Optional[CalculatorDefinition]:
        """Get calculator definition for a sheet."""
        return self.calculators.get(sheet)

    def list_calculators(self) -> List[str]:
        """List available calculator names."""
        return list(self.calculators.keys())


# Global engine instance
_engine: Optional[FormulaEngine] = None


def get_engine() -> FormulaEngine:
    """Get or create the global formula engine."""
    global _engine
    if _engine is None:
        _engine = FormulaEngine()
    return _engine


def reload_formulas():
    """Reload formulas from files."""
    global _engine
    _engine = FormulaEngine()


def calculate(sheet: str, inputs: Dict[str, float]) -> Dict[str, float]:
    """Execute calculations for a sheet."""
    return get_engine().calculate(sheet, inputs)


def list_calculators() -> List[str]:
    """List available calculators."""
    return get_engine().list_calculators()
