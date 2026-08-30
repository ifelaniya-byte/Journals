#!/usr/bin/env python3
"""
Demonstration script for Ω-ABSOLUTE Enhanced CLI Interface.
Shows the various CLI commands and their outputs.
"""

import sys
from pathlib import Path

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent))

def demo_cli():
    """Demonstrate CLI functionality"""
    print("=" * 70)
    print("Ω-ABSOLUTE Enhanced CLI Demonstration")
    print("=" * 70)
    print()
    
    # Import CLI module
    from cli import OmegaCLI
    
    cli = OmegaCLI()
    
    print("1. STATUS COMMAND")
    print("-" * 70)
    cli.status()
    print()
    
    print("2. INSPECT COMMAND (list all components)")
    print("-" * 70)
    cli.inspect()
    print()
    
    print("3. INSPECT COMMAND (specific component)")
    print("-" * 70)
    cli.inspect("omega.core")
    print()
    
    print("4. SOLVE DEMO")
    print("-" * 70)
    cli.solve_demo("Example task description")
    print()
    
    print("5. RESOURCE TEST")
    print("-" * 70)
    cli.resource_test()
    print()
    
    print("6. LOGGING DEMO")
    print("-" * 70)
    cli.logging_demo()
    print()
    
    print("=" * 70)
    print("CLI Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    demo_cli()