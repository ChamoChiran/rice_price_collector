"""
rice_price_collector.parser

Main entry point for testing the rice PDF parsing pipeline.

Usage:
    python -m rice_price_collector.parser <pdf_path>

Example:
    python -m rice_price_collector.parser ../data/raw/2024/2024-01-03.pdf
"""

import sys
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Import local modules
from .extractors.rice import extract_and_parse_rice
from .batch_extract import process_year_folder
from ..config import RAW_DATA_DIR, PROCESSED_DIR


# Main function entry point

def main():
    # Parse CLI Args
    if len(sys.argv) < 2:
        print("Usage: python -m rice_price_collector.parser.batch_extract <year1> <year2> ...")
        sys.exit(1)

    # Accept multiple years separated by spaces
    years = [y for y in sys.argv[1:] if y.isdigit()]
    if not years:
        print("No valid years provided. Example:")
        print("    python -m rice_price_collector.parser.batch_extract 2025 2024 2023")
        sys.exit(1)

    base_dir = RAW_DATA_DIR
    output_dir = PROCESSED_DIR / "batch"
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = datetime.now()
    print("=" * 70)
    print(f"Batch Extraction Started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    combined = []
    for year in years:
        folder = base_dir / year
        if not folder.exists():
            print(f"Folder not found: {folder}")
            continue

        df_year = process_year_folder(folder, output_dir)
        if df_year is not None:
            combined.append(df_year)

    # Combine all years
    if combined:
        full_df = pd.concat(combined, ignore_index=True)
        combined_file = output_dir / "rice_prices_all_years.csv"
        full_df.to_csv(combined_file, index=False)
        print(f"\nCombined all years → {combined_file.resolve()}")
        print(f"Total rows: {len(full_df)}")
    else:
        print("\nNo data extracted from provided years.")

    print("\nDone.")


if __name__ == "__main__":
    main()