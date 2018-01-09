from robot import *
from vision import *
import time

def main():
    robot = Robot()

    while True:
        try:
            markers = robot.camera.see()
            for each in markers:
                debugPrintMarker(each)
                getOrientation(each)
        except Exception as e:
            print("Error")
            print(e)
