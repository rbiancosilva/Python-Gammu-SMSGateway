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
            except gammu.ERR_DEVICENOTEXIST as e:
                print(f"Not able to start StateMachine. Error: {(e.args[0])['Text']}. Rebooting E3531...")
                log.logger.error(f"{(e.args[0])['Text']}. Rebooting E3531...")
                os.system("sh /usr/local/bin/usb_modeswitch_reset.sh")
                time.sleep(5)
                log.logger.info("E3531 Rebooted.")
                tries += 1
                return StateMachineHandler.start_state_machine(log, tries)
            except gammu.ERR_DEVICEOPENERROR as e:
                print(f"Unable to start StateMachine. Error: {(e.args[0])['Text']}")
                log.logger.error(f"{(e.args[0])['Text']}. Retrying...")
                tries += 1
                return StateMachineHandler.start_state_machine(log, tries)
            except gammu.GSMError as e:
                print(f"Unknown error. Error: {(e.args[0])['Text']}")
                log.logger.error(f"{(e.args[0])['Text']}. Retrying...")
                tries += 1
                return StateMachineHandler.start_state_machine(log, tries)

        raise Exception("Not able to start StateMachine.")

    def send_sms(self, phone_number: str, message: str, log: LoggingHelper):

        sms_info = {
            'Text': message,
            'SMSC': {'Location': 1},
            'Number': phone_number,
        }

        try:
            log.logger.info(f"Sending SMS to {phone_number}")
            self.delete_all_sms(self.GetSMSStatus()['SIMUsed'])
            self.SendSMS(sms_info)
            self.sms_sent_status()
            log.logger.info(f"SMS sent to {phone_number}.")
            log.status_logger('success')
        except gammu.ERR_EMPTYSMSC as e:
            print(f"E3531 disconnected while sending SMS to {phone_number}. Error: {(e.args[0])['Text']}")
            log.logger.error(f"{(e.args[0])['Text']}. E3531 Disconnected.")
            log.status_logger('failure')
            raise Exception(f"{e.args[0]['Text']}")
        except gammu.GSMError as e:
            print(f"Unable to send the SMS to {phone_number}. Error: {(e.args[0])['Text']}")
            log.logger.error(f"{(e.args[0])['Text']}")
            log.status_logger('failure')
            raise Exception(f"{e.args[0]['Text']}")
        except Exception as e:
            print(f"Unable to send the SMS to {phone_number}. Error: {e}")
            log.logger.error(f"{e.args[0]['Text']}")
            log.status_logger('failure')
            raise Exception(f"{e.args[0]['Text']}")

    def sms_sent_status(self):

        message = []

        sms_list_size = self.GetSMSStatus()['SIMUsed']

        if sms_list_size >= 1:
            sms = self.GetNextSMS(Folder=1, Location=sms_list_size-1)
            message.extend(sms)
        else:
            return 1

        for sms_part in message:
            if int(sms_part['Number']) == 1:
                self.delete_all_sms(sms_list_size)
                raise Exception('SIM Card has not enough data to send SMS.')

        if sms_list_size != 0: self.delete_all_sms(sms_list_size)

    def delete_all_sms(self, list_size: int):

        for sms_index in range(list_size, 0, -1):
            self.DeleteSMS(Folder=1, Location=sms_index)