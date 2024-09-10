from .gammu_error import GammuError

class SMSErrorGSMError(GammuError):
    def __init__(self, gammu_exception, phone_number):
        super().__init__(gammu_exception)
        self.phone_number = phone_number
        self.raise_exception()

    def raise_exception(self):
        print(f"Unable to send the SMS to {self.phone_number}. Error: {self._e}")
        self._logging_handler.logger.error(f"{self._e}")
        self._logging_handler.iterate_status_counter('failure')
        raise Exception(self._e)


