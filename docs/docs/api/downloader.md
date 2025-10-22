# Downloader API Reference

## download_all_pdfs

```python
download_all_pdfs(years=None, outputdir=None)
```

Downloads all available CBSL rice price PDFs for the specified years into the given output directory. If no years or output directory are provided, prompts the user for input.

**Parameters:**
- `years` (list of int or str, optional): Years to download (e.g., `[2024, 2025]`). If `None`, prompts the user.
- `outputdir` (str or Path, optional): Directory to save PDFs. If `None`, prompts the user.

**Usage Example:**
```python
import asyncio
from rice_price_collector.downloader import download_all_pdfs
await download_all_pdfs([2024, 2025], './data/raw')
```

---

## download_pdfs_to

```python
download_pdfs_to(years, outputdir)
```

Downloads CBSL rice price PDFs for the specified years directly into the given output directory, without prompting the user.

**Parameters:**
- `years` (list of int or str): Years to download (e.g., `[2024, 2025]`).
- `outputdir` (str or Path): Directory to save PDFs.

**Usage Example:**
```python
import asyncio
from rice_price_collector.downloader import download_pdfs_to
await download_pdfs_to([2024, 2025], './data/raw')
```

---

Both functions are asynchronous and should be called with `await` inside an async function or Jupyter notebook cell.
