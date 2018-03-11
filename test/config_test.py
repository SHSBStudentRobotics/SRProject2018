import unittest
from config import *

class TestConfig(unittest.TestCase):
    def test_GetConfigSettings(self):
        filePath = "test/testConfig.ini"
        if os.path.isfile(filePath):
            os.remove(filePath)
        getConfigSettings(filePath)
        self.assertTrue(os.path.isfile(filePath))
        os.remove(filePath)

