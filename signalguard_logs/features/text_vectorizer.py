from __future__ import annotations

from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer as SklearnTFIDF


class TFIDFVectorizer:
    """
    Thin wrapper around scikit-learn TF-IDF for log messages.
    """

    def __init__(self, max_features: int = 5000, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self._vec: SklearnTFIDF | None = None

    def fit(self, messages: List[str]):
        self._vec = SklearnTFIDF(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
        )
        self._vec.fit(messages)

    def transform(self, messages: List[str]) -> np.ndarray:
        if self._vec is None:
            raise RuntimeError("TFIDFVectorizer not fitted")
        return self._vec.transform(messages).toarray()

    def fit_transform(self, messages: List[str]) -> np.ndarray:
        self.fit(messages)
        return self.transform(messages)
