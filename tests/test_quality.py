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


if __name__ == "__main__":
    unittest.main()
