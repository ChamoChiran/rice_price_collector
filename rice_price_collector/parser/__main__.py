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
import pandas as pd

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

# Utility: process a dict of years and folders
def process_year_folders_dict(year_folder_dict, output_dir=None):
    """
    Process a dictionary mapping years to folder paths, combine results into a DataFrame.
    Args:
        year_folder_dict (dict): {"2023": "/path/to/2023", ...}
        output_dir (Path or str, optional): Where to save combined CSV (if provided)
    Returns:
        pd.DataFrame: Combined DataFrame for all years
    """

    combined = []
    for year, folder in year_folder_dict.items():
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"Folder not found: {folder_path}")
            continue
        df_year = process_year_folder(folder_path, output_dir) if output_dir else process_year_folder(folder_path, Path("."))
        if df_year is not None:
            combined.append(df_year)
    if combined:
        full_df = pd.concat(combined, ignore_index=True)
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            combined_file = output_dir / "rice_prices_all_years.csv"
            full_df.to_csv(combined_file, index=False)
            print(f"\nCombined all years → {combined_file.resolve()}")
        return full_df
    else:
        print("No data extracted from provided folders.")
        return None


if __name__ == "__main__":
    main()