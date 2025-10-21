# Rice Price Collector

**Rice Price Collector** is a modular Python package designed to automatically **download**, **parse**, and **extract** daily rice price data from the **Central Bank of Sri Lanka (CBSL)** reports.  
It aims to build a clean and structured dataset suitable for **time-series forecasting**, **price trend analysis**, and **data-driven policy research**.

---

## Overview

The system is divided into two main modules:

### 1. Downloader (`rice_price_collector.downloader`)
Handles fetching of daily CBSL PDF reports via asynchronous web scraping using `aiohttp` and `BeautifulSoup`.  
All downloaded PDFs are saved by year in the `data/raw/<year>/` folder.

Key features:
- Fast, async PDF downloads from CBSL.
- Robust against missing pages and timeouts.
- Configurable base URLs and year filters.

---

### 2. Parser (`rice_price_collector.parser`)
Extracts structured rice price tables from downloaded PDFs using libraries such as **pdfplumber** or **tabula**.  
It supports both **batch** and **single-file** extraction.

Key features:
- Automatically detects Pettah and Marandagahamula tables.
- Handles irregular column spacing and missing values.
- Produces CSV/Parquet outputs ready for downstream analysis.

---

## Project Structure

```text
rice_price_collector/
├── downloader/
│   ├── pdf_downloader.py     ← Main async downloader
│   ├── config.py             ← CBSL URLs and constants
│   └── __main__.py           ← Entry point: run downloader
└── parser/
    ├── batch_extract.py      ← Batch extraction pipeline
    ├── parser.py             ← High-level extraction logic
    ├── columns.py            ← Column mapping + validation
    ├── utils.py              ← Helper functions
    └── extractors/
        └── rice.py           ← Rice table parser
```
