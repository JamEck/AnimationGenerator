import pygame as pg
from Utils import *
import math
import traceback as tb
import struct

class Geometry(object):
  """docstring for Geometry"""

  def __init__(self):
    super(Geometry, self).__init__()
    self.color = (200,200,200)
    self.visible = True
    self.id = None
    self.fontSize = 20
    self.font = pg.font.SysFont("monospace", self.fontSize)

  def giveAttr(self,other):
    other.color = self.color # it's okay to do this with tuples
    other.visible = self.visible
    other.id = self.id

  def printText(self, screen, message, pos = (100,100), color = (0xFF,0xFF,0x00)):
    text = self.font.render(str(message), 0, color)
    screen.blit(text, pos)

  def printAttr(self, screen):
    pass

  def makeDict(self):
    return {
      "color"   : COLOR.toInt(*self.color),
      "visible" : self.visible,
      "id"      : self.id
    }

  def fromDictGeom(self, data):
    self.color   = COLOR.toList(data["color"])
    self.visible = data["visible"]
    self.id      = data["id"     ]

# JSON IS STORING REDUNDANT VERTICES
# STORE VERTS FROM HIGHER LEVEL GEOM AS IDS O_NDELAY

# FOR SOME REASON, COLOR IS COMING IN AS TUPLES (ALREADY TRANSLATED FROM INT)


class Vertex(Geometry):
  """docstring for Vertex"""
  def __init__(self, *p):
    super(Vertex, self).__init__()
    self.pos = Vec2(*p)

  def copy(self):
    v = Vertex(self.pos.copy())
    self.giveAttr(v)
    return v

  def set(self,v):
    if isinstance(v, Vec2):
      self.pos = v.toInt()
    if isinstance(v, Vertex):
      self.pos = v.pos.toInt()

  def draw(self, screen, color = None):
    if self.visible:
      if color == None:
        color = self.color
      pg.draw.circle(screen, color, self.pos.asTuple(), 3)

  def printAttr(self, screen):
    self.printText(screen, "Vert: " + str(self.id), self.pos.asTuple())
    self.printText(screen, "Pos: " + str(self.pos), (self.pos + Vec2(0, self.fontSize)).asTuple())

  def makeDict(self):
    return { __class__.__name__ : {
      **super(Vertex, self).makeDict(),
      "pos" : self.pos.asTuple()
    }}

  @staticmethod
  def fromDict(data):
    v = Vertex()
    v.fromDictGeom(data)
    v.pos = Vec2(data["pos"])
    return v

  def asBytes(self):
    return struct.pack("Hxx", self.id) + self.pos.asBytes()

class Line(Geometry):
  """docstring for Line"""
  def __init__(self, p1 = None, p2 = None):
    super(Line, self).__init__()
    self.p1 = p1
    self.p2 = p2
    self.maxlen = 0

  def copy(self):
    l = Line(self.p1.copy(), self.p2.copy())
    self.giveAttr(l)
    return l

  def midpoint(self):
    return self.p1.pos.midpoint(self.p2.pos)

  def draw(self, screen, color = None):
    if self.visible:
      if color == None:
        color = self.color
      pg.draw.line(screen, color, self.p1.pos.asTuple(), self.p2.pos.asTuple())

  def printAttr(self, screen):
    mid = self.midpoint()
    self.printText(screen, "Line: " + str(self.id), mid.asTuple())
    self.printText(screen, "Len : {:.1f}".format(self.p1.pos.dist(self.p2.pos)), (mid + Vec2(0,self.fontSize)).asTuple())
    self.p1.printAttr(screen)
    self.p2.printAttr(screen)

  def restrictLength(self, p):
    if self.maxlen > 0:
      other = self.p2 if self.p1 == p else self.p1
      disp = p.pos - other.pos
      if disp.mag() > self.maxlen:
        p.set(other.pos + disp.norm() * self.maxlen)

  def toVec(self):
    return self.p2.pos - self.p1.pos

  def makeDict(self):
    return { __class__.__name__ : {
      **super(Line, self).makeDict(),
      "p1"     : self.p1.id,
      "p2"     : self.p2.id,
      "maxlen" : self.maxlen
    }}

  @staticmethod
  def fromDict(data):
    l = Line()
    l.fromDictGeom(data)
    l.p1     = data["p1"]
    l.p2     = data["p2"]
    l.maxlen = data["maxlen"]
    return l

  def asBytes(self):
    return struct.pack("HHH", self.id, self.p1.id, self.p2.id)

class Circle(Geometry):
  """docstring for Circle"""
  def __init__(self, pos = None, rad = 100):
    super(Circle, self).__init__()
    self.center = pos
    self.rad = rad
    self.maxRad = 0

  def copy(self):
    c = Circle(self.center.copy(), self.rad)
    self.giveAttr(c)
    return c

  def nearestPoint(self, pos):
    return self.center.pos - (self.center.pos - pos).norm()*self.rad

  def draw(self, screen, color = None):
    if self.visible:
      if color == None:
        color = self.color
      pg.draw.circle(screen, color, self.center.pos.asTuple(), self.rad, 1)

  def printAttr(self, screen):
    nearest = self.nearestPoint(self.center.pos - Vec2(1,1))
    self.printText(screen, "Circ: " + str(self.id), nearest.asTuple())
    self.printText(screen, "Rad: " + str(self.rad), (nearest + Vec2(0, self.fontSize)).asTuple())
    self.center.printAttr(screen)

  def restrictRadius(self):
    if self.maxRad > 0 and self.rad > self.maxRad:
      self.rad = self.maxRad

  def makeDict(self):
    return { __class__.__name__ : {
      **super(Circle, self).makeDict(),
      "center" : self.center.id,
      "rad"    : self.rad,
      "maxRad" : self.maxRad
    }}

  @staticmethod
  def fromDict(data):
    c = Circle()
    c.fromDictGeom(data)
    c.rad    = data["rad"]
    c.maxRad = data["maxRad"]
    c.center = data["center"]
    return c

  def asBytes(self):
    return struct.pack("HHH", self.id, self.rad, self.center.id)

class Pill(Geometry):
  """docstring for Pill"""
  PI = 3.14159265

  def __init__(self, *params):
    super(Pill, self).__init__()
    self.circle1 = None
    self.circle2 = None
    self.angles  = list()
    self.points  = list()
    self.failure = False
    self.overlapCircle = None
    if len(params) == 0: return
    if isinstance(params[0],Circle):
      self.circle1 = params[0]
      self.circle2 = params[1]
    elif isinstance(params[0],Vertex):
      self.circle1 = Circle(params[0], params[1])
      self.circle2 = Circle(params[2], params[3])
    else:
      print("Improper input to pill constructor")
      return
    self.update()

  def copy(self):
    p = Pill(self.circle1.copy(),self.circle2.copy())
    self.giveAttr(p)
    return p


  def sortCircles(self):
    return (self.circle1,self.circle2) if (self.circle1.rad < self.circle2.rad) else (self.circle2,self.circle1)

  def update(self):
    self.angles = self.getAngles()
    self.points = self.getPoints()

    if self.circle1.rad < 2: self.circle1.rad = 2
    if self.circle2.rad < 2: self.circle2.rad = 2

    smaller,larger = self.sortCircles()
    if larger.rad >= (self.circle2.center.pos - self.circle1.center.pos).mag() + smaller.rad:
      larger.visible = True
      self.overlapCircle = larger
    else:
      larger.visible = False
      self.overlapCircle = None


  def getAngles(self):
    mainAngle = (self.circle2.center.pos - self.circle1.center.pos).angle()
    mag   = (self.circle2.center.pos - self.circle1.center.pos).mag()
    ratio = mag if mag == 0 else (self.circle2.rad - self.circle1.rad)/mag
    aot = 0
    try:
      aot = math.asin(ratio)
    except:
      pass
    offset = math.pi/2.0 + aot
    return [-mainAngle + offset, -mainAngle - offset]

  def getPoints(self):
    if len(self.angles) < 2: self.angles = self.getAngles()
    return [
      self.circle1.center.pos + Vec2.normAtAngle(-self.angles[0])*self.circle1.rad,
      self.circle2.center.pos + Vec2.normAtAngle(-self.angles[0])*self.circle2.rad,
      self.circle1.center.pos + Vec2.normAtAngle(-self.angles[1])*self.circle1.rad,
      self.circle2.center.pos + Vec2.normAtAngle(-self.angles[1])*self.circle2.rad
    ]

  def getAxis(self):
    return Line(self.circle1.center,self.circle2.center)

  def draw(self, screen, color = None):
    if self.visible:
      if color == None:
        color = self.color
      if self.overlapCircle:
        self.overlapCircle.draw(screen, color)
        return
      if self.circle1:
        pg.draw.arc(
          screen, color,
          ((self.circle1.center.pos - Vec2(self.circle1.rad,self.circle1.rad)).asTuple(),
          (self.circle1.rad*2, self.circle1.rad*2)),
          self.angles[0], self.angles[1], 2
        )
      if self.circle2:
        pg.draw.arc(
          screen, color,
          ((self.circle2.center.pos - Vec2(self.circle2.rad,self.circle2.rad)).asTuple(),
          (self.circle2.rad*2, self.circle2.rad*2)),
          self.angles[1], self.angles[0], 2
        )
      if len(self.points) >= 4:
        pg.draw.line(screen, color, self.points[0].asTuple(), self.points[1].asTuple(), 2)
        pg.draw.line(screen, color, self.points[2].asTuple(), self.points[3].asTuple(), 2)

  def makeDict(self):
    return { __class__.__name__ : {
      **super(Pill, self).makeDict(),
      "circle1" : self.circle1.id,
      "circle2" : self.circle2.id,
    }}

  @staticmethod
  def fromDict(data):
    p = Pill()
    p.fromDictGeom(data)
    p.circle1 = data["circle1"]
    p.circle2 = data["circle2"]
    return p

  def printAttr(self, screen):
    axis = self.getAxis()
    drawpoint = axis.midpoint()
    self.printText(screen, "Pill: " + str(self.id), drawpoint.asTuple())
    self.printText(screen, "Len : {:.1f}".format(axis.p1.pos.dist(axis.p2.pos)), (drawpoint + Vec2(0,self.fontSize)).asTuple())
    self.circle1.printAttr(screen)
    self.circle2.printAttr(screen)

  def asBytes(self):
    return struct.pack("HHH", self.id, self.circle1.id, self.circle2.id)