*from action import *
from vision import *

#A list of all token id's belonging to robot 0 , 1 ,2 and 3.
TOKEN_LIST_BY_TEAM = [set(range(44, 49)), set(range(49, 54)), set(range(54, 59)), set(range(59, 64))]

#Mode "ENUM"
SEARCHING = 0
COLLECTING = 1 # Id of cube being collected will be stored somewhere
RETURNING = 2

MAX_CAPACITY = 2 #The amount of cubes the robot is carrying.

HOME_POSITIONS = [Point(200,200), Point(600,200), Point(600,600), Point (200, 600)]

class Decider:
    def __init__(self, robot):
        self.robot = robot
        self.mode = SEARCHING
        self.cubes = [] # A list of cubes (ID's) that the robot believes it has picked up and is carrying.
        self.map = Mapping(robot)
        self.numberOfFailedIterations = 0 #This is a counter that iterates upwards each time an operation fail's due to insufficient camera data.
                                            #If this occurs multiple times in a row ,some solution can be found.

    #returns main action class to be executed by hardware.
    def decide(self):
        markers = self.robot.camera.see()

        #The markers we can pick up.
        OWN_MARKERS = list(filter(lambda x: x in TOKEN_LIST_BY_TEAM[self.robot.zone], markers))

        WALL_MARKERS = list(filter(lambda x: x < 28,markers ))

        #Removes cubes it can see from the list of cubes it is carrying
        OWN_MARKERS_IDS = list(map(lambda x: x.id, OWN_MARKERS))
        self.cubes = list(filter(lambda x: x not in OWN_MARKERS_IDS, self.cubes))


        if len(self.cubes) < MAX_CAPACITY:
            self.mode = RETURNING

        if self.mode == RETURNING:
            if self.map.triangulate(WALL_MARKERS) == 0:
                self.numberOfFailedIterations += 1
                return Action("stop",0,0)

            angleToHome = map.angleToPoint(HOME_POSITIONS[self.robot.zone])
            distanceToHome = map.distanceToPoint(HOME_POSITIONS[self.robot.zone])
            return actionMoveOrTurn(Action("move",angleToHome,distanceToHome))
            
#Changes an action to move on the spot if larger than a maximun angle.
def actionMoveOrTurn(action):
    if action.angle > 60:
        return action.changeType("turn")
    else:
         return action


            






        