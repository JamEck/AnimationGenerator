import pygame as pg
from Utils import *


class Keyboard(object):
  """Wrapper for SDL Mouse Control"""

  keyList = [
    pg.K_s, pg.K_v, pg.K_l, pg.K_c, pg.K_p, pg.K_z, pg.K_w,
    pg.K_ESCAPE, pg.K_LCTRL, pg.K_LSHIFT, pg.K_RETURN,
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
  def __init__(self):
    pg.key.stop_text_input()
    self.active = False
    self.buffer = list()
    self.result = str()

  def start(self):
    pg.key.start_text_input()
    self.active = True
    self.buffer = list()

  def cancel(self):
    pg.key.stop_text_input()
    self.buffer = list()
    self.active = False

  def update(self):
    self.result = self.preview()
    self.cancel()

  def parse(self, event):
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_RETURN:
        self.update()
        return
      elif event.key == pg.K_ESCAPE:
        self.cancel()
        return
      elif event.key == pg.K_BACKSPACE:
        self.backspace()
        return

    if event.type == pg.TEXTINPUT:
      if '`' in event.text:
        return
      self.append(event.text)

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

