from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any

from .schema import NoteDraft


class DraftGenerator(ABC):
    name: str

    @abstractmethod
    def generate(self, source: str) -> NoteDraft:
        raise NotImplementedError


class TemplateGenerator(DraftGenerator):
    name = "template"

    def generate(self, source: str) -> NoteDraft:
        summary = _compact(source)
        title = _title_from_source(source)
        hashtags = _hashtags(source)
        body = "\n\n".join(
            [
                "最近在做一个小工具，想把过程记录下来。",
                summary,
                "我比较在意的不是模型本身有多炫，而是这个 workflow 能不能被复现、被检查、被长期维护。",
                "接下来会继续把它做成更完整的开源项目：补测试、补示例、补真实使用场景。",
            ]
        )
        return NoteDraft(
            title=title,
            hook="一个小而真的 AI 工具，比一堆空概念更有说服力。",
            body=body,
            hashtags=hashtags,
            image_prompts=[
                "A clean desktop screenshot showing a CLI tool generating structured meeting notes",
                "A minimal workflow diagram: audio -> chunks -> transcript -> summary",
            ],
            call_to_action="如果你也在做 AI Agent 或自动化工具，可以交流一下。",
            source_summary=summary,
        )


class OpenAIGenerator(DraftGenerator):
    name = "openai"

    def __init__(self, model: str = "gpt-5.1") -> None:
        self.model = model

    def generate(self, source: str) -> NoteDraft:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install OpenAI support with: pip install -e '.[openai]'") from exc

        client = OpenAI()
        response = client.responses.create(model=self.model, input=_prompt(source))
        payload = _parse_json(getattr(response, "output_text", ""))
        return NoteDraft(
            title=str(payload.get("title") or _title_from_source(source)),
            hook=str(payload.get("hook") or ""),
            body=str(payload.get("body") or ""),
            hashtags=_list(payload.get("hashtags")) or _hashtags(source),
            image_prompts=_list(payload.get("image_prompts")),
            call_to_action=str(payload.get("call_to_action") or ""),
            source_summary=str(payload.get("source_summary") or _compact(source)),
        )


def create_generator(name: str, model: str) -> DraftGenerator:
    if name == "template":
        return TemplateGenerator()
    if name == "openai":
        return OpenAIGenerator(model=model)
    raise ValueError(f"Unknown generator: {name}")


def _prompt(source: str) -> str:
    return f"""You are helping a creator draft a Xiaohongshu / RedNote note.

Return only valid JSON with:
- title: string, <= 24 Chinese characters if Chinese
- hook: string
- body: string, practical and honest, not exaggerated
- hashtags: array of strings
- image_prompts: array of strings
- call_to_action: string
- source_summary: string

Rules:
- Do not invent results, revenue, users, or credentials.
- Do not imply fake engagement or guaranteed growth.
- Make it useful for developers interested in AI agents and automation.
- Avoid spammy language.

Source material:
{source}
"""


def _parse_json(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return {}
        value = json.loads(match.group(0))
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _compact(source: str, limit: int = 260) -> str:
    text = " ".join(line.strip() for line in source.splitlines() if line.strip() and not line.startswith("#"))
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _title_from_source(source: str) -> str:
    lower = source.lower()
    if "meeting" in lower or "会议" in source:
        return "我做了个 AI 会议纪要工具"
    if "agent" in lower:
        return "做 AI Agent 不能只写 prompt"
    return "一个小工具的构建记录"


def _hashtags(source: str) -> list[str]:
    tags = ["AI工具", "独立开发", "开源项目"]
    lower = source.lower()
    if "agent" in lower:
        tags.append("AIAgent")
    if "meeting" in lower or "transcript" in lower:
        tags.append("会议纪要")
    if "cli" in lower:
        tags.append("效率工具")
    return tags[:6]
