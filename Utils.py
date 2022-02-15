import math

class Vec2(object):
  # def __init__(self, x = 0, y = 0):
  #   super(Vec2, self).__init__()
  #   self.x = x
  #   self.y = y

  def __init__(self, *inp):
    super(Vec2, self).__init__()
    if(not inp): self.set(0,0)
    elif isinstance(inp[0], (int,float)): self.set(inp[0],inp[1])
    elif isinstance(inp[0],  Vec2): self.fromVec2(inp[0])
    elif isinstance(inp[0], tuple): self.fromTuple(inp[0])

  def set(self,x,y):
    self.x = x
    self.y = y
  def fromVec2(self, inp):
    self.x = inp.x
    self.y = inp.y
  def fromTuple(self, inp):
    self.x = inp[0]
    self.y = inp[1]

  def __add__(self, other):
    return Vec2(self.x + other.x, self.y + other.y)
  def __sub__(self, other):
    return Vec2(self.x - other.x, self.y - other.y)
  def __mul__(self, other):
    return self.x * other.x + self.y * other.y
  def cross(self, other):
    return self.x * other.y - self.y * other.x

  def dist(self,other):
    return (other-self).mag()
  def midpoint(self, other):
    return Vec2((self.x + other.x)/2, (self.y + other.y)/2)

  def mag(self):
    return math.sqrt(self*self)

  def asTuple(self):
    return (self.x, self.y)

  def copy(self):
    return Vec2(self.x,self.y)

  def __str__(self):
    return "({},{})".format(self.x,self.y)

class Bool2(object):
  """4-state, 2D Boolean"""
  def __init__(self):
    super(Bool2, self).__init__()
    self.act  = False
    self.wait = False

  def fall(self, inp):
    self.act = inp and not self.wait;
    self.wait = inp;
    return self.act;

  def rise(self, inp):
    self.act = not inp and self.wait;
    self.wait = inp;
    return self.act;

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

  def update(self, inp):
    self.state = inp
    self.fall.fall(inp)
    self.rise.rise(inp)

  def checkHeld(self):
    return self.state
  def checkFall(self):
    return self.fall.check()
  def checkRise(self):
    return self.rise.check()