from __future__ import annotations

import re
from typing import List, Tuple, Dict


class LogTemplateExtractor:
    """
    Very simple log template extractor.

    Rules:
      - Replace numbers with <NUM>
      - Replace hex strings with <HEX>
      - Optionally mask tokens that look like IDs (length > max_token_len)

    This is not a full Drain implementation, but good enough for AIOps demos.
    """

    NUM_RE = re.compile(r"^\d+(\.\d+)?$")
    HEX_RE = re.compile(r"^[0-9a-fA-F]{6,}$")

    def __init__(self, max_token_len: int = 30):
        self.max_token_len = max_token_len

    def to_template(self, message: str) -> str:
        tokens = message.split()
        templ_tokens = []
        for tok in tokens:
            if self.NUM_RE.match(tok):
                templ_tokens.append("<NUM>")
            elif self.HEX_RE.match(tok):
                templ_tokens.append("<HEX>")
            elif len(tok) > self.max_token_len:
                templ_tokens.append("<ID>")
            else:
                templ_tokens.append(tok)
        return " ".join(templ_tokens)

    def extract_batch(self, messages: List[str]) -> List[str]:
        return [self.to_template(m) for m in messages]

    def count_templates(self, messages: List[str]) -> Dict[str, int]:
        templates = self.extract_batch(messages)
        counts: Dict[str, int] = {}
        for t in templates:
            counts[t] = counts.get(t, 0) + 1
        return counts
