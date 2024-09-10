from flask import request
from flask_restful import Resource

from src.services import StateMachineHandler, SMSHandlerSend
from src.utils import LoggingJSONHandler


class SMSGatewayController(Resource):
    def __init__(self):
        self.__logging_handler = LoggingJSONHandler()

    def post(self):
        args = request.json
        phone_number = args['phone_number']
        message = args['message']

        try:
            state_machine_handler = StateMachineHandler()
            SMSHandlerSend(phone_number, message, state_machine_handler)
            return {'result': 'success'}, 200
        except Exception as e:
            if str(e) == "Unknown error.":
                return {"error": f"{e}"}, 504
            elif str(e) == "Error opening device. Unknown, busy or no permissions":
                return {"error": f"{e}"}, 503
            else:
                return {"error": f"{e}"}, 500
