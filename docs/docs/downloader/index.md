# Downloader Module Overview

The **Downloader Module** is responsible for automatically fetching **daily rice price PDF reports** from the **Central Bank of Sri Lanka (CBSL)** website.  
It uses asynchronous HTTP requests to efficiently download hundreds of reports across multiple years, ensuring a consistent and up-to-date local dataset for parsing.

---

## Purpose

The CBSL publishes daily “Price Reports” containing retail and wholesale rice prices for Pettah and Marandagahamula.  
Manually saving these PDFs is tedious — so this module automates that process.

The downloader:
- Crawls CBSL’s price publications endpoint.
- Paginates through all available reports.
- Extracts publication dates and direct PDF URLs.
- Downloads and saves them to structured folders (e.g., `data/raw/2023/2023-05-14.pdf`).

---

## Key Features

| Feature | Description |
|----------|--------------|
| **Asynchronous downloading** | Built on `aiohttp`, allowing many reports to be fetched in parallel. |
| **Dynamic pagination** | Automatically traverses CBSL’s AJAX-based pages until no new PDFs are found. |
| **Resumable runs** | Skips already downloaded files to avoid duplication. |
| **Robust error handling** | Retries failed requests and logs warnings for missing or invalid URLs. |
| **Configurable base URLs** | Controlled entirely via `config.py`, so adapting to new CBSL endpoints is simple. |
| **Year-wise output directories** | PDFs are neatly organized by publication year for easier versioning and parsing. |

---

## Module Structure
```text
rice_price_collector/downloader/
├── init.py
├── main.py
├── config.py ← CBSL URLs and output directories
└── pdf_downloader.py ← Core logic: fetch_page(), scrape_all(), save_pdf()
```

---

## Configuration (`config.py`)

The configuration file defines the key constants and directories used by the module:

```python
BASE = "https://www.cbsl.gov.lk/publications/price"
AJAX_URL = "https://www.cbsl.gov.lk/views/ajax"
OUTPUT_DIR = "data/raw"
```

You can update:
- BASE to match the CBSL “Price Reports” main page.
- AJAX_URL if CBSL changes their internal data request endpoint.
- OUTPUT_DIR to change where files are saved.

---

## How It Works

**Initialize session**  
The module starts an aiohttp.ClientSession for efficient reuse of HTTP connections.

**Fetch paginated HTML**  
It posts to the CBSL AJAX endpoint, retrieving a block of price report listings (10–15 reports per page).

**Parse PDF links**  
Using BeautifulSoup, the module extracts all PDF URLs and their publication dates.

**Download PDFs concurrently**  
All found links are downloaded in parallel using asyncio tasks.

**Save with structured filenames**  
Each PDF is named by its date (e.g., 2023-08-15.pdf) and stored in data/raw/<year>/.

---

## Example Usage

**Run interactively through the package menu**
```bash
python -m rice_price_collector
```
→ Choose option 1 for PDF Downloader.

**Run directly**
```bash
python -m rice_price_collector.downloader
```

**Run manually in code**
```python
from rice_price_collector.downloader.pdf_downloader import scrape_all
import asyncio

asyncio.run(scrape_all(year_id="88"))  # e.g. year 2025
```

---

## Example Console Output
```
[001/239] Downloading 2022-08-15.pdf... OK
[002/239] Downloading 2022-08-16.pdf... OK
[003/239] Downloading 2022-08-17.pdf... SKIPPED (already exists)
[004/239] Downloading 2022-08-18.pdf... OK
```
At the end:

Completed! 236 PDFs downloaded successfully.

---

## Integration with Parser Module

Once the PDFs are downloaded, the Parser Module takes over — extracting structured rice price tables.
The downloader and parser are independent but work best when chained:

```bash
python -m rice_price_collector.downloader && python -m rice_price_collector.parser
```

---


## Next Step

Proceed to the next section to explore the parser pipeline:

[Downloader Configuration »](config.md)
