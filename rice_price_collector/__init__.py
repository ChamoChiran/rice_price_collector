__version__ = "0.1.0"
__author__ = "chamodh"

# Expose key submodules for easier imports
from . import downloader
from . import parser

__all__ = ["downloader", "parser"]
