from DataManager import DataManager

class ActionHistory(object):
  """Used for Undo/Redo"""
  def __init__(self):
    super(ActionHistory, self).__init__()
    self.actions = list()
    self.stackptr = -1

  def copy(self):
    return ActionHistory()

  def do(self,action):
    if not isinstance(action, (list,tuple)): action = [action]
    if (self.stackptr < len(self.actions)-1):
      self.actions = self.actions[:self.stackptr+1]
    for each in action:
      each.do()
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

class Action(object):
  """docstring for Action"""
  def __init__(self, obj, dataMan):
    super(Action, self).__init__()
    self.data = obj
    self.dataMan = dataMan

class Creation(Action):
  """docstring for Creation"""
  def __init__(self, obj, dataMan):
    super(Creation, self).__init__(obj, dataMan)

  def do(self):
    self.dataMan.add(self.data)

  def undo(self):
    self.dataMan.remove(self.data)

class CreateVertex(Creation):
  """docstring for CreateVertex"""
  def __init__(self, vertObj, dataMan):
    super(CreateVertex, self).__init__(vertObj, dataMan)

class DeleteVertex(Action):
  """docstring for DeleteVertex"""
  def __init__(self, vertObj, dataMan):
    super(DeleteVertex, self).__init__(vertObj, dataMan)
    self.vert = vertObj
    self.deleteList = (
      self.dataMan.getLineWith(vertObj)   +
      self.dataMan.getCircleWith(vertObj) +
      self.dataMan.getPillWith(vertObj)
    )
    self.data = (self.vert, self.deleteList)

  def do(self):
    self.dataMan.remove(self.vert)
    for each in self.deleteList:
      self.dataMan.remove(each)

  def undo(self):
    self.dataMan.add(self.vert)
    for each in self.deleteList:
      self.dataMan.add(each)


class CreateLine(Creation):
  """docstring for CreateLine"""
  def __init__(self, lineObj, dataMan):
    super(CreateLine, self).__init__(lineObj, dataMan)

class DeleteLine(Action):
  """docstring for DeleteLine"""
  def __init__(self, lineObj, dataMan):
    super(DeleteLine, self).__init__(lineObj, dataMan)

  def do(self):
    self.dataMan.remove(self.data)

  def undo(self):
    self.dataMan.add(self.data)



class CreateCircle(Creation):
  """docstring for CreateCircle"""
  def __init__(self, circObj, dataMan):
    super(CreateCircle, self).__init__(circObj, dataMan)


class DeleteCircle(Action):
  """docstring for DeleteCircle"""
  def __init__(self, circObj, dataMan):
    self.circle = circObj
    self.pills = dataMan.getPillWith(circObj)
    self.survingCircles = [
      each.circle2
      if self.circle == each.circle1 else
      each.circle1 for each in self.pills
    ]
    super(DeleteCircle, self).__init__((self.circle, self.survingCircles, self.pills), dataMan)

  def do(self):
    for each in self.pills:
      self.dataMan.remove(each)
    self.dataMan.remove(self.circle)
    for each in self.survingCircles:
      each.visible = True

  def undo(self):
    self.dataMan.add(self.circle)
    for each in self.pills:
      self.dataMan.add(each)
    for each in self.survingCircles:
      each.visible = False


class CreatePill(Creation):
  """docstring for CreatePill"""
  def __init__(self, pillObj, dataMan):
    super(CreatePill, self).__init__(pillObj, dataMan)


class MoveVertex(Action):
  """docstring for MoveVertex"""
  def __init__(self, vertObj, newPos, dataMan):
    super(MoveVertex, self).__init__(vertObj, dataMan)
    self.oldPos = self.data.pos
    self.newPos = newPos.copy()

  def do(self):
    self.data.pos = self.newPos.copy()
    for each in self.dataMan.getLineWith(self.data): each.restrictLength(self.data)
    for each in self.dataMan.getPillWith(self.data): each.update()

  def undo(self):
    self.data.pos = self.oldPos
    for each in self.dataMan.getPillWith(self.data): each.update()

class ResizeCircle(Action):
  """docstring for ResizeCircle"""
  def __init__(self, circObj, newRad, dataMan):
    super(ResizeCircle, self).__init__(circObj, dataMan)
    self.oldRad = circObj.rad
    self.newRad = int(newRad)

  def do(self):
    self.data.rad = self.newRad
    self.data.restrictRadius()
    for each in self.dataMan.getPillWith(self.data): each.update()

  def undo(self):
    self.data.rad = self.oldRad
    for each in self.dataMan.getPillWith(self.data): each.update()
