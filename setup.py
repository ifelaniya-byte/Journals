"""
Setup script for Ω-ABSOLUTE Enhanced Foundation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "ENHANCED_FOUNDATION_README.md").read_text(encoding='utf-8')

setup(
    name="omega-absolute-enhanced-foundation",
    version="0.2.0-enhanced",
    author="Ω-ABSOLUTE Project",
    description="Bounded Self-Synthesizing Causal Intelligence - Enhanced Foundation Layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ifelaniya-byte/Prime-Phantom-Abilites",
    packages=find_packages(exclude=['tests*', 'docs*', 'benchmarks*', 'experiments*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
    ],
    extras_require={
        "yaml": ["pyyaml>=6.0"],
        "dev": [
            "pytest>=7.0.0",
            "pyyaml>=6.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "omega=omega:main",
            "omega-cli=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.json", "*.md"],
    },
    keywords="artificial-intelligence governance causal-reasoning foundation",
    project_urls={
        "Bug Reports": "https://github.com/ifelaniya-byte/Prime-Phantom-Abilites/issues",
        "Source": "https://github.com/ifelaniya-byte/Prime-Phantom-Abilites",
        "Documentation": "https://github.com/ifelaniya-byte/Prime-Phantom-Abilites/blob/main/omega_absolute_enhanced/ENHANCED_FOUNDATION_README.md",
    },
)