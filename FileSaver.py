from fileinput import filename
import pickle
import os
import tempfile
from FrameManager import FrameManager
from ToolModes import ModeSelector
import pygame as pg

def loadFromFile(dir, fileName):
    filePath = os.path.join(dir, fileName)

    if ".sav" not in fileName:
        raise ValueError("{} Is Not A .sav File".format(filePath))

    if not os.path.exists(filePath):
        raise FileNotFoundError("File {} does not exist".format(filePath))

    data = None
    with open(os.path.join(dir, fileName), "rb") as inFile:
        data = pickle.load(inFile)

    return FrameManager.readPickles(data)


def saveToFile(dir, fileName, frameMan):
    fileName = os.path.splitext(fileName)[0] + ".sav"

    if not os.path.exists(dir):
        print("Directory {} does not exist".format(dir))
        raise FileNotFoundError("Directory {} does not exist".format(dir))

    if not os.path.exists(dir):
        print("Directory {} does not exist".format(dir))
        raise FileNotFoundError("Directory {} does not exist".format(dir))

    if not isinstance(frameMan, (FrameManager)):
        raise ValueError("Please Provide frameManager To Save")

    filePath = os.path.join(dir, fileName)
    tempPath = filePath + ".temp"
    try:
        with open(tempPath, "wb") as outFile:
            pickle.dump(frameMan.getPickles(), outFile)

        if os.path.exists(filePath):
            os.remove(filePath)
        os.rename(tempPath, filePath)

    except Exception as e:
        if os.path.exists(tempPath):
            os.remove(tempPath)
        print(str(e))


