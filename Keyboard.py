import pygame as pg
from Utils import *

class Keyboard(object):
  """Wrapper for SDL Mouse Control"""

  keyList = [
    pg.K_s, pg.K_v, pg.K_l, pg.K_c, pg.K_p, pg.K_z,
    pg.K_ESCAPE, pg.K_LCTRL, pg.K_LSHIFT,
    pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN
  ]
  dummyBtn = Button()

  def __init__(self):
    super(Keyboard, self).__init__()
    self.buttons = { key : Button() for key in Keyboard.keyList }
  def __getitem__(self, key):
    return self.buttons.get(key, Keyboard.dummyBtn)

  def update(self):
    self._rawKeys = pg.key.get_pressed()
    for key in Keyboard.keyList:
      self.buttons[key].update(self._rawKeys[key])