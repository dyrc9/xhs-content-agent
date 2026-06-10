import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from xhs_content_agent.cli import main
from xhs_content_agent.exporters import write_quality_report
from xhs_content_agent.schema import QualityReport


class ExportersTest(unittest.TestCase):
    def test_write_quality_report_writes_json_and_markdown(self):
        report = QualityReport(
            passed=False,
            warnings=["Draft contains spammy or exaggerated language."],
            suggestions=["Add a light call to action."],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            write_quality_report(report, out_dir)

            payload = json.loads((out_dir / "quality-report.json").read_text(encoding="utf-8"))
            markdown = (out_dir / "quality-report.md").read_text(encoding="utf-8")

        self.assertEqual(payload["warnings"], report.warnings)
        self.assertIn("# Quality Report", markdown)
        self.assertIn("Status: Warnings found", markdown)
        self.assertIn("- Draft contains spammy or exaggerated language.", markdown)
        self.assertIn("- Add a light call to action.", markdown)

    def test_check_command_supports_json_without_writing_files(self):
        payload = {
            "title": "一个小工具的构建记录",
            "hook": "hook",
            "body": "这是一段足够长的正文，用来验证 check JSON 输出是否正常，也确认质量报告可以直接接入自动化流程。",
            "hashtags": ["AI工具", "开源项目"],
            "image_prompts": ["Prompt 1"],
            "call_to_action": "欢迎交流。",
            "source_summary": "summary",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            note_path = Path(temp_dir) / "note.json"
            note_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            previous_cwd = Path.cwd()
            os.chdir(temp_dir)
            try:
                with patch("sys.stdout.write") as write_mock:
                    exit_code = main(["check", str(note_path), "--json"])
            finally:
                os.chdir(previous_cwd)

            rendered = "".join(call.args[0] for call in write_mock.call_args_list)
            result = json.loads(rendered)

            self.assertEqual(exit_code, 0)
            self.assertTrue(result["passed"])
            self.assertEqual(result["warnings"], [])
            self.assertFalse((Path(temp_dir) / "runs").exists())

    def test_check_command_strict_returns_non_zero_for_warnings(self):
        payload = {
            "title": "百分百必火",
            "hook": "hook",
            "body": "短内容",
            "hashtags": ["AI工具"],
            "image_prompts": [],
            "call_to_action": "",
            "source_summary": "summary",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            note_path = Path(temp_dir) / "note.json"
            note_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            previous_cwd = Path.cwd()
            os.chdir(temp_dir)
            try:
                with patch("sys.stdout.write") as write_mock:
                    exit_code = main(["check", str(note_path), "--json", "--strict"])
            finally:
                os.chdir(previous_cwd)

            rendered = "".join(call.args[0] for call in write_mock.call_args_list)
            result = json.loads(rendered)

            self.assertEqual(exit_code, 1)
            self.assertFalse(result["passed"])
            self.assertTrue(result["warnings"])
            self.assertFalse((Path(temp_dir) / "runs").exists())


if __name__ == "__main__":
    unittest.main()
