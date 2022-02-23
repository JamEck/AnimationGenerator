import pygame as pg
from Utils import *


class Text(object):

  DEFAULT_TEXT_COLOR = COLOR.WHITE
  DEFAULT_TEXT_SIZE  = 20

  def __init__(self, text = str(), size = 0, pos = (0,0)):
    self.pos = Vec2(pos)
    self._set(text)
    self._setColor(Text.DEFAULT_TEXT_COLOR)
    self._setFontSize(size)
    self.updateTextRender()

  def _set(self, text):
    if isinstance(text, str):
      self.text = text

  def set(self, text):
    self._set(text)
    self.updateTextRender()

  def _setFontSize(self, size):
    self.size = Text.DEFAULT_TEXT_SIZE if size < 1 else size
    self.font = pg.font.SysFont("monospace", self.size)

  def setFontSize(self, size):
    self._setFontSize(size)
    self.updateTextRender()

  def _setColor(self, color):
    if isinstance(color, (tuple, list)):
      self.color = color

  def setColor(self, color):
    self._setColor(color)
    self.updateTextRender()

  def resetColor(self):
    self.setColor(Text.DEFAULT_TEXT_COLOR)

  def updateTextRender(self):
    self.textrender = self.font.render(self.text, 0, self.color)

  def draw(self, screen, pos_off = None):
    pos = self.pos + pos_off if pos_off else self.pos
    if self.text:
      screen.blit(self.textrender, pos.asTuple())

  def __bool__(self):
    return bool(self.text)

class TextBox(object):
  BORDER_BUFFER = 3
  DEFAULT_BOX_COLOR  = COLOR.GREY

  def __init__(self, text = str(), dim = (100,50), pos = (0,0)):
    self.pos = Vec2(pos)
    self.text = Text(text = text, pos = (TextBox.BORDER_BUFFER,0))
    self.drawBox  = True
    self.boxColor = TextBox.DEFAULT_BOX_COLOR
    self.dim  = Vec2(dim)
    self.fitFontSizeToDims()

  def fitFontSizeToDims(self):
    letterCount = len(self.text.text)
    if letterCount == 0: letterCount = 1
    fontsize = int((self.dim.x - TextBox.BORDER_BUFFER) / letterCount * 8 / 5)
    fontsize = min(fontsize, self.dim.y - TextBox.BORDER_BUFFER)
    self.text.setFontSize(fontsize)

  def toggleOutline(self, inp):
    self.drawBox = inp

  def setBoxColor(self, color):
    self.boxColor = color

  def resetBoxColor(self):
    self.setBoxColor(TextBox.DEFAULT_BOX_COLOR)

  def setText(self, text):
    self.text._set(text)
    self.fitFontSizeToDims()
  
  def setDim(self,w,h):
    self.dim = Vec2(w,h)
    self.fitFontSizeToDims()

  def incDim(self,w,h):
    self.dim.iadd(w,h)
    self.fitFontSizeToDims()

  def draw(self, screen):
    pg.draw.rect(screen, self.boxColor, (self.pos.asTuple(), self.dim.asTuple()), sign(self.drawBox))
    self.text.draw(screen, self.pos)

  def __bool__(self):
    return self.text.__bool__()
