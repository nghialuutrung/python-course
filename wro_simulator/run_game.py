#!/usr/bin/env python3
"""
WRO Python Robot Control System - Main Launcher
Professional modular architecture for educational robot programming
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main application
try:
    from src.main import main
except ImportError:
    # Fallback for direct execution
    import src.main as main_module
    main = main_module.main

if __name__ == "__main__":
    main()
