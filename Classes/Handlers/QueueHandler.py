import queue

from Classes.Handlers.StateMachineHandler import StateMachineHandler
from Classes.Helpers.LoggingHelper import LoggingHelper


class QueueHandler:
    def __init__(self):
        self.queue = queue.Queue()

    def enqueue(self, phone_number: str, message: str):
        self.queue.put((phone_number, message))

    def dequeue(self):
        while not self.queue.empty():
            phone_number, message = self.queue.get()
            log = LoggingHelper()
            try:
                sm = StateMachineHandler.start_state_machine(log)
                sm.send_sms(phone_number, message, log)
            except Exception as e:
                raise Exception(f'{e}')