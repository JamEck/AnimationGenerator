import this
import pygame as pg
from Utils import *
from ActionHistory import *
from EventManager import EventManager
from Geometry import *
from DataManager import DataManager
from UIButton import UIButton
import traceback as tb

class Mode(object):
  """docstring for Mode"""
  def __init__(self, fm, em, screen):
    super(Mode, self).__init__()
    self.em = em
    self.fm = fm
    self.screen = screen
    self.tempData = None
    self.selectedData = None
    self.cmds = dict()
    self.doLaters = list()

  def doLater(self, func, *params):
    self.doLaters.append((func, params))

  def reset(self):
    self.tempData = None
    self.selectedData = None

  def findNearest(self, items): # items "vlcpi"
    if 'v' in items:
      self.tempData = self.fm.getDM().findNearestVertex(self.em.mouse.pos,10)
      if self.tempData:
        self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.tempData.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'l' in items:
      self.tempData = self.fm.getDM().findNearestLine(self.em.mouse.pos,10)
      if self.tempData:
        self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.tempData.midpoint() - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'p' in items:
      self.tempData = self.fm.getDM().findNearestPill(self.em.mouse.pos,10)
      if self.tempData:
        self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.tempData.getAxis().midpoint() - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'c' in items:
      self.tempData = self.fm.getDM().findNearestCircle(self.em.mouse.pos,10)
      if self.tempData:
        self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.tempData.nearestPoint(self.em.mouse.pos) - Vec2(5,5)).asTuple(), (10,10)), 1)
        return self.tempData
    if 'i' in items:
      if self.fm.getDM().image != None:
        if self.fm.getDM().image.contains_point(self.em.mouse.pos):
          self.tempData = self.fm.getDM().image
        else:
          self.tempData = None
          self.boxTemp = None
        return self.tempData
    return None

  def runFromConsole(self, cmdLine, targetData):
    print(cmdLine)
    parts = [each for each in cmdLine.split(' ') if each]
    funcName = parts[0]
    action = self.cmds[funcName].buildFromConsole(parts[1:], targetData, self.fm.getDM())
    self.fm.getAH().do(action)

  def drawOverlay(self):
    for func,params in self.doLaters:
      func(*params)
    self.doLaters.clear()

class ImageMode(Mode):
  """docstring for ImageMode"""
  NAME = "Image"
  BINDING = pg.K_i
  CONSOLE_CMDS = {
    "pos" : MoveImage,
    "scale" : ScaleImage,
    "reset" : ResetImage
  }

  def __init__(self, frame, em, screen):
    super(ImageMode, self).__init__(frame, em, screen)
    self.cmds = ImageMode.CONSOLE_CMDS
    self.boxTemp = None
    self.boxSel  = None

  def makeBox(self, imgObj):
    if imgObj == None:
      return None
    imgSize = imgObj.size()
    return ((imgObj.pos - imgSize//2).asTuple(), imgSize.asTuple())

  def onHover(self):
    self.findNearest('i')
    if self.tempData:
      self.boxTemp = self.makeBox(self.tempData)
      self.doLater(pg.draw.rect, self.screen, (255,255,255), self.boxTemp, 1)
    if self.selectedData:
      self.boxSel = self.makeBox(self.selectedData)
      self.doLater(pg.draw.rect, self.screen, (255,255,0), self.boxSel, 1)

      if self.em.keyboard[pg.K_DELETE].checkFall():
        self.fm.getAH().do(ClearImage(self.selectedData, self.fm.getDM()))



  def onLeftFall(self):
    self.selectedData = self.tempData

  def onLeftHeld(self):
    if self.selectedData:
      self.doLater(pg.draw.line, self.screen, (100,100,100), self.em.mouse.clickPos.asTuple(), self.em.mouse.pos.asTuple())
      self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftRise(self):
    if self.selectedData:
      disp = self.em.mouse.pos - self.em.mouse.clickPos
      self.fm.getAH().do(MoveImage(self.selectedData, self.selectedData.pos + disp, self.fm.getDM()))

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass

  def onRightRise(self):
    self.selectedData = self.findNearest('i')

  def runFromConsole(self, cmdLine):
    super(ImageMode, self).runFromConsole(cmdLine, self.fm.getDM().image)

class VertexMode(Mode):
  """docstring for VertexMode"""
  NAME = "Vertex"
  BINDING = pg.K_v
  CONSOLE_CMDS = {
    "pos" : MoveVertex
  }

  def __init__(self, frame, em, screen):
    super(VertexMode, self).__init__(frame, em, screen)
    self.cmds = VertexMode.CONSOLE_CMDS

  def onHover(self):
    self.findNearest('v')

  def onLeftFall(self):
    self.selectedData = True

  def onLeftHeld(self):
    pass

  def onLeftRise(self):
    if self.selectedData:
      self.fm.getAH().do(CreateVertex(Vertex(self.em.mouse.pos),self.fm.getDM()))

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass

  def onRightRise(self):
    nearest = self.fm.getDM().findNearestVertex(self.em.mouse.pos,10)
    if nearest: self.fm.getAH().do(DeleteVertex(nearest,self.fm.getDM()))

  def runFromConsole(self, cmdLine):
    super(VertexMode, self).runFromConsole(cmdLine, self.fm.getDM().vertices[-1])

class LineMode(Mode):
  """docstring for LineMode"""
  NAME = "Line"
  BINDING = pg.K_l
  CONSOLE_CMDS = {
    "len"    : SetLineLen,
    "maxlen" : SetLineMaxLen,
  }

  def __init__(self, frame, em, screen):
    super(LineMode, self).__init__(frame, em, screen)
    self.linked = False
    self.cmds = LineMode.CONSOLE_CMDS

  def reset(self):
    super().reset()
    self.linked = False

  def onHover(self):
    self.findNearest("v")

  def onLeftFall(self):
    self.selectedData = self.tempData
    if self.selectedData:
      self.linked = True
    else:
      self.selectedData = Vertex(self.em.mouse.pos)

  def onLeftHeld(self):
    if self.selectedData:
      self.doLater(pg.draw.line, self.screen, (100,100,100), self.em.mouse.pos.asTuple(), self.selectedData.pos.asTuple())
      self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
      self.doLater(self.selectedData.draw, self.screen)

  def onLeftRise(self):
    if self.selectedData:
      action = list()
      if not self.linked:
        action.append(CreateVertex(self.selectedData, self.fm.getDM()))
      endPoint = self.tempData
      if not endPoint:
        endPoint = Vertex(self.em.mouse.pos)
        action.append(CreateVertex(endPoint,self.fm.getDM()))
      action.append(CreateLine(Line( self.selectedData, endPoint),self.fm.getDM()))
      self.fm.getAH().do(action)
      self.reset()

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass
  def onRightRise(self):
    nearest = self.fm.getDM().findNearestLine(self.em.mouse.pos,10)
    if nearest: self.fm.getAH().do(DeleteLine(nearest,self.fm.getDM()))

  def runFromConsole(self, cmdLine):
    super(LineMode, self).runFromConsole(cmdLine, self.fm.getDM().lines[-1])


class CircleMode(Mode):
  """docstring for CircleMode"""
  NAME = "Circle"
  BINDING = pg.K_c
  CONSOLE_CMDS = {
    "rad" : ResizeCircle
  }

  def __init__(self, frame, em, screen):
    super(CircleMode, self).__init__(frame, em, screen)
    self.linked = False
    self.cmds = CircleMode.CONSOLE_CMDS

  def reset(self):
    super().reset()
    self.linked = False

  def onHover(self):
    self.findNearest("v")

  def onLeftFall(self):
    self.selectedData = self.tempData
    if self.selectedData:
      self.linked = True
    else:
      self.selectedData = Vertex(self.em.mouse.pos)

  def onLeftHeld(self):
    if isinstance(self.selectedData, Vertex):
      rad = (self.selectedData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      self.doLater(self.selectedData.draw, self.screen)
      self.doLater(pg.draw.circle, self.screen, (100,100,100), self.selectedData.pos.asTuple(), rad, 1)

  def onLeftRise(self):
    if isinstance(self.selectedData, Vertex):
      rad = (self.selectedData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      action = [] if self.linked else [CreateVertex(self.selectedData,self.fm.getDM())]
      action.append(CreateCircle(Circle(self.selectedData, rad),self.fm.getDM()))
      self.fm.getAH().do(action)
      self.reset()

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass
  def onRightRise(self):
    nearest = self.fm.getDM().findNearestCircle(self.em.mouse.pos,10)
    if nearest: self.fm.getAH().do(DeleteCircle(nearest,self.fm.getDM()))

  def runFromConsole(self, cmdLine):
    super(CircleMode, self).runFromConsole(cmdLine, self.fm.getDM().circles[-1])


class PillMode(Mode):
  """docstring for PillMode"""
  NAME = "Pill"
  BINDING = pg.K_p

  def __init__(self, frame, em, screen):
    super(PillMode, self).__init__(frame, em, screen)
    self.first = True
    self.geom  = Pill()
    self.action = []

  def reset(self):
    super().reset()
    self.first = True
    self.geom  = Pill()
    self.action = []

  def onHover(self):
    self.findNearest("v")
    if not self.first:
      if not self.selectedData:
        self.doLater(pg.draw.line, self.screen, (100,100,100), self.em.mouse.pos.asTuple(), self.geom.circle1.center.pos.asTuple())
        self.doLater(self.geom.circle1.draw, self.screen)

  def onLeftFall(self):
    self.selectedData = self.tempData
    if not self.selectedData:
      self.selectedData = Vertex(self.em.mouse.pos)
      self.action.append(CreateVertex(self.selectedData,self.fm.getDM()))

    if self.first:
      self.geom.circle1 = Circle(self.selectedData, 0)
      self.geom.circle1.color = (100,100,100)
    else:
      self.geom.circle2 = Circle(self.selectedData, 0)
      self.geom.circle2.color = (100,100,100)


  def onLeftHeld(self):
    if self.selectedData:
      self.doLater(self.selectedData.draw, self.screen)
      rad = (self.selectedData.pos - self.em.mouse.pos).mag()
      rad = 1 if rad < 1 else int(rad)
      if self.first:
        self.geom.circle1.rad = rad
        self.doLater(self.geom.circle1.draw, self.screen)
      else:
        self.doLater(pg.draw.line, self.screen, (100,100,100), self.geom.circle1.center.pos.asTuple(), self.geom.circle2.center.pos.asTuple())
        self.geom.circle2.rad = rad
        self.doLater(self.geom.circle1.draw, self.screen)
        self.doLater(self.geom.circle2.draw, self.screen)

  def onLeftRise(self):
    if self.selectedData:
      if self.first:
        self.first = False
        self.selectedData = None
      else:
        self.geom.circle1.visible = False
        self.geom.circle2.visible = False
        self.geom.update()
        self.action = self.action + [
          CreateCircle(self.geom.circle1,self.fm.getDM()),
          CreateCircle(self.geom.circle2,self.fm.getDM()),
          CreatePill  (self.geom,self.fm.getDM())
        ]
        self.fm.getAH().do(self.action)
        self.reset()

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
    pass
  def onRightHeld(self):
    pass
  def onRightRise(self):
    pass

  def runFromConsole(self, cmdLine):
    super(PillMode, self).runFromConsole(cmdLine, self.fm.getDM().pills[-1])


class SelectMode(Mode):
  """docstring for SelectMode"""
  NAME = "Select"
  BINDING = pg.K_s
  GEOM_TO_MODE = {
    Vertex : VertexMode,
    Line   : LineMode,
    Circle : CircleMode,
    Pill   : PillMode,
  }
  CONSOLE_CMDS = {
    "copyPrevFrame" : CopyPrevFrame,
    "lerp" : LerpToFrame,
    "serp" : SerpToFrame,
  }

  def __init__(self, frame, em, screen):
    super(SelectMode, self).__init__(frame, em, screen)

  def onHover(self):
    self.findNearest("vlcp")
    if self.selectedData:
      self.doLater(self.selectedData.printAttr, self.screen)

  def onLeftFall(self):
    self.selectedData = self.tempData

  def onLeftHeld(self):
    if self.selectedData:
      if   isinstance(self.selectedData, Vertex):
        self.doLater(pg.draw.line, self.screen, (100,100,100), self.selectedData.pos.asTuple(), self.em.mouse.pos.asTuple())
        self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)
      elif isinstance(self.selectedData, Circle):
        self.doLater(pg.draw.line, self.screen, (100,100,100), self.selectedData.center.pos.asTuple(), self.em.mouse.pos.asTuple())
        self.doLater(pg.draw.rect, self.screen, (100,100,100), ((self.em.mouse.pos - Vec2(5,5)).asTuple(), (10,10)), 1)

  def onLeftRise(self):
    if self.selectedData:
      if   isinstance(self.selectedData, Vertex):
        self.fm.getAH().do(MoveVertex(self.selectedData, self.em.mouse.pos, self.fm.getDM()))
      elif isinstance(self.selectedData, Circle):
        newRad = (self.em.mouse.pos - self.selectedData.center.pos).mag()
        self.fm.getAH().do(ResizeCircle(self.selectedData, newRad, self.fm.getDM()))

  def onMiddleFall(self):
    pass
  def onMiddleHeld(self):
    pass
  def onMiddleRise(self):
    pass
  def onRightFall(self):
      self.selectedData = self.tempData
  def onRightHeld(self):
    pass
  def onRightRise(self):
    pass

  def runFromConsole(self, cmdLine):
    print(cmdLine)
    parts = [each for each in cmdLine.split(' ') if each]
    funcName = parts[0]
    del parts[0]

    action = None
    if self.selectedData == None:
      cmd = SelectMode.CONSOLE_CMDS[funcName]
      action = cmd.buildFromConsole(parts, self, self.fm.getDM())
    else:
      cmd = SelectMode.GEOM_TO_MODE[type(self.selectedData)].CONSOLE_CMDS[funcName]
      action = cmd.buildFromConsole(parts, self.selectedData, self.fm.getDM())

    self.fm.getAH().do(action)


class ModeSelector(object):
  """docstring for ModeSelector"""
  MODES = [SelectMode, ImageMode, VertexMode, LineMode, CircleMode, PillMode]

  def __init__(self, fm, em, screen):
    super(ModeSelector, self).__init__()
    self.pos = Vec2(10,10)
    self.font = pg.font.SysFont("monospace", 20)
    self.makeUIButtons(fm, em, screen)
    self.currMode = self.uibuttons[SelectMode].dataRise

  def swapMode(self, mode):
      self.currMode.reset()
      self.uibuttons[type(self.currMode)].resetUpColor()
      self.uibuttons[type(self.currMode)].text.resetColor()
      self.currMode = mode
      self.uibuttons[type(mode)].setUpColor(COLOR.YELLOW)
      self.uibuttons[type(mode)].text.setColor(COLOR.BLACK)

  def swapModeByClass(self, cls):
    self.swapMode(self.uibuttons[cls].dataRise)

  def setFrameManager(self, fm):
    for mode in ModeSelector.MODES:
      self.uibuttons[mode].dataRise.fm = fm


  def makeUIButtons(self, fm, em, screen):
    self.uibuttons = {
      mode : UIButton(pos = self.pos + (i*120, 0), dim = (100,30), text=mode.NAME)
      for i,mode in enumerate(ModeSelector.MODES)
    }

    for mode in ModeSelector.MODES:
      self.uibuttons[mode].dataRise = mode(fm,em,screen)

    for val in self.uibuttons.values():
      val.onRise = self.swapMode

  def update(self, em):
    for key,but in self.uibuttons.items():
      but.update(em.mouse)

    # Choose Tool Mode With Keyboard #
    for mode in ModeSelector.MODES:
      if em.keyboard[mode.BINDING].checkFall():
        self.swapModeByClass(mode)
    if em.keyboard[pg.K_ESCAPE].checkFall():
      self.currMode.reset()
    ##################################

    # HACK: Changing Frame clears selected data #
    if em.keyboard[pg.K_LEFT].checkFall() or em.keyboard[pg.K_RIGHT].checkFall():
      self.currMode.reset()
    ##################################

    # Mode Actions #
    if em.keyboard[pg.K_LSHIFT].checkHeld():
      self.currMode.tempData = None
    else:
      self.currMode.onHover()

    if em.mouse.left  .checkFall(): self.currMode.onLeftFall  ()
    if em.mouse.left  .checkHeld(): self.currMode.onLeftHeld  ()
    if em.mouse.left  .checkRise(): self.currMode.onLeftRise  ()
    if em.mouse.middle.checkFall(): self.currMode.onMiddleFall()
    if em.mouse.middle.checkHeld(): self.currMode.onMiddleHeld()
    if em.mouse.middle.checkRise(): self.currMode.onMiddleRise()
    if em.mouse.right .checkFall(): self.currMode.onRightFall ()
    if em.mouse.right .checkHeld(): self.currMode.onRightHeld ()
    if em.mouse.right .checkRise(): self.currMode.onRightRise ()
    ################

  def draw(self, screen):
    for key,but in self.uibuttons.items():
      but.draw(screen)

    self.currMode.drawOverlay()
