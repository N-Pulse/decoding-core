# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import ClassVar
from dataclasses import dataclass


# ================================================================
# 1. Section: Class definition
# ================================================================
@dataclass
class DownloadSpec:
    """Values of one download; the entry script builds it, `Downloader.run` uses it.

    Each source subclasses it with its own fields (record id, remote path,
    credentials, ...). Only values go here; how to reach the source belongs in
    its `DownloadStrategy`.

    Attributes:
        source: Key the matching strategy is registered under in
            `DownloadRegistry`. Every subclass must set it.
        dest: Local folder the data is written to.
    """

    source: ClassVar[str]
    dest: str
