import gammu

import os
import time

from Classes.Helpers.LoggingHelper import LoggingHelper

class StateMachineHandler(gammu.StateMachine):
    def __init__(self):
        gammu.StateMachine.__init__(self)
        self.ReadConfig()
        self.Init()

    @staticmethod
    def start_state_machine(log: LoggingHelper, tries: int=0):

        while tries < 3:
            try:
                return StateMachineHandler()
            except gammu.ERR_DEVICENOTEXIST as err:
                print(f"Not able to start StateMachine. Error: {(err.args[0])['Text']}. Rebooting E3531...")
                log.logger.error(f"{(err.args[0])['Text']}. Rebooting E3531...")
                os.system("sh /usr/local/bin/usb_modeswitch_reset.sh")
                log.logger.info("E3531 Rebooted.")
                tries += 1
                return StateMachineHandler.start_state_machine(log, tries)
            except gammu.ERR_DEVICEOPENERROR as err:
                print(f"Unable to start StateMachine. Error: {(err.args[0])['Text']}")
                log.logger.error(f"{(err.args[0])['Text']}. Retrying...")
                tries += 1
                time.sleep(3)
                return StateMachineHandler.start_state_machine(log, tries)

        log.logger.error("Not able to start StateMachine.")
        log.status_logger('failure')
        raise Exception("Not able to start StateMachine.")

    def send_sms(self, phone_number: str, message: str, log: LoggingHelper):

        sms_info = {
            'Text': message,
            'SMSC': {'Location': 1},
            'Number': phone_number,
        }

        try:
            log.logger.info(f"Sending SMS to {phone_number}")
            self.SendSMS(sms_info)
            self.sms_sent_status()
            log.logger.info(f"SMS sent to {phone_number}.")
            log.status_logger('success')
        except gammu.ERR_EMPTYSMSC as err:
            print(f"E3531 disconnected while sending SMS to {phone_number}. Error: {(err.args[0])['Text']}")
            log.logger.error(f"{(err.args[0])['Text']}. E3531 Disconnected.")
            log.status_logger('failure')
            raise Exception(f"{err.args[0]['Text']}")
        except gammu.GSMError as err:
            print(f"Unable to send the SMS to {phone_number}. Error: {(err.args[0])['Text']}")
            log.logger.error(f"{(err.args[0])['Text']}")
            log.status_logger('failure')
            raise Exception(f"{err.args[0]['Text']}")
        except Exception as err:
            print(f"Unable to send the SMS to {phone_number}. Error: {err}")
            log.logger.error(f"{err}")
            log.status_logger('failure')
            raise Exception(f"{err}")

    def sms_sent_status(self):

        def delete_all_sms(list_size:int):

            for sms_index in range(list_size, 0, -1):
                self.DeleteSMS(Folder=1, Location=sms_index)

        message = []

        sms_list_size = (self.GetSMSStatus()['SIMUsed'])

        if sms_list_size >= 1:
            sms = self.GetNextSMS(Folder=1, Location=sms_list_size-1)
            message.extend(sms)
        else:
            print('Folder is empty')
            return 1

        for sms_part in message:
            if sms_part['Number'] == "1":
                delete_all_sms(sms_list_size)
                raise Exception('SIM Card has not enough data to send SMS.')

        if sms_list_size != 0: delete_all_sms(sms_list_size)

