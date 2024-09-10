import gammu

class StateMachineStarter(gammu.StateMachine):
    def __init__(self):
        gammu.StateMachine.__init__(self)
        self.ReadConfig()
        self.Init()