TODO: Fill this out properly.

Swapping to / from virtual robot:
To use the virtual robot, replace the line
`from robot import *`
with the line
`from VirtualRobot import *`
AND replace the line
`robot = Robot()`
with the line
`robot = VirtualRobot()`
Both lines should be in main.py
This replaces all references to the robot object with a virtual object.
