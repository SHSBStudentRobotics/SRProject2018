from MockFramework import *
from vision import *
import unittest

camera = MockCameraJSONReader("data1.json")

markers = camera.see()

#debugPrintMarker(markers[0])

#print("orientation: " + str(getOrientation(markers[0])))

class TestVision(unittest.TestCase):
    def test_AngleToPoint(self):
        r = MockRobot()
        map = Mapping(r)
        map.robotPos.update(400,400)
        map.robotAngle = 0

        self.assertEqual(clampAngle(map.angleToPoint(Point(600,600))), 135)
        self.assertEqual(clampAngle(map.angleToPoint(Point(200,200))), -45)
        self.assertEqual(clampAngle(map.angleToPoint(Point(200,600))), -135)
        self.assertEqual(clampAngle(map.angleToPoint(Point(600,200))), 45)

    def test_DistanceToPoint(self):
        r = MockRobot()
        map = Mapping(r)
        map.robotPos.update(400,400)
        map.robotAngle = 0

        self.assertEqual(map.distanceToPoint(Point(700,800)),500)

if __name__ == '__main__':
    unittest.main()
