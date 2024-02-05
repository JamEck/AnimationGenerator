from Utils import Vec2, linspace, sigmoid

def checkArgCount(args, n):
  if len(args) < n:
    raise AssertionError("Command Requires {} Arguments".format(n))

def castInt(item):
    try:
      val = int(item)
      return val
    except Exception as e:
      raise ValueError("Could Not Cast \"{}\" To Int".format(str(item)))

def assertRange(val, lower, upper):
  if val < lower or val > upper:
    raise AssertionError("Value ({}) Must Be In Range [{},{}]".format(val, lower, upper))

def assertMin(val, minim):
  if val < minim:
    raise AssertionError("Value ({}) Must Be At Least {}".format(val, minim))

def assertMax(val, maxi):
  if val > maxi:
    raise AssertionError("Value ({}) Must Be At Most {}".format(val, maxi))


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

class LoadImage(Action):
  """docstring for LoadImage"""
  def __init__(self, imgDropObj, dataMan):
    super(LoadImage, self).__init__(imgDropObj, dataMan)

  def do(self):
    self.dataMan.loadImageDrop(self.data)

  def undo(self):
    self.dataMan.image = None

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


class MoveItem(Action):
  """docstring for MoveItem"""
  def __init__(self, obj, newPos, dataMan):
    super(MoveItem, self).__init__(obj, dataMan)
    self.oldPos = self.data.pos
    self.newPos = newPos.copy()


class MoveImage(MoveItem):
  """docstring for MoveImage"""
  def __init__(self, imgObj, newPos, dataMan):
    super(MoveImage, self).__init__(imgObj, newPos, dataMan)

  def do(self):
    self.data.setPos(self.newPos.copy())

  def undo(self):
    self.data.pos = self.oldPos

  @classmethod
  def buildFromConsole(cls, args, imageObj, dataMan):
    if len(args) < 2:
      raise AssertionError(cls.__name__ + " Command Requires Two Integer Arguments")
    try:
      val = Vec2(int(args[0]), int(args[1]))
      return MoveImage(imageObj, val, dataMan)
    except Exception as e:
      raise AssertionError(e)

class ResetImage(Action):
  """docstring for ResetImage"""
  def __init__(self, imgObj, dataMan):
    super(ResetImage, self).__init__(imgObj, dataMan)
    self.OLD_visible = self.data.visible
    self.OLD_pos     = self.data.pos
    self.OLD_data    = self.data.data.copy()
    self.OLD_scale   = self.data.scale

  def do(self):
    self.data.reset()

  def undo(self):
    self.data.visible = self.OLD_visible
    self.data.pos     = self.OLD_pos
    self.data.data    = self.OLD_data.copy()
    self.data.scale  = self.OLD_scale

  @classmethod
  def buildFromConsole(cls, args, imageObj, dataMan):
    if len(args) != 0:
      raise AssertionError(cls.__name__ + " Command Takes No Arguments")
    try:
      return ResetImage(imageObj, dataMan)
    except Exception as e:
      raise AssertionError(e)

class ClearImage(Action):
  """docstring for ClearImage"""
  def __init__(self, imgObj, dataMan):
    super(ClearImage, self).__init__(imgObj.copy(), dataMan)

  def do(self):
    self.data.data = None
    self.data.data_bkp = None
    self.dataMan.image = None

  def undo(self):
    self.dataMan.image = Image(self.data.path)
    self.dataMan.image.pos     = self.data.pos
    self.dataMan.image.visible = self.data.visible
    self.dataMan.image.data    = self.data.data.copy()
    self.dataMan.image.scale  = self.data.scale

  @classmethod
  def buildFromConsole(cls, args, imageObj, dataMan):
    if len(args) != 0:
      raise AssertionError(cls.__name__ + " Command Takes No Arguments")
    try:
      return ClearImage(imageObj, dataMan)
    except Exception as e:
      raise AssertionError(e)

class ScaleImage(Action):
  """docstring for ScaleImage"""
  def __init__(self, imgObj, newScale, dataMan):
    super(ScaleImage, self).__init__(imgObj, dataMan)
    self.oldScale = imgObj.scale
    self.newScale = newScale

  def do(self):
    self.data.setScale(self.newScale)

  def undo(self):
    self.data.setScale(self.oldScale)

  @classmethod
  def buildFromConsole(cls, args, imageObj, dataMan):
    if len(args) < 1:
      raise AssertionError(cls.__name__ + " Command Requires One Integer Argument")
    try:
      return ScaleImage(imageObj, int(args[0]), dataMan)
    except Exception as e:
      raise AssertionError(e)

class MoveVertex(MoveItem):
  """docstring for MoveVertex"""
  def __init__(self, vertObj, newPos, dataMan):
    super(MoveVertex, self).__init__(vertObj, newPos, dataMan)

  def do(self):
    self.data.pos = self.newPos.copy()
    for each in self.dataMan.getLineWith(self.data): each.restrictLength(self.data)
    for each in self.dataMan.getPillWith(self.data): each.update()

  def undo(self):
    self.data.pos = self.oldPos
    for each in self.dataMan.getPillWith(self.data): each.update()

  @classmethod
  def buildFromConsole(cls, args, vertObj, dataMan):
    if len(args) < 2:
      raise AssertionError(cls.__name__ + " Command Requires Two Integer Arguments")
    try:
      val = Vec2(int(args[0]), int(args[1]))
      return MoveVertex(vertObj, val, dataMan)
    except Exception as e:
      raise AssertionError(e)

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

  @staticmethod
  def buildFromConsole(args, circObj, dataMan):
    checkArgCount(args, 1)
    rad = castInt(args[0])
    assertMin(rad, 1)
    return ResizeCircle(circObj, rad, dataMan)

class SetLineMaxLen(Action):
  def __init__(self, lineObj, maxlen, dataMan):
    super(SetLineMaxLen, self).__init__(lineObj, dataMan)
    self.prevmaxlen = lineObj.maxlen
    self.maxlen = maxlen
    self.moveVert = MoveVertex(self.data.p2, self.data.p2.pos, self.dataMan)

  def do(self):
    self.data.maxlen = self.maxlen
    self.moveVert.do()

  def undo(self):
    self.data.maxlen = self.prevmaxlen
    self.moveVert.undo()

  @staticmethod
  def buildFromConsole(args, lineObj, dataMan):
    checkArgCount(args, 1)
    maxLen = castInt(args[0])
    assertMin(maxLen, 0)
    return SetLineMaxLen(lineObj, maxLen, dataMan)

class SetLineLen(Action):
  def __init__(self, lineObj, len, dataMan):
    super(SetLineLen, self).__init__(lineObj, dataMan)
    heading = lineObj.toVec().norm()
    self.newpos = (lineObj.p1.pos + heading * len).toInt()
    self.moveVert = MoveVertex(self.data.p2, self.newpos, self.dataMan)

  def do(self):
    self.moveVert.do()

  def undo(self):
    self.moveVert.undo()

  @staticmethod
  def buildFromConsole(args, lineObj, dataMan):
    checkArgCount(args, 1)
    len = castInt(args[0])
    return SetLineLen(lineObj, len, dataMan)

class CopyFrame(Action):
  def __init__(self, toolMode, dataMan, framenum):
    super(CopyFrame, self).__init__(toolMode, dataMan)
    if (framenum < 0 or framenum > len(toolMode.fm.frames)):
      raise AssertionError("Frame %d does not exist" % framenum)
    self.otherDataMan = toolMode.fm.frames[framenum].dm
    self.data_bkp = self.dataMan.copy()

  def do(self):
    self.data.reset()
    self.dataMan.clear()
    self.dataMan.copy_from(self.otherDataMan)

  def undo(self):
    self.data.reset()
    self.dataMan.clear()
    self.dataMan.copy_from(self.data_bkp)

  @staticmethod
  def buildFromConsole(args, toolMode, dataMan):
    checkArgCount(args, 1)
    framenum = castInt(args[0])
    return CopyFrame(toolMode, dataMan, framenum)

class CopyPrevFrame(Action):
  def __init__(self, toolMode, dataMan):
    super(CopyPrevFrame, self).__init__(toolMode, dataMan)
    self.prevDataMan = toolMode.fm.frames[toolMode.fm.fidx-1].dm if toolMode.fm.fidx > 0 else dataMan
    self.data_bkp = self.dataMan.copy()

  def do(self):
    self.data.reset()
    self.dataMan.clear()
    self.dataMan.copy_from(self.prevDataMan)

  def undo(self):
    self.data.reset()
    self.dataMan.clear()
    self.dataMan.copy_from(self.data_bkp)

  @staticmethod
  def buildFromConsole(args, toolMode, dataMan):
    checkArgCount(args, 0)
    return CopyPrevFrame(toolMode, dataMan)

class InterpToFrame(Action):
  def __init__(self, toolMode, dataMan, endFrame):
    super(InterpToFrame, self).__init__(toolMode, dataMan)
    ran = endFrame - toolMode.fm.fidx
    if ran < 2:
      raise AssertionError("No Frames Between Current And End Frame")
    if endFrame > len(toolMode.fm.frames):
      raise AssertionError("Frame {} Does Not Exist".format(endFrame))

    self.tFunc = lambda x: x

    self.frameSaves = {i : toolMode.fm.frames[i] for i in range(toolMode.fm.fidx + 1, endFrame)}
    self.endFrame   = endFrame

  def do(self):
    ran = abs(self.endFrame - self.data.fm.fidx)
    endFrameDM = self.data.fm.frames[self.endFrame].dm
    psteps = list(linspace(0,1,ran))[1:-1]
    for i,p in enumerate(psteps):
      frame = self.data.fm.frames[self.data.fm.fidx].copy()
      frame.dm.lerp(self.dataMan, endFrameDM, self.tFunc(p))
      self.data.fm.frames[self.data.fm.fidx + i + 1] = frame

  def undo(self):
    for frameNum, frame in self.frameSaves.items():
      self.data.fm.frames[frameNum] = frame


class LerpToFrame(InterpToFrame):
  def __init__(self, toolMode, dataMan, endFrame):
    super(LerpToFrame, self).__init__(toolMode, dataMan, endFrame)
    self.tFunc = lambda x: x

  @staticmethod
  def buildFromConsole(args, toolMode, dataMan):
    checkArgCount(args, 1)
    endFrame = castInt(args[0])
    return LerpToFrame(toolMode, dataMan, endFrame)


class SerpToFrame(InterpToFrame):
  def __init__(self, toolMode, dataMan, endFrame):
    super(SerpToFrame, self).__init__(toolMode, dataMan, endFrame)
    self.tFunc = lambda x: sigmoid(x)

  @staticmethod
  def buildFromConsole(args, toolMode, dataMan):
    checkArgCount(args, 1)
    endFrame = castInt(args[0])
    return SerpToFrame(toolMode, dataMan, endFrame)