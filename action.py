#Type is either "move", "stop" or "turn".

class Action:
    def __init__(self,newType,angle,dist = 0):
        self.type = newType
        self.angle = clampAngle(angle)
        self.dist = dist

    def changeType(self,newType):
        self.type = newType
        return self

def clampAngle(angle):
    if angle > 180:
        return clampAngle(angle-360)
    if angle < -180:
        return clampAngle(angle+360)
    return angle