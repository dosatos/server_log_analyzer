import sys


class CommandLineInterface:
    def __init__(self):
        self.config_path = None
        self.config = {
            "REPORT_SIZE": 1000,
            "REPORT_DIR": "./reports",
            "LOG_DIR": "./log"
        }

        # update config if config path is provided
        try:
            path = self.get_config_path()
            self.update_config(path)
        except ValueError:
            pass

    def get_args(self):
        return sys.argv[1:]

    def get_config_path(self):
        args = self.get_args()
        try:
            idx = args.index("--config")
            return args[idx+1]
        except ValueError:
            return None

    def set_config_path(self, path):
        self.config_path = path

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config

    def update_config(self, path):
        config = {}
        with open(path, 'r') as content:
            for line in content:
                k, v = line.split("=")
                v = v.strip()
                try:
                    v = int(v)
                except ValueError:
                    pass
                config.update({k.strip(): v})
        self.set_config(config)
