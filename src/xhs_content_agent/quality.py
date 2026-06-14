from __future__ import annotations

from .schema import NoteDraft, QualityReport


SPAMMY_WORDS = ["暴富", "稳赚", "躺赚", "必火", "百分百", "无脑", "割韭菜"]
BODY_WARNING_THRESHOLD = 1200
HOOK_WARNING_THRESHOLD = 40


def _normalize_hashtag(tag: str) -> str:
    return tag.strip().lstrip("#").casefold()


def check_note(draft: NoteDraft) -> QualityReport:
    warnings: list[str] = []
    suggestions: list[str] = []
    hook = draft.hook.strip()
    normalized_hashtags = [_normalize_hashtag(tag) for tag in draft.hashtags if _normalize_hashtag(tag)]
    unique_hashtags = set(normalized_hashtags)
    body_paragraphs = len([part for part in draft.body.split("\n\n") if part.strip()])

    if len(draft.title) > 40:
        warnings.append("Title may be too long for mobile reading.")
    if not hook:
        suggestions.append("Add a concise hook so the note angle is obvious before the body starts.")
    elif len(hook) > HOOK_WARNING_THRESHOLD:
        warnings.append("Hook may be too long; keep the opening line easy to scan.")
    if len(draft.body) < 80:
        suggestions.append("Body is short. Add more concrete context or implementation detail.")
    if len(draft.body) > BODY_WARNING_THRESHOLD:
        warnings.append("Body may be too long for a focused mobile note.")
    if body_paragraphs < 2:
        suggestions.append("Body is a single block. Split it into shorter paragraphs for readability.")
    if len(draft.hashtags) > 8:
        warnings.append("Too many hashtags can look noisy.")
    if len(unique_hashtags) != len(normalized_hashtags):
        warnings.append("Duplicate hashtags reduce signal and make the draft look repetitive.")
    if any(word in draft.title + draft.body for word in SPAMMY_WORDS):
        warnings.append("Draft contains spammy or exaggerated language.")
    if not draft.call_to_action:
        suggestions.append("Add a light call to action.")
    if not draft.source_summary.strip():
        suggestions.append("Add a short source summary so future edits stay grounded.")
    if not draft.image_prompts:
        suggestions.append("Add image prompts or screenshot ideas.")

    return QualityReport(passed=not warnings, warnings=warnings, suggestions=suggestions)
