import pygame as pg
from Utils import *


class Keyboard(object):
  """Wrapper for SDL Mouse Control"""

  keyList = [
    pg.K_s, pg.K_v, pg.K_i, pg.K_l, pg.K_c, pg.K_p, pg.K_z, pg.K_w, pg.K_d,
    pg.K_ESCAPE, pg.K_LCTRL, pg.K_LSHIFT, pg.K_RETURN, pg.K_DELETE,
    pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN
  ]
  dummyBtn = Button()

  def __init__(self):
    super(Keyboard, self).__init__()
    self.buttons = { key : Button() for key in Keyboard.keyList }

  def __getitem__(self, key):
    return self.buttons.get(key, Keyboard.dummyBtn)

  def parse(self, event):
    if event.type == pg.KEYDOWN:
      self.set(event.key, True)
    elif event.type == pg.KEYUP:
      self.set(event.key, False)

  def set(self, key, inp):
    try:
      self.buttons[key].state = inp # jank
    except:
      pass

  def update(self):
    for key,button in self.buttons.items():
      button.update(button.state)


class TextEntry:
  HISTORY_LEN = 20

  def __init__(self):
    self.active     = False
    self.buffer     = list()
    self.tempbuffer = list()
    self.result     = str()
    self.history    = list()
    self.historyIndex = -1
    self.keyTrig    = False
    self.enterTrig  = False

  def start(self):
    self.active = True
    self.buffer = list()

  def cancel(self):
    self.buffer = list()
    self.historyIndex = -1
    self.active = False

  def enter(self):
    self.result = self.preview()
    self.enterTrig = True
    self.historyIndex = -1
    if len(self.buffer) > 0:
      self.history.insert(0, self.buffer.copy())
      if len(self.history) > TextEntry.HISTORY_LEN:
        del self.history[-1]
    self.cancel()

  def historyBack(self):
    if self.historyIndex == -1:
      self.tempbuffer = self.buffer.copy()
    self.historyIndex = min(self.historyIndex + 1, len(self.history) - 1)
    self.buffer = self.history[self.historyIndex].copy()

  def historyForward(self):
    self.historyIndex = max(self.historyIndex - 1, -1)
    if self.historyIndex == -1:
      self.buffer = self.tempbuffer.copy()
    else:
      self.buffer = self.history[self.historyIndex].copy()

  def get(self):
    return str(self)

  def checkEnter(self):
    return self.enterTrig

  def checkFall(self):
    return self.keyTrig

  def clearTriggers(self):
    self.keyTrig   = False
    self.enterTrig = False

  def parse(self, event):
    if event.type == pg.KEYDOWN:
      self.keyTrig = True
      if event.key == pg.K_RETURN:
        self.enter()
        return
      elif event.key == pg.K_ESCAPE:
        self.cancel()
        return
      elif event.key == pg.K_BACKSPACE:
        self.backspace()
        return
      elif event.key == pg.K_UP:
        self.historyBack()
        return
      elif event.key == pg.K_DOWN:
        self.historyForward()
        return
      elif event.unicode:
        self.append(event.unicode)


  def append(self, inp):
    if isinstance(inp, (list, tuple)):
      self.buffer += inp
    else:
      self.buffer.append(inp)

  def backspace(self):
    self.buffer = self.buffer[:-1]

  def preview(self):
    return ''.join(self.buffer)

  def __str__(self):
    return self.result

  def __bool__(self):
    return self.active

