from MockFramework.MockCamera import *
from MockFramework.MockMotorBoard import *

global BRAKE
BRAKE = 0

global COAST
COAST = "coast"

class MockRobot:
    def __init__(self, motor_board = MockMotorBoardPrinter(), camera = MockCameraJSONReader("data1.json")):
        self.motor_board = motor_board
        self.camera = camera

