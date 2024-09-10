import gammu

from src.core import StateMachineStarter
from src.errors import *


class StateMachineHandler(StateMachineStarter):
    def __init__(self):
        try:
            super().__init__()
        except gammu.ERR_DEVICENOTEXIST as e:
            StateMachineErrorDeviceNotExist((e.args[0])['Text'])
        except gammu.ERR_DEVICEOPENERROR as e:
            StateMachineError((e.args[0])['Text'])
        except gammu.GSMError as e:
            StateMachineError((e.args[0])['Text'])



