# ================================================================
# 0. Section: IMPORTS
# ================================================================
from typing import Protocol

from .download_spec import DownloadSpec


# ================================================================
# 1. Section: Class definition
# ================================================================
class DownloadStrategy[SpecT: DownloadSpec](Protocol):
    """Logic to reach one data source; the values of a download live in the spec.

    Keep it that way: dataset-specific values (record ids, remote paths)
    belong in the spec or the entry script, never in the strategy.

    To add a source, subclass with the matching spec as `SpecT`, register it
    under the spec's `source` and re-export it from `adapters/__init__.py` so the
    registration runs on import:

        @DownloadRegistry.register(MySourceSpecs.source)
        @dataclass
        class MySourceStrategy(DownloadStrategy[MySourceSpecs]):
            def validate(self, spec: MySourceSpecs) -> None: ...
            def fetch(self, spec: MySourceSpecs) -> None: ...

    `Downloader.run` always calls `validate` and then `fetch` with the same
    spec.
    """

    def validate(self, spec: SpecT) -> None:
        """Fail fast, before anything is written to disk.

        Implementations check the source is reachable, the credentials are
        accepted and the requested remote file or folder exists. They must not
        touch local files.

        Raises:
            Exception: When the download cannot run, with a message that tells
                the user what to fix (e.g. `ValueError` for a missing remote
                file, `requests.HTTPError` for a rejected request).
        """

    def fetch(self, spec: SpecT) -> None:
        """Write the data under `spec.dest`, creating it if missing.

        Implementations should be safe to re-run: files already downloaded are
        kept, not fetched again, so an interrupted download resumes where it
        stopped.

        Raises:
            Exception: When the received data does not match what the source
                announced (e.g. `ValueError` on a size or checksum mismatch).
        """
