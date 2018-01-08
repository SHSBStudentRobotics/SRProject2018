from robot import *
from vision import *
import time

def main():
    robot = Robot()

    while True:
        try:
            markers = robot.see()
            for each in markers:
                debugPrintMarker(each)
                getOrientation(each)
        except error as e:
            print("Error")
            print(e)
