from MockFramework.MockCamera import *
from MockFramework.MockMotorBoard import *

class MockRobot:
    def __init__(self, motor_board = MockMotorBoardPrinter(), camera = MockCameraJSONReader("data1.json")):
        self.motor_board = motor_board
        self.camera = camera
        self.zone = 0

