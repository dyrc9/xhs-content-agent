import unittest

from xhs_content_agent.quality import check_note
from xhs_content_agent.schema import NoteDraft


class QualityTest(unittest.TestCase):
    def test_quality_flags_spammy_language(self):
        report = check_note(
            NoteDraft(
                title="百分百必火",
                hook="",
                body="短内容",
                hashtags=["AI"],
            )
        )

        self.assertFalse(report.passed)
        self.assertTrue(report.warnings)

    def test_quality_flags_duplicate_hashtags_and_long_single_block_body(self):
        report = check_note(
            NoteDraft(
                title="构建一个 AI 工作流工具",
                hook="",
                body="这是一段很长的正文。" * 220,
                hashtags=["AI工具", "#ai工具", "开源项目"],
                call_to_action="欢迎交流。",
                source_summary="source",
            )
        )

        self.assertFalse(report.passed)
        self.assertIn("Duplicate hashtags reduce signal and make the draft look repetitive.", report.warnings)
        self.assertIn("Body may be too long for a focused mobile note.", report.warnings)
        self.assertIn(
            "Body is a single block. Split it into shorter paragraphs for readability.",
            report.suggestions,
        )

    def test_quality_suggests_source_grounding_when_missing(self):
        report = check_note(
            NoteDraft(
                title="一个小工具的构建记录",
                hook="",
                body="第一段介绍问题和背景。\n\n第二段补充具体做法和结果，确保正文足够长并且可读。",
                hashtags=["AI工具"],
                image_prompts=["Show the CLI output"],
                call_to_action="欢迎交流。",
                source_summary="",
            )
        )

        self.assertTrue(report.passed)
        self.assertIn("Add a short source summary so future edits stay grounded.", report.suggestions)


if __name__ == "__main__":
    unittest.main()
