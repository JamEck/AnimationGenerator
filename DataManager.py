from Geometry import *

class DataManager(object):
  """docstring for DataManager"""
  def __init__(self):
    super(DataManager, self).__init__()
    self.vertices  = list()
    self.lines    = list()
    self.circles = list()
    self.pills  = list()
    self.font = pg.font.SysFont("monospace", 20)

  def add(self, item):
    if  (isinstance(item, Vertex)): self.vertices.append(item)
    elif(isinstance(item, Line  )): self.   lines.append(item)
    elif(isinstance(item, Circle)): self. circles.append(item)
    elif(isinstance(item, Pill  )): self.   pills.append(item)
    else: print("Improper input type!")

  def remove(self, item):
    if  (isinstance(item, Vertex)): self.vertices.remove(item)
    elif(isinstance(item, Line  )): self.   lines.remove(item)
    elif(isinstance(item, Circle)): self. circles.remove(item)
    elif(isinstance(item, Pill  )): self.   pills.remove(item)
    else: print("Improper input type!")

  def get(self, key):
    if  (key == "vertex"): return self.vertices
    elif(key ==   "line"): return self.lines
    elif(key == "circle"): return self.circles
    elif(key ==   "pill"): return self.pills
    return None

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
    text = self.font.render("Vertices| " + str(len(self.vertices)), 0, (255,255,255))
    screen.blit(text, (20, 80))
    text = self.font.render("Lines   | " + str(len(self.lines   )), 0, (255,255,255))
    screen.blit(text, (20, 100))
    text = self.font.render("Circles | " + str(len(self.circles )), 0, (255,255,255))
    screen.blit(text, (20, 120))
    text = self.font.render("Pills   | " + str(len(self.pills   )), 0, (255,255,255))
    screen.blit(text, (20, 140))