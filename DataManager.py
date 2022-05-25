from Geometry import *
from Image import Image

class DataManager(object):
  """docstring for DataManager"""
  def __init__(self):
    super(DataManager, self).__init__()
    self.vertices = list()
    self.lines    = list()
    self.circles  = list()
    self.pills    = list()
    self.font = pg.font.SysFont("monospace", 20)
    self.dataMap = {
      Vertex : self.vertices,
      Line   : self.lines   ,
      Circle : self.circles ,
      Pill   : self.pills
    }
    self.image = None

  def clear(self):
    self.vertices.clear()
    self.lines   .clear()
    self.circles .clear()
    self.pills   .clear()

  def add(self, item):
    try:
      self.assign(item, self.dataMap[type(item)])
    except Exception:
      print("Improper input type! ({})".format(type(item)))

  def remove(self, item):
    try:
      self.dataMap[type(item)].remove(item)
    except Exception:
      print("Improper input type! ({})".format(type(item)))

  def copy(self):
    dm = DataManager()
    for these,those in zip(self.dataMap.values(), dm.dataMap.values()):
      for each in these: those.append(each.copy())
    self._link(dm)
    return dm

  def copy_from(self, other):
    for these,those in zip(self.dataMap.values(), other.dataMap.values()):
      for each in those: 
        these.append(each.copy())
    other._link(self)

  def findByID(self, array, id):
    for each in array:
      if id == each.id:
        return each
    return None

  def _link(self, other):
    for i in range(len(self.lines)):
      other.lines[i].p1 = self.findByID(other.vertices,self.lines[i].p1.id)
      other.lines[i].p2 = self.findByID(other.vertices,self.lines[i].p2.id)
    for i in range(len(self.circles)):
      other.circles[i].center = self.findByID(other.vertices,self.circles[i].center.id)
    for i in range(len(self.pills)):
      other.pills[i].circle1 = self.findByID(other.circles,self.pills[i].circle1.id)
      other.pills[i].circle2 = self.findByID(other.circles,self.pills[i].circle2.id)

  @staticmethod
  def assign(item, array):
    newid = len(array)
    for each in range(len(array)):
      if each != array[each].id:
        newid = each
        break
    item.id = newid
    array.insert(newid, item)

  @staticmethod
  def shiftIds(array):
    for i,item in enumerate(array):
      item.id = i

  def get(self, cls):
    try:
      cls.__name__
      return self.dataMap[cls]
    except AttributeError:
      print("Input is not a class type")
    except Exception:
      print("Improper input type! ({})".format(cls))
    return None

  def getPickles(self):
    return (
      tuple(each.getPickles() for each in self.vertices),
      tuple(each.getPickles() for each in self.lines),
      tuple(each.getPickles() for each in self.circles),
      tuple(each.getPickles() for each in self.pills),
      self.image
    )

  @staticmethod
  def readPickles(data):
    dm = DataManager()
    for vert in data[0]: dm.vertices.append(Vertex.readPickles(vert))
    for line in data[1]: dm.lines   .append(Line  .readPickles(line))
    for circ in data[2]: dm.circles .append(Circle.readPickles(circ))
    for pill in data[3]: dm.pills   .append(Pill  .readPickles(pill))
    dm.image = data[4]
    dm._link(dm)
    return dm

  def loadImageDrop(self, file_drop):
    self.image = Image(file_drop.path)
    self.image.pos = file_drop.pos

  @staticmethod
  def sqDist(p1,p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return dx*dx+dy*dy

  @staticmethod
  def distFromCircle(point,circle):
    dist  = (point - circle.center.pos).mag()
    dist -= circle.rad
    return dist

  @staticmethod
  def distFromLine(point,line):
    lineDir = Vec2(line.p2.pos.x - line.p1.pos.x, line.p2.pos.y - line.p1.pos.y)
    d1      = Vec2(point.x - line.p1.pos.x, point.y - line.p1.pos.y)
    d2      = Vec2(point.x - line.p2.pos.x, point.y - line.p2.pos.y)
    if d1*lineDir < 0:
      return point.dist(line.p1.pos)
    if d2*lineDir > 0:
      return point.dist(line.p2.pos)
    lineLen = lineDir.mag()
    return 0 if lineLen == 0 else lineDir.cross(d1)/lineLen

  def findNearestVertex(self, pos, maxDist = -1):
    if len(self.vertices) < 1: return None
    ans = self.vertices[0]
    minDist = self.sqDist(pos, self.vertices[0].pos)
    for vert in self.vertices:
      dist = self.sqDist(pos, vert.pos)
      if dist < minDist:
        minDist = dist
        ans = vert
    return ans if (minDist <= maxDist*maxDist or maxDist == -1) else None

  def findNearestLine(self, pos, maxDist = -1):
    if len(self.lines) < 1: return None
    ans = self.lines[0]
    minDist = self.distFromLine(pos, self.lines[0])
    if minDist < 0: minDist = -minDist
    for line in self.lines:
      dist = self.distFromLine(pos, line)
      if dist < 0: dist = -dist
      if dist < minDist:
        minDist = dist
        ans = line
    return ans if (minDist <= maxDist or maxDist == -1) else None

  def findNearestCircle(self, pos, maxDist = -1):
    if len(self.circles) < 1: return None
    ans = self.circles[0]
    minDist = self.distFromCircle(pos, self.circles[0])
    if minDist < 0: minDist = -minDist
    for circ in self.circles:
      dist = self.distFromCircle(pos, circ)
      if dist < 0: dist = -dist
      if dist < minDist:
        minDist = dist
        ans = circ
    return ans if (minDist <= maxDist or maxDist == -1) else None

  def findNearestPill(self, pos, maxDist = -1):
    if len(self.pills) < 1: return None
    ans = self.pills[0]
    edge = Line(Vertex(self.pills[0].points[0]), Vertex(self.pills[0].points[1]))
    minDist = self.distFromLine(pos, edge)
    if minDist < 0: minDist = -minDist
    for pill in self.pills:
      edge = Line(Vertex(pill.points[0]), Vertex(pill.points[1]))
      dist = self.distFromLine(pos, edge)
      if dist < 0: dist = -dist
      if dist < minDist:
        minDist = dist
        ans = pill
      edge = Line(Vertex(pill.points[2]), Vertex(pill.points[3]))
      dist = self.distFromLine(pos, edge)
      if dist < 0: dist = -dist
      if dist < minDist:
        minDist = dist
        ans = pill
    return ans if (minDist <= maxDist or maxDist == -1) else None

  def getVertex(self, index):
    return self.vertices[index]
  def getLine(self, index):
    return self.lines[index]
  def getCircle(self, index):
    return self.circles[index]
  def getPills(self, index):
    return self.pils[index]

  def getLineWith(self, objRef):
    if len(self.lines) < 1: return list()
    results = list()
    if isinstance(objRef, Vertex):
      for line in self.lines:
        if (objRef == line.p1 or objRef == line.p2):
          results.append(line)
    return results

  def getCircleWith(self, objRef):
    if len(self.circles) < 1: return list()
    results = list()
    if isinstance(objRef, Vertex):
      for circle in self.circles:
        if (objRef == circle.center or
            objRef == circle.center
        ):
          results.append(circle)

    return results

  def getPillWith(self, objRef):
    if len(self.pills) < 1: return list()
    results = list()
    if isinstance(objRef, Vertex):
      for pill in self.pills:
        if (objRef == pill.circle1.center or
            objRef == pill.circle2.center
        ):
          results.append(pill)
    elif isinstance(objRef, Circle):
      for pill in self.pills:
        if (objRef == pill.circle1 or
            objRef == pill.circle2
        ):
          results.append(pill)

    return results

  def draw_image(self, screen):
    if self.image != None:
      self.image.draw(screen)

  def draw(self, screen, color = None):
    if color == None: color = (255,255,255)
    for p in self.pills:
      p.draw(screen, color)
    for c in self.circles:
      c.draw(screen, color)
    for l in self.lines:
      l.draw(screen, color)
    for v in self.vertices:
      v.draw(screen, color)

  def drawInfo(self, screen):
    pos = Vec2(20,80)
    text = self.font.render("Vertices| " + str(len(self.vertices)), 0, (255,255,255))
    screen.blit(text, pos.asTuple()); pos.y += 20
    text = self.font.render("Lines   | " + str(len(self.lines   )), 0, (255,255,255))
    screen.blit(text, pos.asTuple()); pos.y += 20
    text = self.font.render("Circles | " + str(len(self.circles )), 0, (255,255,255))
    screen.blit(text, pos.asTuple()); pos.y += 20
    text = self.font.render("Pills   | " + str(len(self.pills   )), 0, (255,255,255))
    screen.blit(text, pos.asTuple())
