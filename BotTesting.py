from MockFramework import *
from PowerMotor import *
import time, unittest

"""
r = MockRobot()

while MotorList[0] < 1:
    PowerMotor(r, 0, 1)
    r.OutputValues()
    time.sleep(0.5)

while MotorList[0] > -1:
    PowerMotor(r, 0, -1)
    r.OutputValues()
    time.sleep(0.5)
"""

class TestHardware(unittest.TestCase):
    def test_PowerMotor(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)

        powerMotor(r, 0, 1)
        self.assertEqual(r.motor_board.m0, 0.5)

        powerMotor(r, 1, -0.3)
        self.assertEqual(r.motor_board.m1, -0.3)

        powerMotor(r, 0, -1)
        self.assertEqual(r.motor_board.m0, 0)

if __name__ == '__main__':
    unittest.main()
