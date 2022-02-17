from typing import Iterable
import pygame as pg
from setuptools import setup
from Utils import *
from Mouse import Mouse

class UIButton(Button, TextBox):
  """docstring for UIButton"""

  DEFAULT_UP_COLOR   = (100,100,100)
  DEFAULT_DOWN_COLOR = (200,200,200)

  @staticmethod
  def doNothing(data = None): pass
  def moveMe(self, mouse):
    offset = mouse.clickPos - self.pos
    self.pos = mouse.pos - offset
    mouse.clickPos = mouse.pos.copy()

  def __init__(self, pos = (0,0), dim = (100,100), text = str()):
    Button.__init__(self)

    TextBox.__init__(self, text, dim = dim, pos = pos)
    self.upColor   = UIButton.DEFAULT_UP_COLOR
    self.downColor = UIButton.DEFAULT_DOWN_COLOR
    self.onFall = self.doNothing
    self.onRise = self.doNothing
    self.onHeld = self.doNothing
    self.dataFall = None
    self.dataRise = None
    self.dataHeld = None

  def setUpColor  (self,*color): self.upColor   = tuple(color)
  def setDownColor(self,*color): self.downColor = tuple(color)
  def setPos(self,x,y): self.pos = Vec2(x,y)

  def resetDownColor(self):
    self.setDownColor(UIButton.DEFAULT_DOWN_COLOR)

  def resetUpColor(self):
    self.setUpColor(UIButton.DEFAULT_UP_COLOR)

  def checkInside(self, pos):
    return (
      pos.x > self.pos.x and
      pos.y > self.pos.y and
      pos.x < self.pos.x + self.dim.x and
      pos.y < self.pos.y + self.dim.y
    )

  def update(self, mouse):
    super().update(mouse.checkHeld() and self.checkInside(mouse.clickPos))

    if self.checkFall():
      mouse.left.fallSpent = True
      if isinstance(self.dataFall, Iterable):
        self.onFall(*self.dataFall)
      else:
        self.onFall(self.dataFall)

    if self.checkRise():
      mouse.left.riseSpent = True
      if isinstance(self.dataRise, Iterable):
        self.onRise(*self.dataRise)
      else:
        self.onRise(self.dataRise)

    if self.checkHeld():
      mouse.left.holdSpent = True
      if isinstance(self.dataHeld, Iterable):
        self.onHeld(*self.dataHeld)
      else:
        self.onHeld(self.dataHeld)

  def draw(self, screen):
    color = self.downColor if self.checkHeld() else self.upColor
    pg.draw.rect(screen, color, (self.pos.asTuple(),self.dim.asTuple()))
    TextBox.draw(self, screen)

  def __str__(self):
    return "Pos: {}, Dim: {}, Text: \"{}\"".format(self.pos.asTuple(), self.dim.asTuple(), self.text)