import pygame as pg
from Utils import *

class Geometry(object):
  """docstring for Geometry"""
  def __init__(self):
    super(Geometry, self).__init__()
    self.color = (200,200,200)
    self.visible = True


class Vertex(Geometry):
  """docstring for Vertex"""
  def __init__(self, *p):
    super(Vertex, self).__init__()
    self.pos = Vec2(*p)

  def draw(self, screen):
    pg.draw.circle(screen, self.color, self.pos.asTuple(), 3)


class Line(Geometry):
  """docstring for Line"""
  def __init__(self, p1, p2):
    super(Line, self).__init__()
    self.p1 = p1
    self.p2 = p2

  def midpoint(self):
    return self.p1.pos.midpoint(self.p2.pos)

  def draw(self, screen):
    pg.draw.line(screen, self.color, self.p1.pos.asTuple(), self.p2.pos.asTuple())


class Circle(Geometry):
  """docstring for Circle"""
  def __init__(self, pos, rad = 100):
    super(Circle, self).__init__()
    self.center = pos
    self.rad = rad

  def draw(self, screen):
    pg.draw.circle(screen, self.color, self.center.pos.asTuple(), self.rad, 1)