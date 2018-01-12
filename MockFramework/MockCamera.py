import json
import time

#A Mock Mamera object that reads in a json file made by JSONCameraTool
#When see() is called it returns the camera data , iterating through each
#image for each successive call of see(). Also replicates the delay caused 
# by image processing.

class MockCameraJSONReader():
    def __init__(self, filename):
        self.importCameraData(filename)
        self.imageCounter = 0
        self.CAMERADELAY = 0.2

    def importCameraData(self, filename):
        try:
            with open(filename) as file:
                self.cameraData = json.load(file)
        except:
            print("Error loading JSON file: " + str(filename))
            print("Proceeding without camera data")

    def see(self):
        self.imageCounter += 1
        time.sleep(self.CAMERADELAY)
        return self.cameraData[(self.imageCounter - 1) % len(self.cameraData)]



