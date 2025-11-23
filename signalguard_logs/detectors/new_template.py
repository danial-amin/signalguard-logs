from __future__ import annotations

from typing import Tuple, Set, Optional

import numpy as np

from ..models import LogStream
from ..features import LogTemplateExtractor
from .base import BaseLogDetector


class NewTemplateDetector(BaseLogDetector):
    """
    Detect unseen log templates.

    Useful for "new error pattern" detection.
    """

    def __init__(self, known_templates: Optional[Set[str]] = None, max_token_len: int = 30):
        self.extractor = LogTemplateExtractor(max_token_len=max_token_len)
        self.known_templates: Set[str] = set(known_templates or [])

    def detect(self, stream: LogStream) -> Tuple[np.ndarray, np.ndarray]:
        messages = stream.messages()
        n = len(messages)
        if n == 0:
            return np.zeros(0, dtype=int), np.zeros(0, dtype=float)

        templates = self.extractor.extract_batch(messages)
        labels = np.zeros(n, dtype=int)
        scores = np.zeros(n, dtype=float)

        for i, t in enumerate(templates):
            if t not in self.known_templates:
                labels[i] = 1
                scores[i] = 1.0
                self.known_templates.add(t)
            else:
                labels[i] = 0
                scores[i] = 0.0

        return labels, scores
