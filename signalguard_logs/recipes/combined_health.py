from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..models import LogStream
from ..detectors import LogBurstDetector, SemanticIForestDetector
from .base import BaseRecipe


@dataclass
class CombinedLogHealthRecipe(BaseRecipe):
    """
    Combined log health recipe.

    Combines:
      - Burst detection on ERROR level logs
      - Semantic anomaly detection on all logs

    Returns per log entry labels and scores.
    """

    service: str
    error_level: str = "ERROR"
    burst_window_size: float = 60.0
    burst_factor: float = 3.0
    semantic_contamination: float = 0.05

    def run(self, stream: LogStream):
        n = len(stream.records)
        if n == 0:
            return {
                "labels": np.zeros(0, dtype=int),
                "scores": np.zeros(0, dtype=float),
                "stream": stream,
            }

        # Burst on error logs
        error_stream = stream.filter_service(self.service).filter_level(self.error_level)
        burst_det = LogBurstDetector(window_size=self.burst_window_size, baseline_factor=self.burst_factor)
        burst_labels, burst_scores = burst_det.detect(error_stream)

        # Map burst back to global indices via timestamps
        ts_global = stream.timestamps()
        ts_error = error_stream.timestamps()

        burst_map = {ts: (label, score) for ts, label, score in zip(ts_error, burst_labels, burst_scores)}

        burst_labels_global = np.zeros(n, dtype=int)
        burst_scores_global = np.zeros(n, dtype=float)
        for i, ts in enumerate(ts_global):
            if ts in burst_map:
                l, s = burst_map[ts]
                burst_labels_global[i] = l
                burst_scores_global[i] = s

        # Semantic anomalies across all logs
        sem_det = SemanticIForestDetector(contamination=self.semantic_contamination)
        sem_labels, sem_scores = sem_det.detect(stream)

        # Combine
        labels = ((burst_labels_global == 1) | (sem_labels == 1)).astype(int)
        scores = (burst_scores_global + sem_scores) / 2.0

        return {
            "labels": labels,
            "scores": scores,
            "burst_labels": burst_labels_global,
            "burst_scores": burst_scores_global,
            "semantic_labels": sem_labels,
            "semantic_scores": sem_scores,
            "stream": stream,
        }
