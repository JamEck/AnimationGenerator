import pygame as pg
from Mouse    import Mouse
from Keyboard import Keyboard, TextEntry
from Text import TextEntryBox

class EventManager(object):
  """Handles all per-frame updates"""
  def __init__(self):
    super(EventManager, self).__init__()
    self.running = True
    self.mouse = Mouse()
    self.keyboard = Keyboard()
    self.console = Console()

  def clearTriggers(self):
    self.console.textEntry.clearTriggers()

  def update(self):
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
