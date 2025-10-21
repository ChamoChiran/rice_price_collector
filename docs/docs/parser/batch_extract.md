# Batch Extractor

The batch extractor automates the extraction of rice price tables from all CBSL PDF reports in one or more yearly folders. It processes each PDF, parses the "RICE" section, and saves the results as combined CSV files for each year.

---

## Purpose

CBSL releases hundreds of daily price report PDFs per year. Manually extracting tables from each file is tedious and error-prone. The batch extractor:
- Scans a folder of PDFs for a given year
- Extracts and parses the "RICE" section from each file
- Combines all results into a single DataFrame
- Saves the output as a CSV for each year
- Optionally, combines multiple years for further analysis

---

## File Location

rice_price_collector/
└── parser/
    └── batch_extract.py

---

## Usage

Run from the command line to process one or more years:

```bash
python -m rice_price_collector.parser.batch_extract 2025 2024 2023
```

This will look inside:
- ../data/raw/2025/
- ../data/raw/2024/
- ../data/raw/2023/

and extract the "RICE" section from every PDF found in each folder. Each year's results are saved as CSV, and a combined file can be created for all years.

---

## Main Function: process_year_folder

```python
def process_year_folder(year_folder: Path, output_dir: Path):
    """
    Process all PDFs within a given year's folder and save the combined CSV.
    """
    # ...
```

- Iterates through all PDFs in the specified year folder
- Extracts and parses the "RICE" section using `extract_and_parse_rice`
- Adds the date (from filename) to each row
- Combines all DataFrames and saves as `rice_prices_<year>.csv`
- Prints progress and error messages for each file

---

## Example Output

```
[1/239] → 2025-01-01.pdf
[2/239] → 2025-01-02.pdf
...
Saved 236 rows → /absolute/path/to/rice_prices_2025.csv
```

---

## Error Handling

- Skips files with no "RICE" section or empty data
- Prints a message for any PDF that fails to parse
- Continues processing remaining files even if some fail

---

## Extending

- You can modify the script to process other sections (e.g., "FISH") by changing the extractor
- Combine multiple years' CSVs for time series analysis
- Integrate with the downloader for a full pipeline

---

## Next Step

Proceed to the rice extractor, parser logic, or configuration documentation for more details on each component.

[ Rice Extractor »](extractors/rice.md)
