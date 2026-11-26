# ================================================================
# 0. Section: IMPORTS
# ================================================================
import datetime

from dataclasses import dataclass
from pypeline import Step, StepRegistry

from ...actors import XdfData


# ================================================================
# 1. Section: Functions
# ================================================================
@StepRegistry.register("date_filter")
@dataclass
class DateFilter(Step[XdfData, XdfData]):
    start_date: datetime.date
    end_date: datetime.date

    def run(self, data: XdfData) -> XdfData | None:
        if data.date < self.end_date and data.date > self.start_date:
            return data

    def validate_input(self, data: XdfData) -> None:
        return super().validate_input(data)

    def validate_output(self, output: XdfData) -> None:
        return super().validate_output(output)
