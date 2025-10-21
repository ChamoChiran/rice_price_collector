# Column Naming Logic

The column naming logic in the parser ensures that extracted rice price tables have clear, meaningful column names that reflect the market, price type, and day. This makes the data easy to analyze and avoids generic names like "Col1", "Col2", etc.

---

## Purpose

CBSL price tables report prices for multiple markets and days. Instead of ambiguous column names, we generate descriptive names such as `wholesale_pettah_yesterday` or `retail_dambulla_today`.

---

## How Column Names Are Created

The function `create_smart_column_names(section_lines)`:

1. **Scans the first 50 lines** of the extracted section to determine which markets are present (e.g., Pettah, Marandagahamula, Dambulla, Narahenpita).
2. **Defines default market lists** for wholesale and retail prices.
3. **Builds column names** for each market and day (yesterday/today) for both wholesale and retail prices.
4. **Returns a list** of column names in the order they appear in the table.

---

## Example Output

A typical output might look like:

```
["item", "unit",
 "wholesale_pettah_yesterday", "wholesale_pettah_today",
 "wholesale_marandagahamula_yesterday", "wholesale_marandagahamula_today",
 "retail_pettah_yesterday", "retail_pettah_today",
 "retail_dambulla_yesterday", "retail_dambulla_today",
 "retail_narahenpita_yesterday", "retail_narahenpita_today"]
```

---

## Customization

- The function can be extended to detect additional markets or handle new table formats.
- If a market is not present in the data, you can adjust the logic to skip or add columns as needed.

---

## Code Reference

```python
def create_smart_column_names(section_lines):
    # ...
    wholesale_locations = ["pettah", "marandagahamula"]
    retail_locations = ["pettah", "dambulla", "narahenpita"]
    # ...
    for location in wholesale_locations:
        column_names.append(f"wholesale_{location}_yesterday")
        column_names.append(f"wholesale_{location}_today")
    for location in retail_locations:
        column_names.append(f"retail_{location}_yesterday")
        column_names.append(f"retail_{location}_today")
    return column_names
```

---

## Next Step

See the parser or extractor documentation for how these column names are used in the final DataFrame.
