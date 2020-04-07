import urllib.request
from time import sleep
from log_helper import LogHelper

class HttpHelper():
    def __init__(self, log: LogHelper, max_attempts: int = 3, secs_reattempt_await: int = 0, max_secs_to_await: int = 300):
        self.max_attempts = max_attempts
        self.secs_await = secs_reattempt_await
        self.log = log
        self._last_secs_awaited = 0
        self._max_secs_to_await = max_secs_to_await

    def get(self, url):
        contents = self._get(url, 1)
        return contents

    def _get(self, url, attempt: int):
        try:
            self._zzz(self._get_secs_to_await(attempt))
            self.log.write('....Descargando ' + url)
            response = urllib.request.urlopen(url, None, 10)
            html = response.read()
            self.log.write('- OK -')
        except Exception as ex:
            self.log.write("Error en HttpHelper._get " + str(ex))
            if attempt < self.max_attempts:
                return self._get(url, attempt + 1)
            self.log.write("Error__ Abortada descarga de " + url + " tras " + str(attempt) + " intentos")
            return False
        return html

    def _get_secs_to_await(self, attempt):
        if attempt == 1:
            secs = self._last_secs_awaited / 2
            if secs < 1:
                secs = 0
            return secs
        else:
            factor = self.secs_await
            if factor < self._last_secs_awaited:
                factor = self._last_secs_awaited
            secs = factor * 2
            if secs > self._max_secs_to_await:
                secs = self._max_secs_to_await
            return secs

    def _zzz(self, secs):
        self._last_secs_awaited = secs
        if secs > 0:
            self.log.write("....Esperando " + str(secs) + " segs.")
            sleep(secs)
