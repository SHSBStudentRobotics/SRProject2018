from robot import *
from hardware import *
import time

robot = Robot()

config = {}
config["Hardware"] = {"CurrentProtectionMaxChange" : "0.5"}

while True:
    for x in range(50):
        powerMotor(robot, 0, 1, config)
        powerMotor(robot, 1, 1, config)

        time.sleep(0.5)

    for x in range(10):
        powerMotor(robot, 0, -1, config)
        powerMotor(robot, 1, -1, config)

        time.sleep(0.5)
