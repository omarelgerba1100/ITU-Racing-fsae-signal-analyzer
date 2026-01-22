#!/usr/bin/env python3
"""
ITU Racing - FSAE Signal Analysis Tool
Setup script for pip installation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = 'FSAE Signal Analysis Tool for Formula Student teams'

setup(
    name='fsae-signal-analyzer',
    version='2.0.0',
    author='ITU Racing Electronics Team',
    author_email='electronics@ituracing.com',
    description='Professional signal processing application for Formula Student teams',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ITU-Racing/fsae-signal-analyzer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    python_requires='>=3.8',
    install_requires=[
        'customtkinter>=5.2.0',
        'CTkMessagebox>=2.5',
        'plotly>=5.18.0',
        'matplotlib>=3.7.0',
        'pillow>=10.0.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'openpyxl>=3.1.0',
        'scipy>=1.11.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
        'build': [
            'pyinstaller>=6.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'fsae-analyzer=fsae_signal_analyzer.main:main',
        ],
        'gui_scripts': [
            'fsae-analyzer-gui=fsae_signal_analyzer.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'fsae_signal_analyzer': [
            '*.md',
            '*.txt',
        ],
    },
    keywords='fsae formula-student signal-processing electronics engineering',
    project_urls={
        'Bug Reports': 'https://github.com/ITU-Racing/fsae-signal-analyzer/issues',
        'Source': 'https://github.com/ITU-Racing/fsae-signal-analyzer',
    },
)
