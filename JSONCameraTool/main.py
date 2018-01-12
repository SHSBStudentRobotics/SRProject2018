from robot import *
import json

def main():
    r = Robot()
    imageList = []
    fileReader = open("output.json", mode = "w")

    try:
        while True:
            markers = r.camera.see()
            imageList.append(markers)

            json.dump(imageList, fileReader)
        
    finally:
        fileReader.close()

main()