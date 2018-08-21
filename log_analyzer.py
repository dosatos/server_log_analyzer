#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';


from utilities.cli import CommandLineInterface
from utilities.report import Report


def main():
    cli = CommandLineInterface()
    config = cli.get_config()

    report = Report(config)
    report.generate()


if __name__ == "__main__":
    main()
