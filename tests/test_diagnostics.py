import json
import unittest
from unittest.mock import patch

from xhs_content_agent.cli import main
from xhs_content_agent.diagnostics import describe_environment, doctor_report_to_text


class DiagnosticsTest(unittest.TestCase):
    @patch("xhs_content_agent.diagnostics.os.getenv")
    @patch("xhs_content_agent.diagnostics._package_version")
    def test_describe_environment_reports_missing_openai_support(self, package_version_mock, getenv_mock):
        package_version_mock.return_value = None
        getenv_mock.return_value = ""

        report = describe_environment()

        self.assertEqual(report.available_generators, ["template"])
        self.assertFalse(report.openai_package_installed)
        self.assertFalse(report.openai_api_key_configured)
        self.assertIn("Install OpenAI support with: pip install -e '.[openai]'", report.missing_optional_features)
        self.assertIn("Set OPENAI_API_KEY for OpenAI draft generation.", report.missing_optional_features)

        rendered = doctor_report_to_text(report)
        self.assertIn("# Environment Doctor", rendered)
        self.assertIn("OpenAI package: missing", rendered)

    @patch("xhs_content_agent.diagnostics.os.getenv")
    @patch("xhs_content_agent.diagnostics._package_version")
    def test_doctor_command_json_prints_environment_report(self, package_version_mock, getenv_mock):
        package_version_mock.return_value = "1.86.0"
        getenv_mock.return_value = "sk-test"

        with patch("sys.stdout.write") as write_mock:
            exit_code = main(["doctor", "--json"])

        rendered = "".join(call.args[0] for call in write_mock.call_args_list)
        result = json.loads(rendered)

        self.assertEqual(exit_code, 0)
        self.assertTrue(result["openai_package_installed"])
        self.assertEqual(result["openai_package_version"], "1.86.0")
        self.assertTrue(result["openai_api_key_configured"])
        self.assertIn("openai", result["available_generators"])
        self.assertEqual(result["missing_optional_features"], [])


if __name__ == "__main__":
    unittest.main()
