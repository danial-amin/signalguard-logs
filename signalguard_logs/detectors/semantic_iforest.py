from __future__ import annotations

from typing import Tuple

import numpy as np
from sklearn.ensemble import IsolationForest

from ..models import LogStream
from ..features import TFIDFVectorizer
from .base import BaseLogDetector


class SemanticIForestDetector(BaseLogDetector):
    """
    Semantic anomaly detector on log messages.

    Pipeline:
      - Fit TF-IDF vectorizer on log messages.
      - Fit IsolationForest on TF-IDF vectors.
      - Use decision_function to compute anomaly scores.

    Parameters
    ----------
    max_features : int
        Maximum TF-IDF features.
    contamination : float
        Expected fraction of anomalies.
    """

    def __init__(self, max_features: int = 5000, contamination: float = 0.05):
        self.vectorizer = TFIDFVectorizer(max_features=max_features)
        self.iforest = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=42,
        )

    def detect(self, stream: LogStream) -> Tuple[np.ndarray, np.ndarray]:
        messages = stream.messages()
        n = len(messages)
        if n == 0:
            return np.zeros(0, dtype=int), np.zeros(0, dtype=float)

        X = self.vectorizer.fit_transform(messages)
        self.iforest.fit(X)

        decision_scores = self.iforest.decision_function(X)
        raw_scores = -decision_scores
        raw_scores = raw_scores - raw_scores.min()
        norm_scores = raw_scores / (raw_scores.max() + 1e-8)

        labels = (norm_scores > 0.8).astype(int)
        return labels, norm_scores.ravel()
