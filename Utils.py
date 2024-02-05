import math
import pygame as pg
import struct

SCREEN_SIZE = (1280,960)

class COLOR:
  BLACK   = (0x00, 0x00, 0x00)
  BLUE    = (0x00, 0x00, 0xFF)
  GREEN   = (0x00, 0xFF, 0x00)
  CYAN    = (0x00, 0xFF, 0xFF)
  RED     = (0xFF, 0x00, 0x00)
  MAGENTA = (0xFF, 0x00, 0xFF)
  YELLOW  = (0xFF, 0xFF, 0x00)
  WHITE   = (0xFF, 0xFF, 0xFF)
  GREY    = (0x7F, 0x7F, 0x7F)

  def toInt(r, g, b, a = 0xFF):
    ans = 0
    for ch in (r, g, b, a):
      ans <<= 8
      ans |= ch
    return ans

  def toList(color):
    ans = list()
    for i in range(4):
      ans.append(color & 0xFF)
      color >>= 8
    return ans


def sign(boolean):
  return 1 if boolean else -1

def lerp(a, b, p):
  return (b - a) * p + a

def linspace(start, end, stepCount):
  for i in range(stepCount+1):
    yield lerp(start, end, i/stepCount)

def sigmoid(inp):
    return 1/(1+2.718**(-10 * inp + 5))

class Vec2(object):
  def __init__(self, *inp):
    super(Vec2, self).__init__()
    if(not inp): self.set(0,0)
    elif isinstance(inp[0], (int,float)): self.set(inp[0],inp[1])
    elif isinstance(inp[0],  Vec2): self.fromVec2(inp[0])
    elif isinstance(inp[0], (list,tuple)): self.fromTuple(inp[0])

  def set(self,x,y):
    self.x = x
    self.y = y
  def fromVec2(self, inp):
    self.x = inp.x
    self.y = inp.y
  def fromTuple(self, inp):
    self.x = inp[0]
    self.y = inp[1]


  def addxy(self, x, y):
    return Vec2(self.x + x, self.y + y)

  def add(self, other):
    if isinstance(other, Vec2):
      return Vec2(self.x + other.x, self.y + other.y)
    elif isinstance(other, (list, tuple)):
      s = len(other)
      if s == 0:
        return self.copy()
      elif s < 2:
        return self.add(len[0])
      return Vec2(self.x + other[0], self.y + other[1])
    elif isinstance(other, (int, float)):
      return Vec2(self.x + other, self.y + other)

  def __add__(self, other):
    return self.add(other)
  def __radd__(self, other):
    return self.add(other)

  def iadd(self, x, y):
    self.x += x
    self.y += y

  def __iadd__(self, other):
    self.x += other.x
    self.y += other.y


  def sub(self, other, minuend=True):
    if isinstance(other, Vec2):
      if minuend:
        return Vec2(self.x - other.x, self.y - other.y)
      else:
        return Vec2(other.x - self.x, other.y - self.y)
    elif isinstance(other, (int, float)):
      if minuend:
        return Vec2(self.x - other, self.y - other)
      else:
        return Vec2(other - self.x, other - self.y)
  def __sub__(self, other):
    return self.sub(other, True)
  def __rsub__(self, other):
    return self.sub(other, False)
  def __isub__(self, other):
    self.x -= other.x
    self.y -= other.y


  def dot(self, other):
    return self.x * other.x + self.y * other.y
  def mul(self, other):
    if isinstance(other, Vec2):
      return self.dot(other)
    elif isinstance(other, (int, float)):
      return Vec2(self.x * other, self.y * other)
  def __mul__(self, other):
    return self.mul(other)
  def __rmul__(self, other):
    return self.mul(other)
  def __imul__(self, other):
    self.x *= other.x
    self.y *= other.y


  def __div__(self, other):
    if isinstance(other, (int,float)):
      return Vec2(self.x / other, self.y / other)
  def __truediv__(self, other):
    if isinstance(other, (int,float)):
      return Vec2(self.x / other, self.y / other)
  def __floordiv__(self, other):
      return Vec2(self.x // other, self.y // other)

  def angle(self):
    return math.atan2(self.y, self.x)

  @staticmethod
  def normAtAngle(angle):
    return Vec2(math.cos(angle), math.sin(angle))

  def cross(self, other):
    return self.x * other.y - self.y * other.x

  def sqDist(self,other):
    dv = other-self
    return dv*dv
  def dist(self,other):
    return (other-self).mag()
  def midpoint(self, other):
    return Vec2((self.x + other.x)/2, (self.y + other.y)/2)

  def mag(self):
    return math.sqrt(self*self)
  def norm(self):
    mag = self.mag()
    return self/mag if mag else Vec2(0,0)

  def min(self, x, y):
    return Vec2(max(self.x, x), max(self.y, y))

  def imin(self, x, y):
    self.x = max(self.x, x)
    self.y = max(self.y, y)

  def max(self, x, y):
    return Vec2(min(self.x, x), min(self.y, y))

  def imax(self, x, y):
    self.x = min(self.x, x)
    self.y = min(self.y, y)

  def asTuple(self):
    return (self.x, self.y)

  def asBytes(self):
    fmt = "ii"
    return struct.pack(fmt, int(self.x), int(self.y))

  def toInt(self):
    return Vec2(int(self.x),int(self.y))

  def copy(self):
    return Vec2(self.x,self.y)

  def __str__(self):
    return "({},{})".format(self.x,self.y)

  def lerp(self, other, perc):
    return (other - self) * perc + self

class Bool2(object):
  """4-state, 2D Boolean"""
  def __init__(self):
    super(Bool2, self).__init__()
    self.act  = False
    self.wait = False

  def fall(self, inp):
    self.act = inp and not self.wait
    self.wait = inp
    return self.act

  def rise(self, inp):
    self.act = not inp and self.wait
    self.wait = inp
    return self.act

  def change(self, inp):
    if inp != act:
      act = inp
      return True
    act = inp
    return False

  def check(self):
    return self.act


class Button(object):
  """Button :)"""
  def __init__(self):
    super(Button, self).__init__()
    self.state = False
    self.fall  = Bool2()
    self.rise  = Bool2()
    self.holdSpent = False
    self.fallSpent = False
    self.riseSpent = False

  def anything(self):
    return self.state or self.fall.check() or self.rise.check()

  def update(self, inp):
    self.state = inp
    self.fall.fall(inp)
    self.rise.rise(inp)
    self.holdSpent = False
    self.fallSpent = False
    self.riseSpent = False

  def checkHeld(self):
    return self.state and not self.holdSpent
  def checkFall(self):
    return self.fall.check() and not self.fallSpent
  def checkRise(self):
    return self.rise.check() and not self.riseSpent