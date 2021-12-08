import argparse
import os
from collections import defaultdict


def get_columns(line):
    """
    Retrieve column names and respective indexes using the
    #Fields metadata.
    :param line: field line containing the column names
    :return: defaultdict : column name : index
    """
    return {col: i for i, col in enumerate(line.split(" ")[1:])}


class Logs:
    def __init__(self, files, uri_field):
        self.files = files  # user-specified paths
        self.logs = {}  # processed log paths
        self.uri_field = uri_field  # name of uri field
        self.uris = defaultdict(int)  # uri hit counter
        self.cols = {}  # column names

    def get_logs(self):
        """
        Returns a list of all paths relative to the current
        project directory, ignoring any non .log files.

        :param paths passed by user as arguments to "paths" parameter
        :return: set of .log paths

        """
        logs = []
        for path in self.files:
            if os.path.isfile(path):
                logs.append(path)
            if os.path.isdir(path):
                for subpath in os.listdir(path):
                    logs.append(os.path.join(path, subpath))
        self.logs = set(log for log in logs if log.endswith(".log"))
        return self.logs

    def read_logs(self):
        """
        Creates a formatted list of all log entries from all paths requested by user.
        Outputs an ordered list of uri queries and the number of hits each uri has received.

        :param logs:
        :return:
        """
        if not self.logs:
            print("Log paths not processed yet - use get_logs() method.")

        lines = []
        for log in self.logs:
            with open(log) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith("#Fields"):
                        # find fields metadata to extract columns
                        self.cols = get_columns(line)
                    if line.startswith("#"):
                        # ignore comments at the start
                        continue
                    lines.append(line)
                    # ignoring lines that appear before the metadata
                    if self.cols:
                        uri = line.split(" ")[self.cols[self.uri_field]]
                        self.uris[uri] += 1
        self.uris = sorted(self.uris.items(), key=lambda item: item[1], reverse=True)
        return lines

    @property
    def uri_statistics(self):
        return self.uris


if __name__ == "__main__":
    # type , help , Python logger
    parser = argparse.ArgumentParser(description="Parse and analyse logs")
    parser.add_argument("paths", nargs="*")  # paths
    parser.add_argument("--uri_field", required=True)  # name of uri field
    args = parser.parse_args()
    logs = Logs(args.paths, args.uri_field)
    log_file_paths = logs.get_logs()
    lines_all = logs.read_logs()
    if logs.uri_statistics:
        print("Ordered list of URI hits successfully generated:")
        print(logs.uri_statistics)
