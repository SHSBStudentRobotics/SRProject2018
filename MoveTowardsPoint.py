from WillCollide import *
from math import *
from action import *

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

def moveToMarker(marker,objects):
    #Marker must not be in the objects list.
    return moveToPoint(marker.polar.rot_y_degrees , marker.distance_metres , objects)

def moveToPoint(angle, distance, objects):
    #Distance in metres , angle in degrees.

    #How far the robot aims to stay away from the object.
    TARGET_SEPERATION = 0.5

    #List of objects that are in the way, sorted by distance.
    collisionObjects = sorted(list(filter(lambda x: WillCollide(x,angle,distance), objects)), key = lambda x: x.distance_metres)
    

    if len(collisionObjects) == 0:
        return Action("move", angle, distance)

    #Currently only considers the closest object.
    #Calculates the angle to maintain a 0.5m seperation
    requiredAngle = math.degrees(math.atan(TARGET_SEPERATION / collisionObjects[0].distance_metres))
    movementAngle = 0


    #If the object in question is on the left.
    if collisionObjects[0].polar.rot_y_deg < 0:
        movementAngle = collisionObjects[0].polar.rot_y_deg + requiredAngle
    else:
        movementAngle = collisionObjects[0].polar.rot_y_deg - requiredAngle

    #Will turn on spot if distance less than 1.5 metres
    if collisionObjects[0].distance_metres < 1.5:
        return Action("turn", movementAngle)

    else:
        return Action("move",movementAngle , distance)
    


    





def Turn(AngleToTurn):
    print("DUMMY FUNCTION, USED AS PLACEHOLDER, NEED TO TURN ROBOT TO FACE DIRECTION")
    raise NotImplementedError

def Move(DistanceToMove):
    print("DUMMY FUNCTION, USED AS PLACEHOLDER, NEED TO MOVE ROBOT FORWARD")
    raise NotImplementedError