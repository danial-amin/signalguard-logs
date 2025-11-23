from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LogRecord:
    """
    Structured log record.

    Attributes
    ----------
    timestamp : float
        Seconds since epoch.
    level : str
        Log level such as INFO, WARN, ERROR.
    message : str
        Raw message text.
    service : str
        Logical service or component name.
    extra : dict
        Optional additional fields (request_id, user_id, etc.).
    """

    timestamp: float
    level: str
    message: str
    service: str = ""
    extra: Dict[str, Any] = None

    def __post_init__(self):
        if self.extra is None:
            self.extra = {}

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "service": self.service,
        }
        d.update(self.extra)
        return d

