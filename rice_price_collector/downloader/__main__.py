"""
Main entry point for rice_price_collector.downloader
Runs the PDF downloader as a standalone module.

Usage:
    python -m rice_price_collector.downloader
"""

import asyncio
from . import download_all_pdfs

if __name__ == "__main__":
    years_input = input("Enter years to download (e.g. 2025 2024 2023): ").strip()
    years = [y for y in years_input.split() if y.isdigit()]
    if not years:
        print("No valid years provided. Example: 2025 2024 2023")
        exit(1)
    asyncio.run(download_all_pdfs(years))
