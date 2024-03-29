import pygame as pg
from Mouse    import Mouse
from Keyboard import Keyboard, TextEntry
from Text import TextEntryBox
from Utils import Vec2, SCREEN_SIZE
import os

class FileDrop:
  def __init__(self, path, pos):
    self.path = path
    self.pos  = pos

class EventManager(object):
  """Handles all per-frame updates"""
  def __init__(self):
    super(EventManager, self).__init__()
    self.running = True
    self.mouse = Mouse()
    self.keyboard = Keyboard()
    self.console = Console()
    self.file_drop = None
    self.fps = 60
    self.clock = pg.time.Clock()


  def clearTriggers(self):
    self.console.textEntry.clearTriggers()
    self.file_drop = None

  def update(self):
    self.clock.tick(self.fps)
    self.clearTriggers()
    self.mouse.update()

    for event in pg.event.get():

      if event.type == pg.QUIT:
        self.running = False
        return

      if self.console.isActive():
        self.console.textEntry.parse(event)
      else:
        self.keyboard.parse(event)

      if event.type == pg.KEYDOWN:
        if event.key == pg.K_BACKQUOTE:
          self.console.textEntry.start()

      if event.type == pg.DROPFILE:
        x,y = SCREEN_SIZE
        x //= 2; y //= 2
        self.file_drop = FileDrop(event.file, Vec2(x,y))

    self.console.update()
    self.keyboard.update()


class Console(object):
  def __init__(self):
    super(Console, self).__init__()
    self.textEntry = TextEntry()
    self.display   = TextEntryBox(dim = (1280,30), pos = (0,930))

  def getTextEntry(self):
    return str(self.textEntry)

  def getTextEntryPreview(self):
    return self.textEntry.preview()

  def isActive(self):
    return self.textEntry.active

  def update(self):
    if self.textEntry.checkFall():
      self.display.input.setText(self.getTextEntryPreview())

  def checkExecute(self):
    return self.textEntry.checkEnter()

  def draw(self, screen):
    self.display.draw(screen)
