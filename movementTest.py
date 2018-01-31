from robot import *
from PowerMotor import *
import time

robot = Robot()

while True:
    for x in range(10):
        powerMotor(robot, 0, 1)
        powerMotor(robot, 1, 1)

        time.sleep(0.5)

    for x in range(10):
        powerMotor(robot, 0, -1)
        powerMotor(robot, 1, -1)

        time.sleep(0.5)