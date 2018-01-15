from robot import *
import math

#Internally , all angles are in degrees and all are distances in meters


#  Returns the orientation of a marker in degrees , where Turning a marker clockwise (as viewed from above)
#  increases the value of rot_y, while turning it anticlockwise decreases it. A value of 0 means that
#  the marker is perpendicular to the line of sight of the camera.
def getOrientation(marker):

    print(type(marker.pixel_corners[0]))

    markerWidth = 0.25 if marker.id <= 43 else 0.1


    pixelCorners = [[0,0],[0,0]] #[0,0] is top left, [1,0] is top right, [0,1] is bottom left, [1,1] is bottom right
    pixelCorners[0][0] = list(filter(lambda x: x[0] < marker.pixel_centre[0] and x[1] > marker.pixel_centre[1], marker.pixel_corners))[0]
    pixelCorners[1][0] = list(filter(lambda x: x[0] > marker.pixel_centre[0] and x[1] > marker.pixel_centre[1], marker.pixel_corners))[0]
    pixelCorners[0][1] = list(filter(lambda x: x[0] < marker.pixel_centre[0] and x[1] < marker.pixel_centre[1], marker.pixel_corners))[0]
    pixelCorners[1][1] = list(filter(lambda x: x[0] > marker.pixel_centre[0] and x[1] < marker.pixel_centre[1], marker.pixel_corners))[0]

    #The average x camera coordinates of the corners of the marker. Allows use to approximate the marker as a line below.
    averageXLeft = (pixelCorners[0][0][0] + pixelCorners[0][1][0])/2
    averageXRight = (pixelCorners[1][0][0] + pixelCorners[1][1][0])/2

    cartZ = marker.polar.distance_meters * math.cos(marker.polar.rot_x_rad)

    #Calculates the focal length (in terms of whatever units are values are in)
    focalLength = marker.cartesian.z  * marker.pixel_centre.x / marker.polar.x


    cosTheta = (1 / (markerWidth * focalLength)) * (averageXRight * (marker.cartesian.z + markerWidth/2) - averageXLeft * (marker.cartesian.z - markerWidth/2))

    print(cosTheta)

    return degrees(math.acos(cosTheta))

#Converts an angle from degrees to radians
def radians(angle):
    return angle * math.pi / 180

def debugPrintMarker(marker):
    print("Marker: " + marker.id())
    print("Distance: " + marker.polar.distance_meters())
    print("Rot X: " + marker.polar.rot_x_deg ())
    print("Rot Y: " + marker.polar.rot_y_deg ())
    print("X: " + marker.cartesian.x())
    print("Y: " + marker.cartesian.y())
    print("Z: " + marker.cartesian.z())
    print()


#Converts an angle from radians to degrees
def degrees(angle):
    return angle * 180 / math.pi

#Some stuff from last year:

def getGlobalPos(marker):
    # This converts the marker into an entity with absolute x, y, and rotation from north
    ENTITY = markerToEntity(marker)
    # This is the angle from north that the robot is from the marker
    ANGLE = ENTITY.angle - marker.orientation.rot_y
    # This converts that angle from north into the robots position relative
    # to the marker and adds that to the markers position
    X = ENTITY.x + marker.centre.polar.length*100 * math.sin(radians(ANGLE))
    print(math.sin(radians(ANGLE)))
    print(ANGLE)
    Y = ENTITY.y + marker.centre.polar.length*100 * math.cos(radians(ANGLE))
    ROBOT_ANGLE = ANGLE-180
    print("ROBOT X : "+str(X))
    print("ROBOT Y : "+str(Y))
    return Entity(X, Y, ROBOT_ANGLE)

def getAngleFromNorth(x, y):
    print(x)
    print(y)
    POSY = float(math.fabs(y))
    POSX = float(math.fabs(x))
    if x > 0 and y > 0:
        print(0)
        ANGLE_ANTI_FROM_EAST = degrees(math.atan(POSY / POSX))
    if x < 0 and y > 0:
        print(1)
        ANGLE_ANTI_FROM_EAST = 90 + degrees(math.atan(POSY / POSX))
    if x < 0 and y < 0:
        print(2)
        ANGLE_ANTI_FROM_EAST = 180 + degrees(math.atan(POSY / POSX))
    if x > 0 and y < 0:
        print(3)
        ANGLE_ANTI_FROM_EAST = 270 + degrees(math.atan(POSY / POSX))
    
    print(ANGLE_ANTI_FROM_EAST)
    print(-ANGLE_ANTI_FROM_EAST - 270)
    return -ANGLE_ANTI_FROM_EAST - 270

def getRobotEntity(markers):
    POSITIONS = map(getGlobalPos, markers)
    # The mean of all of the x, y and angles
    X = sum(map(lambda x: x.x, POSITIONS))/len(POSITIONS)
    Y = sum(map(lambda x: x.y, POSITIONS))/len(POSITIONS)
    ANGLE = sum(map(lambda x: x.angle, POSITIONS))/len(POSITIONS)
    return Entity(X, Y, ANGLE)

def markerToEntity(marker):
    ARENA_ENTITIES = [
        Entity(0, 100, 90),
        Entity(0, 200, 90),
        Entity(0, 300, 90),
        Entity(0, 400, 90),
        Entity(0, 500, 90),
        Entity(0, 600, 90),
        Entity(0, 700, 90),
        Entity(100, 800, 180),
        Entity(200, 800, 180),
        Entity(300, 800, 180),
        Entity(400, 800, 180),
        Entity(500, 800, 180),
        Entity(600, 800, 180),
        Entity(700, 800, 180),
        Entity(800, 700, 270),
        Entity(800, 600, 270),
        Entity(800, 500, 270),
        Entity(800, 400, 270),
        Entity(800, 300, 270),
        Entity(800, 200, 270),
        Entity(800, 100, 270),
        Entity(700, 0, 0),
        Entity(600, 0, 0),
        Entity(500, 0, 0),
        Entity(400, 0, 0),
        Entity(300, 0, 0),
        Entity(200, 0, 0),
        Entity(100, 0, 0),
    ]
    # Return the entity that corresponds to which arena marker it is
    return ARENA_ENTITIES[marker.info.code]

class Entity:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle


