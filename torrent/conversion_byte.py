from typing import List

METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

def human_bytes(num: int) -> str:
    """
    Human-readable formatting of bytes, metric (powers of 1000) representation.
    """

    assert isinstance(num, int), "num must be an int"

    unit_labels = METRIC_LABELS
    last_label = unit_labels[-1]
    unit_step = 1000
    unit_step_thresh = unit_step - 0.005

    for unit in unit_labels:
        if num < unit_step_thresh:
            break
        if unit != last_label:
            num /= unit_step

    return "{:.2f} {}".format(num, unit)
