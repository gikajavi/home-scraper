import datetime
import logging

class LogHelper():
    def __init__(self, path='log.log', name="log", stdout: bool=False):
        self._stdout = stdout
        logging.basicConfig(filename=path, filemode='w+', format='%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')
        self._logger = logging.getLogger(name)

    def info(self, s: str):
        self._logger.info(s)
        self.stdout_print(s)

    def warning(self, s: str):
        self._logger.warning(s)
        self.stdout_print(s)

    def error(self, s: str):
        self._logger.error(s)
        self.stdout_print(s)

    def stdout_print(self, s):
        if self._stdout:
            s = str(datetime.datetime.now()) + ': ' + s
            print(s)
