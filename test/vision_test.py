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

    def test_Triangulate(self):
        marker1 = Marker({"id": 0, "polar": [
            0,
          radians(-30),
          223
        ],})
        marker2 = Marker({"id": 2, "polar": [
         0,
         radians(30),
          223
        ],})
        r = MockRobot()
        mapObj = Mapping(r)
        mapObj.triangulate([marker1, marker2])
        
        self.assertAlmostEqual(mapObj.robotPos.x, 200,places=-1)
        self.assertAlmostEqual(mapObj.robotPos.y, 200,places=-1)
        self.assertAlmostEqual(mapObj.robotAngle, 0,places=-1)

    def test_isInHome(self):
        r = MockRobot()
        map = Mapping(r)

        map.robotPos.update(245,245)
        self.assertTrue(map.isInScoringZone())

        map.robotPos.update(400,200)
        self.assertFalse(map.isInScoringZone())

        map.robotPos.update(200,400)
        self.assertFalse(map.isInScoringZone())