from action import *
import time
from vision import *

#A list of all token id's belonging to robot 0 , 1 ,2 and 3.
TOKEN_LIST_BY_TEAM = [set(range(44, 49)), set(range(49, 54)), set(range(54, 59)), set(range(59, 64))]

#Mode "ENUM"
SEARCHING = 0
COLLECTING = 1 # Id of cube being collected will be stored somewhere
RETURNING = 2

MAX_CAPACITY = 2 #The amount of cubes the robot is carrying.

MAX_FAILED_ITERATIONS =  5 #The maximun number of failed iterations before some corrective maneuver is taken to try to restore vision.

class Decider:
    def __init__(self, robot, startTime):
        self.robot = robot
        self.mode = SEARCHING
        self.cubes = [] # A list of cubes (ID's) that the robot believes it has picked up and is carrying.
        self.map = Mapping(robot)
        self.startTime = startTime
        self.numberOfFailedIterations = 0 #This is a counter that iterates upwards each time an operation fail's due to insufficient camera data.
                                            #If this occurs multiple times in a row ,some solution can be found.

        #Used in the search/pickup logic when the cube leaves the camera vision.
        self.targetDistance = 99999
        self.targetCube = 999

    #returns main action class to be executed by hardware.
    def decide(self):
        markers = self.robot.camera.see()

        #The markers we can pick up, sorted by distance.
        OWN_MARKERS = sorted(list(filter(lambda x: x in TOKEN_LIST_BY_TEAM[self.robot.zone], markers)) , key = lambda x: x.spherical.distance_metres)

        WALL_MARKERS = list(filter(lambda x: x < 28,markers ))

        #Removes cubes we can see from the list of cubes it is carrying
        OWN_MARKERS_IDS = list(map(lambda x: x.id, OWN_MARKERS))
        self.cubes = list(filter(lambda x: x not in OWN_MARKERS_IDS, self.cubes))

        TIME_LEFT = 150 - (time.time() - self.startTime)

        HAS_TRIANGULATION = self.map.triangulate(WALL_MARKERS) == 1

        #Changes to return mode if beyond MAX_CAPACITY or less that 30 seconds left and their is a cube to return.
        if len(self.cubes) >= MAX_CAPACITY:
            self.mode = RETURNING
        if TIME_LEFT < 30 and len(self.cubes) >= 1:
            self.mode = RETURNING

        if self.mode == RETURNING:
            if not HAS_TRIANGULATION:
                self.numberOfFailedIterations += 1
                if self.numberOfFailedIterations > MAX_FAILED_ITERATIONS:
                    #TODO: ultrasound sensor for backing up if against a wall. 

                    #Turns clockwise in a stop-start motion , hoping to find markers.
                    if self.numberOfFailedIterations % 2 == 0:
                        return Action("turn",0,0)
                    else:
                        return Action("stop",180,0)

            if map.isInScoringZone():
                #TODO: drop cubes.

                self.mode = SEARCHING

            angleToHome = map.angleToScoringZone()
            distanceToHome = map.distanceToScoringZone()
            return actionMoveOrTurn(Action("move",angleToHome,distanceToHome))

       if self.mode == SEARCHING:
           if len(OWN_MARKERS) > 0:
                TARGET = OWN_MARKERS[0]
                self.targetDistance = TARGET.spherical.distance_metres
                self.targetCube = TARGET.id

                return actionMoveOrTurn(Action("move",TARGET.spherical.rot_y_degrees ,targetDistance))

            
#Changes an action to move on the spot if larger than a maximun angle.
def actionMoveOrTurn(action):
    if action.angle > 60:
        return action.changeType("turn")
    else:
         return action


            






        