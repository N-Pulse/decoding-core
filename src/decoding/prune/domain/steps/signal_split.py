# ================================================================
# 0. Section: IMPORTS
# ================================================================
import copy

import numpy as np

from pypeline import Step, StepRegistry
from dataclasses import dataclass, replace

from decoding.prune.types import SignalType

from ..actors import XdfData

_ACCEPTED_TYPES: dict[SignalType, set[str]] = {
    "eeg": {"eeg"},
    "emg": {"emg", "aux"},
}


# ================================================================
# 1. Section: Functions
# ================================================================
@StepRegistry.register("signal_split")
@dataclass
class SignalSplit(Step[XdfData, XdfData]):
    signal: SignalType

    def run(self, data: XdfData) -> XdfData:
        accepted = _ACCEPTED_TYPES[self.signal]

        kept_streams: list[dict] = []
        for stream in data.streams:
            # Markers carry the task events and are kept for every signal.
            stream_name = stream["info"]["type"][0].lower()

            if stream_name == "markers":
                kept_streams.append(stream)
                continue

            new_stream = build_filtered_stream(stream, accepted)
            kept_streams.append(new_stream)

        return replace(data, streams=kept_streams)

    def validate_input(self, data: XdfData) -> None:
        return super().validate_input(data)

    def validate_output(self, output: XdfData) -> None:
        return super().validate_output(output)



# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def build_filtered_stream(stream: dict, accepted: set[str]) -> dict:
    channels = stream["info"]["desc"][0]["channels"][0]["channel"]

    keep_idx = [
        i for i, chan in enumerate(channels) if chan["type"][0].lower() in accepted
    ]

    if not keep_idx:
        raise ValueError(f"File is missing any channel labeled: {accepted}")

    new_stream = dict(stream)
    new_stream["time_series"] = np.asarray(stream["time_series"])[:, keep_idx]

    info = copy.deepcopy(stream["info"])
    info["type"] = [next(iter(accepted)).upper()]
    info["channel_count"] = [str(len(keep_idx))]
    info["desc"][0]["channels"][0]["channel"] = [channels[i] for i in keep_idx]
    new_stream["info"] = info

    return new_stream
