# Download

Fetches datasets from remote sources into a local folder. You describe what to download with a spec and pass it to `Downloader`, which picks the strategy registered for that spec's source, checks the source is reachable, then downloads.

```python
from decoding.download import Downloader, ZenodoSpecs

spec = ZenodoSpecs(dest="data/raw/emg_epn_612", record_id=4421500, filename="EMG-EPN612 Dataset.zip")
Downloader().run(spec)
```

## Adding a source

A source is a pair of classes in `adapters/<source>/`:

- **Spec** (`<source>_specs.py`): a `DownloadSpec` dataclass that holds the values of one download (record id, remote path, credentials). Set `source: ClassVar[str] = "<source-name>"`.
- **Strategy** (`<source>_strategy.py`): a `DownloadStrategy[<Source>Specs]` that holds the logic to reach the source. Implement `validate` (fail fast, write nothing) and `fetch` (download into `spec.dest`, safe to re-run). Decorate it with `@DownloadRegistry.register(<Source>Specs.source)`.

Re-export both from the folder's `__init__.py` and from `adapters/__init__.py` so the strategy registers on import, then add a row to the table below.

## Sources

| Source | Spec | Strategy | What it does |
|---|---|---|---|
| `zenodo` | `ZenodoSpecs` | `ZenodoStrategy` | Downloads one file of a Zenodo record, checks its size and MD5, and unzips it if `extract` is set. No credentials needed. |
| `archive-raw` | `ArchiveSpecs` | `ArchiveStrategy` | Mirrors a folder of EPFL's WebDAV archive (`make-archives.epfl.ch`) into `dest`, skipping files already downloaded. Needs credentials, see below. |

<details>
<summary>Getting the archive credentials</summary>

- **`username`**: your EPFL username.
- **`password`**: an app password. On the Archive MAKE Drive, go to Profile Settings (top right) > Security > Create New App Password.
- **`dav_user`**: on the Archive MAKE Drive, go to Files Settings (bottom left) > WebDAV, copy the URL and take the part after `https://make-archives.epfl.ch/remote.php/dav/files/`.

Never commit them.

</details>

## Review status

A ✅ means the file was reviewed by a TL/SE.

| File | Reviewed | Commit/PR |
|---|---|---|
| `domain/download_spec.py` | ✅ | |
| `domain/download_strategy.py` | ✅ | |
| `domain/download_registry.py` | ✅ | |
| `service/downloader.py` | ✅ | |
| `adapters/zenodo/zenodo_specs.py` | | |
| `adapters/zenodo/zenodo_strategy.py` | | |
| `adapters/archive/archive_specs.py` | | |
| `adapters/archive/archive_strategy.py` | | |
