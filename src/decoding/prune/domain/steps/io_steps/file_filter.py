# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from pypeline import Step, StepRegistry

from ...actors import XdfData


# ================================================================
# 1. Section: Functions
# ================================================================
@StepRegistry.register("file_filter")
@dataclass
class FileFilter(Step[XdfData, XdfData]):
    files_to_remove: list[str]

    def run(self, data: XdfData) -> XdfData | None:
        if data.path_of_origin.stem not in self.files_to_remove:
            return data

    def validate_input(self, data: XdfData) -> None:
        return super().validate_input(data)

    def validate_output(self, output: XdfData) -> None:
        return super().validate_output(output)
