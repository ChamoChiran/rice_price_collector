# Lazy import for download_all_pdfs to avoid circular import issues
import importlib


def __getattr__(name):
	if name == "download_all_pdfs":
		return importlib.import_module(".pdf_downloader", __name__).main
	if name == "download_pdfs_to":
		return importlib.import_module(".pdf_downloader", __name__).download_pdfs_to
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["download_all_pdfs", "download_pdfs_to"]