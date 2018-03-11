import unittest
from action import *

class TestActiion(unittest.TestCase):
    def test_ClampAngle(self):
        self.assertEqual(clampAngle(30),30)
        self.assertEqual(clampAngle(390),30)
        self.assertEqual(clampAngle(-330),30)

        self.assertEqual(clampAngle(-30), -30)
        self.assertEqual(clampAngle(330), -30)
        self.assertEqual(clampAngle(-390), -30)