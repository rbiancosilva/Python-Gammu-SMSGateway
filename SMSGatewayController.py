from flask import request
from flask_restful import Resource

from Classes.Handlers.QueueHandler import QueueHandler

class SMSGatewayController(Resource):
    @staticmethod
    def post():
        args = request.json
        phone_number = args['phone_number']
        message = args['message']

        sms_queue = QueueHandler()
        sms_queue.enqueue(phone_number, message)

        try:
            sms_queue.dequeue()
            return {'result': 'success'}, 200
        except Exception as e:
            return {'error': f'{e}'}, 500




