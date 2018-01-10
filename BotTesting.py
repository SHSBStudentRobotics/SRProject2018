from VirtualRobot import *
from PowerMotor import *
import time

r = VirtualRobot()

PowerMotor(r, 0, 1) #SHOULD GIVE M0, 0.5
r.OutputValues()

PowerMotor(r, 1, -0.3) # SHOULD GIVE M1, -0.3
r.OutputValues()

PowerMotor(r, 0, -1) #SHOULD GIVE M0, 0
r.OutputValues()

while MotorList[0] < 1:
    PowerMotor(r, 0, 1)
    r.OutputValues()
    time.sleep(0.5)

while MotorList[0] > -1:
    PowerMotor(r, 0, -1)
    r.OutputValues()
    time.sleep(0.5)
