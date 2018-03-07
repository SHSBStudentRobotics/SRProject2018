import math
from action import *

def willCollide(Object, PathAngle, PathDistance):
    #Object is object taken from sourcebots API
    #PathAngle is the absolute angle between where the
    #robot is facing and where the robot wants to be in degrees
    #PathDistance is the distance we wish to travel along that line (metres)

    OBJECTBUFFER = 0.25 #Buffer around object to account for errors (metres)
    SELFWIDTH = 0.50 #Width of self, perpendicular to direction of travel (metres)
                     #Edge to edge

    PathAngle = math.radians(PathAngle)
    
    hyp = Object.distance_metres #Hypotenuse
    theta = math.fabs(Object.polar.rot_y_rad - PathAngle) #Angle between self and path in radians

    adj = hyp * math.cos(theta)
    if adj > (PathDistance + OBJECTBUFFER): return False
    
    opp = hyp * math.sin(theta)
    if (opp - (OBJECTBUFFER + (SELFWIDTH / 2))) > 0:
        return False

    else: return True

def moveToMarker(marker,objects):
    #Marker must not be in the objects list.
    return moveToPoint(marker.spherical.rot_y_degrees, marker.distance_metres , objects)

def moveToPoint(angle, distance, objects):
    #Distance in metres , angle in degrees.

    if len(objects) == 0:
        return Action("move", angle, distance)

    #How far the robot aims to stay away from the object.
    TARGET_SEPERATION = 0.5

    #List of objects that are in the way, sorted by distance.
    collisionObjects = sorted(list(filter(lambda x: willCollide(x,angle,distance), objects)), key = lambda x: x.distance_metres)
    

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
    

    
