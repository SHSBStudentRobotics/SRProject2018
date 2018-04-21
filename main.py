import decision, hardware, time, config, logger
from robot import *

robot = Robot()
startTime = time.time()
decider = decision.Decider(robot, startTime)
configData = config.getConfigSettings()
#logger.setupLoggers(configData)

while time.time() - startTime < 150:
    action = decider.decide()
    hardware.move(robot, action, len(decider.cubes), configData)
