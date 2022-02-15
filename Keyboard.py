import pygame as pg
from Utils import *

class Keyboard(object):
  """Wrapper for SDL Mouse Control"""
  def __init__(self):
    super(Keyboard, self).__init__()
    self._rawKeys = pg.key.get_pressed()
    self.buttons = [Button() for x in range(len(self._rawKeys))]

  def __getitem__(self, key):
    return self.buttons[key]

  def update(self):
    self._rawKeys = pg.key.get_pressed()
    for i,btn in enumerate(self.buttons):
      btn.update(self._rawKeys[i])