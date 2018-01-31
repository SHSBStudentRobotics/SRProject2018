import math, time

#Internally , all angles are in degrees and all are distances in meters


#  Returns the orientation of a marker in degrees , where Turning a marker clockwise (as viewed from above)
#  increases the value of rot_y, while turning it anticlockwise decreases it. A value of 0 means that
#  the marker is perpendicular to the line of sight of the camera.
def getOrientation(marker):

    markerWidth = 0.25 if marker.id <= 43 else 0.1


    pixelCorners = [[0,0],[0,0]] #[0,0] is top left, [1,0] is top right, [0,1] is bottom left, [1,1] is bottom right
    pixelCorners[0][0] = list(filter(lambda x: x[0] < marker.pixel_centre[0] and x[1] > marker.pixel_centre[1], marker.pixel_corners))[0]
    pixelCorners[1][0] = list(filter(lambda x: x[0] > marker.pixel_centre[0] and x[1] > marker.pixel_centre[1], marker.pixel_corners))[0]
    pixelCorners[0][1] = list(filter(lambda x: x[0] < marker.pixel_centre[0] and x[1] < marker.pixel_centre[1], marker.pixel_corners))[0]
    pixelCorners[1][1] = list(filter(lambda x: x[0] > marker.pixel_centre[0] and x[1] < marker.pixel_centre[1], marker.pixel_corners))[0]

    #The average x camera coordinates of the corners of the marker. Allows use to approximate the marker as a line below.
    averageXLeft = (pixelCorners[0][0][0] + pixelCorners[0][1][0])/2
    averageXRight = (pixelCorners[1][0][0] + pixelCorners[1][1][0])/2

    cartZ = marker._raw_data["cartesian"][0]
    cartX = marker._raw_data["cartesian"][1]

    cartX = 0.01 if cartX == 0 else cartX

    #Calculates the focal length (in terms of whatever units are values are in)
    focalLength = cartZ * marker.pixel_centre[0] / cartX

    cosTheta = (1 / (markerWidth * focalLength)) * (averageXRight * (cartZ + markerWidth/2) - averageXLeft * (cartZ- markerWidth/2))

    return degrees(math.acos(cosTheta))

#Converts an angle from degrees to radians
def radians(angle):
    return angle * math.pi / 180

def debugPrintMarker(marker):
    print("Marker: " + str(marker.id))
    print("Distance: " + str(marker.polar.distance_metres))
    print("Rot X: " + str(marker.polar.rot_x_deg ))
    print("Rot Y: " + str(marker.polar.rot_y_deg ))
    #print("X: " + marker.cartesian.x())
    #print("Y: " + marker.cartesian.y())
    #print("Z: " + marker.cartesian.z())
    print()


#Converts an angle from radians to degrees
def degrees(angle):
    return angle * 180 / math.pi

#Some stuff from last year:

def getGlobalPos(marker):
    # This converts the marker into an entity with absolute x, y, and rotation from north
    ENTITY = markerToEntity(marker)
    # This is the angle from north that the robot is from the marker
    ANGLE = ENTITY.angle - getOrientation(marker)
    # This converts that angle from north into the robots position relative
    # to the marker and adds that to the markers position
    X = ENTITY.x + marker.polar.distance_metres*100 * math.sin(radians(ANGLE))
    print(math.sin(radians(ANGLE)))
    print(ANGLE)
    Y = ENTITY.y + marker.polar.distance_metres*100 * math.cos(radians(ANGLE))
    ROBOT_ANGLE = ANGLE-180
    print("ROBOT X : "+str(X))
    print("ROBOT Y : "+str(Y))
    return Entity(X, Y, ROBOT_ANGLE)

def getAngleFromNorth(x, y):
    POSY = float(math.fabs(y))
    POSX = float(math.fabs(x))
    if x > 0 and y > 0:
        ANGLE_ANTI_FROM_EAST = -degrees(math.atan(POSY / POSX))
    if x < 0 and y > 0:
        ANGLE_ANTI_FROM_EAST = degrees(math.atan(POSY / POSX))
    if x < 0 and y < 0:
        ANGLE_ANTI_FROM_EAST = 90 + degrees(math.atan(POSY / POSX))
    if x > 0 and y < 0:
        ANGLE_ANTI_FROM_EAST =  -90 - degrees(math.atan(POSY / POSX))
    
    return ANGLE_ANTI_FROM_EAST

class Entity:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle


class Mapping:
    def __init__(self, robot):
        self.robot = robot
        self.markerPos = [
            Point(100, 0),
            Point(200, 0),
            Point(300, 0),
            Point(400, 0),
            Point(500, 0),
            Point(600, 0),
            Point(700, 0),
            Point(800, 100),
            Point(800, 200),
            Point(800, 300),
            Point(800, 400),
            Point(800, 500),
            Point(800, 600),
            Point(800, 700),
            Point(700, 800),
            Point(600, 800),
            Point(500, 800),
            Point(400, 800),
            Point(300, 800),
            Point(200, 800),
            Point(100, 800),
            Point(0, 700),
            Point(0, 600),
            Point(0, 500),
            Point(0, 400),
            Point(0, 300),
            Point(0, 200),
            Point(0, 100)
        ]
        if self.robot.zone == 0:
            self.base = Point(0,0)
        elif self.robot.zone == 1:
            self.base = Point(800,0)
        elif self.robot.zone == 2:
            self.base = Point(800,800)
        elif self.robot.zone == 3:
            self.base = Point(0,800)
        self.robotPos = Point(self.base.x,self.base.y)
        self.robotAngle = 0


    def triangulate(self, markers):
        if len(markers) < 2:
            print("Failed to Triangulate due to lack of points")
            return

        x1 = self.markerPos[markers[0].id].x
        y1 = self.markerPos[markers[0].id].y
        d1 = markers[0].polar.distance_metres
        x2 = self.markerPos[markers[1].id].x
        y2 = self.markerPos[markers[1].id].y
        d2 = markers[1].polar.distance_metres

        if y1 == y2:
            y2 += 0.001
        try:
            a = -1*(x1-x2)/(y1-y2)
            b = ((d1**2-d2**2)-(x1**2-x2**2)-(y1**2-y2**2))/(-2*(y1-y2))
        except:
            print("Divide By 0 Error")
            return
        c = 1+a**2
        d = -2*x1 + 2*a*b - 2*a*y1
        e = x1**2 + b**2 - 2*b*y1 + y1**2 - d1**2
        try:
            x = (-1*d+math.sqrt(d**2-4*c*e))/(2*c)
            y = a*x+b
            otherx = (-1*d-math.sqrt(d**2-4*c*e))/(2*c)
            othery = a*otherx+b
        except:
            print("Triangulation failed , discrimant is negative")
            return

        if x >= 0 and x <= 800 and y >= 0 and y <= 800: #If First solution in bounds
            if otherx >= 0 and otherx <= 800 and othery >= 0 and othery <= 800: #If second solution in bounds
                dist1 = math.sqrt((x-self.robotPos.x)**2 + (y-self.robotPos.y)**2)
                dist2 = math.sqrt((otherx-self.robotPos.x)**2 + (othery-self.robotPos.y)**2)
                if dist2 < dist1: #Pick solution closest to last coordinate
                    x = otherx
                    y = othery
        else:
            if otherx >= 0 and otherx <= 800 and othery >= 0 and othery <= 800: #If only second solution in bounds
                x = otherx
                y = othery
            else: #No solutions
                print("Triangulation failed , both solutions out of bounds")
                return

        c = y
        a = math.sqrt((x-x1)**2 + y1**2)
        b = math.sqrt((x-x1)**2 +(y-y1)**2)
        if x1 > x:
            angle = degrees(math.acos((b**2+c**2-a**2)/(2*b*c))) - markers[0].polar.rot_y_deg
        else:
            angle = -degrees(math.acos((b**2+c**2-a**2)/(2*b*c))) - markers[0].polar.rot_y_deg + 360
        if angle > 360:
            angle -= 360

        self.robotAngle = angle
        self.robotPos.update(x, y)
        self.triangluationTime = time.time()

    def angleToPoint(self, point):
        return angleBetweenPoints(self.robotPos, point)
    
    def distanceToPoint(self, point):
        return distanceBetweenPoints(point, self.robotPos )

def angleBetweenPoints(point, point2):
    return getAngleFromNorth(point.x - point2.x, point.y - point2.y)

def distanceBetweenPoints(point , point2):
    return math.sqrt((point.x - point2.x)**2 + (point.y - point2.y)**2)

def clampAngle(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

class Point:
    def __init__(self, x = 0, y= 0):
        self.x = x
        self.y = y
    
    def update(self, x , y):
        self.x = x
        self.y = y