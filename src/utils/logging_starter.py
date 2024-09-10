import logging

class LoggingStarter:
    def __init__(self):
        logging.basicConfig(
            filename='/home/gammu-python-V1/logs-teste-v2/log-files/gammu-python-1009-v1.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(pathname)s - %(levelname)s - %(message)s'
        )

        self.logger = logging.getLogger()