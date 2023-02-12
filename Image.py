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
    self.scale = 1.0
    self.pos = Vec2(SCREEN_SIZE)/2
    self.visible = True
    if path != None:
      self.load(path)

  def reset(self):
    self.visible = True
    self.scale = 1.0
    self.pos = Vec2(SCREEN_SIZE)/2
    self.data = self.data_bkp.copy()

  def copy(self, other):
    img = Image()
    img.data = other.data.copy()
    img.data_bkp = other.data_bkp.copy()
    img.path = other.path
    img.visible = other.visible
    img.scale = other.scale
    img.pos = other.pos
    return img

  def load(self, img_path):
    self.path = img_path
    self.data = pg.image.load(img_path)
    self.data_bkp = self.data.copy()

  def setScale(self, scale):
    if scale <= 0:
      return
    self.scale = scale
    if scale == 1.0:
      self.data = self.data_bkp.copy()
      return
    size = self.data_bkp.get_size()
    self.data = pg.transform.scale(self.data_bkp, (size[0]*scale, size[1]*scale))

  def setPos(self, pos : Vec2):
    self.pos = (pos // self.scale) * self.scale

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

  def makeDict(self):
    return {__class__.__name__ : {
      "path"    : self.path,
      "pos"     : self.pos.asTuple(),
      "scale"   : self.scale,
      "visible" : self.visible
    }}

  @staticmethod
  def fromDict(data):
    if data == None:
      return None
    img =    Image( data["path" ])
    img.pos = Vec2(*data["pos"  ])
    img.setScale  ( data["scale"])
    img.visible =   data["visible"]
    return img