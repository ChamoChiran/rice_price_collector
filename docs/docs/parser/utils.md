# Parser Utilities

The utilities in the parser module provide essential helper functions for extracting and cleaning rice price data from CBSL PDFs. They handle PDF text extraction and ensure data consistency in the resulting tables.

---

## Purpose

CBSL price tables are embedded in PDFs with inconsistent formatting and sometimes missing data. The utilities:
- Extract text between specific keywords in a PDF page
- Ensure all rows in the parsed table have the correct number of columns

---

## Main Functions

### 1. extract_section_between

Extracts all text between two keywords (e.g., "RICE" and "FISH") from a specific page of a PDF.

```python
def extract_section_between(pdf_path, start_letters, end_letters, page_num=2):
    # ...
```

- Uses `pdfplumber` to read the PDF and group text by line position
- Finds the y-coordinates of the start and end keywords
- Returns all lines of text between those positions
- Handles cases where keywords are spaced out (e.g., "R I C E")

**Typical usage:**
- Isolate the rice price table from a multi-table PDF

---

### 2. fix_missing_columns

Ensures each row in the price table has the expected number of columns, filling in missing values as needed.

```python
def fix_missing_columns(price_list, total_columns=10, insert_position=6):
    # ...
```

- Checks if a row has fewer columns than expected
- Inserts `None` values at the specified position to pad the row
- Returns a list with exactly `total_columns` items

**Why?**
- Some rows may be missing prices (e.g., missing retail prices)
- Ensures the DataFrame is rectangular and ready for analysis

---

## Example Usage

```python
section = extract_section_between("data/raw/2025/2025-01-01.pdf", "RICE", "FISH", page_num=2)
row = fix_missing_columns([130.00, 132.00, 135.00], total_columns=10, insert_position=6)
```

---

## Extending

- Adjust the keyword logic in `extract_section_between` to support new table formats
- Change `total_columns` or `insert_position` in `fix_missing_columns` for different data layouts

---

## Next Step

See the extractor, parser, or batch extraction documentation for how these utilities are used in the full pipeline.

[Configuration »](config.md)
