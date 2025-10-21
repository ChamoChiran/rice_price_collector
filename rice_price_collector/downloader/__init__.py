# Import the async entry point from the main script
from .pdf_downloader import main as download_all_pdfs

__all__ = ["download_all_pdfs"]