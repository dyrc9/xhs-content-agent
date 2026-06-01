from __future__ import annotations

import json
from pathlib import Path

from .schema import NoteDraft


def read_text(path: Path) -> str:
    return path.expanduser().read_text(encoding="utf-8")


def read_topics(path: Path) -> list[str]:
    return [line.strip() for line in read_text(path).splitlines() if line.strip()]


def read_note(path: Path) -> NoteDraft:
    payload = json.loads(read_text(path))
    return NoteDraft(
        title=str(payload.get("title", "")),
        hook=str(payload.get("hook", "")),
        body=str(payload.get("body", "")),
        hashtags=[str(item) for item in payload.get("hashtags", [])],
        image_prompts=[str(item) for item in payload.get("image_prompts", [])],
        call_to_action=str(payload.get("call_to_action", "")),
        source_summary=str(payload.get("source_summary", "")),
    )
