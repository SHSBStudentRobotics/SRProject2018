import decision, hardware, time, config, logger
from robot import *

robot = Robot()
startTime = time.time()
decider = decision.Decider(robot, startTime)
configData = config.getConfigSettings()
#logger.setupLoggers(configData)

print("Mode is: " + str(robot.mode))

for x in range(20):
    hardware.setBothMotors(robot, configData, 0.4, 0.4)
    time.sleep(0.25)

hardware.setBothMotors(robot, configData, 0, 0)

while time.time() - startTime < 150:
    action = decider.decide()
    hardware.move(robot, action, len(decider.cubes), configData)
