import math, logging
from action import *


logger = logging.getLogger(__name__)

def getUltrasoundAction(ultrasoundSensorDistance, config):
    logger.info("Ultrasound distance : " + str(ultrasoundSensorDistance))
    if ultrasoundSensorDistance <= float(config["Hardware"]["UltrasoundBuffer"]):
        logger.info("Ultrasound reads object within 1 metre")
        return Action("reverseTurn", 180, 1)
    else: return Action("none", 0, 0)

def willCollide(Object, PathAngle, PathDistance):
    #Object is object taken from sourcebots API
    #PathAngle is the absolute angle between where the
    #robot is facing and where the robot wants to be in degrees
    #PathDistance is the distance we wish to travel along that line (metres)

    logger.debug("Testing for collision between object {0} at a path with angle {1} and distance {2}.".format(Object.id, PathAngle, PathDistance))

    OBJECTBUFFER = 0.25 #Buffer around object to account for errors (metres)
    SELFWIDTH = 0.50 #Width of self, perpendicular to direction of travel (metres)
                     #Edge to edge

    PathAngle = math.radians(PathAngle)
    
    hyp = Object.distance_metres #Hypotenuse
    theta = math.fabs(Object.polar.rot_y_rad - PathAngle) #Angle between self and path in radians

    adj = hyp * math.cos(theta)

    logger.debug("hyp: {0} theta: {1} adj: {2}".format(hyp, theta, adj))

    if adj > (PathDistance + OBJECTBUFFER): 
        logger.debug("Path Distance too short, no collision.")
        return False
    
    opp = hyp * math.sin(theta)
    logger.debug("opp: " + str(opp))
    if (opp - (OBJECTBUFFER + (SELFWIDTH / 2))) > 0:
        logger.debug("opp too large, no collision.")
        return False

    logger.debug("Collision with object " + str(Object.id))
    return True

def moveToMarker(robot, config, marker,objects):
    #Marker must not be in the objects list.
    return moveToPoint(robot, config, marker.spherical.rot_y_degrees, marker.distance_metres , objects)

def moveToPoint(robot, config, angle, distance, objects):
    #Distance in metres , angle in degrees.

    logger.info("Checking for collision on path of distance {0} and and angle {1}".format(distance,angle))

    if len(objects) == 0:
        return Action("move", angle, distance)

    #How far the robot aims to stay away from the object.
    TARGET_SEPERATION = 0.5

    #List of objects that are in the way, sorted by distance.
    collisionObjects = sorted(list(filter(lambda x: willCollide(x,angle,distance), objects)), key = lambda x: x.distance_metres)
    
    #Distance to nearest object via ultrasound
    ultrasoundAction = getUltrasoundAction(robot.servo_board.read_ultrasound(6, 7), config)
    if (ultrasoundAction.type != "none") and abs(): return ultrasoundAction
        

    if len(collisionObjects) == 0:
        logger.info("No collision")
        return Action("move", angle, distance)

    #Currently only considers the closest object.
    #Calculates the angle to maintain a 0.5m seperation
    requiredAngle = math.degrees(math.atan(TARGET_SEPERATION / collisionObjects[0].distance_metres))
    movementAngle = 0

    logger.debug("Required angle to avoid collision: " + str(requiredAngle))


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

