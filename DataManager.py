from Geometry import *

class DataManager(object):
  """docstring for DataManager"""
  def __init__(self):
    super(DataManager, self).__init__()
    self.vertices  = list()
    self.lines    = list()
    self.circles = list()

  def add(self, item):
    if  (isinstance(item,Vertex)): self.vertices.append(item)
    elif(isinstance(item,Line  )): self.   lines.append(item)
    elif(isinstance(item,Circle)): self. circles.append(item)
    else: print("Improper input type!")

  def remove(self, item):
    if  (isinstance(item,Vertex)): self.vertices.remove(item)
    elif(isinstance(item,Line  )): self.   lines.remove(item)
    elif(isinstance(item,Circle)): self. circles.remove(item)
    else: print("Improper input type!")

  @staticmethod
  def sqDist(p1,p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return dx*dx+dy*dy

  @staticmethod
  def distFromLine(point,line):
    lineDir = Vec2(line.p2.pos.x - line.p1.pos.x, line.p2.pos.y - line.p1.pos.y)
    d1      = Vec2(point.x - line.p1.pos.x, point.y - line.p1.pos.y)
    d2      = Vec2(point.x - line.p2.pos.x, point.y - line.p2.pos.y)
    if d1*lineDir < 0:
      return point.dist(line.p1.pos)
    if d2*lineDir > 0:
      return point.dist(line.p2.pos)
    return lineDir.cross(d1)/lineDir.mag()

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


  def getVertex(self, index):
    return self.vertices[index]
  def getLine(self, index):
    return self.lines[index]
  def getCircle(self, index):
    return self.circles[index]

  def getLineWith(self, objRef):
    if len(self.lines) < 1: return list()
    results = list()
    for line in self.lines:
      if (objRef == line.p1 or objRef == line.p2):
        results.append(line)
    return results

  def draw(self, screen):
    for c in self.circles:
      c.draw(screen)
    for l in self.lines:
      l.draw(screen)
    for v in self.vertices:
      v.draw(screen)