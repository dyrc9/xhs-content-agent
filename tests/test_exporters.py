import json
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
