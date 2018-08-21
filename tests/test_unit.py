import os
import sys
sys.path.append("./")
import unittest
# import logging

from utilities.cli import CommandLineInterface
from utilities.report import Report


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CommandLineInterface()
        sys.argv = [__name__, "--config", "config.txt"]

    def test_get_args(self):
        args = self.cli.get_args()
        self.assertTrue(args, sys.argv[1:])

    def test_get_config_path(self):
        # a user sets new config using CLI
        config_folder = self.cli.get_config_path()
        self.assertEqual(config_folder, "config.txt")

        # a user sets new config using CLI INCORRECTLY
        with self.assertRaises(ValueError):
            sys.argv = [__name__, "-config", "config.txt"]
            self.cli.get_config_path()

    def test_get_config(self):
        path = self.cli.get_config_path()
        self.cli.update_config(path)
        config = self.cli.get_config()
        config_validation = {
            "REPORT_SIZE": 100,
            "REPORT_DIR": "./report",
            "LOG_DIR": "./test_log"
        }
        self.assertEqual(config, config_validation)


class TestReport(unittest.TestCase):

    def setUp(self):
        sys.argv = [__name__, "--config", "config.txt"]
        self.cli = CommandLineInterface()
        config = self.cli.get_config()
        self.report = Report(config)

        # check report.get_log_names()
        self.report.update_log_names(kind='ui')

    def test_get_log_names(self):
        check_names = ['nginx-access-ui.log-20180525', 'nginx-access-ui.log-20170525',
                       'nginx-access-ui.log-20180630.gz']
        self.assertEqual(set(self.report.log_names), set(check_names))

    def test_get_last_log_name(self):
        last = self.report.get_latest_log_name()
        self.assertEqual(last, 'nginx-access-ui.log-20180630.gz')

    def test_generate(self):
        log = self.report.generate()
        self.assertEqual(log, 1)  # TODO: correct the test




if __name__ == "__main__":
    unittest.main()
