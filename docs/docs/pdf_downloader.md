
# PDF Downloader Module

The **PDF Downloader** is a fully asynchronous module that automatically fetches and organizes **daily rice price reports** from the [Central Bank of Sri Lanka (CBSL)](https://www.cbsl.gov.lk) website.

It forms the first stage of the **Rice Price Collector** pipeline, responsible for retrieving raw report PDFs before extraction and analysis.

---

## Overview

- Built on `aiohttp` + `asyncio` for concurrent, efficient downloads  
- Handles CBSL’s paginated AJAX interface  
- Extracts report dates from link text to name files  
- Organizes reports automatically by year  
- Avoids duplicate downloads  
- Gracefully skips malformed or empty links  

---

## How It Works

1. The module sends async POST requests to CBSL’s internal AJAX endpoint.  
2. Each response contains an embedded HTML fragment listing PDF links.  
3. The script extracts these links and parses dates from their titles.  
4. PDFs are downloaded concurrently (five at a time by default).  
5. Files are stored neatly under `data/raw/<year>/`.

---

## Example Console Output

Fetching reports for 2025 (year_id=88)...
Found 24 reports on page 0 (2025)
Found 24 reports on page 1 (2025)
Total PDFs found for 2025: 378
Starting downloads for 2025...
Saved data/raw/2025/2025-09-25.pdf
Saved data/raw/2025/2025-09-26.pdf
Completed downloads for 2025. Saved in data/raw/2025

---

## Run the Downloader

From your project root, run:

```bash
python -m rice_price_collector.downloader.pdf_dowloader
```

This will:

- Fetch all CBSL daily price reports for the configured years
- Create a folder per year inside data/raw/
- Download all available PDFs concurrently

**Output Folder Example**

```
data/raw/
├── 2023/
│   ├── 2023-06-18.pdf
│   └── ...
├── 2024/
│   ├── 2024-07-05.pdf
│   └── ...
└── 2025/
    ├── 2025-09-25.pdf
    └── 2025-09-26.pdf
```

---

## Key Dependencies

- `aiohttp` – asynchronous HTTP client
- `asyncio` – concurrency handling
- `BeautifulSoup4` – HTML parsing
- `datetime` – date parsing
- `os` / `urllib.parse` – file and path utilities

---


## Notes

- Each year’s CBSL reports are identified by a numeric year_id in the code (e.g. 88 for 2025).
- The downloader uses polite scraping practices — 1-second pauses per page and limited concurrency.
- Any malformed or duplicate entries are automatically skipped.

---

## Module Location

```text
rice_price_collector/downloader/pdf_dowloader.py
```
