"""
rice_price_collector.parser

Parser subpackage for extracting and cleaning CBSL rice price data.
"""

# Expose key functions at the package level using lazy imports to avoid circular import issues
import importlib

def __getattr__(name):
    if name == "extractors":
        return importlib.import_module(".extractors", __name__)
    if name == "parse_price_section":
        return importlib.import_module(".parser", __name__).parse_price_section
    if name == "create_smart_column_names":
        return importlib.import_module(".columns", __name__).create_smart_column_names
    if name == "extract_section_between":
        return importlib.import_module(".utils", __name__).extract_section_between
    if name == "fix_missing_columns":
        return importlib.import_module(".utils", __name__).fix_missing_columns
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "extractors",
    "parse_price_section",
    "create_smart_column_names",
    "extract_section_between",
    "fix_missing_columns",
]
