import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from xhs_content_agent.cli import main
from xhs_content_agent.schema import NoteDraft
from xhs_content_agent.titles import build_title_variants, variants_to_text


class TitleVariantsTest(unittest.TestCase):
    def test_build_title_variants_returns_distinct_mobile_safe_options(self):
        draft = NoteDraft(
            title="我做了个 AI 会议纪要工具",
            hook="hook",
            body="我把长会议录音拆分、转写，再汇总成结构化纪要。",
            hashtags=["AI工具"],
            source_summary="meeting transcript workflow for AI agents",
        )

        variant_set = build_title_variants(draft)

        self.assertEqual(variant_set.source_title, draft.title)
        self.assertTrue(variant_set.source_summary_present)
        self.assertGreaterEqual(len(variant_set.variants), 3)
        self.assertEqual(len({item.title for item in variant_set.variants}), len(variant_set.variants))
        self.assertTrue(all(item.mobile_safe for item in variant_set.variants))

        rendered = variants_to_text(variant_set)
        self.assertIn("# Title Variants", rendered)
        self.assertIn("[workflow]", rendered)

    def test_titles_command_supports_json_output(self):
        payload = {
            "title": "一个小工具的构建记录",
            "hook": "hook",
            "body": "这是一段足够长的正文，用来验证标题变体 JSON 输出是否正常，也确认包装迭代可以直接接入人工 review 流程。",
            "hashtags": ["AI工具", "开源项目"],
            "image_prompts": ["Prompt 1"],
            "call_to_action": "欢迎交流。",
            "source_summary": "AI agent workflow project build log",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            note_path = Path(temp_dir) / "note.json"
            note_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            with patch("sys.stdout.write") as write_mock:
                exit_code = main(["titles", str(note_path), "--json"])

        rendered = "".join(call.args[0] for call in write_mock.call_args_list)
        result = json.loads(rendered)
        self.assertEqual(exit_code, 0)
        self.assertEqual(result["source_title"], payload["title"])
        self.assertTrue(result["source_summary_present"])
        self.assertGreaterEqual(len(result["variants"]), 3)
        self.assertTrue(all("angle" in item for item in result["variants"]))


if __name__ == "__main__":
    unittest.main()
