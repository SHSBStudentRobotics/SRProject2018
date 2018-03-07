from MockFramework import *
from decision import *
import unittest, time

class TestDecisions(unittest.TestCase):
    def test_decide(self):
        r = MockRobot()
        decider = Decider(r, time.time())

        #moving to cube
        self.assertEqual(decider.decide().type, "move")
        self.assertEqual(decider.mode, 0)

        decider.cubes += [5,6,7]
        decider.decide()

        self.assertEqual(decider.mode, 2)
