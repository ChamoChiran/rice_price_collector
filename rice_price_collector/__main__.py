"""
Main entry point for rice_price_collector
----------------------------------------
Choose a module to run:
1. Downloader
2. Parser

Usage:
    python -m rice_price_collector
"""

import sys
import runpy

MENU = """
Please select an option:
1. Run PDF Downloader
2. Run Parser
Enter your choice (1 or 2): """

if __name__ == "__main__":
    choice = input(MENU).strip()
    if choice == "1":
        print("Launching PDF Downloader...")
        runpy.run_module("rice_price_collector.downloader", run_name="__main__")
    elif choice == "2":
        print("Launching Parser...")
        runpy.run_module("rice_price_collector.parser", run_name="__main__")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)