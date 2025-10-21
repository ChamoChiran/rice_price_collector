# PDF Downloader

The **PDF Downloader** is the heart of the Downloader module.  
It fetches, parses, and downloads CBSL “Price Report” PDFs asynchronously using `aiohttp` and `BeautifulSoup`.

---

## File Location
```text
rice_price_collector/
└── downloader/
    └── pdf_downloader.py
```

This script can be run directly or imported as part of a larger pipeline.

---

## Purpose

CBSL publishes daily price reports as PDFs. Each year has hundreds of files, spread across multiple AJAX-driven pages.  
The downloader automates:

1. Querying the CBSL AJAX endpoint  
2. Extracting PDF URLs and publication dates  
3. Downloading and saving them by year  

It’s designed for speed, reliability, and reusability.

---

## Main Functions

### 1. `fetch_page(session, page_num, year_id)`

Fetches one page of PDF listings from the CBSL AJAX endpoint.

```python
async def fetch_page(session, page_num, year_id):
    """
    Fetch a single page of PDF links from the CBSL website.
    
    Args:
        session (aiohttp.ClientSession): The HTTP session to use for requests
        page_num (int): The page number to fetch (0-indexed)
        year_id (str): The CBSL year ID filter (e.g., "88" for 2025)
    
    Returns:
        list: A list of tuples containing (date_object, pdf_url)
    """
```

What it does:

- Posts a JSON payload to AJAX_URL (defined in config.py).
- Parses the HTML response using BeautifulSoup.
- Extracts each PDF’s URL and publication date.
- Returns them as a Python list.
- If a request fails, it retries or returns an empty list with a warning.

### 2. `download_pdf(session, url, dest_path)`

Downloads a single PDF asynchronously and writes it to disk.

```python
async def download_pdf(session, url, dest_path):
    """
    Download a PDF and save it to disk.

    Args:
        session (aiohttp.ClientSession): Active HTTP session
        url (str): Full URL to the PDF file
        dest_path (str): Local file path to save
    """
```

- Checks if the file already exists — unless OVERWRITE = True in config — and creates directories automatically.
- Any failed downloads are logged with a retry message.

### 4. `main()` or `__main__` entry

This allows running the downloader directly from the command line:

```bash
python -m rice_price_collector.downloader
```

Internally, it calls scrape_all() for the configured year_id (which you can modify in config.py).

---

## Example Run

```bash
python -m rice_price_collector.downloader
```

Output:

Starting CBSL PDF scrape for 2025 (year_id=88)...
[001/239] Downloading 2025-01-02.pdf... OK
[002/239] Downloading 2025-01-03.pdf... OK
[003/239] Downloading 2025-01-04.pdf... SKIPPED (already exists)
Completed! 236 PDFs downloaded successfully.

---

## Example Programmatic Usage

You can also import and run it from your own scripts:

```python
import asyncio
from rice_price_collector.downloader.pdf_downloader import scrape_all

asyncio.run(scrape_all("88"))  # Year 2025
```

To scrape multiple years in one run:

```python
import asyncio
from rice_price_collector.downloader.pdf_downloader import scrape_all

async def run_all():
    await asyncio.gather(
        scrape_all("86"),  # 2023
        scrape_all("87"),  # 2024
        scrape_all("88"),  # 2025
    )

asyncio.run(run_all())
```

---

## Logging and Progress Output

Each file download is numbered and timestamped:

[145/239] Downloading 2022-08-12.pdf... OK
[146/239] Downloading 2022-08-13.pdf... OK
[147/239] Downloading 2022-08-14.pdf... WARNING: failed, retrying...
[147/239] Downloading 2022-08-14.pdf... OK

All warnings and errors are printed directly to the console.
You can extend this with the logging module if you prefer file logs.

---

## Error Handling

The downloader is designed to fail gracefully.

| Scenario           | Behavior                                 |
|--------------------|------------------------------------------|
| Network timeout    | Retries up to RETRY_LIMIT times          |
| 404 / Missing PDF  | Logs a warning and skips file            |
| Duplicate filename | Skips unless OVERWRITE=True              |
| Invalid year_id    | Exits cleanly after zero results         |

---

## Performance Notes

Each page fetch returns 10–15 PDFs; typical full-year runs involve ~250–300 files.

With 10 concurrent connections, a full year downloads in ~30–40 seconds on a good network.

If CBSL rate-limits requests, reduce concurrency in config.py (MAX_CONCURRENT).

---

## Developer Tips

- Use asyncio.Semaphore to limit active downloads.
- Set session.timeout = aiohttp.ClientTimeout(total=60) to avoid hanging connections.
- Add headers like User-Agent if CBSL starts blocking generic requests.

Example snippet:

```python
headers = {"User-Agent": "rice-price-collector/1.0"}
async with aiohttp.ClientSession(headers=headers) as session:
    ...
```

---

## Next Step

Once you’ve downloaded all PDFs, head to the Parser Module to start extracting tables:

[Parser Overview »](../parser/index.md)
