from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class NoteDraft:
    title: str
    hook: str
    body: str
    hashtags: list[str]
    image_prompts: list[str] = field(default_factory=list)
    call_to_action: str = ""
    source_summary: str = ""


@dataclass(frozen=True)
class CalendarItem:
    day: int
    topic: str
    angle: str
    suggested_title: str


@dataclass(frozen=True)
class QualityReport:
    passed: bool
    warnings: list[str]
    suggestions: list[str]


def to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_dict(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items()}
    return value
