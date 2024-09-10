from src.utils import LoggingJSONHandler

class SMSStarter:
    def __init__(self, state_machine_handler):
        self._logging_handler = LoggingJSONHandler()
        self._state_machine_handler = state_machine_handler

