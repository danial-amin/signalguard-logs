from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set

from ..models import LogStream
from ..detectors import NewTemplateDetector
from .base import BaseRecipe


@dataclass
class NewErrorPatternRecipe(BaseRecipe):
    """
    Recipe for detecting new error patterns based on unseen log templates.
    """

    service: str
    level: str = "ERROR"
    known_templates: Set[str] = field(default_factory=set)

    def run(self, stream: LogStream):
        s = stream.filter_service(self.service).filter_level(self.level)
        det = NewTemplateDetector(known_templates=self.known_templates)
        labels, scores = det.detect(s)
        # known_templates is updated in place
        return {
            "service": self.service,
            "level": self.level,
            "labels": labels,
            "scores": scores,
            "filtered_stream": s,
            "known_templates": det.known_templates,
        }
