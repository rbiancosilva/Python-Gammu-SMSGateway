import abc

from src.utils import LoggingJSONHandler


class GammuError:
    def __init__(self, gammu_exception):
        self._logging_handler = LoggingJSONHandler()
        self._e = gammu_exception

    @abc.abstractmethod
    def raise_exception(self):
        pass


