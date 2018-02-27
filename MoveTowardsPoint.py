from WillCollide import *
from math import *

def MoveTowardsPoint(Robot, DistanceForward, DistanceRight):

    #Robot is Sourcebots / Mock Robot instance
    #DistanceForward is distance in metres parallel to the direction the robot's facing, forwards being positive
    #DistanceRight is distance in metres perpendicular to the direction the robot's facing, right being positive

    DISTANCETOMOVEBETWEENATTEMPTS = 0.5

    Objects = Robot.camera.see()

    PathAngleDeg = degrees(atan(DistanceRight/DistanceForward))
    PathDistance = sqrt(DistanceForward^2 + DistanceRight^2)

    Turn(PathAngleDeg)

    WillThereBeCollision = False

    for i in Objects:
        if WillCollide(i, 0, PathDistance):
            WillThereBeCollision = True

    if not WillThereBeCollision:
        Move(PathDistance)

    else:
        Turn(90)
        Move(DISTANCETOMOVEBETWEENATTEMPTS)

def Turn(AngleToTurn):
    print("DUMMY FUNCTION, USED AS PLACEHOLDER, NEED TO TURN ROBOT TO FACE DIRECTION")
    raise NotImplementedError

def Move(DistanceToMove):
    print("DUMMY FUNCTION, USED AS PLACEHOLDER, NEED TO MOVE ROBOT FORWARD")
    raise NotImplementedError