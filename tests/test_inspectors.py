import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from xhs_content_agent.cli import main
from xhs_content_agent.inspectors import describe_note, description_to_text
from xhs_content_agent.schema import NoteDraft


class InspectorsTest(unittest.TestCase):
    def test_describe_note_reports_publishability_signals(self):
        draft = NoteDraft(
            title="百分百必火 AI 工具",
            hook="",
            body="第一段。\n\n第二段。",
            hashtags=["AI工具", "独立开发"],
            image_prompts=["Show the workflow"],
            call_to_action="欢迎交流。",
        )

        description = describe_note(draft, Path("runs/demo/note.json"))

        self.assertEqual(description.title_length, len(draft.title))
        self.assertEqual(description.hook_length, 0)
        self.assertEqual(description.body_paragraphs, 2)
        self.assertEqual(description.hashtag_count, 2)
        self.assertFalse(description.has_hook)
        self.assertIn("百分百", description.spammy_terms_found)
        self.assertFalse(description.passed)

        text = description_to_text(description)
        self.assertIn("# Draft Inspection", text)
        self.assertIn("Hook: no", text)
        self.assertIn("Quality status: warnings found", text)
        self.assertIn("Add a short source summary so future edits stay grounded.", text)

    def test_cli_inspect_json_prints_description(self):
        payload = {
            "title": "一个小工具的构建记录",
            "hook": "hook",
            "body": "这是一段足够长的正文，用来验证 inspect JSON 输出是否正常，也确认正文长度统计可以工作。",
            "hashtags": ["AI工具", "开源项目"],
            "image_prompts": ["Prompt 1"],
            "call_to_action": "欢迎交流。",
            "source_summary": "summary",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            note_path = Path(temp_dir) / "note.json"
            note_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            with patch("sys.stdout.write") as write_mock:
                exit_code = main(["inspect", str(note_path), "--json"])

        rendered = "".join(call.args[0] for call in write_mock.call_args_list)
        result = json.loads(rendered)
        self.assertEqual(exit_code, 0)
        self.assertEqual(result["source_path"], str(note_path))
        self.assertTrue(result["has_hook"])
        self.assertEqual(result["hook_length"], 4)
        self.assertEqual(result["hashtag_count"], 2)
        self.assertTrue(result["passed"])


if __name__ == "__main__":
    unittest.main()
