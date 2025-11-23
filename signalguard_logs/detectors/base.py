from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

from ..models import LogStream


class BaseLogDetector(ABC):
    """
    Base class for log anomaly detectors.

    detect() returns:
      - labels: np.ndarray of shape (n,), values in {0, 1}
      - scores: np.ndarray of shape (n,), higher = more anomalous
    """

    @abstractmethod
    def detect(self, stream: LogStream) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError
