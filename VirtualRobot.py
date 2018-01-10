global BRAKE
BRAKE = 0

global COAST
COAST = "coast"

class MotorBoard:
    m0 = 0
    m1 = 0

class VirtualRobot:
    motor_board = MotorBoard()

    def OutputValues(self):
        print("MOTOR M0")
        print(self.motor_board.m0)

        print("MOTOR M1")
        print(self.motor_board.m1)
