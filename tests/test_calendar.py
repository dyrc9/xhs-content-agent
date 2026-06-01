import unittest

from xhs_content_agent.calendar import build_calendar


class CalendarTest(unittest.TestCase):
    def test_build_calendar_repeats_topics(self):
        items = build_calendar(["one", "two"], days=3)

        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].topic, "one")
        self.assertEqual(items[2].topic, "one")


if __name__ == "__main__":
    unittest.main()
