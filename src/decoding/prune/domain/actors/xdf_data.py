# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Any
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Mapping, Sequence


# ================================================================
# 1. Section: Class definition
# ================================================================
@dataclass
class XdfData:
    streams: Sequence[dict]
    metadata: Mapping[str, Any]
    path_of_origin: Path
