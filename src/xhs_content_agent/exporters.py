from __future__ import annotations

import json
from pathlib import Path

from .schema import CalendarItem, NoteDraft, QualityReport, to_dict


def write_note(draft: NoteDraft, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "note.json").write_text(
        json.dumps(to_dict(draft), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "note.md").write_text(note_to_markdown(draft), encoding="utf-8")
    (out_dir / "publish-checklist.md").write_text(checklist_markdown(draft), encoding="utf-8")


def write_calendar(items: list[CalendarItem], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "calendar.json").write_text(
        json.dumps(to_dict(items), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    lines = ["# Content Calendar", ""]
    for item in items:
        lines.append(f"## Day {item.day}: {item.topic}")
        lines.append("")
        lines.append(f"- Angle: {item.angle}")
        lines.append(f"- Suggested title: {item.suggested_title}")
        lines.append("")
    (out_dir / "calendar.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_quality_report(report: QualityReport, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "quality-report.json").write_text(quality_report_to_json(report), encoding="utf-8")
    (out_dir / "quality-report.md").write_text(quality_report_markdown(report), encoding="utf-8")


def note_to_markdown(draft: NoteDraft) -> str:
    tags = " ".join(f"#{tag}" for tag in draft.hashtags)
    image_prompts = "\n".join(f"- {prompt}" for prompt in draft.image_prompts) or "- Add image ideas."
    return f"""# {draft.title}

## Hook

{draft.hook}

## Body

{draft.body}

## Call To Action

{draft.call_to_action}

## Hashtags

{tags}

## Image Prompts

{image_prompts}
"""


def checklist_markdown(draft: NoteDraft) -> str:
    del draft
    return """# Publish Checklist

- [ ] Claims are true and not exaggerated
- [ ] No private information or credentials
- [ ] No fake engagement language
- [ ] Title is readable on mobile
- [ ] Body has useful details, not only slogans
- [ ] Hashtags are relevant
- [ ] Images match the content
- [ ] Human reviewed before publishing
"""


def quality_report_markdown(report: QualityReport) -> str:
    lines = ["# Quality Report", ""]
    lines.append(f"Status: {'Passed' if report.passed else 'Warnings found'}")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if report.warnings:
        lines.extend(f"- {warning}" for warning in report.warnings)
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Suggestions")
    lines.append("")
    if report.suggestions:
        lines.extend(f"- {suggestion}" for suggestion in report.suggestions)
    else:
        lines.append("- None.")
    return "\n".join(lines) + "\n"


def quality_report_to_json(report: QualityReport) -> str:
    return json.dumps(to_dict(report), ensure_ascii=False, indent=2)
