from __future__ import annotations

from dataclasses import dataclass

from ..models import LogStream
from ..detectors import LogBurstDetector
from .base import BaseRecipe


@dataclass
class ErrorBurstRecipe(BaseRecipe):
    """
    Recipe for detecting bursts of ERROR logs for a specific service.
    """

    service: str
    level: str = "ERROR"
    window_size: float = 60.0
    baseline_factor: float = 3.0

    def run(self, stream: LogStream):
        # filter to desired service and level
        s = stream.filter_service(self.service).filter_level(self.level)
        det = LogBurstDetector(window_size=self.window_size, baseline_factor=self.baseline_factor)
        labels, scores = det.detect(s)
        return {
            "service": self.service,
            "level": self.level,
            "labels": labels,
            "scores": scores,
            "filtered_stream": s,
        }
