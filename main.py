#!/usr/bin/env python3
"""
ITU Racing - Advanced FSAE Signal Analysis Tool
================================================
A professional signal processing application for Formula Student teams.

Run this file to start the application:
    python main.py

Requirements:
    pip install customtkinter CTkMessagebox plotly pandas numpy scipy matplotlib pillow openpyxl
"""

from ui.main_window import FSAESignalAnalyzer


def main():
    """Main entry point for the application."""
    print("""
+======================================================================+
|  ITU Racing - FSAE Signal Analysis Tool v2.0                         |
+======================================================================+
|  Required packages:                                                  |
|    pip install customtkinter CTkMessagebox plotly pandas             |
|              numpy scipy matplotlib pillow                           |
+======================================================================+
    """)

    app = FSAESignalAnalyzer()
    app.mainloop()


if __name__ == "__main__":
    main()
