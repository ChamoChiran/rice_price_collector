# Getting Started

This guide walks you through setting up and running the **Rice Price Collector** package — from environment setup to running both the downloader and parser modules.

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ChamoChiran/rice_price_collector.git
cd rice_price_collector
```

### 2. Create and Activate the Environment

```bash
conda env create -f environment.yml
conda activate rice_price_collector
```

The environment installs everything you need:
- `aiohttp` and `BeautifulSoup4` for asynchronous web scraping
- `pdfplumber` or `tabula` for table extraction
- `pandas` and `numpy` for data cleaning

---

## Running the Package

### Option 1 — Launch Interactive Menu

Your package includes a launcher script (`rice_price_collector/__main__.py`) that provides a simple command-line interface to choose a module.

Run it like this:

```bash
python -m rice_price_collector
```

You’ll see:

```
Please select an option:
1. Run PDF Downloader
2. Run Parser
Enter your choice (1 or 2):
```

Choose 1 to start the downloader, or 2 to start the parser.

---

## Running the Downloader

The downloader retrieves CBSL daily rice price PDFs asynchronously.

```bash
python -m rice_price_collector.downloader
```

**What it does:**
- Fetches price report PDFs from CBSL’s publications site.
- Organizes them by year in the `data/raw/<year>/` directory.
- Skips duplicates automatically.

**Example:**

```
data/
└── raw/
    ├── 2023/
    │   ├── 2023-05-01.pdf
    │   ├── 2023-05-02.pdf
    │   └── ...
    └── 2024/
        ├── 2024-01-01.pdf
        └── ...
```

Configuration (base URL, AJAX params, output paths) lives in
`rice_price_collector/downloader/config.py`.

---

## Running the Parser

Once PDFs are downloaded, run the parser to extract structured rice price data.

```bash
python -m rice_price_collector.parser
```

**What it does:**
- Opens each PDF using your chosen backend (`pdfplumber`, `tabula`, or fallback).
- Detects Pettah and Marandagahamula tables automatically.
- Cleans and aligns columns, filling missing price cells.
- Exports a processed CSV to `data/processed/`.

**Example output:**

```
data/
└── processed/
    ├── 2023_prices.csv
    ├── 2024_prices.csv
    └── summary_report.csv
```

---

## Configuration Files

| File                        | Description                                              |
|-----------------------------|----------------------------------------------------------|
| downloader/config.py        | Controls CBSL endpoints and output directories           |
| parser/config.py            | Defines paths, start/end keywords, and extraction settings|
| parser/columns.py           | Defines standardized column names (e.g., “Retail_Pettah”, “Wholesale_Marandagahamula”) |

---

## Data Flow Summary

CBSL Website → Downloader → PDF Files → Parser → Clean CSV → Model-ready Dataset

The modular design means you can run each stage independently or orchestrate both with:

```bash
python -m rice_price_collector
```

---

## Tip for Developers

Want to test just one piece?

```bash
python -m rice_price_collector.parser.extractors.rice
```

You can isolate submodules for debugging or incremental development.

---

## You’re Ready!

You now have the tools to:
- Fetch CBSL rice price PDFs automatically
- Parse and clean the extracted data
- Build forecasting models on top of the generated dataset

Next, explore:

[Downloader Module »](downloader/index.md)

[Parser Module »](parser/index.md)
