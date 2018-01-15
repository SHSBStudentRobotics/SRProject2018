import time, os, json

#A Mock Mamera object that reads in a json file made by JSONCameraTool
#When see() is called it returns the camera data , iterating through each
#image for each successive call of see(). Also replicates the delay caused 
# by image processing.

class MockCameraJSONReader():
    def __init__(self, filename):
        self.importCameraData(filename)
        self.imageCounter = 0
        self.CAMERADELAY = 0.2

    #Filename is relative to the MockFramework directory.
    def importCameraData(self, filename):
        #try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)) as file:
            self.cameraData = json.load(file)
        #except:
        #    print("Error loading JSON file: " + str(filename))
        #    print("Proceeding without camera data")

    def see(self):
        self.imageCounter += 1
        time.sleep(self.CAMERADELAY)
        return self.cameraData[(self.imageCounter - 1) % len(self.cameraData)]

    #Returns a particular image, rather than iterating through them, for consistent testing
    #In the unit testing framework.
    def seeImage(self, imageID):
        return self.cameraData[imageID % len(self.cameraData)]


