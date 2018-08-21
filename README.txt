### Nginx server log analyzer
Python 3.6


###
This package generates an HTML report analyzing a server log

To run it
>>> python log_analyzer.py --config config.txt

where --config is an optional flag to specify

Config parameters:
REPORT_SIZE: number of URLs in the report
REPORT_DIR: location of the report
LOG_DIR: location of the log
