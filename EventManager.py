import pygame as pg
from Mouse    import Mouse
from Keyboard import Keyboard

class EventManager(object):
  """Handles all per-frame updates"""
  def __init__(self):
    super(EventManager, self).__init__()
    self.running = True
    self.mouse = Mouse()
    self.keyboard = Keyboard()
    self.buttons = list() # array for managing UI Buttons

  def update(self):
    self.mouse.update()
    self.keyboard.update()
    for event in pg.event.get():
      if event.type == pg.QUIT:
        self.running = False
    if self.keyboard[pg.K_w].checkFall():
      if self.keyboard[pg.K_LCTRL].checkHeld():
        self.running = False