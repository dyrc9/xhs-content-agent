from __future__ import annotations

import argparse
from pathlib import Path

from .calendar import build_calendar
from .exporters import write_calendar, write_note, write_quality_report
from .generators import create_generator
from .io import read_note, read_text, read_topics
from .quality import check_note


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xhs-content-agent",
        description="CLI content studio for Xiaohongshu / RedNote creators.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    draft = subparsers.add_parser("draft", help="Generate a note draft from local source material.")
    draft.add_argument("source", type=Path)
    draft.add_argument("--out", type=Path, default=Path("runs/draft"))
    draft.add_argument("--generator", choices=["template", "openai"], default="template")
    draft.add_argument("--model", default="gpt-5.1")
    draft.set_defaults(func=_draft)

    calendar = subparsers.add_parser("calendar", help="Build a content calendar from topics.")
    calendar.add_argument("topics", type=Path)
    calendar.add_argument("--days", type=int, default=7)
    calendar.add_argument("--out", type=Path, default=Path("runs/calendar"))
    calendar.set_defaults(func=_calendar)

    check = subparsers.add_parser("check", help="Check a note draft package.")
    check.add_argument("note", type=Path)
    check.add_argument("--out", type=Path, default=Path("runs/check"))
    check.set_defaults(func=_check)

    return parser


def _draft(args: argparse.Namespace) -> None:
    generator = create_generator(args.generator, model=args.model)
    source = read_text(args.source)
    draft = generator.generate(source)
    write_note(draft, args.out)
    report = check_note(draft)
    write_quality_report(report, args.out)
    print(f"wrote draft package to {args.out}")


def _calendar(args: argparse.Namespace) -> None:
    topics = read_topics(args.topics)
    items = build_calendar(topics, days=args.days)
    write_calendar(items, args.out)
    print(f"wrote content calendar to {args.out}")


def _check(args: argparse.Namespace) -> None:
    draft = read_note(args.note)
    report = check_note(draft)
    write_quality_report(report, args.out)
    if report.passed:
        print("check passed")
    else:
        print("check completed with warnings")
