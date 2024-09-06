from Classes.Setups.APISetup import APISetup
from SMSGatewayController import SMSGatewayController

api = APISetup()
api.set_controller(SMSGatewayController)

if __name__ == '__main__':
    api.init_app()

