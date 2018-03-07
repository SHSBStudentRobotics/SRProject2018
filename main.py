import decision, hardware, time
from robot import Robot

robot = Robot()
decider = decision.Decider()


startTime = time.time()

while time.time() - StartTime < 150:
    action = decider.decide(robot, startTime)
    hardware.move(robot, action, len(decider.cubes))
