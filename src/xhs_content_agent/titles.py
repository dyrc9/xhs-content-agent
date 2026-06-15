from __future__ import annotations

import json

from .schema import NoteDraft, TitleVariant, TitleVariantSet, to_dict


TITLE_LIMIT = 24


def build_title_variants(draft: NoteDraft) -> TitleVariantSet:
    subject = _subject_from_draft(draft)
    candidates = [
        ("direct", draft.title.strip() or f"我做了个{subject}"),
        ("problem", f"做{subject}，先别急着追热点"),
        ("workflow", f"把{subject}做成可检查 workflow"),
        ("lesson", f"{subject}这次我补了检查和交付"),
    ]

    variants: list[TitleVariant] = []
    seen: set[str] = set()
    for angle, raw_title in candidates:
        title = _fit_title(raw_title)
        normalized = title.casefold()
        if not title or normalized in seen:
            continue
        seen.add(normalized)
        variants.append(
            TitleVariant(
                angle=angle,
                title=title,
                length=len(title),
                mobile_safe=len(title) <= TITLE_LIMIT,
            )
        )

    return TitleVariantSet(
        source_title=draft.title,
        source_summary_present=bool(draft.source_summary.strip()),
        variants=variants,
    )


def variants_to_json(variant_set: TitleVariantSet) -> str:
    return json.dumps(to_dict(variant_set), ensure_ascii=False, indent=2)


def variants_to_text(variant_set: TitleVariantSet) -> str:
    lines = ["# Title Variants", ""]
    lines.append(f"Source title: {variant_set.source_title or 'unknown'}")
    lines.append(f"Source summary: {'yes' if variant_set.source_summary_present else 'no'}")
    lines.append("")
    for item in variant_set.variants:
        lines.append(f"- [{item.angle}] {item.title} ({item.length} chars, mobile {'ok' if item.mobile_safe else 'tight'})")
    return "\n".join(lines) + "\n"


def _subject_from_draft(draft: NoteDraft) -> str:
    base = (draft.source_summary or draft.title or draft.body).strip()
    if not base:
        return "AI 工具"

    for needle, subject in (
        ("会议", "AI 会议纪要工具"),
        ("transcript", "AI 会议纪要工具"),
        ("meeting", "AI 会议纪要工具"),
        ("agent", "AI Agent 工具"),
        ("workflow", "AI workflow 工具"),
        ("自动化", "自动化工具"),
        ("内容", "内容工具"),
    ):
        if needle in base.lower() or needle in base:
            return subject
    return "AI 工具"


def _fit_title(title: str) -> str:
    compact = " ".join(title.split())
    if len(compact) <= TITLE_LIMIT:
        return compact
    return compact[: TITLE_LIMIT - 3].rstrip() + "..."
