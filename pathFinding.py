from vision import *
from action import *

COLUMNS = [Point(4,2), Point(6,4), Point(4,6), Point(2,4)]

class MappingGrid:
    #size is the number of squares per side (8m) , 16 means 50cm x 50cm boxes
    #points is a list of points , representing each item to be considered.
    def __init__(self, points, size = 16):
        self.size = size
        self.grid = [[False for x in range(size)] for y in range(size)]

        for each in points + COLUMNS:
            self.grid[int(round(each.x // (8/size))][int(round(each.y // (8/size))]  = True

    def makeRoute(self, destinationPoint, robotPos):

        
def shouldUseRoute(route, grid, robotPos):
    return True

#route is a list of points representing grid coordinates.
def getActionFromRoute(route, grid, robotPos, robotAngle):
    nextItem = route[0]
    
    nextPoint = Point(nextItem.x * grid.size, nextItem.y * grid.size)

    while distanceBetweenPoints(nextItem, robotPos) < 0.1:
        route = route[1:]
        nextItem = route[0]
        nextPoint = Point(nextItem.x * grid.size, nextItem.y * grid.size)

    return Action("move",angleBetweenPoints(robotPos, nextPoint) - robotPos, distanceBetweenPoints(nextPoint,robotPos))


