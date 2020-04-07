import datetime

class LogHelper():
    def __init__(self, path):
        self.path = path

    def write(self, s: str):
        s = str(datetime.datetime.now()) + ': ' + s
        self.write_raw(s)

    def write_raw(self, s: str):
        print(s)
        self._file_put_contents(self.path, s + "\n")

    def _file_put_contents(self, path, contents):
        f = open(path, "a")
        f.write(contents)
        f.close()

