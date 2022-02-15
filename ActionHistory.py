from DataManager import DataManager

class ActionHistory(object):
  """Used for Undo/Redo"""
  def __init__(self):
    super(ActionHistory, self).__init__()
    self.actions = list()
    self.stackptr = -1

  def do(self,action):
    if not isinstance(action, (list,tuple)): action = [action]
    if (self.stackptr < len(self.actions)-1):
      self.actions = self.actions[:self.stackptr+1]
    for each in action:
      each.do();
    self.actions.append(action)
    self.stackptr += 1

  def undo(self):
    if(self.stackptr < 0): return
    for each in self.actions[self.stackptr]:
      each.undo()
    self.stackptr-=1

  def redo(self):
    if (self.stackptr < len(self.actions)-1):
      self.stackptr+=1
      for each in self.actions[self.stackptr]:
        each.do()

  def clear(self):
    self.actions = list()

  def __str__(self):
    ans = str()
    for each in self.actions:
      ans += "{} ".format(each)
    return ans

class CreateVertex(object):
  """docstring for CreateVertex"""
  def __init__(self, vertObj, dataMan):
    super(CreateVertex, self).__init__()
    self.data = vertObj
    self.dataMan = dataMan

  def do(self):
    self.dataMan.add(self.data)

  def undo(self):
    self.dataMan.remove(self.data)

class DeleteVertex(object):
  """docstring for DeleteVertex"""
  def __init__(self, vertObj, dataMan):
    super(DeleteVertex, self).__init__()
    self.vert = vertObj
    self.dataMan = dataMan
    self.lineList = self.dataMan.getLineWith(vertObj)
    self.data = (self.vert, self.lineList)

  def do(self):
    self.dataMan.remove(self.vert)
    for line in self.lineList:
      self.dataMan.remove(line)

  def undo(self):
    self.dataMan.add(self.vert)
    for line in self.lineList:
      self.dataMan.add(line)

class MoveVertex(object):
  """docstring for MoveVertex"""
  def __init__(self, vertObj, newPos, dataMan):
    super(MoveVertex, self).__init__()
    self.data = vertObj
    self.dataMan = dataMan
    self.oldPos = self.data.pos
    self.newPos = newPos

  def do(self):
    self.data.pos = self.newPos.copy()

  def undo(self):
    self.data.pos = self.oldPos


class CreateLine(object):
  """docstring for CreateLine"""
  def __init__(self, lineObj, dataMan):
    super(CreateLine, self).__init__()
    self.data = lineObj
    self.dataMan = dataMan

  def do(self):
    self.dataMan.add(self.data)

  def undo(self):
    self.dataMan.remove(self.data)

class CreateCircle(object):
  """docstring for CreateCircle"""
  def __init__(self, circObj, dataMan):
    super(CreateCircle, self).__init__()
    self.data = circObj
    self.dataMan = dataMan

  def do(self):
    self.dataMan.add(self.data)

  def undo(self):
    self.dataMan.remove(self.data)