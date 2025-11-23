from __future__ import annotations

import json
import time
from typing import Iterable, Iterator

from ..models import LogRecord


class JsonLogParser:
    """
    Parse line based JSON logs.

    Assumes each line is a JSON object that may contain:
      - timestamp (float, int, or ISO string)
      - level
      - message
      - service

    All other keys go into LogRecord.extra.
    """

    def __init__(self, ts_key: str = "timestamp", level_key: str = "level", msg_key: str = "message", service_key: str = "service"):
        self.ts_key = ts_key
        self.level_key = level_key
        self.msg_key = msg_key
        self.service_key = service_key

    def parse_lines(self, lines: Iterable[str]) -> Iterator[LogRecord]:
        for line in lines:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                yield LogRecord(timestamp=time.time(), level="INFO", message=line)
                continue

            ts_raw = data.pop(self.ts_key, time.time())
            ts = self._parse_timestamp(ts_raw)

            level = str(data.pop(self.level_key, "INFO")).upper()
            message = str(data.pop(self.msg_key, ""))
            service = str(data.pop(self.service_key, ""))

            yield LogRecord(timestamp=ts, level=level, message=message, service=service, extra=data)

    @staticmethod
    def _parse_timestamp(ts_raw) -> float:
        if isinstance(ts_raw, (int, float)):
            return float(ts_raw)
        try:
            # naive attempt to parse ISO like "2025-11-23T12:34:56"
            import datetime as dt

            return dt.datetime.fromisoformat(str(ts_raw)).timestamp()
        except Exception:
            return time.time()
