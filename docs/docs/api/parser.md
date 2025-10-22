# Parser API Reference

## process_year_folders_dict

```python
process_year_folders_dict(folders_dict)
```

Processes a dictionary mapping years to folders containing CBSL rice price PDFs, extracting data from all PDFs and returning a combined pandas DataFrame.

**Parameters:**
- `folders_dict` (dict): Mapping of year (str or int) to folder path (str or Path) containing PDFs. Example: `{ "2024": "./data/raw/2024" }`

**Returns:**
- `pandas.DataFrame` or `None`: Combined extracted data, or `None` if no data found.

**Usage Example:**
```python
from rice_price_collector.parser import process_year_folders_dict
folders = {"2024": "./data/raw/2024", "2025": "./data/raw/2025"}
df = process_year_folders_dict(folders)
```

---

## parse_price_section

```python
parse_price_section(section_lines)
```

Parses a section of lines from a rice price PDF and extracts structured data.

**Parameters:**
- `section_lines` (list of str): Lines of text from a PDF section.

**Returns:**
- `dict`: Extracted data from the section.

---

## create_smart_column_names

```python
create_smart_column_names(header_lines)
```

Generates smart column names from header lines in a PDF table.

**Parameters:**
- `header_lines` (list of str): Lines representing table headers.

**Returns:**
- `list of str`: List of column names.

---

## extract_section_between

```python
extract_section_between(lines, start_marker, end_marker)
```

Extracts lines between two markers in a list of lines.

**Parameters:**
- `lines` (list of str): All lines from a PDF or text.
- `start_marker` (str): Start marker.
- `end_marker` (str): End marker.

**Returns:**
- `list of str`: Extracted lines.

---

## fix_missing_columns

```python
fix_missing_columns(df)
```

Fixes missing columns in a DataFrame extracted from a PDF.

**Parameters:**
- `df` (pandas.DataFrame): DataFrame to fix.

**Returns:**
- `pandas.DataFrame`: Fixed DataFrame.
