# Parser Configuration

The parser’s behavior is controlled through `rice_price_collector/parser/config.py` and the shared project config in `rice_price_collector/config.py`. These files define the keywords, page numbers, column handling, and data directories used for extracting and processing CBSL rice price tables.

---

## Location
```text
rice_price_collector/
├── config.py                # Project-wide directories
└── parser/
    └── config.py           # Parser-specific settings
```
---

## Overview

The configuration files provide:

1. **Data directories** – Where to find raw PDFs and save processed CSVs
2. **Section extraction settings** – Keywords and page numbers for table extraction
3. **Column handling** – Number and position of price columns
4. **File naming** – Timestamp format for output files

---

## Data Directories

Defined in `rice_price_collector/config.py`:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Ensure directories exist or path in [RAW_DATA_DIR, PROCESSED_DIR]:
    path.mkdir(parents=True, exist_ok=True)
```

- `RAW_DATA_DIR`: Where input PDFs are stored (organized by year)
- `PROCESSED_DIR`: Where cleaned CSVs and batch outputs are saved

---

## Section Extraction Settings

Defined in `rice_price_collector/parser/config.py`:

```python
DEFAULT_START_WORD = "RICE"
DEFAULT_END_WORD = "FISH"
DEFAULT_PAGE_NUMBER = 2
```

- `DEFAULT_START_WORD`: Keyword marking the start of the rice price table
- `DEFAULT_END_WORD`: Keyword marking the end of the section
- `DEFAULT_PAGE_NUMBER`: Which page to extract from (usually 2)

---

## Column Handling

```python
TOTAL_PRICE_COLUMNS = 10
INSERT_POSITION = 6
```

- `TOTAL_PRICE_COLUMNS`: Expected number of price columns in the table
- `INSERT_POSITION`: Where to insert missing columns if data is incomplete

---

## File Naming

```python
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"
```

- `TIMESTAMP_FORMAT`: Used for naming output files with timestamps

---

## Good Practices

- Keep config.py versioned to track changes in extraction logic or CBSL report structure
- Adjust keywords and page numbers if CBSL changes their PDF format
- Use relative paths for portability

---

## Next Step

Continue to the batch extractor, rice extractor, or parser implementation for more details on how these settings are used.


