import json

class jsonCameraExporter:
    def __init__(self):
        self.imageList = []

    def newImage(self, markers):
        self.imageList.append(list(map(lambda x: x._raw_data, markers)))
        self.exportImages()

    def exportImages(self):
        with open("logs/images.json", mode="w") as file:
            file.write(json.dumps(self.imageList,indent=4))