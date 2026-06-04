from __future__ import annotations

import json
from pathlib import Path

from .quality import SPAMMY_WORDS, check_note
from .schema import DraftDescription, NoteDraft, to_dict


def describe_note(draft: NoteDraft, source_path: Path) -> DraftDescription:
    report = check_note(draft)
    text = f"{draft.title}\n{draft.body}"
    body_paragraphs = len([part for part in draft.body.split("\n\n") if part.strip()])
    spammy_terms_found = [word for word in SPAMMY_WORDS if word in text]
    return DraftDescription(
        source_path=str(source_path),
        title=draft.title,
        title_length=len(draft.title),
        body_characters=len(draft.body),
        body_paragraphs=body_paragraphs,
        hashtag_count=len(draft.hashtags),
        hashtags=draft.hashtags,
        image_prompt_count=len(draft.image_prompts),
        has_call_to_action=bool(draft.call_to_action.strip()),
        source_summary_present=bool(draft.source_summary.strip()),
        spammy_terms_found=spammy_terms_found,
        passed=report.passed,
        warnings=report.warnings,
        suggestions=report.suggestions,
    )


def description_to_text(description: DraftDescription) -> str:
    lines = ["# Draft Inspection", ""]
    lines.append(f"Source: {description.source_path}")
    lines.append(f"Title: {description.title}")
    lines.append(f"Title length: {description.title_length}")
    lines.append(f"Body characters: {description.body_characters}")
    lines.append(f"Body paragraphs: {description.body_paragraphs}")
    lines.append(f"Hashtags: {description.hashtag_count}")
    lines.append(f"Image prompts: {description.image_prompt_count}")
    lines.append(f"Call to action: {'yes' if description.has_call_to_action else 'no'}")
    lines.append(f"Source summary: {'yes' if description.source_summary_present else 'no'}")
    lines.append(f"Quality status: {'passed' if description.passed else 'warnings found'}")
    lines.append("")
    lines.append("## Spammy Terms")
    lines.append("")
    if description.spammy_terms_found:
        lines.extend(f"- {term}" for term in description.spammy_terms_found)
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if description.warnings:
        lines.extend(f"- {warning}" for warning in description.warnings)
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Suggestions")
    lines.append("")
    if description.suggestions:
        lines.extend(f"- {suggestion}" for suggestion in description.suggestions)
    else:
        lines.append("- None.")
    return "\n".join(lines) + "\n"


def description_to_json(description: DraftDescription) -> str:
    return json.dumps(to_dict(description), ensure_ascii=False, indent=2)
