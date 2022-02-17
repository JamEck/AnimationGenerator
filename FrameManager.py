from DataManager import DataManager
from ActionHistory import *
import pygame as pg

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

class FrameManager(object):
  """docstring for FrameManager"""
  def __init__(self):
    super(FrameManager, self).__init__()
    self.fidx   = 0 # frame index
    self.frames = [Frame()]
    self.currFrame = self.frames[self.fidx]
    self.font = pg.font.SysFont("monospace", 20)

  def next(self):
    if self.fidx < len(self.frames) - 1:
      self.fidx += 1
      self.currFrame = self.frames[self.fidx]
    else:
      self.frames.append(Frame(self.currFrame))
      self.fidx = len(self.frames)-1
      self.currFrame = self.frames[self.fidx]

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

  def update(self, em):
    if em.keyboard[pg.K_RIGHT].checkFall():
      self.next()
    if em.keyboard[pg.K_LEFT].checkFall():
      self.prev()
    if em.keyboard[pg.K_d].checkFall():
      if em.keyboard[pg.K_LCTRL].checkHeld():
        self.delete()

  def draw(self, screen):
    if self.fidx > 0:
      self.frames[self.fidx - 1].dm.draw(screen, (50,30,30))
    if self.fidx < len(self.frames) - 1:
      self.frames[self.fidx + 1].dm.draw(screen, (30,50,30))
    text = self.font.render("Frame: {} Total: {}".format(str(self.fidx), len(self.frames)), 0, (255,255,255))
    screen.blit(text, (20, 40))
    self.currFrame.dm.draw(screen)
    self.currFrame.dm.drawInfo(screen)
