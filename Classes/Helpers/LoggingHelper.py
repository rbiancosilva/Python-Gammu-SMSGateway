import json
import logging

class LoggingHelper:
    def __init__(self):
        logging.basicConfig(
            filename='/home/gammu-python-V1/logs-teste-v2/log-files/gammu-python-0409-v1.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(pathname)s - %(levelname)s - %(message)s'
        )

        self.logger = logging.getLogger()

    def status_logger(self, status: str):
        with open('/home/gammu-python-V1/logs-teste-v2/json-files/success-failure-teste-v4.json', 'r+') as file:
            log = json.load(file)

            log[status] += 1

            file.seek(0)
            json.dump(log, file, indent=4)
            file.truncate()

            self.logger.info(f"SUCCESS: {log['success']} FAILED: {log['failure']}")