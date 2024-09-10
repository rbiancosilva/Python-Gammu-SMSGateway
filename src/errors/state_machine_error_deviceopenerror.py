from .gammu_error import GammuError


class StateMachineErrorDeviceOpenError(GammuError):
    def __init__(self, gammu_exception):
        super().__init__(gammu_exception)
        self.raise_exception()

    def raise_exception(self):
        print(f"Unable to start StateMachine. Error: {self._e}.")
        self._logging_handler.logger.error(f"{self._e}.")
        self._logging_handler.iterate_status_counter('failure')
        raise Exception(self._e)