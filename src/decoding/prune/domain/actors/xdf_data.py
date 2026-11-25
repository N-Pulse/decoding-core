# ================================================================
# 0. Section: IMPORTS
# ================================================================
import datetime

from typing import Any
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Mapping, Sequence


# ================================================================
# 1. Section: Class definition
# ================================================================
@dataclass
class XdfData:
    """
    Path look like:
        YYYY-MM-DD/sub-XX/ses-XX/sourcedata/file.xdf
    """

    streams: Sequence[dict]
    metadata: Mapping[str, Any]
    path_of_origin: Path

    @property
    def session_id(self) -> int:
        return int(self.path_of_origin.parents[1].name.removeprefix("ses-"))

    @property
    def subject_id(self) -> int:
        return int(self.path_of_origin.parents[2].name.removeprefix("sub-"))

    @property
    def date(self) -> datetime.date:
        return datetime.date.fromisoformat(self.path_of_origin.parents[3].name)
