from MockFramework import *
from vision import *
from WillCollide import *
import unittest, json

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

    def test_WillCollide(self):
        data = """
        {  
            "homography_matrix":[  
               [  
                  0.019211170349161224,
                  0.7332668180891213,
                  2.9453105555864765
               ],
               [  
                  -0.6927628167568876,
                  0.0338688672237774,
                  3.335956040762492
               ],
               [  
                  2.3390455511951388e-05,
                  6.273610239377743e-05,
                  0.008795744737576883
               ]
            ],
            "id":44,
            "pixel_corners":[  
               [  
                  251.77137756353264,
                  458.671081542915
               ],
               [  
                  414.18548583989747,
                  459.8241271973196
               ],
               [  
                  416.3298950194744,
                  301.407440185601
               ],
               [  
                  254.81420898432418,
                  297.99057006830725
               ]
            ],
            "certainty":0.0,
            "cartesian":[  
               147.1849237842708,
               0.0,
               -21.064577021744885
            ],
            "polar":[  
               0.14215112134173036,
               0,
               1.6846266245661
            ],
            "pixel_centre":[  
               334.8563019346867,
               379.2693103644463
            ]
         }
         """
        marker = Marker(json.loads(data))
        self.assertTrue(WillCollide(marker,0, 5))
        self.assertFalse(WillCollide(marker,0, 1))
        self.assertFalse(WillCollide(marker,30, 1))

if __name__ == '__main__':
    unittest.main()
