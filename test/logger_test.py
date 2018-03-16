from logger import *
from config import *
from hardware import *
from MockFramework import *
import unittest, os

class TestLoggers(unittest.TestCase):
    def test_loggin(self):
        config = getConfigSettings("test/tempConfig.ini")
        setupLoggers(config)

        r = MockRobot()
        move(r,Action("move",30,100),0,config)
        os.remove("test/tempConfig.ini")

