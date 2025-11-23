from __future__ import annotations

import re
import time
from typing import Iterable, Iterator, Optional

from ..models import LogRecord


class RegexLogParser:
    """
    Parse plain text logs using a regular expression.

    Default pattern supports:
      [2025-11-23 12:34:56] [ERROR] [service] Message text...

    You can pass a custom pattern with named groups:
      timestamp, level, service, message
    """

    DEFAULT_PATTERN = (
        r"^\[(?P<timestamp>[^\]]+)\]\s+\[(?P<level>[^\]]+)\]\s+\[(?P<service>[^\]]*)\]\s+(?P<message>.*)$"
    )

    def __init__(self, pattern: Optional[str] = None, time_format: str = "%Y-%m-%d %H:%M:%S"):
        self.pattern = re.compile(pattern or self.DEFAULT_PATTERN)
        self.time_format = time_format

    def parse_lines(self, lines: Iterable[str]) -> Iterator[LogRecord]:
        for line in lines:
            line = line.rstrip("\n")
            m = self.pattern.match(line)
            if not m:
                # Fallback: treat whole line as message with current timestamp
                yield LogRecord(
                    timestamp=time.time(),
                    level="INFO",
                    message=line,
                )
                continue

            ts_str = m.group("timestamp")
            try:
                ts_struct = time.strptime(ts_str, self.time_format)
                ts = time.mktime(ts_struct)
            except Exception:
                ts = time.time()

            level = m.group("level") or "INFO"
            service = m.group("service") or ""
            message = m.group("message") or ""

            yield LogRecord(
                timestamp=ts,
                level=level.upper(),
                message=message,
                service=service,
            )
