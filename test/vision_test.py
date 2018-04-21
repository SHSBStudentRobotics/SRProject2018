from MockFramework import *
from vision import *
import unittest

camera = MockCameraJSONReader("data1.json")

markers = camera.see()

#debugPrintMarker(markers[0])

#print("orientation: " + str(getOrientation(markers[0])))

class TestVision(unittest.TestCase):
    def test_AngleToPoint(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)
        map = Mapping(r)
        map.robotPos.update(400,400)
        map.robotAngle = 0

        self.assertEqual(clampAngle(map.angleToPoint(Point(600,600))), 135)
        self.assertEqual(clampAngle(map.angleToPoint(Point(200,200))), -45)
        self.assertEqual(clampAngle(map.angleToPoint(Point(200,600))), -135)
        self.assertEqual(clampAngle(map.angleToPoint(Point(600,200))), 45)

    def test_DistanceToPoint(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)
        map = Mapping(r)
        map.robotPos.update(400,400)
        map.robotAngle = 0

        self.assertEqual(map.distanceToPoint(Point(700,800)),500)

    def test_Triangulate(self):
        marker1 = Marker({"id": 0, "polar": [
            0,
          radians(-30),
          2.23
        ],})
        marker2 = Marker({"id": 2, "polar": [
         0,
         radians(30),
          2.23
        ],})
        r = MockRobot()
        mapObj = Mapping(r)
        mapObj.triangulate([marker1, marker2])
        
        self.assertAlmostEqual(mapObj.robotPos.x, 2.00,places=-1)
        self.assertAlmostEqual(mapObj.robotPos.y, 2.00,places=-1)
        self.assertAlmostEqual(mapObj.robotAngle, 0,places=-1)

    def test_isInHome(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)
        map = Mapping(r)

        map.robotPos.update(2.45,2.45)
        self.assertTrue(map.isInScoringZone())

        map.robotPos.update(4.00,2.00)
        self.assertFalse(map.isInScoringZone())

        map.robotPos.update(2.00,4.00)
        self.assertFalse(map.isInScoringZone())

    def test_markerToPoint(self):
        r = MockRobot(motor_board = MockMotorBoard() ,camera = None)
        map = Mapping(r)

        map.robotPos.update(4.00,4.00)
        map.robotAngle = 45

        marker = Marker({
            "id": 44,
            "polar": 
            [
                0,
                radians(0),
                1.00
            ]
        })

        #Just checking the signs are correct (correct quadrant)
        temp = map.markerToPoint(marker)
        self.assertGreater(temp.x, 4.00)
        self.assertLess(temp.y, 4.00)

        map.robotAngle = 135
        temp = map.markerToPoint(marker)
        self.assertGreater(temp.x, 4.00)
        self.assertGreater(temp.y, 4.00)

        map.robotAngle = 225
        temp = map.markerToPoint(marker)
        self.assertLess(temp.x, 4.00)
        self.assertGreater(temp.y, 4.00)

        map.robotAngle = 315
        temp = map.markerToPoint(marker)
        self.assertLess(temp.x, 4.00)
        self.assertLess(temp.y, 4.00)

