import gammu

from src.core import StateMachineStarter
from src.errors import StateMachineErrorDeviceNotExist, StateMachineError


class StateMachineHandler(StateMachineStarter):
    def __init__(self, tries: int=0):
        try:
            super().__init__()
        except gammu.ERR_DEVICENOTEXIST as e:
            StateMachineErrorDeviceNotExist((e.args[0])['Text'], tries)
            self.__init__(tries+1)
        except gammu.ERR_DEVICEOPENERROR as e:
            StateMachineError((e.args[0])['Text'])
        except gammu.GSMError as e:
            StateMachineError((e.args[0])['Text'])



