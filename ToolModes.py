import pygame as pg
from Utils import *
from ActionHistory import *
from EventManager import EventManager
from Geometry import *
from DataManager import DataManager

class ModeIndicator(object):
  """docstring for ModeIndicator"""
  def __init__(self, dataMan):
    super(ModeIndicator, self).__init__()
    self.pos    = Vec2(10,10)
    self.dm = dataMan
    self.indicators = {"select":True, "vertex":False, "line":False, "circle":False, "pill":False}
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
      pos = (self.pos + Vec2(i*100, 0)).asTuple()
      color = (255,255,0) if vals[i] else (100,100,100)
      text = self.font.render(key, 0, (0,0,0))
      pg.draw.rect(screen, color, (pos,(85,20)))
      screen.blit(text, (pos[0]+5, pos[1]))


class Mode(object):
  """docstring for Mode"""
  def __init__(self, frame, em, screen):
    super(Mode, self).__init__()
    self.em = em
    self.dm = frame.dm
    self.ah = frame.ah
    self.screen = screen
    self.tempData = None
    self.selectedData = None
    self.font = pg.font.SysFont("monospace", 20)

  def reset(self):
    self.tempData = None
    self.selectedData = None

  def findNearest(self, items): # items "vlcp"
    if 'v' in items:
      self.tempData = self.dm.findNearestVertex(self.em.mouse.pos,10)
      if self.tempData:
        pg.draw.rect(self.screen, (100,100,100), ((self.tempData.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'l' in items:
      self.tempData = self.dm.findNearestLine(self.em.mouse.pos,10)
      if self.tempData:
        pg.draw.rect(self.screen, (100,100,100), ((self.tempData.midpoint() - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'p' in items:
      self.tempData = self.dm.findNearestPill(self.em.mouse.pos,10)
      if self.tempData:
        pg.draw.rect(self.screen, (100,100,100), ((self.tempData.getAxis().midpoint() - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'c' in items:
      self.tempData = self.dm.findNearestCircle(self.em.mouse.pos,10)
      if self.tempData:
        pg.draw.rect(self.screen, (100,100,100), ((self.tempData.nearestPoint(self.em.mouse.pos) - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    return None

class SelectMode(Mode):
  """docstring for SelectMode"""
  def __init__(self, frame, em, screen):
    super(SelectMode, self).__init__(frame, em, screen)

  def onHover(self):
    self.findNearest("vlcp")
    if self.selectedData:
      self.selectedData.printAttr(self.screen);

  def onLeftFall(self):
    self.selectedData = self.tempData

  def onLeftHeld(self):
    if self.selectedData:
      if   isinstance(self.selectedData, Vertex):
        pg.draw.line(self.screen, (100,100,100), self.selectedData.pos.asTuple(), self.em.mouse.pos.asTuple())
        pg.draw.rect(self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
      elif isinstance(self.selectedData, Circle):
        pg.draw.line(self.screen, (100,100,100), self.selectedData.center.pos.asTuple(), self.em.mouse.pos.asTuple())
        pg.draw.rect(self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftRise(self):
    if self.selectedData:
      if   isinstance(self.selectedData, Vertex):
        self.ah.do(MoveVertex(self.selectedData, self.em.mouse.pos, self.dm))
      elif isinstance(self.selectedData, Circle):
        newRad = (self.em.mouse.pos - self.selectedData.center.pos).mag()
        self.ah.do(ResizeCircle(self.selectedData, newRad, self.dm))

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
      self.selectedData = self.tempData
  def onRightHeld(self):
    pass
  def onRightRise(self):
    pass


class VertexMode(Mode):
  """docstring for VertexMode"""
  def __init__(self, frame, em, screen):
    super(VertexMode, self).__init__(frame, em, screen)

  def onHover(self):
    self.findNearest('v')

  def onLeftFall(self):
    self.selectedData = True

  def onLeftHeld(self):
    pass

  def onLeftRise(self):
    if self.selectedData:
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


class LineMode(Mode):
  """docstring for LineMode"""
  def __init__(self, frame, em, screen):
    super(LineMode, self).__init__(frame, em, screen)
    self.linked = False

  def reset(self):
    super().reset()
    self.linked = False

  def onHover(self):
    self.findNearest("v")

  def onLeftFall(self):
    self.selectedData = self.tempData
    if self.selectedData:
      self.linked = True
    else:
      self.selectedData = Vertex(self.em.mouse.pos)

  def onLeftHeld(self):
    if self.selectedData:
      pg.draw.line(self.screen, (100,100,100), self.em.mouse.pos.asTuple(), self.selectedData.pos.asTuple())
      pg.draw.rect(self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
      self.selectedData.draw(self.screen)

  def onLeftRise(self):
    if self.selectedData:
      action = list()
      if not self.linked: action.append(CreateVertex(self.selectedData, self.dm))
      endPoint = self.dm.findNearestVertex(self.em.mouse.pos,10)
      if not endPoint:
        endPoint = Vertex(self.em.mouse.pos)
        action.append(CreateVertex(endPoint,self.dm))
      action.append(CreateLine(Line(endPoint, self.selectedData),self.dm))
      self.ah.do(action)
      self.reset()

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


class CircleMode(Mode):
  """docstring for CircleMode"""
  def __init__(self, frame, em, screen):
    super(CircleMode, self).__init__(frame, em, screen)
    self.linked = False

  def reset(self):
    super().reset()
    self.linked = False

  def onHover(self):
    self.findNearest("v")

  def onLeftFall(self):
    self.selectedData = self.tempData
    if self.selectedData:
      self.linked = True
    else:
      self.selectedData = Vertex(self.em.mouse.pos)

  def onLeftHeld(self):
    if self.selectedData:
      rad = (self.selectedData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      self.selectedData.draw(self.screen)
      pg.draw.circle(self.screen, (100,100,100), self.selectedData.pos.asTuple(), rad, 1)

  def onLeftRise(self):
    if self.selectedData:
      rad = (self.selectedData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      action = [] if self.linked else [CreateVertex(self.selectedData,self.dm)]
      action.append(CreateCircle(Circle(self.selectedData, rad),self.dm))
      self.ah.do(action)
      self.reset()

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


class PillMode(Mode):
  """docstring for PillMode"""
  def __init__(self, frame, em, screen):
    super(PillMode, self).__init__(frame, em, screen)
    self.first = True
    self.geom  = Pill()
    self.action = []

  def reset(self):
    super().reset()
    self.first = True
    self.geom  = Pill()
    self.action = []

  def onHover(self):
    self.findNearest("v")
    if not self.first:
      if not self.selectedData:
        pg.draw.line(self.screen, (100,100,100), self.em.mouse.pos.asTuple(), self.geom.circle1.center.pos.asTuple())
        self.geom.circle1.draw(self.screen)

  def onLeftFall(self):
    self.selectedData = self.tempData
    if not self.selectedData:
      self.selectedData = Vertex(self.em.mouse.pos)
      self.action.append(CreateVertex(self.selectedData,self.dm))

    if self.first:
      self.geom.circle1 = Circle(self.selectedData, 0)
      self.geom.circle1.color = (100,100,100)
    else:
      self.geom.circle2 = Circle(self.selectedData, 0)
      self.geom.circle2.color = (100,100,100)


  def onLeftHeld(self):
    if self.selectedData:
      self.selectedData.draw(self.screen)
      rad = (self.selectedData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      if self.first:
        self.geom.circle1.rad = rad
        self.geom.circle1.draw(self.screen)
      else:
        pg.draw.line(self.screen, (100,100,100), self.geom.circle1.center.pos.asTuple(), self.geom.circle2.center.pos.asTuple())
        self.geom.circle2.rad = rad
        self.geom.circle1.draw(self.screen)
        self.geom.circle2.draw(self.screen)

  def onLeftRise(self):
    if self.selectedData:
      if self.first:
        self.first = False
        self.selectedData = None
      else:
        self.geom.circle1.visible = False
        self.geom.circle2.visible = False
        self.geom.update()
        self.action = self.action + [
          CreateCircle(self.geom.circle1,self.dm),
          CreateCircle(self.geom.circle2,self.dm),
          CreatePill  (self.geom,self.dm)
        ]
        self.ah.do(self.action)
        self.reset()

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