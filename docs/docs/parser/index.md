# Parser Module Overview

The Parser module is responsible for extracting, cleaning, and structuring rice price data from CBSL price report PDFs. It transforms raw, unstructured text into clean, analysis-ready tables using a modular, extensible pipeline.

---

## Purpose

CBSL price reports contain rice price tables embedded in PDFs, with inconsistent formatting and occasional missing data. The Parser automates:
- Locating and extracting the relevant table section from each PDF
- Parsing messy text into structured rows and columns
- Cleaning, aligning, and labeling columns for downstream analysis
- Batch processing of entire year folders for large-scale data extraction

---

## Key Features

| Feature                  | Description                                                                 |
|------------------------- |-----------------------------------------------------------------------------|
| Section extraction       | Finds and extracts the “RICE” section from each PDF using keyword boundaries |
| Smart column naming      | Dynamically generates column names based on detected markets and days         |
| Data cleaning utilities  | Fixes missing columns, merges broken lines, and standardizes units            |
| Batch processing         | Processes all PDFs in a year folder and outputs combined CSVs                 |
| Extensible extractors    | Easily add new extractors for other commodities or table types                |

---

## Module Structure
```text
rice_price_collector/parser/
├── __init__.py
├── batch_extract.py      # Batch extraction for multiple years
├── columns.py            # Smart column naming logic
├── config.py             # Extraction and cleaning settings
├── extractors/
│   └── rice.py           # Main rice table extractor
├── parser.py             # Core parsing logic for price tables
└── utils.py              # PDF section extraction and helpers
```
---

## Main Components

- **extract_and_parse_rice** (extractors/rice.py): Extracts and parses the rice price table from a PDF page.
- **parse_price_section** (parser.py): Cleans and splits raw text into a DataFrame.
- **create_smart_column_names** (columns.py): Generates meaningful column names based on detected markets.
- **extract_section_between** (utils.py): Extracts text between keywords in a PDF page.
- **fix_missing_columns** (utils.py): Ensures all rows have the correct number of columns.
- **process_year_folder** (batch_extract.py): Processes all PDFs in a year folder and saves combined CSVs.

---

## Example Usage

**Batch extract all years:**

```bash
python -m rice_price_collector.parser.batch_extract 2025 2024 2023
```

**Extract and parse a single PDF:**

```python
from rice_price_collector.parser.extractors.rice import extract_and_parse_rice

df = extract_and_parse_rice("data/raw/2025/2025-01-01.pdf")
print(df.head())
```

---

## Data Flow

PDF file → Extract section → Parse text → Clean columns → Output DataFrame/CSV

---

## Next Step

Continue to the batch extractor, rice extractor, or configuration documentation for more details on each component.

[Batch Extractor »](batch_extract.md)
