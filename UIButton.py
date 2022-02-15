import pygame as pg
from Utils import *
from Mouse import Mouse

class UIButton(Button):
  """docstring for UIButton"""

  @staticmethod
  def doNothing(data = None): pass
  def moveMe(self, mouse):
    offset = mouse.clickPos - self.pos
    self.pos = mouse.pos - offset
    mouse.clickPos = mouse.pos.copy()

  def __init__(self, pos = (0,0), dim = (100,100)):
    super(UIButton, self).__init__()
    self.dim = Vec2(dim)
    self.pos = Vec2(pos)
    self.upColor   = (100,100,100)
    self.downColor = (200,200,200)
    self.onFall = self.doNothing
    self.onRise = self.doNothing
    self.onHeld = self.doNothing
    self.dataFall = None
    self.dataRise = None
    self.dataHeld = None

  def setUpColor  (self,*color): self.upColor   = tuple(color)
  def setDownColor(self,*color): self.downColor = tuple(color)
  def setPos(self,x,y): self.pos = Vec2(x,y)
  def setDim(self,w,h): self.dim = Vec2(w,h)

  def checkInside(self, pos):
    return (
      pos.x > self.pos.x and
      pos.y > self.pos.y and
      pos.x < self.pos.x + self.dim.x and
      pos.y < self.pos.y + self.dim.y
    )

  def update(self, mouse):
    super().update(mouse.checkHeld() and self.checkInside(mouse.clickPos))
    if self.checkFall (): self.onFall(self.dataFall);
    if self.checkRise (): self.onRise(self.dataRise);
    if self.checkHeld(): self.onHeld(self.dataHeld);

  def draw(self, screen, pos = None):
    if (pos != None): self.pos = pos.copy()
    color = self.downColor if self.checkHeld() else self.upColor
    pg.draw.rect(screen, color, (self.pos.asTuple(),self.dim.asTuple()))

  def __str__(self):
    return "Pos: {}, Dim: {}".format(self.pos.asTuple(), self.dim.asTuple())