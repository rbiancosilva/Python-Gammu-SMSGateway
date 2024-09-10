from .gammu_error import GammuError

class SMSError(GammuError):
    def __init__(self, gammu_exception, phone_number: str):
        super().__init__(gammu_exception)
        self.phone_number = phone_number
        self.raise_exception()

    def raise_exception(self):
        self._logging_handler.logger.error(f"{self._e}. Occurred when sending SMS to {self.phone_number}")
        self._logging_handler.iterate_status_counter('failure')
        raise Exception(self._e)


