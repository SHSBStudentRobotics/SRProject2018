TODO: Fill this out properly.

Swapping to / from virtual robot:
To use the virtual robot, replace the line
`from robot import *`
with the line
`from MockFramework import *`
AND replace the line
`robot = Robot()`
with the line
`robot = MockRobot()`
Both lines should be in main.py
This replaces all references to the robot object with a virtual object.
Their are optional paramaters for the constructor of MockRobot
that allow you to choose what mock components are used. E.G.
`robot = MockRobot(motor_board = MockMotorBoard() ,camera = None)`
will create a MockRobot object that has a motor board MockMotorBoard(),
as opposed to the default MockMotorBoardPrinter, and no camera.
