from action import *
import time, logging
from vision import *
from collision import *
from cameraExporter import *

#A list of all token id's belonging to robot 0 , 1 ,2 and 3.
TOKEN_LIST_BY_TEAM = [set(range(44, 48)), set(range(49, 53)), set(range(54, 58)), set(range(59, 63))]

#Mode "ENUM"
SEARCHING = 0
COLLECTING = 1 # Id of cube being collected will be stored somewhere
RETURNING = 2

MAX_CAPACITY = 2 #The amount of cubes the robot is carrying.

MAX_FAILED_ITERATIONS =  5 #The maximun number of failed iterations before some corrective maneuver is taken to try to restore vision.

logger = logging.getLogger(__name__)

class Decider:
    def __init__(self, robot, startTime, config={}):
        self.robot = robot
        self.mode = SEARCHING
        self.cubes = [] # A list of cubes (ID's) that the robot believes it has picked up and is carrying.
        self.returnedCubes = [] # A list of cubes (ID's) that the robot has returned
        self.mapObj = Mapping(robot)
        self.cameraExporter = jsonCameraExporter() #Used to export the camera data for later testing.
        self.startTime = startTime
        self.config = config
        self.numberOfFailedIterations = 0 #This is a counter that iterates upwards each time an operation fail's due to insufficient camera data.
                                            #If this occurs multiple times in a row ,some solution can be found.

        #Used in the search/pickup logic when the cube leaves the camera vision.
        self.targetDistance = -1
        self.targetCube = -1

    #returns main action class to be executed by hardware.
    def decide(self):
        TIME_LEFT = 150 - (time.time() - self.startTime)

        logger.info("New Iteration, {0} seconds left.".format(TIME_LEFT))
        markers = self.robot.camera.see()

        self.cameraExporter.newImage(markers)

        logger.info("Markers seen: ")
        for each in markers:
            logger.info("ID: " + str(each.id) + " Distance: " + str(each.spherical.distance_metres) + " Angle: " + str(each.spherical.rot_y_degrees))

        #The markers we can pick up.
        OWN_MARKERS = list(filter(lambda x: x.id in TOKEN_LIST_BY_TEAM[self.robot.zone], markers))

        WALL_MARKERS = list(filter(lambda x: x.id < 28,markers ))
        OBSTACLE_MARKERS = list(filter(lambda x: x.id >= 28 and x.id <= 43,markers ))

        #Removes cubes we can see from the list of cubes it is carrying
        OWN_MARKERS_IDS = list(map(lambda x: x.id, OWN_MARKERS))
        self.cubes = list(filter(lambda x: x not in OWN_MARKERS_IDS, self.cubes))

        HAS_TRIANGULATION = self.mapObj.triangulate(WALL_MARKERS) == 1

        #Updates self.returned cubes based on markers seen
        if HAS_TRIANGULATION:
            for marker in OWN_MARKERS:
                markerPos = self.mapObj.markerToPoint(marker)
                if self.mapObj.isPointInScoringZone(markerPos) and marker.id in self.returnedCubes:
                    self.returnedCubes.remove(marker.id)
                elif marker.id not in self.returnedCubes:
                    self.returnedCubes += [marker.id]      
                        
        #Removes markers in scoring zone from Own_Markers, and sorts by distance.
        OWN_MARKERS = sorted(list(filter(lambda x: x.id not in self.returnedCubes, OWN_MARKERS)), key = lambda x: x.spherical.distance_metres)

        logger.info("Triangulation position x: {0} y: {1} bearing: {2}.".format(self.mapObj.robotPos.x, self.mapObj.robotPos.y, self.mapObj.robotAngle))

        #Changes to return mode if beyond MAX_CAPACITY or less that 30 seconds left and their is a cube to return.
        if len(self.cubes) >= MAX_CAPACITY:
            self.mode = RETURNING
        if TIME_LEFT < 30 and len(self.cubes) >= 1:
            self.mode = RETURNING

        logger.info("Mode: " + str(self.mode))

        if self.mode == RETURNING:
            if not HAS_TRIANGULATION:
                return self.cameraFailure()
            
            if self.mapObj.isInScoringZone():
                self.returnedCubes += self.cubes
                self.cubes = []
                self.mode = SEARCHING

                return Action("move",0, -500)

            angleToHome = self.mapObj.angleToScoringZone()
            distanceToHome = self.mapObj.distanceToScoringZone()
            return actionMoveOrTurn(moveToPoint(angleToHome,distanceToHome,OBSTACLE_MARKERS))

        if self.mode == SEARCHING:
            if self.targetDistance < 1 and self.targetCube not in OWN_MARKERS_IDS and self.targetCube != -1:
                logger.info("Final Approach to cube: {0} at distance: {1} with {2} failed iterations.".format(self.targetCube, self.targetDistance,self.numberOfFailedIterations))
                self.numberOfFailedIterations += 1
                if self.numberOfFailedIterations < 5:
                    return Action("move", 0 ,5)
                else:
                    logger.info("Picked up cube with ID: " + str(self.targetCube))
                    self.numberOfFailedIterations = 0
                    self.cubes += [self.targetCube]
                    self.targetCube = -1
                    return Action("stop", 0)

            if len(OWN_MARKERS) > 0:
                self.numberOfFailedIterations = 0

                TARGET = OWN_MARKERS[0]
                self.targetDistance = TARGET.spherical.distance_metres
                self.targetCube = TARGET.id

                logger.info("Aproaching cube: {0} at distance: {1} and angle: {2}".format(self.targetCube, self.targetDistance, TARGET.spherical.rot_y_degrees))

                return actionMoveOrTurn(moveToMarker(TARGET, OBSTACLE_MARKERS))
            else:     
                return self.cameraFailure()

    def cameraFailure(self):
        logger.warning("Camera Failure: Number of failed iterations: " + str(self.numberOfFailedIterations))
        self.numberOfFailedIterations += 1

        #If the ultrasound detects a close object, reverse.
        if "hardware" in self.config:
            if "useultrasound" in self.config:
                if self.config["hardware"]["useultrasound"] in ['y','yes']:
                    if self.robot.servo_board.read_ultrasound(6, 7) < 1:
                        return Action("move",0,-5)

        if self.numberOfFailedIterations < 5:
            return Action("stop",0,0)

        #Turns clockwise in a stop-start motion , hoping to find markers.
        if self.numberOfFailedIterations % 2 == 0:
            return Action("turn",180,0)
        else:
            return Action("stop",0,0)

            
#Changes an action to move on the spot if larger than a maximun angle.
def actionMoveOrTurn(action):
    if action.angle > 60:
        return action.changeType("turn")
    else:
         return action