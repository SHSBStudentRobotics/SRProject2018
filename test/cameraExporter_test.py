import unittest
from cameraExporter import *
from MockFramework import *

class TestCameraExporter(unittest.TestCase):
    def test_export(self):
        exporter = jsonCameraExporter()
        camera = MockCameraJSONReader("data1.json")
        exporter.newImage(camera.see())
