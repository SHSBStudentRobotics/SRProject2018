from robot import *
import json

def main():
    r = Robot()
    imageList = []
    fileReader = open("output.json", mode = "w")

    try:
        while True:
            markers = r.camera.see()
            imageList.append(list(map(lambda x: x._raw_data, markers)))

            print(imageList)

            fileReader.truncate(0)
            fileReader.write(json.dumps(imageList))
        
    finally:
        fileReader.close()

main()