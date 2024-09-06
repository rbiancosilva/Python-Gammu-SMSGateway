from flask import Flask
from flask_restful import Api

class APISetup:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    def set_controller(self, controller):
         return self.api.add_resource(controller, '/')

    def init_app(self):
        self.app.run(port=5000, host='0.0.0.0')
