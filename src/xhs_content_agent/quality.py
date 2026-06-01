from __future__ import annotations

from .schema import NoteDraft, QualityReport


SPAMMY_WORDS = ["暴富", "稳赚", "躺赚", "必火", "百分百", "无脑", "割韭菜"]


def check_note(draft: NoteDraft) -> QualityReport:
    warnings: list[str] = []
    suggestions: list[str] = []

    if len(draft.title) > 40:
        warnings.append("Title may be too long for mobile reading.")
    if len(draft.body) < 80:
        suggestions.append("Body is short. Add more concrete context or implementation detail.")
    if len(draft.hashtags) > 8:
        warnings.append("Too many hashtags can look noisy.")
    if any(word in draft.title + draft.body for word in SPAMMY_WORDS):
        warnings.append("Draft contains spammy or exaggerated language.")
    if not draft.call_to_action:
        suggestions.append("Add a light call to action.")
    if not draft.image_prompts:
        suggestions.append("Add image prompts or screenshot ideas.")

    return QualityReport(passed=not warnings, warnings=warnings, suggestions=suggestions)
