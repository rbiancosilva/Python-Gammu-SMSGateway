from .logging_starter import LoggingStarter
import json

class LoggingJSONHandler(LoggingStarter):
    def __init__(self):
        super().__init__()

    def iterate_status_counter(self, status:str):
        with open('/home/gammu-python-V1/logs-teste-v2/json-files/success-failure-teste-v5.json', 'r+') as file:
            log = json.load(file)

            log[status] += 1

            file.seek(0)
            json.dump(log, file, indent=4)
            file.truncate()

            self.logger.info(f"Success: {log['success']} Failure: {log['failure']}")


