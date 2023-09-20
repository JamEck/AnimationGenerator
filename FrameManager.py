from DataManager import DataManager
from ActionHistory import ActionHistory
import os
import pygame as pg
import json
import struct

class Frame(object):
  """docstring for Frame"""
  def __init__(self, frame = None):
    super(Frame, self).__init__()
    if frame == None:
      self.dm = DataManager()
    else:
      self.dm = frame.dm.copy()
    self.ah = ActionHistory()

  def copy(self):
    f = Frame()
    f.dm = self.dm.copy()
    f.ah = ActionHistory()
    return f

  def makeDict(self):
    return {__class__.__name__ : self.dm.makeDict()}

  @staticmethod
  def fromDict(data):
    f = Frame()
    f.dm = DataManager.fromDict(data["DataManager"])
    return f

class FrameManager(object):
  """docstring for FrameManager"""
  def __init__(self):
    super(FrameManager, self).__init__()
    self.fidx   = 0 # frame index
    self.frames = [Frame()]
    self.currFrame = self.frames[self.fidx]
    self.font = pg.font.SysFont("monospace", 20)

  def next(self, create = False):
    if self.fidx < len(self.frames) - 1:
      self.fidx += 1
    elif create:
      self.frames.append(Frame(self.currFrame))
      self.fidx = len(self.frames)-1
    self.currFrame = self.frames[self.fidx]

  def insert(self):
    self.frames.insert(self.fidx+1, Frame())

  def prev(self):
    if self.fidx > 0:
      self.fidx -= 1
      self.currFrame = self.frames[self.fidx]

  def delete(self):
    del self.frames[self.fidx]
    if self.fidx > 0:
      self.fidx -= 1
      self.currFrame = self.frames[self.fidx]
    else:
      if len(self.frames) == 0:
        self.frames.append(Frame())
      self.currFrame = self.frames[0]

  def getDM(self):
    return self.currFrame.dm

  def getAH(self):
    return self.currFrame.ah

  def loadFromJson(self, dir, fileName):
    filePath = os.path.join(dir, fileName)

    if ".json" not in fileName:
        raise ValueError("{} Is Not A .json File".format(filePath))

    if not os.path.exists(filePath):
        raise FileNotFoundError("File {} does not exist".format(filePath))

    data = None
    # with open(os.path.join(dir, fileName), "rb") as inFile:
    #     data = pickle.load(inFile)

    with open(os.path.join(dir, fileName), "r") as inFile:
        data = json.load(inFile)

    self.fromDict(data["FrameManager"])

  def genFromJson(dir, fileName):
    ret = FrameManager()
    ret.loadFromJson(dir, fileName)
    return ret

  def handleFileDrop(self, file_drop):
    print("File Dropped: " + file_drop.path)
    ext = os.path.splitext(file_drop.path)[-1].lower()
    if ext == ".png" or ext == ".bmp":
      self.currFrame.ah.do(LoadImage(file_drop, self.currFrame.dm))
    if ext == ".json":
      print("json loaded")
      self.loadFromJson(*os.path.split(file_drop.path))

  def update(self, em):
    if em.keyboard[pg.K_RIGHT].checkFall():
      if em.keyboard[pg.K_LCTRL].checkHeld():
        self.insert()
      else:
        self.next(em.keyboard[pg.K_LSHIFT].checkHeld())
    if em.keyboard[pg.K_LEFT].checkFall():
      self.prev()
    if em.keyboard[pg.K_d].checkFall():
      if em.keyboard[pg.K_LCTRL].checkHeld():
        self.delete()

    if em.file_drop != None:
      self.handleFileDrop(em.file_drop)

  def draw(self, screen):
    if self.fidx >= 0 and self.fidx < len(self.frames):
      self.currFrame.dm.draw_image(screen)
    if self.fidx > 0:
      self.frames[self.fidx - 1].dm.draw(screen, (50,30,30))
    if self.fidx < len(self.frames) - 1:
      self.frames[self.fidx + 1].dm.draw(screen, (30,50,30))
    text = self.font.render("Frame: {} Total: {}".format(str(self.fidx), len(self.frames)), 0, (255,255,255))
    screen.blit(text, (20, 40))
    self.currFrame.dm.draw(screen)
    self.currFrame.dm.drawInfo(screen)

  def makeDict(self):
    return {__class__.__name__ : [frame.makeDict() for frame in self.frames]}

  def fromDict(self, data):
    self.frames.clear()
    for frame in data:
      self.frames.append(Frame.fromDict(frame["Frame"]))
    self.currFrame = self.frames[0]

  @staticmethod
  def genFromDict(data):
    fm = FrameManager()
    fm.fromDict(data)
    return fm

  def asBytes(self):
    block = struct.pack("H", len(self.frames))
    for frame in self.frames:
      block += frame.dm.asBytes()
    return block