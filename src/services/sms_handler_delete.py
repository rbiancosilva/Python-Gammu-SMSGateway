from src.core import SMSStarter


class SMSHandlerDelete(SMSStarter):
    def __init__(self, state_machine_handler):
        super().__init__(state_machine_handler)
        self.delete_all_sms()

    def delete_all_sms(self):
        for sms_index in range(self._state_machine_handler.GetSMSStatus()['SIMUsed'], 0, -1):
            self._state_machine_handler.DeleteSMS(Folder=1, Location=sms_index)