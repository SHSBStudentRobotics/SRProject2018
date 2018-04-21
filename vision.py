import math, time
from hardware import *

#Internally , all angles are in degrees and all are distances in meters

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
            Point(1, 0),
            Point(2, 0),
            Point(3, 0),
            Point(4, 0),
            Point(5, 0),
            Point(6, 0),
            Point(7, 0),
            Point(8, 1),
            Point(8, 2),
            Point(8, 3),
            Point(8, 4),
            Point(8, 5),
            Point(8, 6),
            Point(8, 7),
            Point(7, 8),
            Point(6, 8),
            Point(5, 8),
            Point(4, 8),
            Point(3, 8),
            Point(2, 8),
            Point(1, 8),
            Point(0, 7),
            Point(0, 6),
            Point(0, 5),
            Point(0, 4),
            Point(0, 3),
            Point(0, 2),
            Point(0, 1)
        ]
        #Base is the starting area, scoring is the center of scoring zone.
        if getZone(self.robot) == 0:
            self.base = Point(0,0)
            self.scoringZone = Point(1.50,1.50)
        elif getZone(self.robot) == 1:
            self.base = Point(8.00,0)
            self.scoringZone = Point(6.50,1.50)
        elif getZone(self.robot)== 2:
            self.base = Point(8.00,8.00)
            self.scoringZone = Point(6.50,6.50)
        elif getZone(self.robot) == 3:
            self.base = Point(0,8.00)
            self.scoringZone = Point(1.50,6.50)
        self.robotPos = Point(self.base.x,self.base.y)
        self.robotAngle = 0

    #Returns 1 for success , 0 for failure.
    def triangulate(self, markers):
        if len(markers) < 2:
            print("Failed to Triangulate due to lack of points")
            return 0

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
            return 0
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
            return 0

        if x >= 0 and x <= 8 and y >= 0 and y <= 8: #If First solution in bounds
            if otherx >= 0 and otherx <= 8 and othery >= 0 and othery <= 8: #If second solution in bounds
                dist1 = math.sqrt((x-self.robotPos.x)**2 + (y-self.robotPos.y)**2)
                dist2 = math.sqrt((otherx-self.robotPos.x)**2 + (othery-self.robotPos.y)**2)
                if dist2 < dist1: #Pick solution closest to last coordinate
                    x = otherx
                    y = othery
        else:
            if otherx >= 0 and otherx <= 8 and othery >= 0 and othery <= 8: #If only second solution in bounds
                x = otherx
                y = othery
            else: #No solutions
                print("Triangulation failed , both solutions out of bounds")
                return 0

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
        return 1

    def angleToPoint(self, point):
        return angleBetweenPoints(self.robotPos, point)
    
    def distanceToPoint(self, point):
        return distanceBetweenPoints(point, self.robotPos )

    def isInScoringZone(self):
        return self.isPointInScoringZone(self.robotPos, 0.50)

    def isPointInScoringZone(self, point, border = 0.50):
        #Border is How far the point must be into the scoring zone
        
        #Calculates the edges of the box that the robot must be in
        lowerX = [1, 4.815, 4.815, 1][getZone(self.robot)] + border
        upperX = lowerX + 2.185 - border * 2
        lowerY = [1,1,4.815,4.815][getZone(self.robot)] + border
        upperY = lowerY + 2.185 - border * 2

        return point.x > lowerX and point.x < upperX and point.y > lowerY and point.y < upperY

    def angleToScoringZone(self):
        return self.angleToPoint(self.scoringZone)

    def distanceToScoringZone(self):
        return self.distanceToPoint(self.scoringZone)     

    def markerToPoint(self, marker):
        x = self.robotPos.x + marker.spherical.distance_metres * math.sin(math.radians(self.robotAngle) + marker.spherical.rot_y_radians)
        y = self.robotPos.y - marker.spherical.distance_metres * math.cos(math.radians(self.robotAngle) + marker.spherical.rot_y_radians)

        return Point(x, y)

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