__version__ = "0.1.0"
__author__ = "chamodh"

# Lazy import submodules to avoid circular import issues
import importlib

def __getattr__(name):
	if name == "downloader":
		return importlib.import_module(".downloader", __name__)
	if name == "parser":
		return importlib.import_module(".parser", __name__)
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["downloader", "parser"]
