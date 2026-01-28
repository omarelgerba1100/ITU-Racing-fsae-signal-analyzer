"""Browser-based calculator system."""

from .calculator_html import open_calculator_in_browser, save_calculator_html
from .calculator_data import CALCULATORS

__all__ = ['open_calculator_in_browser', 'save_calculator_html', 'CALCULATORS']
