import os
import time
import gzip
import statistics


class Report:
    def __init__(self, config):
        self.allowed_methods = ["GET", "POST", "DELETE",
                                "HEAD", "UPDATE", "PUT",
                                "OPTION", "CONNECT", "TRACE", "PATCH"]
        self.config = config
        self.path = None
        self.first_line = None
        self.log_names = None
        self.total_time = 0
        self.total_count = 0
        self.date = None
        self.update_log_names()

    def get_config(self):
        return self.config

    def get_latest_log_name(self):
        # get latest log
        res = max(self.log_names, key=lambda name: int(get_date(name)))
        date = parse_time(res)
        self.date = f"{date.tm_year}.{date.tm_mon:02}.{date.tm_mday}"
        return res

    def update_log_names(self, kind='ui'):
        logs_dir = self.config['LOG_DIR']
        names = list(os.walk(logs_dir))[0][2]
        self.log_names = [name for name in names if kind in name and is_valid_name(name)]
        self.path = os.path.join(logs_dir, self.get_latest_log_name())

    def process_line(self, line):
        first_quotes = line.find('"')
        start_pos = line.find(' ', first_quotes)+1
        method = line[first_quotes+1:start_pos].strip().upper()
        if method not in self.allowed_methods:
            return
        end_pos = line.find(' ', start_pos)
        url = line[start_pos:end_pos]
        duration = get_duration(line)
        return url, duration

    def update_url(self, responses, line):
        try:
            url, duration = self.process_line(line)
            self.total_time += duration
            self.total_count += 1
        except TypeError:
            return
        # store each duration in a corresponding stack, to calculate
        # the metrics: count, time_avg, time_max, time_sum,
        #              time_med, time_perc, count_perc
        try:
            responses[url].append(duration)
        except KeyError:
            responses[url] = [duration]

    def process_log(self, log):
        responses = {}
        for line in log:
            line = str(line)
            if "HTTP/" not in line:
                continue
            self.update_url(responses, line)
        return responses

    def get_report_json(self, report):
        results = []
        for url, durations in report.items():
            count = len(durations)
            time_sum = nullify(sum(durations))
            time_avg = nullify(time_sum / count)
            time_max = nullify(max(durations))
            time_med = nullify(statistics.median(durations))
            time_perc = nullify(time_sum / self.total_time)
            count_perc = count / self.total_count

            data_point = {
                 "count": count,
                 "time_avg": f"{time_avg:0.3}",
                 "time_max": f"{time_max:0.3}",
                 "time_sum": f"{time_sum:0.3}",
                 "url": url,
                 "time_med": f"{time_med:0.3}",
                 "time_perc": f"{time_perc:0.3}",
                 "count_perc": f"{count_perc:0.3}"
            }
            results.append(data_point)
        return results

    def save_html(self, log):
        report = self.process_log(log)
        report_name = f"reports/report-{self.date}.html"
        with open("templates/report.html", "r") as template:
            with open(f"{report_name}", "w") as save_file:
                for line in template:
                    if "var table = $table_json;" in line:
                        report_table_json = self.get_report_json(report)
                        save_file.write(f"var table = {report_table_json}\n")
                    else:
                        save_file.write(line)

    def generate(self):
        if self.path.endswith(".gz"):
            with gzip.open(self.path, 'rb') as log:
                self.save_html(log)
        else:
            with open(self.path, 'rb') as log:
                report = self.process_log(log)


# other helping functions
def parse_time(name):
    date = get_date(name)
    return time.strptime(date, "%Y%m%d")


def get_date(name):
    return name[-8:] if not name.endswith('.gz') else name[-11:-3]


def get_duration(line):
    dur = line.split(" ")[-1]
    return float("".join(l for l in list(dur) if l.isdigit() or l == "."))


def is_valid_name(name):

    if '.log' not in name:
        return False

    try:
        parse_time(name)
        return True
    except ValueError:
        return False


def nullify(num):
    return round(num, 3)
