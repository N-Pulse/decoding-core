# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from pypeline.domain.step import Step


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class DateFilter(Step[Xdf]):
    def run(self, data: InputClass) -> OutputClass:
        
