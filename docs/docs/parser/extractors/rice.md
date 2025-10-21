# Rice Extractor

The rice extractor is a specialized function for extracting and parsing the "RICE" price table from CBSL price report PDFs. It locates the relevant section, parses the text into a structured DataFrame, and assigns meaningful column names based on the detected markets and days.

---

## Purpose

CBSL price report PDFs contain multiple tables for different commodities. The rice extractor automates:
- Locating the "RICE" section within a PDF page
- Parsing the messy text into a clean, tabular DataFrame
- Assigning smart column names for easy analysis

---

## File Location

rice_price_collector/
└── parser/
    └── extractors/
        └── rice.py

---

## Main Function: extract_and_parse_rice

```python
def extract_and_parse_rice(pdf_path, start_word="RICE", end_word="FISH", page_number=2):
    """
    Extracts the RICE section from a PDF and converts it to a table with smart column names.
    """
    # ...
```

### What it does:
1. Uses `extract_section_between` to find all text between the start and end keywords (default: "RICE" to "FISH") on the specified page (default: 2).
2. Parses the extracted lines into a DataFrame using `parse_price_section`.
3. Generates meaningful column names with `create_smart_column_names` and assigns them to the DataFrame.

---

## Parameters

- `pdf_path`: Path to the PDF file
- `start_word`: Section start keyword (default: "RICE")
- `end_word`: Section end keyword (default: "FISH")
- `page_number`: Page number to extract from (default: 2)

---

## Returns

A pandas DataFrame containing the parsed rice price data with smart column names.

---

## Example Usage

```python
from rice_price_collector.parser.extractors.rice import extract_and_parse_rice

df = extract_and_parse_rice("data/raw/2025/2025-01-01.pdf")
print(df.head())
```

---

## Extending

- Change `start_word` and `end_word` to extract other sections (e.g., "FISH")
- Adjust `page_number` if the table appears on a different page
- Integrate with batch extraction to process entire year folders

---

## Next Step

See the parser logic, batch extractor, or configuration documentation for more details on the full extraction pipeline.

[Columns »](../columns.md)