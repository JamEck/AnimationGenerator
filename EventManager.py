import pygame as pg
from Mouse    import Mouse
from Keyboard import Keyboard, TextEntry


class EventManager(object):
  """Handles all per-frame updates"""
  def __init__(self):
    super(EventManager, self).__init__()
    self.running = True
    self.mouse = Mouse()
    self.keyboard = Keyboard()
    self.textEntry = TextEntry()

  def getTextEntry(self):
    return str(self.textEntry)

  def getTextEntryPreview(self):
    return self.textEntry.preview()

  def update(self):
    self.mouse.update()

    for event in pg.event.get():

      if event.type == pg.QUIT:
        self.running = False
        return

      if event.type == pg.KEYDOWN:
        if event.key == pg.K_BACKQUOTE:
          self.textEntry.start()

      if self.textEntry.active:
        self.textEntry.parse(event)
      else:
        self.keyboard.parse(event)

    self.keyboard.update()










