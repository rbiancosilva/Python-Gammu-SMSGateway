from flask import request
from flask_restful import Resource

from Classes.Helpers.LoggingHelper import LoggingHelper
from Classes.Handlers.StateMachineHandler import StateMachineHandler

class SMSGatewayController(Resource):
    @staticmethod
    def post():
        args = request.json
        phone_number = args['phone_number']
        message = args['message']

        log = LoggingHelper()

        try:
            sm = StateMachineHandler.start_state_machine(log)
            sm.send_sms(phone_number, message, log)
            return {'result': 'success'}, 200
        except Exception as e:
            if str(e) == "Unknown error.":
                log.logger.error(f"{e}")
                log.status_logger('failure')
                return {"error": f"{e}"}, 504
            elif str(e) == "Error opening device. Unknown, busy or no permissions":
                log.logger.error(f"{e}")
                log.status_logger('failure')
                return {"error": f"{e}"}, 503
            else:
                log.logger.error(f"{e}")
                log.status_logger('failure')
                return {"error": f"{e}"}, 500




