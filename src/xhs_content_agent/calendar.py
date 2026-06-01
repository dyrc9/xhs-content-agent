from __future__ import annotations

from .schema import CalendarItem


def build_calendar(topics: list[str], days: int) -> list[CalendarItem]:
    clean_topics = [topic.strip() for topic in topics if topic.strip()]
    if not clean_topics:
        clean_topics = ["Build one small AI tool in public"]

    items: list[CalendarItem] = []
    for day in range(1, days + 1):
        topic = clean_topics[(day - 1) % len(clean_topics)]
        items.append(
            CalendarItem(
                day=day,
                topic=topic,
                angle=_angle_for_day(day),
                suggested_title=_title_for_topic(topic),
            )
        )
    return items


def _angle_for_day(day: int) -> str:
    angles = [
        "problem and motivation",
        "implementation detail",
        "failure or tradeoff",
        "before and after workflow",
        "small demo",
        "lessons learned",
        "next iteration",
    ]
    return angles[(day - 1) % len(angles)]


def _title_for_topic(topic: str) -> str:
    if len(topic) <= 28:
        return topic
    return topic[:25].rstrip() + "..."
