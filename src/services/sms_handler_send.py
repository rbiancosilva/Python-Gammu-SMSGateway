import gammu

from src.core import SMSStarter
from src.errors.sms_error_emptysmsc import SMSErrorEmptySMSC
from src.errors.sms_error_gsmerror import SMSErrorGSMError
from .sms_handler_delete import SMSHandlerDelete



class SMSHandlerSend(SMSStarter):
    def __init__(self, phone_number: str, message: str, _state_machine_handler):
        super().__init__(_state_machine_handler)
        self.__phone_number = phone_number
        self.__message = message
        self.__send_sms()

    def __send_sms(self):
        sms_info = {
            'Text': self.__message,
            'SMSC': {'Location': 1},
            'Number': self.__phone_number,
        }

        try:
            self._logging_handler.logger.info(f"Sending SMS to {self.__phone_number}")
            if self._state_machine_handler.GetSMSStatus()['SIMUsed'] > 0 : SMSHandlerDelete(self._state_machine_handler)
            self._state_machine_handler.SendSMS(sms_info)
            self.__send_sms_status()
            self._logging_handler.logger.info(f"SMS is sent to {self.__phone_number}")
            self._logging_handler.iterate_status_counter('success')
        except gammu.ERR_EMPTYSMSC as e:
            SMSErrorEmptySMSC((e.args[0])['Text'], self.__phone_number)
        except gammu.GSMError as e:
            SMSErrorGSMError((e.args[0])['Text'], self.__phone_number)

    def __send_sms_status(self):
        message = []

        sms_list_size = self._state_machine_handler.GetSMSStatus()['SIMUsed']

        if sms_list_size >= 1:
            sms = self._state_machine_handler.GetNextSMS(Folder=1, Location=sms_list_size - 1)
            message.extend(sms)
        else:
            return 1

        for sms_part in message:
            if str(sms_part['Number']) == "1":
                SMSHandlerDelete(self._state_machine_handler)
                raise Exception("It's not possible to send the SMS. Telephone operator issues.")


