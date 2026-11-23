# ================================================================
# 0. Section: IMPORTS
# ================================================================
from ..domain import DownloadSpec, DownloadRegistry


# ================================================================
# 1. Section: Class definition
# ================================================================
class Downloader:
    """Entry point for downloading a dataset from any registered source.

    Examples:
        >>> spec = ZenodoSpecs(dest="data/raw", record_id=4421500, filename="data.zip")
        >>> Downloader().run(spec)
    """

    def run(self, spec: DownloadSpec) -> None:
        """Validate the source, then fetch from it with the strategy of `spec.source`.

        Raises:
            ValueError: If no strategy is registered for `spec.source`, usually
                because its adapter was not imported.
        """
        # 1. Select strategy based on source
        source = spec.source
        strategy = DownloadRegistry.get(source)

        # 2. Check the source is reachable, then fetch from it
        strategy.validate(spec)
        strategy.fetch(spec)
