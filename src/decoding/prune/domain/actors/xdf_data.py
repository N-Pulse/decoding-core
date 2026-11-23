# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from dataclasses import dataclass


# ================================================================
# 1. Section: Class definition
# ================================================================
@dataclass
class XdfData:
    streams: list[dict]
    metadata: dict
    path_of_origin: Path
