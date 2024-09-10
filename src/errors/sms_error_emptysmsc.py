from .sms_error import SMSError


class SMSErrorEmptySMSC(SMSError):
    def __init__(self, gammu_exception, phone_number: str):
        super().__init__(gammu_exception, phone_number)

    def raise_exception(self):
        self._logging_handler.logger.error(f"{self._e}. E3531 Disconnected while sending SMS to {self.phone_number}.")
        self._logging_handler.iterate_status_counter('failure')
        raise Exception(self._e)

