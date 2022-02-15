import pygame as pg
from Utils import *

class Mouse(object):
  """Wrapper for SDL Mouse Control"""
  def __init__(self):
    super(Mouse, self).__init__()
    self.left   = Button()
    self.middle = Button()
    self.right  = Button()
    self.pos    = Vec2(0,0)
    self.clickPos = Vec2(0,0)

  def update(self):
    self.pos.x, self.pos.y = pg.mouse.get_pos()
    l,m,r = pg.mouse.get_pressed()
    self.left  .update(l)
    self.middle.update(m)
    self.right .update(r)
    if self.checkFall():
      self.clickPos = self.pos.copy()

  def checkFall(self):
    return (self.left.checkFall() or
            self.right.checkFall() or
            self.middle.checkFall()
    )
  def checkHeld(self):
    return (self.left.checkHeld() or
            self.right.checkHeld() or
            self.middle.checkHeld()
    )

  def __str__(self):
    ans =  "state/fall/rise: {} {} {}".format(
      1 if self.left  .checkHeld() else 0,
      1 if self.middle.checkHeld() else 0,
      1 if self.right .checkHeld() else 0
    )
    ans +=  " , {} {} {}".format(
      1 if self.left  .checkFall() else 0,
      1 if self.middle.checkFall() else 0,
      1 if self.right .checkFall() else 0
    )
    ans += " , {} {} {}".format(
      1 if self.left  .checkRise() else 0,
      1 if self.middle.checkRise() else 0,
      1 if self.right .checkRise() else 0
    )
    return ans