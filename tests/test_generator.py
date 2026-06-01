import unittest

from xhs_content_agent.generators import TemplateGenerator


class GeneratorTest(unittest.TestCase):
    def test_template_generator_creates_note(self):
        draft = TemplateGenerator().generate("AI agent CLI meeting transcription tool")

        self.assertTrue(draft.title)
        self.assertTrue(draft.body)
        self.assertIn("开源项目", draft.hashtags)


if __name__ == "__main__":
    unittest.main()
