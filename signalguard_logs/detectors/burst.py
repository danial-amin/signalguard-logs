from __future__ import annotations

from typing import Tuple

import numpy as np

from ..models import LogStream
from .base import BaseLogDetector


class LogBurstDetector(BaseLogDetector):
    """
    Detect bursts in log volume over time.

    Typically run on a filtered stream, for example only ERROR logs for a service.

    Parameters
    ----------
    window_size : float
        Window size in seconds.
    baseline_factor : float
        Burst threshold factor relative to median count. For example
        baseline_factor=3 means counts above 3 * median are flagged.
    """

    def __init__(self, window_size: float = 60.0, baseline_factor: float = 3.0):
        self.window_size = float(window_size)
        self.baseline_factor = float(baseline_factor)

    def detect(self, stream: LogStream) -> Tuple[np.ndarray, np.ndarray]:
        ts = stream.timestamps()
        n = len(ts)
        if n == 0:
            return np.zeros(0, dtype=int), np.zeros(0, dtype=float)

        # Bin timestamps into windows
        start = ts.min()
        bins = ((ts - start) / self.window_size).astype(int)

        # count logs per bin
        max_bin = bins.max()
        counts = np.zeros(max_bin + 1, dtype=int)
        for b in bins:
            counts[b] += 1

        # baseline and threshold
        median = np.median(counts) or 1.0
        threshold = median * self.baseline_factor

        bin_scores = counts.astype(float) / (median + 1e-8)
        bin_labels = (counts > threshold).astype(int)

        # map bin labels back to log records
        labels = np.zeros(n, dtype=int)
        scores = np.zeros(n, dtype=float)
        for i, b in enumerate(bins):
            labels[i] = bin_labels[b]
            scores[i] = bin_scores[b]

        return labels, scores
