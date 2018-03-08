from MockFramework import *
from hardware import *
import time, unittest

class TestHardware(unittest.TestCase):
    def test_PowerMotor(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)

        powerMotor(r, 0, 1)
        self.assertEqual(r.motor_board.m0, 0.5)

        powerMotor(r, 1, -0.3)
        self.assertEqual(r.motor_board.m1, -0.3)

        powerMotor(r, 0, -1)
        self.assertEqual(r.motor_board.m0, 0)