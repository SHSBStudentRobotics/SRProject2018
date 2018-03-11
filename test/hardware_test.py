from MockFramework import *
from hardware import *
import time, unittest

class TestHardware(unittest.TestCase):
    def test_PowerMotor(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)

        config = {"Hardware" : {
            "CurrentProtectionMaxChange" : 0.5}}

        powerMotor(r, 0, 1, config)
        self.assertEqual(r.motor_board.m0, 0.5)

        powerMotor(r, 1, -0.3, config)
        self.assertEqual(r.motor_board.m1, -0.3)

        powerMotor(r, 0, -1, config)
        self.assertEqual(r.motor_board.m0, 0)

    def test_move(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)

        config = {"Movement" : {
            "SpeedIncreasePerCube" : "0",
            "BaseSpeed" : "0.6",
            "MaxDistForFullPower": "1",
            "ProportionalConstant" : "0.1",
            "IntegralConstant"  : "0.1",
            "DerivativeConstant" : "0.1"},
            "Hardware" : {
            "InvertLeftMotor" : "no",
            "InvertRightMotor": "no",
            "LeftMotorNumber" : "0",
            "RightMotorNumber" : "1",
            "CurrentProtectionMaxChange" : "50"}}

        move(r,Action("stop",0),0,config)
        self.assertEqual(r.motor_board.m0, 0)
        self.assertEqual(r.motor_board.m1, 0)

        move(r,Action("move",0,500),0,config)
        self.assertEqual(r.motor_board.m0, 0.6)
        self.assertEqual(r.motor_board.m1, 0.6)

        move(r,Action("turn",-150),0,config)
        self.assertLess(r.motor_board.m0, 0)
        self.assertGreater(r.motor_board.m1, 0)

    def test_setBothMotors(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)

        config = {"Hardware" : {
            "InvertLeftMotor" : "no",
            "InvertRightMotor": "no",
            "LeftMotorNumber" : "0",
            "RightMotorNumber" : "1",
            "CurrentProtectionMaxChange" : 50}}

        setBothMotors(r,config,1,1)
        self.assertEqual(r.motor_board.m0,1)
        self.assertEqual(r.motor_board.m1,1)

        config = {"Hardware" : {
            "InvertLeftMotor" : "yes",
            "InvertRightMotor": "yes",
            "LeftMotorNumber" : "0",
            "RightMotorNumber" : "1",
            "CurrentProtectionMaxChange" : 50}}

        setBothMotors(r,config,1,1)
        self.assertEqual(r.motor_board.m0,-1)
        self.assertEqual(r.motor_board.m1,-1)

        config = {"Hardware" : {
            "InvertLeftMotor" : "no",
            "InvertRightMotor": "no",
            "LeftMotorNumber" : "0",
            "RightMotorNumber" : "1",
            "CurrentProtectionMaxChange" : 50}}

        setBothMotors(r,config,-1,1)
        self.assertEqual(r.motor_board.m0,-1)
        self.assertEqual(r.motor_board.m1,1)

        config = {"Hardware" : {
            "InvertLeftMotor" : "no",
            "InvertRightMotor": "no",
            "LeftMotorNumber" : "1",
            "RightMotorNumber" : "0",
            "CurrentProtectionMaxChange" : 50}}

        setBothMotors(r,config,-1,1)
        self.assertEqual(r.motor_board.m0,1)
        self.assertEqual(r.motor_board.m1,-1)

    
