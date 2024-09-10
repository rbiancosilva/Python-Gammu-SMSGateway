import os

from .state_machine_error import StateMachineError


class StateMachineErrorDeviceNotExist(StateMachineError):
    def __init__(self, gammu_exception):
        super().__init__(gammu_exception)

    def raise_exception(self):
        self._logging_handler.logger.error(f"{self._e}. Rebooting E3531.")
        os.system("sh /usr/local/bin/usb_modeswitch_reset.sh")
        self._logging_handler.iterate_status_counter('failure')
        raise Exception(self._e)