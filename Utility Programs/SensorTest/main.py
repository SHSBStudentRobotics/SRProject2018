from robot import *
import time, math

r = Robot()

class imuMapper:
    def __init__(self,robot):
        self._robot = robot
        self.velocityX = 0
        self.velocityY = 0
        self.positionX = 0
        self.positionY = 0
        self.prevTime = time.time()

    def update(self, printStatus = False):
        dt = time.time() - self.prevTime
        self.prevTime = time.time()

        data = self._robot.servo_board.direct_command('getIMUData')

        self.velocityX += dt*float(data[3]) * math.cos(float(data[4]))
        self.velocityY += dt*float(data[4]) * math.cos(float(data[5]))

        self.positionX += dt * self.velocityX
        self.positionX += dt * self.positionY

        if printStatus:
            self.printStatus(data)

    def printStatus(self,data):
        print("Orientation x: " + data[0])
        print("Orientation y: " + data[1])
        print("Orientation z: " + data[2])
        print()
        print("Acceleration x:" + data[3])
        print("Acceleration y:" + data[4])
        print("Acceleration z:" + data[5])
        print()
        print("Velocity x: " + str(self.velocityX))
        print("Velocity y: " + str(self.velocityY))
        print()
        print("Position x: " + str(self.positionX))
        print("Position y: " + str(self.positionY))
        print()

imu = imuMapper(r)

while True:
    print("Ultrasound: " + str(r.servo_board.read_ultrasound(6, 7)))
    imu.update(True)