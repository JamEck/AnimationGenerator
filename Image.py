import pygame as pg
from Utils import *
import math

class Image(object):
  """docstring for Image"""

  def __init__(self, path = None):
    super(Image, self).__init__()
    self.path = str()
    self.data = None
    self.data_bkp = None
    self.pos = Vec2(SCREEN_SIZE)/2
    self._scale = 1.0
    self.visible = True
    if path != None:
      self.load(path)

  def reset(self):
    self.visible = True
    self.pos = Vec2(SCREEN_SIZE)/2
    self.data = self.data_bkp.copy()
    self._scale = 1.0

  def copy(self, other):
    img = Image()
    img.data = other.data.copy()
    img.data_bkp = other.data_bkp.copy()
    img.path = other.path
    img.visible = other.visible
    img.pos = other.pos
    img._scale = other._scale
    return img

  def load(self, img_path):
    self.path = img_path
    self.data = pg.image.load(img_path)
    self.data_bkp = self.data.copy()

  def setScale(self, scale):
    if scale <= 0:
      return
    self._scale = scale
    if scale == 1.0:
      self.data = self.data_bkp.copy()
      return
    size = self.data_bkp.get_size()
    self.data = pg.transform.scale(self.data_bkp, (size[0]*scale, size[1]*scale))

  def size(self):
    return Vec2(self.data.get_size())

  def get_bounding_box(self):
    halfsize = self.size()/2
    return (self.pos - halfsize, self.pos + halfsize)

  def get_rect(self):
    return ((self.pos - self.size()/2).asTuple(), self.size().asTuple())

  def contains_point(self, p):
    UL, BR = self.get_bounding_box()
    return (
      p.x >= UL.x and
      p.y >= UL.y and
      p.x <= BR.x and
      p.y <= BR.y
    )

  def draw(self, screen):
    if self.visible:
      screen.blit(self.data, (self.pos - self.size()/2).asTuple())

  @staticmethod
  def load_from_path(img_path):
    return pg.image.load(img_path)

  def getPickles(self):
    return ( self.path, self.pos, self._scale, self.visible )

  @staticmethod
  def readPickles(data):
    if data == None:
      return None
    img = Image  (data[0])
    img.pos     = data[1]
    img.setScale (data[2])
    img.visible = data[3]
    return img