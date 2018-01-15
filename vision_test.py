from MockFramework import *
from vision import *

camera = MockCameraJSONReader("data1.json")

markers = camera.see()

print(markers[0].polar.distance_metres)

print(getOrientation(markers[0]))

