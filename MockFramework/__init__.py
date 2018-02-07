#The modules imported when the user does from: MockRobot import *
#__all__ = ["MockRobot"]

from MockFramework.MockRobot import *
from MockFramework.MockCamera import *
from MockFramework.MockMotorBoard import *

TOKEN_ZONE_0 = set(range(44, 49))
TOKEN_ZONE_1 = set(range(49, 54))
TOKEN_ZONE_2 = set(range(54, 59))
TOKEN_ZONE_3 = set(range(59, 64))