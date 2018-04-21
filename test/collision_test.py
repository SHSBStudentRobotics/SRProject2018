from MockFramework import *
from collision import *
import unittest
from config import *

class TestCollisions(unittest.TestCase):
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
        self.assertTrue(willCollide(marker,0, 5))
        self.assertFalse(willCollide(marker,0, 1))
        self.assertFalse(willCollide(marker,30, 1))

    def test_MoveTowardsPoint(self):
        robot = MockRobot
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
        config = getConfigSettings()
        marker = Marker(json.loads(data))
        self.assertNotEqual(moveToPoint(robot, config, 0,8,[marker]).angle, 0)
        self.assertEqual(moveToPoint(robot, config, 0,1,[marker]).angle, 0)
        self.assertEqual(moveToPoint(robot, config, 50,8,[marker]).angle, 50)

        ultrasoundData = [0.5, 1, 1.5, 4]
        self.assertEqual(getUltrasoundAction(ultrasoundData[0], config).type, "reverseTurn")
        self.assertEqual(getUltrasoundAction(ultrasoundData[1], config).type, "reverseTurn")
        self.assertEqual(getUltrasoundAction(ultrasoundData[2], config).type, "none")
        self.assertEqual(getUltrasoundAction(ultrasoundData[3], config).type, "none")