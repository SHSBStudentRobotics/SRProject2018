#Collision avoidance

import math

def WillCollide(Object, PathAngle, PathDistance):
    #Object is object taken from sourcebots API
    #PathAngle is the absolute angle between where the
    #robot is facing and where the robot wants to be in degrees
    #PathDistance is the distance we wish to travel along that line (metres)

    OBJECTBUFFER = 0.25 #Buffer around object to account for errors (metres)
    SELFWIDTH = 0.50 #Width of self, perpendicular to direction of travel (metres)
                     #Edge to edge

    PathAngle = math.radians(PathAngle)
    
    hyp = Object.distance_metres #Hypotenuse
    theta = abs(Object.rot_y_rad - PathAngle) #Angle between self and path in radians]

    adj = hyp * cos(theta)
    if adj > (PathDistance + OBJECTBUFFER): return False
    
    opp = hyp * sin(theta)

    if (opp - (OBJECTBUFFER + (SELFWIDTH / 2)) > 0:
        return False

    else: return True
    
