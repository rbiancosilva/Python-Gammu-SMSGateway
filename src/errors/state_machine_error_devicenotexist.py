import os

from .gammu_error import GammuError

class StateMachineErrorDeviceNotExist(GammuError):
    def __init__(self, gammu_exception, tries: int):
        super().__init__(gammu_exception)
        self._tries = tries
        if self._tries < 3:
            self.retry_state_machine_handler()
        else:
            self.raise_exception()

    def raise_exception(self):
        self._logging_handler.logger.error(f"{self._e}.")
        self._logging_handler.iterate_status_counter('failure')
        raise Exception(self._e)

    def retry_state_machine_handler(self):
        self._logging_handler.logger.warning(f"{self._e}. Rebooting E3531.")
        os.system("sh /usr/local/bin/usb_modeswitch_reset.sh")
        self._logging_handler.logger.info(f"Rebooted E3531.")
        return 1