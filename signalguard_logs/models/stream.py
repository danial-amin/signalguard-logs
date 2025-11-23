from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Callable

import numpy as np

from .record import LogRecord


@dataclass
class LogStream:
    """
    Collection of LogRecord objects with convenience methods.
    """

    records: List[LogRecord]

    @classmethod
    def from_iterable(cls, records: Iterable[LogRecord]) -> "LogStream":
        return cls(records=list(records))

    def filter(self, predicate: Callable[[LogRecord], bool]) -> "LogStream":
        return LogStream(records=[r for r in self.records if predicate(r)])

    def filter_level(self, level: str) -> "LogStream":
        level_upper = level.upper()
        return self.filter(lambda r: r.level.upper() == level_upper)

    def filter_service(self, service: str) -> "LogStream":
        return self.filter(lambda r: r.service == service)

    def messages(self) -> List[str]:
        return [r.message for r in self.records]

    def timestamps(self) -> np.ndarray:
        return np.array([r.timestamp for r in self.records], dtype=float)
