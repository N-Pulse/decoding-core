# ================================================================
# 0. Section: IMPORTS
# ================================================================
from decoding.core import Registry

from .download_strategy import DownloadStrategy



# ================================================================
# 1. Section: Class definition
# ================================================================
class DownloadRegistry(Registry[DownloadStrategy]):
    """The registry that holds all download strategies"""
