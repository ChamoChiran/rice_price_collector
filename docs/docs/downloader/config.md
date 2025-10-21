# Downloader Configuration

The downloader’s behavior is entirely controlled through `rice_price_collector/downloader/config.py`.  
This file defines the base URLs, output directories, and year identifiers required to fetch CBSL price report PDFs.

---

## Location
```text
rice_price_collector/
└── downloader/
    └── config.py
```

---

## Overview

The configuration file provides three categories of settings:

1. **Endpoints** – URLs used to access CBSL’s price report listings  
2. **Output paths** – Where to store downloaded PDFs  
3. **Runtime parameters** – Defaults like timeouts, concurrency, and year filters  

---

## Endpoint Settings

```python
# Base CBSL publication page for daily price reports
BASE = "https://www.cbsl.gov.lk/publications/price"

# AJAX endpoint used by CBSL’s internal Drupal views to load paginated content
AJAX_URL = "https://www.cbsl.gov.lk/views/ajax"
```

What these do:

BASE is the visible “Price Reports” page users can access in a browser.

AJAX_URL is the hidden request endpoint used to fetch each page of PDFs asynchronously.
The downloader posts a JSON payload to this endpoint (e.g., page number, year ID) and parses the returned HTML block.

If CBSL changes their website layout or endpoint, update these two constants first.

---

## Output Paths

```python
# Folder where PDFs will be stored (created automatically if not found)
OUTPUT_DIR = "data/raw"
```

Each year’s reports are saved in a subfolder:

```
data/
└── raw/
    ├── 2023/
    │   ├── 2023-05-01.pdf
    │   └── ...
    └── 2024/
        ├── 2024-01-01.pdf
        └── ...
```

You can change this directory to any path of your choice — relative or absolute:

```python
OUTPUT_DIR = "/mnt/storage/cbsl_pdfs"
```

---

## Year Identifiers

CBSL organizes publications by internal “year IDs.”
These IDs don’t always match the calendar year directly — for example:

- 88 → 2025
- 87 → 2024
- 86 → 2023

To download reports for multiple years, simply call the downloader multiple times:

```python
from rice_price_collector.downloader.pdf_downloader import scrape_all
import asyncio

for year_id in ["86", "87", "88"]:
    asyncio.run(scrape_all(year_id))
```

You can also parameterize this inside your script or CLI wrapper.

---

## Runtime Parameters (optional)

You can add or tune extra parameters to control runtime behavior:

```python
# Maximum number of concurrent downloads
MAX_CONCURRENT = 10

# Request timeout (seconds)
REQUEST_TIMEOUT = 30

# Number of retry attempts for failed downloads
RETRY_LIMIT = 3

# Whether to overwrite existing PDFs
OVERWRITE = False
```

These are optional defaults — not all may exist in your initial version, but defining them helps make the downloader resilient to flaky connections.

---

## Example Payload (behind the scenes)

When requesting a page, the downloader sends a POST request to AJAX_URL like this:

```python
payload = {
    "view_name": "price_report",
    "view_display_id": "block_1",
    "view_path": "node/144",
    "view_base_path": "publications/price",
    "pager_element": 0,
    "page": 3,            # current page number (0-indexed)
    "year": "88",         # CBSL year ID for 2025
}
```

This returns a block of HTML containing the links to PDF files for that page, which is then parsed by BeautifulSoup.

---

## Example Configuration Summary

| Variable         | Type   | Description                                 | Example                                      |
|------------------|--------|---------------------------------------------|----------------------------------------------|
| BASE             | str    | CBSL public “Price Reports” page            | "https://www.cbsl.gov.lk/publications/price" |
| AJAX_URL         | str    | Hidden AJAX endpoint for fetching report pages | "https://www.cbsl.gov.lk/views/ajax"         |
| OUTPUT_DIR       | str    | Local directory where PDFs are stored        | "data/raw"                                   |
| MAX_CONCURRENT   | int    | Maximum parallel downloads                  | 10                                           |
| REQUEST_TIMEOUT  | int    | Timeout per request in seconds              | 30                                           |
| RETRY_LIMIT      | int    | Number of retries for failed requests       | 3                                            |
| OVERWRITE        | bool   | Whether to overwrite existing files         | False                                        |

---

## Next Step

Once your configuration is set, continue to the detailed downloader implementation:

[PDF Downloader »](downloader.md)
