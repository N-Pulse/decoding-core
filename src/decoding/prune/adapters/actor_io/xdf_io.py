# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pyxdf

from pathlib import Path
from typing import ClassVar, Any
from collections.abc import Callable
from pypeline.adaptors import ActorIO, ActorIORegistry

from ...domain.actors import XdfData



# ================================================================
# 1. Section: Functions
# ================================================================
def read_xdf(path: Path) -> XdfData:
    streams, file_header = pyxdf.load_xdf(path)
    return XdfData(streams=streams, metadata=file_header, path_of_origin=path)

@ActorIORegistry.register("XDF")
class XdfIO(ActorIO):
    readers: ClassVar[dict[str, Callable[[Path], Any]]] = {".xdf": read_xdf}
    writers: ClassVar[dict[str, Callable[[Any, Path], None]]] = {}
