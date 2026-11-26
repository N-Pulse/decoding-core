# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pyxdf

from pathlib import Path
from typing import ClassVar, Any, overload
from pypeline import ActorIO, ActorIORegistry
from collections.abc import Callable, Iterator, Mapping, Sequence

from ...domain.actors import XdfData


# ================================================================
# 1. Section: Functions
# ================================================================
def read_xdf(path: Path) -> XdfData:
    file = _XdfFile(path)
    return XdfData(
        streams=LazyXdfStreams(file),
        metadata=LazyXdfHeader(file),
        path_of_origin=path,
    )

def write_txt(actor: XdfData, path: Path) -> None:
    path.write_text(str(actor.path_of_origin), encoding="utf-8")


# ================================================================
# 2. Section: Class definitions
# ================================================================
@ActorIORegistry.register("XdfData")
class XdfIO(ActorIO):
    readers: ClassVar[dict[str, Callable[[Path], Any]]] = {".xdf": read_xdf}
    writers: ClassVar[dict[str, Callable[[Any, Path], None]]] = {".txt": write_txt}


# ================================================================
# 3. Section: Lazy Loading Code
# ================================================================
class LazyXdfStreams(Sequence[dict]):
    def __init__(self, file: _XdfFile):
        self._file = file

    # ──────────────────────────────────────────────────────
    # 3.1 Subsection: Dunder Getters
    # ──────────────────────────────────────────────────────
    @overload
    def __getitem__(self, index: int) -> dict: ...
    @overload
    def __getitem__(self, index: slice) -> list[dict]: ...
    def __getitem__(self, index: int | slice) -> dict | list[dict]:
        return self._file.streams()[index]

    # ──────────────────────────────────────────────────────
    # 3.2 Subsection: Sequence Dunders
    # ──────────────────────────────────────────────────────
    def __len__(self) -> int:
        return len(self._file.streams())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LazyXdfStreams):
            return NotImplemented
        return self._file.path == other._file.path

    def __repr__(self) -> str:
        return f"LazyXdfStreams({self._file.path.name})"


class LazyXdfHeader(Mapping[str, Any]):
    def __init__(self, file: _XdfFile):
        self._file = file

    # ──────────────────────────────────────────────────────
    # 3.3 Subsection: Getter Dunders
    # ──────────────────────────────────────────────────────
    def __getitem__(self, key: str) -> Any:
        return self._file.header()[key]

    # ──────────────────────────────────────────────────────
    # 3.4 Subsection: Other Dunders
    # ──────────────────────────────────────────────────────
    def __iter__(self) -> Iterator[str]:
        return iter(self._file.header())

    def __len__(self) -> int:
        return len(self._file.header())

    # Mapping.__eq__ would compare contents and so load the file.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LazyXdfHeader):
            return NotImplemented
        return self._file.path == other._file.path

    def __repr__(self) -> str:
        return f"LazyXdfHeader({self._file.path.name})"


# ================================================================
# 4. Section: Supporting Class
# ================================================================
class _XdfFile:
    def __init__(self, path: Path):
        self.path = path
        self._contents: tuple[list[dict], dict] | None = None

    def streams(self) -> list[dict]:
        return self._load()[0]

    def header(self) -> dict:
        return self._load()[1]

    def _load(self) -> tuple[list[dict], dict]:
        if self._contents is None:
            streams, header = pyxdf.load_xdf(self.path)
            self._contents = (streams, header)
        return self._contents
