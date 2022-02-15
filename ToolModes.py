import pygame as pg
from Utils import *
from ActionHistory import *
from EventManager import EventManager
from Geometry import *
from DataManager import DataManager

class ModeIndicator(object):
  """docstring for ModeIndicator"""
  def __init__(self):
    super(ModeIndicator, self).__init__()
    self.pos    = Vec2(10,10)
    self.indicators = {"select":True, "vertex":False, "line":False, "circle":False}
    self.current = "select"
    self.font = pg.font.SysFont("monospace", 20)

  def clear(self):
    self.current = None
    for each in self.indicators:
      self.indicators[each] = False

  def select(self, mode):
    if mode not in self.indicators:
      print(mode + " is not a valid mode")
      return
    self.clear()
    self.indicators[mode] = True
    self.current = mode

  def draw(self, screen):
    vals = list(self.indicators.values())
    for i,key in enumerate(self.indicators):
      pos = (self.pos + Vec2(i*90, 0)).asTuple()
      color = (255,255,0) if vals[i] else (100,100,100)
      text = self.font.render(key, 0, (0,0,0))
      pg.draw.rect(screen, color, (pos,(85,20)))
      screen.blit(text, (pos[0]+5, pos[1]))


class SelectMode(object):
  """docstring for SelectMode"""
  def __init__(self, em, dm, ah, screen):
    super(SelectMode, self).__init__()
    self.em = em
    self.dm = dm
    self.ah = ah
    self.screen = screen
    self.tempData = None

  def onHover(self):
    nearest = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if nearest:
      pg.draw.rect(self.screen, (100,100,100), ((nearest.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftFall(self):
    self.tempData = self.dm.findNearestVertex(self.em.mouse.pos,10)

  def onLeftHeld(self):
    if self.tempData:
      pg.draw.line(self.screen, (100,100,100), self.tempData.pos.asTuple(), self.em.mouse.pos.asTuple())
      pg.draw.rect(self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftRise(self):
    if self.tempData:
      self.ah.do(MoveVertex(self.tempData, self.em.mouse.pos, self.dm))

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass
  def onRightRise(self):
    pass


class VertexMode(object):
  """docstring for VertexMode"""
  def __init__(self, em, dm, ah, screen):
    super(VertexMode, self).__init__()
    self.em = em
    self.dm = dm
    self.ah = ah
    self.screen = screen

  def onHover(self):
    nearest = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if nearest:
      pg.draw.rect(self.screen, (100,100,100), ((nearest.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftFall(self):
    pass
  def onLeftHeld(self):
    pass

  def onLeftRise(self):
    self.ah.do(CreateVertex(Vertex(self.em.mouse.pos),self.dm))

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass

  def onRightRise(self):
    nearest = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if nearest: self.ah.do(DeleteVertex(nearest,self.dm))


class LineMode(object):
  """docstring for LineMode"""
  def __init__(self, em, dm, ah, screen):
    super(LineMode, self).__init__()
    self.em = em
    self.dm = dm
    self.ah = ah
    self.screen = screen
    self.tempData = None

  def onHover(self):
    nearestV = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if nearestV:
      pg.draw.rect(self.screen, (100,100,100), ((nearestV.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
    else:
      nearestL = self.dm.findNearestLine(self.em.mouse.pos,10)
      if nearestL:
        pg.draw.rect(self.screen, (100,100,100), ((nearestL.midpoint() - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftFall(self):
    self.tempData = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if not self.tempData:
      self.tempData = Vertex(self.em.mouse.pos)

  def onLeftHeld(self):
    if self.tempData:
      pg.draw.line(self.screen, (100,100,100), self.em.mouse.pos.asTuple(), self.tempData.pos.asTuple())
      pg.draw.rect(self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
      self.tempData.draw(self.screen)

  def onLeftRise(self):
    if self.tempData:
      endPoint = self.dm.findNearestVertex(self.em.mouse.pos,10)
      action = [CreateVertex(self.tempData, self.dm)]
      if not endPoint:
        endPoint = Vertex(self.em.mouse.pos)
        action.append(CreateVertex(endPoint,self.dm))
      action.append(CreateLine(Line(endPoint, self.tempData),self.dm))
      self.ah.do(action)

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass
  def onRightRise(self):
    pass


class CircleMode(object):
  """docstring for CircleMode"""
  def __init__(self, em, dm, ah, screen):
    super(CircleMode, self).__init__()
    self.em = em
    self.dm = dm
    self.ah = ah
    self.screen = screen
    self.tempData = None

  def onHover(self):
    nearest = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if nearest:
      pg.draw.rect(self.screen, (100,100,100), ((nearest.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftFall(self):
    self.tempData = self.dm.findNearestVertex(self.em.mouse.pos,10)
    if not self.tempData:
      self.tempData = Vertex(self.em.mouse.pos)
  def onLeftHeld(self):
    if self.tempData:
      rad = (self.tempData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      self.tempData.draw(self.screen)
      pg.draw.circle(self.screen, (100,100,100), self.tempData.pos.asTuple(), rad, 1)
  def onLeftRise(self):
    if self.tempData:
      rad = (self.tempData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      action = [
        CreateVertex(self.tempData,self.dm),
        CreateCircle(Circle(self.tempData, rad),self.dm)
      ]
      self.ah.do(action)
  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass
  def onRightRise(self):
    pass
