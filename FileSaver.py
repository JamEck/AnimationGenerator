from fileinput import filename
import os
from FrameManager import FrameManager
import pickle
import json
import traceback as tb


def saveToJson(dir, fileName, frameMan):
    fileName = os.path.splitext(fileName)[0] + ".json"

    if not os.path.exists(dir):
        raise FileNotFoundError("Directory {} does not exist".format(dir))

    if not isinstance(frameMan, (FrameManager)):
        raise ValueError("Please Provide frameManager To Save")

    filePath = os.path.join(dir, fileName)
    tempPath = filePath + ".temp"
    try:
        with open(tempPath, "w") as outFile:
            json.dump(frameMan.makeDict(), outFile, indent=2)

        if os.path.exists(filePath):
            os.remove(filePath)
        os.rename(tempPath, filePath)

    except Exception as e:
        if os.path.exists(tempPath):
            os.remove(tempPath)
        print(str(e))
        print(tb.format_exc())

def saveToBinary(dir, fileName, frameMan):
    fileName = os.path.splitext(fileName)[0] + ".skel"

    if not os.path.exists(dir):
        raise FileNotFoundError("Directory {} does not exist".format(dir))

    if not isinstance(frameMan, (FrameManager)):
        raise ValueError("Please Provide frameManager To Save")

    filePath = os.path.join(dir, fileName)
    tempPath = filePath + ".temp"
    try:

        with open(tempPath, "wb") as outFile:
            outFile.write(frameMan.asBytes())

        if os.path.exists(filePath):
            os.remove(filePath)
        os.rename(tempPath, filePath)

    except Exception as e:
        if os.path.exists(tempPath):
            os.remove(tempPath)
        print(str(e))
        print(tb.format_exc())
