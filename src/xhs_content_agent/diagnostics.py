from __future__ import annotations

import json
import os
import sys
from importlib import metadata

from .schema import DoctorReport, to_dict


def describe_environment() -> DoctorReport:
    openai_version = _package_version("openai")
    available_generators = ["template"]
    missing_optional_features: list[str] = []

    if openai_version:
        available_generators.append("openai")
    else:
        missing_optional_features.append("Install OpenAI support with: pip install -e '.[openai]'")

    if not os.getenv("OPENAI_API_KEY"):
        missing_optional_features.append("Set OPENAI_API_KEY for OpenAI draft generation.")

    return DoctorReport(
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        openai_package_installed=bool(openai_version),
        openai_package_version=openai_version,
        openai_api_key_configured=bool(os.getenv("OPENAI_API_KEY")),
        available_generators=available_generators,
        missing_optional_features=missing_optional_features,
    )


def doctor_report_to_json(report: DoctorReport) -> str:
    return json.dumps(to_dict(report), ensure_ascii=False, indent=2)


def doctor_report_to_text(report: DoctorReport) -> str:
    openai_status = "installed"
    if report.openai_package_version:
        openai_status = f"installed ({report.openai_package_version})"
    elif not report.openai_package_installed:
        openai_status = "missing"

    lines = ["# Environment Doctor", ""]
    lines.append(f"Python: {report.python_version}")
    lines.append(f"OpenAI package: {openai_status}")
    lines.append(f"OPENAI_API_KEY: {'set' if report.openai_api_key_configured else 'missing'}")
    lines.append("")
    lines.append("## Available Generators")
    lines.append("")
    lines.extend(f"- {name}" for name in report.available_generators)
    lines.append("")
    lines.append("## Missing Optional Features")
    lines.append("")
    if report.missing_optional_features:
        lines.extend(f"- {item}" for item in report.missing_optional_features)
    else:
        lines.append("- None.")
    return "\n".join(lines) + "\n"


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None
