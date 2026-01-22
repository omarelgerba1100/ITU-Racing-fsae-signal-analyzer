"""
Data loading utilities with auto-detection of file formats.
"""

import os
import re
import io
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


class DataLoader:
    """Handle data loading with auto-detection of file formats."""

    @staticmethod
    def detect_format(content: str) -> Tuple[str, bool]:
        """
        Auto-detect file format from content.

        Args:
            content: File content as string

        Returns:
            Tuple of (delimiter, comma_is_decimal)
        """
        lines = [line.strip() for line in content.split('\n') if line.strip()][:20]
        sample = '\n'.join(lines)

        # Detect decimal separator
        european_pattern = re.findall(r'-?\d+,\d+', sample)
        standard_pattern = re.findall(r'-?\d+\.\d+', sample)
        comma_is_decimal = len(european_pattern) > len(standard_pattern)

        # Test sample for delimiter detection
        test_sample = sample.replace(',', '.') if comma_is_decimal else sample

        # Count delimiters
        delimiters = {
            '\t': test_sample.count('\t'),
            ';': test_sample.count(';'),
            ' ': len(re.findall(r'  +', test_sample)) + len(re.findall(r'(?<!\s) (?!\s)', test_sample)),
        }

        if not comma_is_decimal:
            delimiters[','] = sample.count(',')

        best_delim = max(delimiters, key=delimiters.get)
        if delimiters[best_delim] == 0:
            best_delim = ' '

        return best_delim, comma_is_decimal

    @staticmethod
    def load(filepath: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Load data file with auto-detection.

        Args:
            filepath: Path to data file

        Returns:
            Tuple of (data array, info dict)
        """
        ext = os.path.splitext(filepath)[1].lower()

        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath, header=None)
            data = df.values.flatten()
            data = np.array([
                float(str(x).replace(',', '.')) if isinstance(x, str) else float(x)
                for x in data if pd.notna(x)
            ])
            info = {'type': 'Excel', 'delimiter': 'N/A', 'decimal': 'auto'}
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            delimiter, comma_is_decimal = DataLoader.detect_format(content)

            if comma_is_decimal:
                content = content.replace(',', '.')

            try:
                if delimiter == '\t':
                    data = np.loadtxt(io.StringIO(content), delimiter='\t')
                elif delimiter == ';':
                    data = np.loadtxt(io.StringIO(content), delimiter=';')
                elif delimiter == ',':
                    data = np.loadtxt(io.StringIO(content), delimiter=',')
                else:
                    data = np.loadtxt(io.StringIO(content))
            except Exception:
                numbers = re.findall(r'-?\d+\.?\d*', content)
                data = np.array([float(n) for n in numbers])

            data = data.flatten()
            delim_names = {'\t': 'TAB', ' ': 'SPACE', ',': 'COMMA', ';': 'SEMICOLON'}
            info = {
                'type': 'Text',
                'delimiter': delim_names.get(delimiter, delimiter),
                'decimal': 'European (,)' if comma_is_decimal else 'Standard (.)'
            }

        return data, info

    @staticmethod
    def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
        """
        Load CSV file as pandas DataFrame.

        Args:
            filepath: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv

        Returns:
            pandas DataFrame
        """
        return pd.read_csv(filepath, **kwargs)

    @staticmethod
    def save_data(data: np.ndarray, filepath: str, delimiter: str = ','):
        """
        Save data array to file.

        Args:
            data: Data array to save
            filepath: Output file path
            delimiter: Column delimiter
        """
        np.savetxt(filepath, data, delimiter=delimiter)
