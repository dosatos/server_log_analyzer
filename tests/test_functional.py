import sys
sys.path.append("./")
import unittest

from utilities.cli import CommandLineInterface
from utilities.report import Report


class TestCLI(unittest.TestCase):

    def test_main(self):
        # a user sets new config using CLI
        cli = CommandLineInterface()
        sys.argv = [__name__, "--config", "config_file_path"]
        config_folder = cli.get_config_path()
        self.assertTrue(config_folder, "config_file_path")

        # a user is generating a report in HTML format
        config = cli.get_config()
        report = Report(config)
        report.generate(filename)
        # Вопрос: как такое лучше всего тестить? т.е. пустую (void) функцию?
        self.assertTrue(report.first_line, "this is the report first line")


if __name__ == "__main__":
    unittest.main()
