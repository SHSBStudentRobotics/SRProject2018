import math, time

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
        #Base is the starting area, scoring is the center of scoring zone.
        if self.robot.zone == 0:
            self.base = Point(0,0)
            self.scoringZone = Point(150,150)
        elif self.robot.zone == 1:
            self.base = Point(800,0)
            self.scoringZone = Point(650,150)
        elif self.robot.zone == 2:
            self.base = Point(800,800)
            self.scoringZone = Point(650,650)
        elif self.robot.zone == 3:
            self.base = Point(0,800)
            self.scoringZone = Point(150,650)
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
        return self.isPointInScoringZone(self.robotPos, 50)

    def isPointInScoringZone(self, point, border = 50):
        #Border is How far the point must be into the scoring zone
        
        #Calculates the edges of the box that the robot must be in
        lowerX = [100, 481.5, 481.5, 100][self.robot.zone] + border
        upperX = lowerX + 218.5 - border * 2
        lowerY = [100,100,481.5,481.5][self.robot.zone] + border
        upperY = lowerY + 218.5 - border * 2

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